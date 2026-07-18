# VPS dashboard publishing architecture

Use this reference when a professional/dashboard deliverable exists as local HTML/JSON but the user needs a real URL from phone/browser.

## Core lesson

Do not treat successful local generation as delivery. A dashboard is not delivered until the exact user-facing URL is reachable and QA'd. Local paths, `python -m http.server`, random high ports, and temporary tunnels are development aids unless explicitly accepted as temporary.

When the user expresses frustration that “nothing works” or “it is bricolage,” stop adding patches and audit the publication architecture.

## Distinguish the problem domains

- **Scraping/proxy egress**: tools like Tailscale userspace SOCKS or mobile exit nodes affect outbound requests from the VPS.
- **Web publication/ingress**: reverse proxies, DNS, TLS, tunnels, firewall, and container routing affect whether the user can open a dashboard.

Do not blame Tailscale for a dashboard URL unless Tailscale Serve/Funnel is actually the chosen ingress path.

## Read-only audit checklist

Before proposing a fix, collect proof for:

1. **Existing reverse proxy**
   - `docker ps` for Traefik/Caddy/nginx.
   - `docker inspect <proxy>` for args, providers, entrypoints, network mode, labels, mounts.
   - Is Docker provider enabled? Is `exposedByDefault=false`?
2. **Current public surfaces**
   - `curl` public IP/host on known ports and paths.
   - Verify whether an existing public path serves the current build or an old artifact.
3. **Local app state**
   - `curl http://127.0.0.1:<port>/` and data assets.
   - Parse embedded JSON / external JSON.
4. **Permissions**
   - Owner/mode of public folders and app artifacts.
   - Avoid `chmod/chown` fixes until the serving service is understood.
5. **Tunnels**
   - Identify whether `trycloudflare`, named Cloudflare Tunnel, Tailscale Serve, or Tailscale Funnel is active.
6. **User-facing QA**
   - Open the exact public URL in browser tooling.
   - Clear localStorage/cache-bust, test reset/search/filter/modal, inspect console.

Save a concise audit artifact under `/opt/data/artifacts/audits/` for serious projects.

## Recommended architecture order

### 1. Traefik + static app containers — preferred when Traefik already exists

Each dashboard should be a containerized static service (nginx/Caddy) with read-only volume to the built artifact and explicit Traefik labels. Traefik owns HTTP/HTTPS, TLS, and routing.

Benefits:
- durable and scalable;
- isolated per app;
- no random public ports;
- no temporary tunnel dependency;
- rollback is container/image/config based;
- compatible with automated QA.

Pitfalls:
- if `exposedByDefault=false`, missing `traefik.enable=true` makes the app invisible;
- Traefik must be able to reach the app container on the right Docker network;
- do not store secrets in labels;
- a hostname/DNS route is usually required for clean HTTPS.

### 2. Cloudflare Tunnel named — strong fallback

Use when ports/DNS/firewall or host-level Traefik access are blocked. Prefer a named tunnel with config/ingress and hostname over `trycloudflare`.

Facts from Cloudflare docs:
- Quick Tunnels (`trycloudflare.com`) are for testing/development, have no SLA/uptime guarantee, and have limits such as concurrent request caps.
- Named tunnels support stable hostnames and ingress rules.

### 3. Tailscale Serve/Funnel — preview or niche public sharing

Use only when it is intentionally the ingress layer.

Facts from Tailscale docs:
- `tailscale serve` is for tailnet/private access.
- `tailscale funnel` exposes publicly, requires HTTPS/MagicDNS/policy support, has allowed ports such as 443/8443/10000, and Funnel may be marked beta/limited depending on docs.

Good for quick previews; not the default foundation for multiple public dashboards if a reverse proxy already exists.

### 4. Existing monolith/public folder — short-term only

Reusing an existing public dashboard path can be tempting, but root-owned folders and mixed artifacts cause brittle delivery. Only use after understanding service ownership and with a reversible publish path.

### 5. Opening random ports — avoid

Avoid per-dashboard public ports. It causes firewall churn, no clean HTTPS, poor security posture, and user-facing URLs that look temporary.

## Implementation pitfalls from VPS/Hermes containers

### Static app base paths and reverse-proxy roots

For Vite/React static apps, check the build `base` before choosing the public URL shape. If `vite.config.js` uses `base: '/miham/'`, the generated `index.html` will request assets under `/miham/assets/...` and images under `/miham/images/...`. Publishing that app at a clean host root such as `https://miham.example/` requires either rebuilding with `base: '/'` or configuring nginx to serve the app's parent directory and route `/` to `/miham/index.html` while preserving `/miham/*` asset paths.

Known-good nginx pattern:

```nginx
root /usr/share/nginx/html;
index index.html;

location = / {
    try_files /miham/index.html =404;
}

location = /status.html {
    add_header Content-Type text/html;
    return 200 '<!doctype html><html><body>OK</body></html>';
}

location /miham/ {
    try_files $uri $uri/ /miham/index.html;
}
```

Mount the parent folder into nginx, e.g. `/opt/hermes/data/artifacts/morning-brief:/usr/share/nginx/html:ro`, not only the app subfolder, otherwise `/miham/assets/...` 404s and the page can look blank even when `/` returns 200.

QA must include curl checks for the exact asset paths referenced by `index.html`, not just the root HTML.

