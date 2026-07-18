# Tailscale userspace consequences + scraper stabilization registry (2026-06)

## Trigger

Use this when the VPS has been connected to an Android/Tailscale exit node, or when the user complains that scraping work is too ad-hoc / scattered (“on galère”, “on teste un truc puis un autre”).

## Field lesson

Installing/using Tailscale, even in userspace mode, has operational consequences. Do not treat “proxy works” as enough. Audit and document the side effects before using it broadly.

Validated pattern from session:

- Tailscale userspace daemon: `tailscaled --tun=userspace-networking --socks5-server=127.0.0.1:1055 --state=... --socket=...`
- Safe default: do **not** route the whole VPS through the phone.
- Use targeted SOCKS only for scripts that need mobile/residential egress.
- Verify direct IP vs proxied IP before any scraper conclusion.
- For Playwright, pass proxy explicitly: `chromium.launch(proxy={"server":"socks5://127.0.0.1:1055"})` or script `--proxy ...`; `ALL_PROXY` can create false negatives.

## Required Tailscale consequence audit

Before saying “everything works”, produce/verify:

1. Process and command line:
   - `pgrep -af 'tailscaled|tailscale'`
2. Listener safety:
   - confirm SOCKS is loopback-only (`127.0.0.1:1055`), not `0.0.0.0`.
   - `/proc/net/tcp` or `ss -ltnp` evidence.
3. Routes/DNS:
   - confirm no global route was changed unless explicitly requested.
   - note DNS behavior: requests libraries should use `socks5h://`; Playwright uses `socks5://` in launch proxy config.
4. Direct vs proxied egress:
   - direct public IP.
   - proxied public IP through SOCKS.
   - fail if they are equal.
5. Docker/Hermes namespace reality:
   - `127.0.0.1` inside the Hermes process namespace may not be reachable from every Docker container.
   - only claim a container can use the proxy after a real curl from that container.
6. Existing shared config:
   - search for old proxy defaults such as `172.16.1.1:1080`, `127.0.0.1:1080`, `ALL_PROXY`, `SOCKS_PROXY`.
   - update a central config module if one exists, rather than patching scripts one by one.
7. Watchdog:
   - add or verify a silent watchdog that alerts if the phone exit node disappears, proxied IP equals VPS IP, or the SOCKS listener opens beyond loopback.

## Safe correction pattern

If an old bridge conflicts with the Tailscale SOCKS endpoint:

- Prefer a central proxy helper that chooses, in order:
  1. explicit `SOCKS_PROXY` / `HERMES_SOCKS_PROXY`;
  2. reachable Tailscale userspace `127.0.0.1:1055`;
  3. legacy bridge fallback (`172.16.1.1:1080` or `127.0.0.1:1080`).
- Verify the helper by actually making a proxied request and checking the mobile IP.
- Update project context (`AGENTS.md` or equivalent) so future agents know the active proxy path.

Do **not** apply root-level kill switches, global proxy env, or VPS-wide exit-node routing without explicit user approval and rollback plan.

## Scraper stabilization response to user frustration

When the user says the scraping process is too scattered, the next step is usually **not** another scraper. Build discipline first:

1. Create/maintain a source registry (`scraper_source_registry.yaml` or DB table):
   - `source_id`, `priority`, `method`, `proxy_policy`, `health_status`, `last_success_at`, `last_error_class`, `artifact_dir`.
2. Add a smoke runner:
   - one representative request/action per source;
   - short timeout;
   - raw artifact or screenshot;
   - no DB write if smoke fails.
3. Classify failures:
   - `prod-candidate`, `needs-hardening`, `blocked-antibot`, `bug-local`, `low-value`.
4. Separate bug-local from site-block:
   - wrong proxy passed to browser = bug-local;
   - Cloudflare 403 with correct proxy and browser evidence = likely site-block.
5. Only then optimize site by site.

## Reporting format

Keep the user-facing report compact:

- “what works now”
- “conflict found/fixed”
- “risks still present”
- “what I refused to change automatically and why”
- artifact paths
- one recommended next engineering step
