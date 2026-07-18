# Android phone as residential/mobile egress — validation notes

Use when a user wants Hermes/VPS scraping traffic to exit through their phone/mobile IP.

## Lesson from field session

A Termux stack can work technically but is high-friction for the user:

- Android may suspend Termux or rotate network state.
- Phone VPN changes the egress path (`VPS -> phone -> VPN -> Internet`) and invalidates a “mobile/residential IP” proof.
- SSH reverse tunnels can show `remote forward success` and later die with `Software caused connection abort` / `Broken pipe`.
- A normal `ssh root@host` login is not equivalent to a reverse tunnel; it does not create the remote SOCKS port.
- Docker/Hermes introduces a second boundary after the host: a port that works on the VPS host may still be unreachable from the Hermes container.

## Boundary validation order

Do not jump directly to Docker/firewall changes. Validate one boundary at a time:

1. **Phone local egress**
   - VPN off if the goal is mobile/residential IP.
   - Phone on 4G/5G if possible.
   - Confirm direct phone IP and proxy-local IP from the phone.
2. **Phone proxy process**
   - Confirm SOCKS/HTTP proxy is running locally on phone.
3. **Reverse/mesh transport to VPS host**
   - For SSH `-R`, look for `remote forward success`.
   - Then immediately test on the VPS host: `curl --socks5-hostname 127.0.0.1:PORT https://ifconfig.me`.
4. **Only after host test passes: integrate Hermes/Docker**
   - Prefer a contained test mechanism (`--network host`, Tailscale client, host-side probe) before durable firewall edits.
   - If touching Docker firewall, use Docker’s documented `DOCKER-USER` path rather than random `INPUT`/`FORWARD` edits.

## Tailscale Android exit node: community-validated but not magic

When the user rejects Termux/SSH and asks for a simpler non-paid way to make a VPS use a phone/mobile/residential egress, Tailscale Android exit node is the most plausible class-level path — but validate before changing routes.

Evidence pattern to check:

- Official Tailscale docs for exit nodes list Android among supported exit-node platforms and describe opt-in approval in the admin console.
- Tailscale GitHub issue history contains signals that Android can run as an exit node (for example, the iOS feature-request discussion notes it was already possible on Android).
- Also check recent Android issues before action: users report connectivity/DNS/notification/automation quirks, so Android is not a guaranteed 24/7 router.

Risk model:

- **Do not route the whole VPS globally as the first test.** Changing the VPS default route through a phone can disrupt SSH, Telegram gateway, Docker, cron, package installs, and webhooks.
- Android exit node stability depends on battery optimization, VPN state, cellular/Wi-Fi transitions, and app foreground/background behavior.
- A phone VPN invalidates the “mobile/residential” proof because the path becomes `VPS -> Tailscale -> phone -> VPN -> Internet`.
- Mobile/residential IP improves the “datacenter IP blocked” hypothesis, but does not bypass browser fingerprinting, hCaptcha, Cloudflare/Turnstile, Imperva, cookies, or behavioral checks.

Recommended Tailscale rollout:

1. Install/login Tailscale on phone and VPS, but do not enable exit routing yet.
2. Confirm both devices appear online in the tailnet.
3. On Android, enable **Run as exit node**; in the admin console approve **Use as exit node**.
4. Prefer an isolated smoke test over global routing. Evaluate Tailscale userspace/SOCKS or a dedicated test lane/container before touching the VPS default route; if global routing is unavoidable, prepare rollback and keep an existing SSH session open.
5. Smoke proof: compare direct VPS IP vs egress IP through the Android exit node. Success requires the egress IP to differ from the VPS and match the expected mobile/operator path.
6. Only after proof, use it for short, targeted RUN Watch tests; do not leave it as the permanent VPS default route.

Useful success probability framing from field research:

- Technical Tailscale Android exit-node success: roughly 70–85% if setup is clean.
- Different-from-VPS egress IP with VPN off + 4G/5G: roughly 80–90%.
- Resolving anti-bot blocking: much lower and site-dependent (roughly 40–65%); treat as diagnostic, not a guarantee.

## Better options when user fatigue appears

If the user signals frustration with Termux/SSH/tunnels/copy-paste, stop expanding instructions. Switch to a **minimum-user-effort mode**:

