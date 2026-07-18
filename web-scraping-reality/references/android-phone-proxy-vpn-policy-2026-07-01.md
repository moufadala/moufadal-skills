# Android phone proxy + VPN policy for Hermes/SearXNG

Session learning from the 2026-07-01 residential proxy discussion.

## Trigger

Use this when Moufadal asks whether to make an Android phone the official residential/mobile proxy for Hermes, SearXNG, agent-reach, or scrapers; or when Tailscale, Every Proxy, NordVPN, exit nodes, and proxy watchdogs are involved.

## Decision pattern

1. **Prefer the already-verified path over a visually “cleaner” new app.**
   - If Tailscale userspace SOCKS on the VPS (`127.0.0.1:1055`) plus an internal HTTP relay is already working and monitored, treat it as the production/default path.
   - Do not install Every Proxy merely because a spec calls it the “official proxy”. Every Proxy adds an Android foreground app, battery/autostart settings, auth, and another service that Samsung can kill.

2. **Classify Every Proxy as plan-B/experiment unless the user explicitly has time to validate it.**
   - It can be compatible with Tailscale: VPS → Tailscale IP of phone → Every Proxy port → Internet.
   - But it increases maintenance and surface area. Do not switch production SearXNG to it until direct ports, auth, battery survival, reboot behavior, and exit IP have been proven.

3. **Never use global VPS routing/exits for this class of work.**
   - No global `tailscale set --exit-node` on the VPS unless explicitly approved with a rollback plan.
   - No global NordVPN/OpenVPN/WireGuard on the VPS for “country access”. Use per-container egress only.

4. **Watchdogs must be silent on success.**
   - For Telegram cockpit hygiene, proxy health jobs should be script-only/no-agent where stdout is empty on OK and non-empty only on failure/leak/recovery if useful.
   - A frequent proxy watchdog that posts “OK” messages is a bug, not observability.

5. **NordVPN on the Android phone is not equivalent to Tailscale and should not be mixed into the critical proxy path.**
   - Android usually allows only one VPN-style tunnel at a time, so NordVPN may disable or conflict with Tailscale.
   - If NordVPN is active behind the phone proxy, the exit IP may become NordVPN/datacenter/geographic-VPN, not the desired mobile/residential IP.
   - If the user needs “United States / another country” access, Tailscale alone does not provide it unless they control an exit machine in that country.

## Recommended architecture

Production scraping/search:

```text
Hermes/SearXNG container
  → internal HTTP proxy relay if needed
  → VPS-local Tailscale userspace SOCKS 127.0.0.1:1055
  → phone/Tailscale/mobile path
  → Internet
```

Country-specific access, future work:

```text
Only the task that needs USA/other country
  → isolated VPN container / proxy provider / remote VPS in that country
  → Internet
```

Do **not** put NordVPN globally on the phone or VPS for Hermes production. Treat country egress as a separate route/class of traffic.

## Minimal acceptance tests before changing production

- Direct VPS IP != proxy IP.
- SearXNG query works through Docker DNS, not just host curl.
- Watchdog stdout is empty on OK and produces an alert only on failure/leak.
- If testing Every Proxy: ports reachable via Tailscale, authenticated, exit IP correct, survives screen-off and reboot, and fallback path remains available.
- If testing NordVPN/country egress: prove Tailscale remains reachable and record whether exit IP is mobile/residential or VPN/datacenter.

## User preference captured

Moufadal explicitly prefers: no chat pollution from watchdogs; no extra experimentation when time is short; preserve the working Tailscale path rather than adding Every Proxy unless there is time for a controlled test.