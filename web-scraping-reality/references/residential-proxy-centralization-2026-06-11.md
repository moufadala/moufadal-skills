# Residential SOCKS proxy centralization — 2026-06-11

## Durable lesson

For scraping stacks that depend on a residential/mobile SOCKS proxy, avoid hardcoding `172.16.1.1:1080` or `127.0.0.1:1080` inside individual scrapers. Use one shared helper or config value so host/container differences are handled once.

## Recommended pattern

- Environment override first: `SOCKS_PROXY` or `HERMES_SOCKS_PROXY`.
- Container default: `socks5://172.16.1.1:1080`.
- Host default: `socks5://127.0.0.1:1080`.
- Requests/PySocks libraries: prefer `socks5h://...` so DNS resolution happens through the proxy.
- Playwright: use `socks5://...` in `proxy={"server": ...}`.

## Verification gate

Before blaming a scraper, verify the SOCKS chain itself:

```python
import socket
for host in ['127.0.0.1', '172.16.1.1']:
    s = socket.socket(); s.settimeout(2)
    try:
        s.connect((host, 1080))
        s.sendall(b'\x05\x01\x00')
        print(host, s.recv(2).hex())  # expected: 0500
    except Exception as e:
        print(host, type(e).__name__, e)
    finally:
        s.close()
```

Expected SOCKS5 no-auth handshake reply: `0500`.

## Restore workflow when down

If both `127.0.0.1:1080` and `172.16.1.1:1080` refuse connections, the scraper config is not the primary issue. Check the upstream mobile/Android reverse SSH leg first, typically VPS `:2222`, then start/restart the host-level SOCKS service.

Recommended host bridge shape:

```bash
ssh -o ExitOnForwardFailure=yes \
  -o ServerAliveInterval=15 \
  -o ServerAliveCountMax=3 \
  -D 0.0.0.0:1080 \
  -p 2222 \
  -N phone_user@localhost
```

Persist this as a systemd service on the VPS host, not inside the Hermes container. Containers should consume it via the Docker host gateway address.

## Scope

This is a production hygiene pattern for scrapers; it does not claim any specific proxy provider or mobile tunnel is always available. Treat missing tunnels as setup state and report it as such.