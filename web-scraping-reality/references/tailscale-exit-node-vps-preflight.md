# Tailscale Android exit node → VPS userspace SOCKS preflight

## Why this reference exists

In a scraping/debugging session, we nearly misclassified flight scrapers as broken because the mobile/residential proxy path was not proven first. The phone was visible in Tailscale and the admin UI showed an `Exit Node` badge at one point, but the VPS still egressed via its datacenter IP.

## Correct mental model

There are separate states that must not be conflated:

1. **Phone connected to tailnet** — `tailscale ping 100.x` works.
2. **Phone advertising/approved as an exit node** — other clients see it as usable.
3. **VPS selected that exit node** — `RouteAll=true`/valid exit-node pref.
4. **SOCKS egress actually exits via mobile IP** — direct IP differs from SOCKS IP.
5. **Scraper/Playwright actually receives the proxy** — Playwright needs explicit proxy config.

Passing (1) does not imply (2)-(5).

## Required VPS preflight

Use the userspace daemon socket and check all boundaries:

```bash
TS=/opt/data/tools/tailscale/tailscale
SOCK=/opt/data/tailscale-userspace.sock

$TS --socket=$SOCK status
$TS --socket=$SOCK exit-node list
$TS --socket=$SOCK status --json | python3 - <<'PY'
import json, sys
d=json.load(sys.stdin)
for n in d.get('Peer', {}).values():
    if 's25' in (n.get('HostName','') + ' ' + n.get('DNSName','')).lower():
        print({k:n.get(k) for k in ['HostName','Online','ExitNode','ExitNodeOption','AllowedIPs','PrimaryRoutes']})
PY

printf 'direct='; curl -4 -sS --max-time 12 https://api.ipify.org; echo
printf 'socks='; env -u HTTP_PROXY -u HTTPS_PROXY -u ALL_PROXY -u http_proxy -u https_proxy -u all_proxy \
  curl -4 -sS --max-time 20 --socks5-hostname 127.0.0.1:1055 https://api.ipify.org; echo
```

Success criteria:

- `exit-node list` includes the phone, or JSON shows the phone as an exit-node option.
- The phone peer has default-route capability, not only `100.x/32`/IPv6 host routes.
- `socks` IP differs from the VPS datacenter IP.

If `socks` equals the direct VPS IP, classify as `network-preflight-failed`, not scraper failure.

## Android/admin UI pitfalls

- Android app `Connected` + green dot only proves tailnet connectivity.
- Admin console badge/button `Exit Node` is not enough proof that the VPS can currently use the phone.
- Android `EXIT NODE = None` means the needed exit-node state is not active for this workflow; re-enable until the app shows an active/running exit-node state, then retest from the VPS.
- Logs containing `wgengine`, `magicsock`, `DERP`, or successful `tailscale ping` prove WireGuard/Tailscale connectivity only, not public-internet egress via the phone.
- A stale VPS preference may show `ExitNodeID` even while `RouteAll=false` and `exit-node list` is empty. Clear it before retesting:

```bash
/opt/data/tools/tailscale/tailscale --socket=/opt/data/tailscale-userspace.sock set --exit-node=
```

Then set the exit node only after it appears as selectable:

```bash
/opt/data/tools/tailscale/tailscale --socket=/opt/data/tailscale-userspace.sock set --exit-node=100.66.56.98 --exit-node-allow-lan-access=true
```

If this returns `node ... is not advertising an exit node`, the fix is not in the scraper. Re-check Android exit-node state, admin approval/routes, and ACL/grants for `autogroup:internet`.

## Scraper rule

Never run or judge anti-bot scrapers that require mobile/residential egress until this preflight passes. Preserve old source classifications and report the blocker as network/proxy, not site anti-bot or parser failure.
