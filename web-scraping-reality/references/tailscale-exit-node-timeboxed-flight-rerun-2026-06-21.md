# Tailscale exit node preflight + time-boxed scraper rerun

## Context
When using a user's Android phone as a Tailscale exit node for anti-bot flight scraping, the phone may disrupt the user's normal connectivity while exit-node mode is active. Treat the proxy window as scarce.

## Durable lesson
Do not spend the validated mobile-proxy window on sources that do not primarily need it. Once the SOCKS proxy is proven live, immediately run the proxy-dependent target(s) first.

## Minimal preflight before any scraper verdict
Run from the VPS/client side:

```bash
TS=/opt/data/tools/tailscale/tailscale
SOCK=/opt/data/tailscale-userspace.sock
$TS --socket=$SOCK exit-node list
$TS --socket=$SOCK status --json | jq '.Peer[]? | select(.HostName|test("s25|moufadal";"i")) | {HostName, ExitNode, ExitNodeOption, AllowedIPs}'
curl -4 -sS --max-time 8 https://api.ipify.org
curl -4 -sS --max-time 15 --socks5-hostname 127.0.0.1:1055 https://api.ipify.org
```

Success requires:
- `exit-node list` shows the Android node.
- `ExitNodeOption: true`.
- `AllowedIPs` includes `0.0.0.0/0` and/or `::/0`.
- SOCKS IP differs from VPS direct IP.

## Interpretation pitfalls
- Android app `Connected` only proves tailnet connectivity, not exit-node routing.
- Admin-console badge `Exit Node` is not enough if the phone app currently shows `EXIT NODE = None`.
- Logs like `magicsock`, `wgengine`, DERP/disco only show Tailscale connectivity, not public egress through the phone.
- If `socks_ip == direct_ip`, classify as `network-preflight-failed`, not scraper/site failure.

## Campaign ordering under a scarce proxy window
1. Validate proxy IP.
2. Start with the scraper/site that actually needs mobile egress (e.g. French Bee/Akamai/Imperva path), not easier official sites that already work directly.
3. Remove any local `--no-proxy` flags before launch.
4. Run in background with `notify_on_complete=true` and artifact paths.
5. Re-check SOCKS IP during the run if the user says they may disable the phone proxy.

## User-facing behavior
If the user says this was trivial or should have been checked first, acknowledge directly and do the preflight immediately. Do not defend the previous conclusion.