# PC remote-control outage over Tailscale — 2026-07-09

## Situation class

Moufadal reports that a home PC still has Wi‑Fi, but both Claude Code Remote Control and Chrome/Google Remote Desktop stopped working after local agent/network/second-brain changes. The agent is on the VPS and may not have an interactive shell on the PC.

## Durable debugging pattern

1. **Do not assume Wi‑Fi or Tailscale is dead. Prove the boundary.**
   - From the VPS/container, first identify whether Tailscale is host-level or userspace.
   - If userspace Tailscale exists, use the explicit socket, e.g. `/opt/data/tools/tailscale/tailscale --socket=/opt/data/tailscale-userspace.sock status --json`.
   - Extract PC peers, `LastSeen`, `Online`, `AllowedIPs`, `ExitNode`, `PeerAPIURL`.
   - `tailscale ping <peer>` is more authoritative than `status Online=false`; a peer can show offline-ish metadata while still answering direct pings.

2. **Separate network reachability from control capability.**
   - Probe common execution/control ports without mutating anything: `22`, `3389`, `5985`, `5986`, app-specific ports such as `8765/8770`, Chrome DevTools `9222`, and observable Windows ports like `135/445/5357/7680`.
   - If `tailscale ping` and Windows service ports answer but SSH/WinRM/RDP/app ports do not, the PC is reachable but lacks a remote execution channel. Do not claim “Tailscale is broken.”

3. **Check provider-side basics before blaming local config.**
   - From the VPS, smoke `https://remotedesktop.google.com`, `https://api.anthropic.com`, and `https://claude.ai` with `curl -I --max-time ...`.
   - Chrome Remote Desktop needs Internet plus outbound UDP responses, TCP 443, and TCP/UDP 3478/STUN per Google help docs.
   - Claude Code Remote Control uses outbound HTTPS only through Anthropic; it does not open inbound ports on the PC.

4. **Use Taildrop as a recovery delivery channel when no shell is available.**
   - If the PC is reachable on Tailscale but no shell/control channel exists, create two PowerShell artifacts:
     - a read-only diagnostic script: routes, DNS, proxy, hosts, services, endpoint tests, Claude version/auth/doctor;
     - a minimal reversible repair script: snapshot first, restart only known services if present, open `claude remote-control --verbose` in a new terminal.
   - Send them with `tailscale file cp <file> <peer>:` and ask the person physically at the PC to run them.

5. **Avoid destructive “network reset” before evidence.**
   - Do not run or ask for `tailscale down`, WireGuard uninstall, DNS/proxy resets, `netsh int ip reset`, firewall rule deletion, Chrome Remote Desktop reinstall, or pairing resets before collecting route/DNS/proxy/service evidence.
   - Prefer disabling/commenting/restarting one component with a transcript/backout path.

## Claude Code Remote Control-specific checks

From Anthropic docs observed during this session:

- Remote Control requires `claude.ai` OAuth/subscription; API-key-only auth is insufficient.
- It only activates when `claude remote-control`, `claude --remote-control`, or `/remote-control` is run unless auto-connect is enabled.
- It uses outbound HTTPS only; failures often come from network/proxy blocking Anthropic.
- `ANTHROPIC_BASE_URL` pointing anywhere other than `api.anthropic.com` disables Remote Control in recent Claude Code versions; unset it for the Remote Control process.
- Local process must stay running. If the laptop sleeps or has an extended network outage, the session can time out/exit; restart `claude remote-control`.
- `claude remote-control --verbose` is the right repair/smoke command because it surfaces credential/network reasons.

## Example evidence contract

A future final answer should distinguish:

- **Network reachable:** `tailscale ping` output, peer IP, relay/direct path.
- **Execution unavailable:** port probes for SSH/WinRM/RDP/app endpoints.
- **Provider endpoints reachable:** HTTP status from Google/Anthropic.
- **Artifacts delivered:** paths to diagnostic/repair scripts and whether Taildrop returned success.
- **Remaining blocker:** human/local PC action needed if no remote execution channel exists.
