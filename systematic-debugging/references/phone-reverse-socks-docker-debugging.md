# Phone reverse SOCKS proxy through VPS + Docker — debugging pattern

Use when the user is trying to make Hermes/a Dockerized agent browse through a phone/mobile residential IP using Termux + SSH reverse forwarding.

## Target architecture

```text
Hermes/container -> VPS host -> SSH reverse forward -> phone local SOCKS -> mobile/VPN/Internet
```

Typical phone side:

```text
microsocks -i 127.0.0.1 -p 1081
ssh -N -R 0.0.0.0:1082:127.0.0.1:1081 root@<vps-ip>
```

Important distinction:

- `ssh -D ...` is the wrong direction for making the VPS/Hermes exit through the phone; it makes the phone use the VPS as a SOCKS proxy.
- `ssh -R ...` is the required direction for making the VPS reach a phone-local SOCKS server.

## Boundary-by-boundary verification

1. **Phone local proxy**
   - Verify the phone can browse through its local SOCKS server before SSH is considered.
   - Example: `curl --socks5-hostname 127.0.0.1:1081 https://ifconfig.me`.

2. **SSH reverse forward accepted**
   - Positive indicator: `remote forward success` / `forwarding_success`.
   - This only proves SSH accepted the port; it does not prove the SOCKS target is alive.

3. **VPS host smoke test**
   - Before changing Docker/firewall, test from the VPS host:
   - `curl --socks5-hostname 127.0.0.1:1082 https://ifconfig.me`.
   - Expected: IP differs from the VPS public IP. If the phone VPN is on, this may be a VPN IP rather than residential/mobile.

4. **Container/Hermes reachability**
   - Only after the host smoke test passes, diagnose Docker access.
   - Docker bridge/firewall rules may prevent container -> host bridge access.
   - Consult Docker docs for `DOCKER-USER`, bridge networking, host networking, and `host-gateway` before mutating firewall rules.

## Durable pitfalls

- Termux command delivery is fragile over Telegram. Prefer `.txt` artifacts with one copy-paste block and explicit expected output.
- Avoid `/tmp` assumptions in Termux; use `$HOME/...` or `$PREFIX/tmp` for logs.
- If the user has a VPN enabled on the phone, the tunnel may exit through the VPN, not the carrier/mobile IP. That can be valid for a VPN test but is not proof of residential/mobile egress.
- Do not claim success from SSH logs alone. Final proof is an IP comparison: direct VPS IP vs IP through the SOCKS proxy.
- Do not ask the user for or store SSH passwords, keys, cookies, or tokens. If they appear in logs, redact them.

## Research anchors

- Docker packet filtering and firewalls: `https://docs.docker.com/engine/network/packet-filtering-firewalls/`
- Docker with iptables / `DOCKER-USER`: `https://docs.docker.com/engine/network/firewall-iptables/`
- Docker bridge network driver: `https://docs.docker.com/engine/network/drivers/bridge/`
- Docker host network driver: `https://docs.docker.com/engine/network/drivers/host/`
- OpenSSH `GatewayPorts`: `https://man.openbsd.org/sshd_config#GatewayPorts`
- OpenSSH `ssh -R`: `https://man.openbsd.org/ssh#R`
