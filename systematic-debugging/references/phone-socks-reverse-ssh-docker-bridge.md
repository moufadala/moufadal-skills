# Phone SOCKS reverse SSH through Docker-hosted Hermes

Use when a user needs Hermes/VPS to test traffic through a phone's residential/mobile network, and Hermes is running in a Docker container.

## Durable pattern

Target data path:

```text
Hermes container -> VPS host bridge -> ssh -R listener on VPS host -> phone-local SOCKS -> phone mobile Internet
```

A common wrong direction is `ssh -D` from the phone. That creates:

```text
phone -> VPS -> Internet
```

which does **not** let Hermes exit through the phone. For Hermes to exit through the phone, the phone should run a local SOCKS proxy and open a reverse SSH tunnel:

```text
# on phone / Termux
microsocks -i 127.0.0.1 -p 1081
ssh -N -R 0.0.0.0:1082:127.0.0.1:1081 root@VPS_IP
```

Success signal in `ssh -vvv`:

```text
remote forward success for: listen 0.0.0.0:1082, connect 127.0.0.1:1081
forwarding_success: all expected forwarding replies received
```

## Docker visibility pitfall

A successful `ssh -R` can still be invisible to Hermes if the listener lives in the VPS host network namespace while Hermes runs inside Docker. Test multiple candidates from the container:

- `127.0.0.1:1082` — container loopback, often wrong
- Docker host gateway, e.g. `172.16.1.1:1082`
- public VPS IP, e.g. `VPS_IP:1082`

If the host sees `127.0.0.1:1082` but the container cannot, create a host-side bridge with `socat`, e.g.:

```text
socat TCP-LISTEN:1083,bind=DOCKER_GATEWAY_IP,fork,reuseaddr TCP:127.0.0.1:1082
```

Then test from Hermes with SOCKS URL:

```text
socks5h://DOCKER_GATEWAY_IP:1083
```

## Copy/paste UX for this user

When the user is operating Termux/SSH manually:

1. Put commands in a `.txt` artifact for Telegram delivery when blocks are long.
2. Prefer one grouped block for the main path, plus an Option B with 3–4 smaller commands.
3. Avoid `/tmp` on Termux for logs; use `$HOME/...` or `$PREFIX/tmp`.
4. Tell the user explicitly that a blocking SSH command after authentication is normal: it means the tunnel is running.
5. Do not ask for or repeat SSH passwords, cookies, tokens, or private keys.

## Termux robustness notes

If Termux `curl` fails after package updates with a dynamic linker/symbol error, do not encode it as “curl broken forever.” The useful recovery pattern is to complete the package upgrade and reinstall the related libraries:

```text
pkg update -y && pkg upgrade -y && pkg install -y openssh curl openssl libngtcp2 microsocks
```

If `microsocks` fails because it cannot write under `/tmp`, redirect logs under `$HOME`:

```text
mkdir -p "$HOME/runwatch"
microsocks -i 127.0.0.1 -p 1081 > "$HOME/runwatch/microsocks.log" 2>&1 &
```

## Verification contract

Do not claim success from `remote forward success` alone. Verify from Hermes/container:

1. direct public IP, e.g. `curl -4 https://ifconfig.me`
2. proxied public IP via each candidate SOCKS endpoint
3. success only if proxied IP is non-empty and different from VPS direct IP

Report separately:

- SSH reverse tunnel accepted: yes/no
- SOCKS endpoint reachable from Hermes: yes/no
- residential/mobile egress proven: yes/no + IP comparison