- Do all possible VPS-side prep yourself first.
- Give the user **one short action at a time**, clearly labeled by location: **Phone**, **Browser/Admin console**, or **VPS**.
- Give one unavoidable action at a time, with the exact location: **Phone**, **Browser/admin console**, or **VPS**.
- Do not ask the user to paste logs until after your own probes are exhausted.

### Low-copy Tailscale rollout when Hermes lacks sudo on the VPS

When root/sudo is unavailable, Hermes can still do most server work without asking the user to paste commands:

1. Download static Tailscale locally under a user-writable path, e.g. `/opt/data/tools/tailscale`.
2. Launch `tailscaled` with Hermes process tracking, not shell `nohup`: `./tailscaled --tun=userspace-networking --socks5-server=127.0.0.1:1055 --state=/opt/data/tailscale-userspace.state --socket=/opt/data/tailscale-userspace.sock`.
3. Run `tailscale --socket=/opt/data/tailscale-userspace.sock up --hostname=vps-hermes-userspace --accept-dns=false` and give the user only the OAuth URL to approve in a browser.
4. Verify membership with `tailscale --socket=... status`; expect both the VPS userspace node and Android node.
5. Try `tailscale --socket=... set --exit-node=<android-100.x-ip> --exit-node-allow-lan-access`.
6. If the error says `node ... is not advertising an exit node`, the Android app may show “Now running as exit node” but the admin-console approval is still missing. Direct the user specifically to **Browser → Tailscale Machines → Android device → Edit route settings → Use as exit node → Save**. Do not point them to Mullvad; Mullvad exit nodes are unrelated.
7. Use the userspace SOCKS endpoint for isolated proof before global routing: compare direct `curl https://ifconfig.me` with `curl --socks5-hostname 127.0.0.1:1055 https://ifconfig.me`.

Respect explicit constraints:

1. **Tailscale exit node on Android** — official exit-node feature supports Android; cleaner than SSH reverse for durable routing, but configure cautiously so the whole VPS is not accidentally routed through the phone.
2. **Android proxy server app + Tailscale** — possible, but app quality varies; validate with a host-side curl smoke test.
3. **Direct phone testing** — only suggest if the user is willing; some users reject it because they specifically need the server/VPS egress.
4. **Paid residential/mobile proxy** — only mention as tradeoff if budget is acceptable; if the user says “payant non”, drop it.

## No-sudo VPS path: local Tailscale userspace probe

When the VPS account has no sudo/root, do not stop immediately. A useful low-risk path is to download Tailscale under `/opt/data` and run `tailscaled` in userspace mode with a local SOCKS proxy. This avoids installing packages, changing routes, or risking SSH/gateway disruption.

Pattern:

```bash
mkdir -p /opt/data/tools/tailscale /opt/data/logs
cd /opt/data/tools/tailscale
curl -fsSL https://pkgs.tailscale.com/stable/tailscale_latest_amd64.tgz -o tailscale.tgz
tar -xzf tailscale.tgz --strip-components=1
./tailscaled \
  --tun=userspace-networking \
  --socks5-server=127.0.0.1:1055 \
  --state=/opt/data/tailscale-userspace.state \
  --socket=/opt/data/tailscale-userspace.sock
```

In Hermes, start the daemon with `terminal(background=true)` rather than shell `nohup`/`&`, then in a separate call run:

```bash
/opt/data/tools/tailscale/tailscale --socket=/opt/data/tailscale-userspace.sock up --hostname=vps-hermes-userspace --accept-dns=false
```

This prints a Tailscale auth URL. Ask the user to open/approve only that link. After auth and Android exit-node approval, smoke-test via the SOCKS path first:

```bash
curl -4 https://ifconfig.me
curl -4 --socks5-hostname 127.0.0.1:1055 https://ifconfig.me
```

Success requires different IPs, with the SOCKS result matching the phone/mobile/operator egress. Only after that consider any global route (`tailscale up --exit-node=...`) and keep rollback ready.

## Success proof

A phone egress setup is not proven by “SSH connected” or “remote forward success” alone. Require:

- VPS direct IP shown (for example `148.230.103.174` in the field session), and
- proxied/exit-node IP shown via the phone path, and
- proxied/exit-node IP differs from VPS direct IP.

Only then call it working.