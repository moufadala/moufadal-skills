# SearXNG mobile proxy relay + watchdog pattern (2026-07-01)

Use this when a spec or user request says to make the residential/mobile proxy critical for SearXNG, agent-reach, scraping, or research.

## Lesson

Do not assume the desired proxy topology is the topology currently wired into the VPS. First inventory the live path and restart any existing relay/watchdog before redesigning.

Validated pattern on Moufadal's VPS:

- Mobile egress can be provided by Tailscale userspace SOCKS on `127.0.0.1:1055`.
- SearXNG may be configured to use an internal HTTP relay such as `http://hermes-gateway:1056` instead of SOCKS directly.
- The relay is launched/checked by `/opt/data/scripts/ensure_searxng_mobile_proxy_stack.sh`.
- The watchdog cron can run that script every 2 minutes and stay silent on success.

## Why the HTTP relay matters

Some SearXNG images do not include SOCKS support (`socksio` / `httpx[socks]`). If `socksio` is absent, putting `socks5h://...` directly in `outgoing.proxies` will fail. A local HTTP relay in front of the SOCKS path avoids rebuilding SearXNG and keeps `outgoing.proxies.http/https` simple.

## Safe diagnostic sequence

1. Capture direct vs proxied IP:

```bash
curl -4 -fsS --max-time 12 https://api.ipify.org
curl -4 -fsS --max-time 20 --socks5-hostname 127.0.0.1:1055 https://api.ipify.org
```

2. Run/restart the existing relay stack if present:

```bash
/opt/data/scripts/ensure_searxng_mobile_proxy_stack.sh
python3 -m json.tool /opt/data/state/searxng_mobile_proxy_stack_status.json
```

3. Verify the SearXNG config and avoid leaking credentials:

```bash
docker exec searxng sh -lc 'python - <<"PY"
import importlib.util
print("socksio", importlib.util.find_spec("socksio") is not None)
PY
sed -n "/^outgoing:/,/^[^ ]/p" /etc/searxng/settings.yml'
```

4. Test SearXNG from the Hermes runtime namespace with Docker DNS, not loopback:

```bash
curl -sS --max-time 30 'http://searxng:8080/search?q=hermes%20agent&format=json'
```

5. Check/enable the watchdog cron:

```bash
hermes cron list --all
# Expected job class: searxng-mobile-proxy-stack-watchdog
```

## Pitfalls

- `127.0.0.1:8888` can be a false negative from inside Hermes; prefer `http://searxng:8080` for runtime QA.
- A direct phone proxy like `100.x.x.x:1080/8080` may be a future target but is not proof of the current working route. Do not switch SearXNG to it until host and container gates both pass.
- Do not enable a global Tailscale exit-node on the VPS to fix SearXNG. Keep proxying per app/container.
- Starting a watchdog is not completion; verify a later cron tick and inspect the status JSON.
- Alert interpretation: if a watchdog run reports `curl: (97) cannot complete SOCKS5 connection` for raw `127.0.0.1:1055`, but the HTTP relay check still returns the same mobile IP as SOCKS normally does and recent later ticks are OK, treat it as a transient Tailscale/SOCKS probe failure, not immediate SearXNG outage. For noisy watchdogs, prefer a tolerance policy: alert only when the app-facing HTTP relay fails, leaks direct VPS IP, or multiple consecutive raw-SOCKS failures occur while relay health is degraded; log isolated raw-SOCKS failures as internal warnings.

## Acceptance gates

- Direct VPS IP differs from proxied IP.
- SOCKS IP equals HTTP relay IP.
- SearXNG query returns JSON results with acceptable `unresponsive_engines`.
- Watchdog cron last run is OK and status JSON has `alerts: []`.
