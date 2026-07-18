# Exit-node debugging: don't skip the trivial client-side proof

## Trigger
Use when a multi-component failure depends on a phone/VPN/proxy/tunnel path, especially when the user operates one endpoint manually.

## Lesson from session
The user correctly called out that a scraper verdict was premature because the exit-node/proxy preflight had not been done first. The fix was trivial once checked: Android was connected to Tailscale, but at one point showed `EXIT NODE = None`; later, after enabling it, the VPS saw `ExitNodeOption: true`, `AllowedIPs` included default routes, and SOCKS egress changed from the VPS IP to the mobile IP.

## Boundary proof order
For phone/Tailscale/SOCKS chains, prove each boundary before diagnosing the application:

1. Phone app: connected and actually advertising/running exit node, not merely connected.
2. Control plane/client view from VPS: `exit-node list` contains the phone and JSON has `ExitNodeOption: true`.
3. Route advertisement: `AllowedIPs` includes `0.0.0.0/0` and/or `::/0`.
4. Egress proof: direct IP and SOCKS IP differ.
5. Application launch: browser/scraper receives the proxy explicitly; remove `--no-proxy` or direct-fallback flags.

## Signals that are not enough
- Tailscale `Connected` in the phone app.
- Admin console badge saying `Exit Node`.
- `magicsock`, `wgengine`, DERP/disco logs.
- `tailscale ping` to the phone.

These prove tailnet connectivity, not public internet egress through the phone.

## User-facing rule
If the user says “you should have checked that first” and they are right, acknowledge directly, then run the preflight. Don't keep explaining the old hypothesis.