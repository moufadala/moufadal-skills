# SearXNG tailnet-only exposure via Tailscale Serve — 2026-07-11

Use this when exposing an already-working SearXNG instance for shared access on a Tailscale tailnet. This is not a public/Funnel exposure pattern.

## Scope and hard guards

- Preserve existing Tailscale Serve entries. If another service already uses `tailscale serve --http=80 -> 127.0.0.1:8770`, **add** a new port; do not reset or replace.
- Never use `tailscale funnel` for SearXNG unless the user explicitly asks for public exposure.
- Never use `tailscale serve reset` during additive exposure; it can erase unrelated guichets. Roll back a single port with `tailscale serve --https=<port> off`.
- Do not touch `hermes-gateway` for SearXNG tailnet exposure.
- Do not edit SearXNG `settings.yml` to work around a tailnet proxy issue unless you first produce a minimal diff and wait for user validation.

## Host vs container trap

Hermes may run inside a Docker container. In that case:

- `tailscale` may be absent in the Hermes container even though it exists on the Docker host.
- `curl http://127.0.0.1:8888/...` from Hermes can be a false negative because it targets the container namespace, not the host loopback.
- Docker inspect can still prove the host binding, for example `8080/tcp -> 127.0.0.1:8888`.
- If direct `nsenter` is not permitted from the container, a verified host-access pattern is a transient privileged container with host namespaces, e.g. `docker run --rm --privileged --pid=host --net=host --entrypoint /usr/bin/nsenter <existing-image> --target 1 --mount --uts --ipc --net --pid sh -lc '<host commands>'`.

Use this only for bounded host diagnostics/mutations and keep the command list explicit.

## Safe sequence

1. Pull/update the vault or handoff first if the runbook is the source of truth.
2. Read current serve config:
   ```bash
   tailscale serve status
   tailscale serve status --json
   ```
   Confirm existing guichets, especially `:80 -> http://127.0.0.1:8770`, remain untouched.
3. Confirm SearXNG from the host, not from the Hermes container:
   ```bash
   curl -sS --max-time 5 'http://127.0.0.1:8888/search?q=test&format=json'
   ```
   Parse JSON and require `results_count > 0` before exposing.
4. Add a dedicated tailnet-only HTTPS port:
   ```bash
   tailscale serve --bg --https=8443 http://127.0.0.1:8888
   ```
   `--https=8443` is additive and distinct from the existing YouTube `--http=80` entry.
5. Verify:
   ```bash
   tailscale serve status --json
   curl -sS --max-time 12 'https://<node-fqdn>:8443/search?q=test&format=json'
   ```
   Only call it exposed/joignable if the tailnet URL returns `results_count > 0`. After the first successful `tailscale serve --bg --https=8443 ...`, a first HTTPS request can time out while the MagicDNS/TLS path is provisioned; retry a small bounded number of times before diagnosing SearXNG. In the 2026-07-11 run, attempt 1 timed out, attempt 2 returned `results_count=137`, `unresponsive_count=0`.
6. Confirm no Funnel/public exposure:
   ```bash
   tailscale funnel status
   ```
   It must show `tailnet only` for both the existing guichet and SearXNG. If any Funnel/public wording appears, stop and roll back `8443`.
7. If SearXNG is used as evidence for search quality after exposure, also keep the standard SearXNG proxy preflight discipline: verify the mobile/residential SOCKS path is PASS, but do not copy mobile IPs into shared notes.

## Known blocker: Serve not enabled on tailnet

Tailscale may refuse `tailscale serve --https=8443 ...` with:

```text
Serve is not enabled on your tailnet.
To enable, visit: https://login.tailscale.com/f/serve?node=...
```

When this happens:

- Stop. Do not edit SearXNG settings and do not touch `hermes-gateway`.
- Do not copy the admin activation URL into a public/shared note; treat it as sensitive operational context.
- Verify `tailscale serve status --json` remains unchanged and no `8443` entry exists.
- Report that the backend is healthy but exposure is blocked by Tailscale tailnet policy.
- Next action is for the admin/user to enable Tailscale Serve, then rerun only the additive `tailscale serve --bg --https=8443 ...` command.

## If the tailnet URL reaches SearXNG but returns 403/empty

Then diagnose SearXNG limiter/proxy behavior before changing config:

- Check if the request is seen as non-localhost due to Tailscale Serve proxying.
- Inspect limiter/botdetection/base_url/trusted proxy assumptions.
- Produce a minimal `settings.yml` diff and wait for validation before applying it.
- Restart only `searxng` if config is approved; never restart `hermes-gateway`.

## Rollback

```bash
tailscale serve --https=8443 off
```

Never use `tailscale serve reset` unless the explicit goal is to remove all serve config and the user has approved losing unrelated guichets.
