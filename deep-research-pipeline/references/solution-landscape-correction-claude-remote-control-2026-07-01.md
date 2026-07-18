# Solution-landscape correction — Claude remote control from phone (2026-07-01)

## Context
Moufadal asked how to control a home Claude Desktop/Claude environment from Android. The first answer listed only obvious remote-desktop/VPN/SSH options. Moufadal corrected: “Non y a d'autres solutions. Deepresearch”. A DeepResearch pass then surfaced a more important product-native path: **Claude Code Remote Control**.

## Durable lesson
For “what are my solutions/options?” questions around tools, remote access, AI agents, or infrastructure, do not answer only from the obvious generic stack. Run a quick landscape discovery and explicitly check whether the target product has a **native remote/mobile/control feature** before recommending generic workarounds.

## Example: Claude environment from Android
Useful solution families found:

- Product-native: **Claude Code Remote Control** (`claude remote-control`) lets `claude.ai/code` or the Claude mobile app connect to a local Claude Code session while local filesystem/MCP/tools stay on the machine. Official doc: `https://code.claude.com/docs/en/remote-control`.
- Private network + GUI: Tailscale + RustDesk.
- Browser gateway: Apache Guacamole for RDP/VNC/SSH through browser.
- Fleet/self-hosted remote admin: MeshCentral.
- Reverse tunnel/gateway: Cloudflare Tunnel/ngrok/frp + Guacamole/noVNC, with security caveats.
- Low-latency graphical: Parsec or Moonlight/Sunshine.
- CLI-native: Tailscale + SSH + tmux + Claude Code.
- Simple proprietary fallback: Chrome Remote Desktop/AnyDesk/TeamViewer.
- Hardware fallback: KVM over IP, only for BIOS/crash-level access.

## Response pattern
When corrected for insufficient breadth:

1. Acknowledge directly that the first answer was too narrow.
2. Run DeepResearch/official-doc extraction instead of defending the initial answer.
3. Separate **native product capability** from generic remote-control workarounds.
4. Rank by user goal: “control the visual desktop” vs “use local Claude with files/MCP/tools”.
5. Warn against direct RDP/VNC exposure; prefer Tailscale/VPN or controlled tunnel.

## Security/UX caveats
- Never recommend exposing RDP/VNC directly to the internet.
- Remote desktop on phone has poor UX for long text work; for Claude workflows prefer Claude Code Remote Control or SSH/tmux when possible.
- Browser gateways and tunnels add attack surface; require auth, MFA, and least exposure.
