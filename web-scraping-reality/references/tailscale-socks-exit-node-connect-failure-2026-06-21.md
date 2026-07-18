# Tailscale userspace SOCKS: magicsock logs ≠ working exit-node internet

## Trigger
Use when a flight/scraping rerun depends on the Android/Tailscale mobile proxy (`127.0.0.1:1055`) and logs show `magicsock` / `wgengine` activity, but scrapers still fail with network/preflight errors.

## Lesson from 2026-06-21
Do **not** treat Tailscale daemon logs as proof that the SOCKS proxy can reach the public internet. In this session:

- `tailscaled --tun=userspace-networking --socks5-server=127.0.0.1:1055` was running.
- Logs showed `magicsock: disco` and `wgengine: sending TSMP disco key advertisement`.
- `tailscale status --json` showed the Android phone online and selected as exit node.
- Local SOCKS handshake succeeded: TCP connect to `127.0.0.1:1055` + greeting returned `0x05 0x00`.
- But SOCKS `CONNECT api.ipify.org:443` failed with `0x05 0x01` / `curl: (97) cannot complete SOCKS5 connection`.

Verdict: tailnet connectivity and SOCKS listener were alive, but internet egress through the phone was not usable. Scraper failures under this condition must be classified as `network-preflight-failed`, not site anti-bot, no-offer, or scraper failure.

## Required preflight before rerunning proxy-dependent scrapers

```bash
printf 'time='; date -u +%Y-%m-%dT%H:%M:%SZ
printf 'direct='; curl -4 -sS --max-time 8 https://api.ipify.org || true; echo
printf 'socks='; curl -4 -sS --max-time 15 --socks5-hostname 127.0.0.1:1055 https://api.ipify.org || true; echo
/opt/data/tools/tailscale/tailscale --socket=/opt/data/tailscale-userspace.sock status --json | python3 -m json.tool | sed -n '1,160p'
/opt/data/tools/tailscale/tailscale --socket=/opt/data/tailscale-userspace.sock debug prefs | grep -E 'RouteAll|ExitNodeID|ExitNodeIP|ExitNodeAllowLANAccess'
/opt/data/tools/tailscale/tailscale --socket=/opt/data/tailscale-userspace.sock exit-node list
```

Optional low-level SOCKS check:

```python
import socket, struct, time
host='api.ipify.org'; port=443
s=socket.socket(); s.settimeout(8)
s.connect(('127.0.0.1',1055))
s.sendall(b'\x05\x01\x00')
print('greeting', s.recv(2))
h=host.encode()
s.sendall(b'\x05\x01\x00\x03'+bytes([len(h)])+h+struct.pack('!H', port))
print('connect_resp', s.recv(10))
```

Interpretation:

- `direct` and `socks` both return IPs and differ → proxy usable; run proxy-dependent cases.
- SOCKS handshake OK but `curl: (97)` or SOCKS connect response `0x05 0x01` → listener is alive but exit-node egress is broken; do **not** rerun scrapers yet.
- `magicsock` / `wgengine` logs only → not sufficient; they prove tailnet chatter, not internet egress.

## Android-side fix checklist

Ask the user to check the phone before rerunning:

1. Open Tailscale Android.
2. Confirm VPN is active.
3. Confirm “Run as exit node” / “Exécuter comme nœud de sortie” is enabled.
4. If already enabled, toggle Tailscale off/on on the phone.
5. Disable battery saver / sleep for the rerun window.

Only rerun the failed proxy-dependent cases after `direct VPS != socks phone` is proven.