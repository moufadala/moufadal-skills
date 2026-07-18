# Tailscale Android Exit Node for VPS Residential/Mobile IP — 2026-06-14

## Why this exists

During RUN Watch anti-bot work, a Termux + `microsocks` + `ssh -R` phone proxy technically reached `remote forward success`, but was too fragile for user operations: Android/network/VPN/keepalive broke the tunnel, and Docker/VPS bridging added complexity.

The better class-level pattern is to validate a phone/VPS exit path via Tailscale Android exit node, with community/docs validation and strict risk controls.

## Verified sources / signals

Official Tailscale docs checked:

- https://tailscale.com/docs/features/exit-nodes
- https://tailscale.com/docs/features/exit-nodes/how-to/setup
- https://tailscale.com/kb/1103/exit-nodes

Useful verified facts:

- Exit nodes route public internet traffic through a tailnet device.
- Exit-node routes are effectively `0.0.0.0/0` and `::/0`.
- Android is listed by Tailscale as supported for exit-node use.
- Exit nodes require explicit approval/use; do not assume they are active just because devices are on the tailnet.

Community/GitHub risk signals checked:

- `tailscale/tailscale#5636`: Android exit-node capability existed/was discussed.
- Android issues around connectivity/DNS/notifications/automation show Android can be less stable than a server/router. Treat as a useful test/mobile IP path, not a guaranteed 24/7 router.

## Recommended architecture

Do **not** naïvely route the whole production VPS/Hermes permanently through the phone.

Safer phases:

1. Phone: install Tailscale, VPN off if true mobile IP is required, battery optimization disabled if available.
2. Tailscale admin: authorize Android as exit node.
3. VPS: install/login Tailscale, verify peer visibility.
4. Smoke test for a short command/window:
   - before: direct IP = VPS public IP;
   - after selecting Android exit node: IP != VPS public IP;
   - verify no critical service is broken.
5. Prefer isolated use for scraping probes:
   - temporary shell/session only, or
   - separate container/network namespace, or
   - userspace/SOCKS mode if supported by installed Tailscale version,
   rather than global permanent route for the whole VPS.
6. Roll back immediately after test: stop using exit node / restore direct route.

## Risk checklist before using for scraping

- VPN on phone disabled? If not, traffic becomes `VPS → phone → VPN → Internet`, not true mobile/residential.
- Phone on mobile data or desired network? Wi-Fi may not prove mobile IP.
- Battery saver disabled / app allowed background activity?
- Tailscale admin console exit-node approval done?
- Direct and proxied IP recorded with timestamps?
- Critical VPS access path still available after any route change?
- Rollback command/runbook written before enabling?

## Expected value for anti-bot

- Good for testing whether datacenter IP reputation is the blocker.
- Not a guaranteed bypass for Cloudflare/Imperva/hCaptcha/Akamai, because fingerprint, cookies, challenges, TLS/HTTP2 behavior, and session state can still block.
- Treat as one evidence branch in the anti-bot hierarchy, not as a universal scraper fix.

## Anti-patterns

- Recommending paid residential proxies before validating free/user-owned mobile exit options when the user wants no paid option.
- Continuing brittle Termux reverse tunnels after the user expresses fatigue; switch to a simpler supported overlay network approach.
- Modifying global VPS routing without a before/after IP proof and rollback.
- Claiming “residential proxy works” from `remote forward success` alone; prove with `curl ifconfig` through the path.