### Docker daemon host paths vs Hermes-visible paths

When Hermes itself runs in a container, the path Hermes sees may not be the same path the Docker daemon sees. A file tree visible inside Hermes as `/opt/data/...` may need to be mounted into a new Docker container as a **host-side** path such as `/opt/hermes/data/...`.

Failure signature:
- app files exist from Hermes;
- nginx/static container starts;
- Traefik reaches the container;
- public route returns `403`, `404`, or nginx default behavior because `/usr/share/nginx/html` is empty/wrong.

Runbook:
1. Check files from Hermes path, e.g. `test -s /opt/data/project/artifacts/app/index.html`.
2. Check Docker can see the host path before recreating the service:
   ```bash
   docker run --rm -v /opt/hermes/data/project/artifacts/app:/check:ro alpine:3.20 \
     sh -lc 'test -s /check/index.html && test -s /check/listings.json'
   ```
3. Mount the Docker host path into the static server as read-only:
   ```bash
   -v /opt/hermes/data/project/artifacts/app:/usr/share/nginx/html:ro
   ```
4. Verify inside the container: `docker exec <container> test -s /usr/share/nginx/html/index.html`.

Do not record this as a universal path rule; it is a host/container boundary check. The durable lesson is to prove both the Hermes-visible path and Docker-daemon-visible path.

### Vite/SPA base path mismatch on a dedicated host

When publishing a built Vite/React static app that was compiled with a non-root `base` such as `/miham/`, a dedicated hostname route like `https://miham.example/` can return HTML 200 but render an empty page because the browser requests assets under `/miham/assets/...` while the nginx container only exposes the app at `/assets/...`.

Failure signature:
- `curl https://host/` returns the app `index.html`;
- browser title is correct but the accessibility snapshot is empty or the root app does not mount;
- console may be clean if the tooling does not capture failed module loads early;
- `curl https://host/miham/assets/<bundle>.js` returns 404 while `curl https://host/assets/<bundle>.js` returns 200.

Safe fix options:
1. Rebuild the app with `base: '/'` for the dedicated hostname; or
2. Keep the existing build untouched and serve the parent directory so `/miham/...` exists, with nginx mapping `/` to `/miham/index.html`:
   ```nginx
   root /usr/share/nginx/html;
   index index.html;

   location = / {
       try_files /miham/index.html =404;
   }

   location /miham/ {
       try_files $uri $uri/ /miham/index.html;
   }
   ```
3. Mount the parent directory into nginx, not the app subdirectory, e.g. host `/opt/hermes/data/artifacts/morning-brief` → container `/usr/share/nginx/html:ro` when the build lives in `morning-brief/miham`.

QA must include both the canonical root and the base-prefixed assets:
```text
https://host/                         200 HTML
https://host/miham/                   200 HTML
https://host/miham/assets/<bundle>.js 200 JS
browser snapshot: non-empty app content
console: 0 blocking errors
```

### DNS AAAA/IPv6 false positives

If HTTPS intermittently fails while IPv4 `curl -4` succeeds, test DNS and IPv6 explicitly before blaming Traefik.

Failure signature:
- DNS returns both `A` and `AAAA`;
- `curl -4 https://host/` returns 200;
- `curl -6 https://host/` fails quickly;
- `/proc/net/if_inet6` shows only loopback or the host lacks a usable public IPv6;
- browser/client behavior depends on whether it attempts IPv6 first.

Fix options:
1. Best: remove the stale/wrong AAAA record in the DNS provider, or configure real IPv6 on the VPS and proxy.
2. Immediate safe workaround: add a second IPv4-only hostname (for example sslip.io/nip.io or a DNS A-only record) and add it to the Traefik router as another `Host(...)` rule.
3. Update QA to report DNS families and test the IPv4-only canonical URL without forcing IPv4; only force IPv4 for the legacy hostname regression.

Acceptance evidence should include:
```text
DNS canonical.example
  AF_INET  <vps-ip>
  AF_INET6 NONE
https://canonical.example/ STATUS 200
https://canonical.example/listings.json STATUS 200
browser console: 0 errors
```

## Delivery contract for static dashboards on VPS

A dashboard publication is complete only when all are true:

- build artifact exists in durable project workspace;
- service/container is up and restartable;
- reverse proxy/tunnel route is declared, not ad hoc;
- exact public URL returns HTTP 200 and current build content;
- data assets load from the same public route;
- a lightweight `/status.html` or equivalent health page on the same host returns 200, so user reports can distinguish network/TLS/proxy failure from heavy-app JS/state failure;
- browser QA passes with zero blocking console errors;
- fresh-state and dirty-state flows are tested (`localStorage.clear()`/cache-bust plus persisted-state behavior, and a user-shareable `?reset=1` link when state can break perceived usability);
- final response gives one canonical public URL first, proof, limitations, and whether the URL is temporary or durable.

## Anti-patterns to call out explicitly

- Claiming delivery with only `/opt/data/.../index.html`.
- Treating localhost success as public accessibility.
- Giving an IP:high-port URL without testing it externally.
- Publishing through `trycloudflare` and implying it is permanent.
- Writing into a root-owned legacy public directory without understanding the owning service.
- Continuing to debug UI/data when the real issue is ingress architecture.
