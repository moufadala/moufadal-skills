# Tailscale userspace exit-node + Uptime Kuma heartbeat — Phase A P0 (2026-07-14)

## Trigger

Use this when a task asks for **per-capability residential egress** through a specific Tailscale exit node, with proof that the VPS itself is **not globally routed**, and with a dead-man heartbeat/Telegram alert.

## What worked

- Keep global VPS routing unchanged.
- Use the existing Tailscale **userspace** node as the per-capability egress path:
  - `tailscaled --tun=userspace-networking --socks5-server=127.0.0.1:1055 --socket=/opt/data/tailscale-userspace.sock`
  - switch only that node with:
    ```bash
    /opt/data/tools/tailscale/tailscale --socket=/opt/data/tailscale-userspace.sock set \
      --exit-node=<pc-dns-name> --exit-node-allow-lan-access=true
    ```
- Prove both boundaries:
  - direct VPS IP: `curl -4 https://ifconfig.co`
  - per-capability SOCKS IP: `curl -4 --socks5-hostname 127.0.0.1:1055 https://ifconfig.co`
  - Tailscale selected node: `tailscale --socket=... status --json`, peer must have `ExitNode=true` and `Online=true`.

## Important pitfall: IP equality can be misleading

If the PC and phone are on the same residential network, `ifconfig.co` may return the **same public IP** for both. Do not claim the egress is via the PC from IP alone. Pair IP proof with Tailscale state showing the selected peer has `ExitNode=true`; also record the S25 peer as `ExitNode=false` or `offers exit node` only.

## Uptime Kuma pattern

- Run Kuma as a separate new container; do not touch `hermes-gateway`, Traefik, or the target app containers.
- Bind Kuma to host loopback only, e.g. `127.0.0.1:3001:3001`.
- From inside Hermes, `127.0.0.1:3001` may be a false negative because it is host-loopback. Verify Kuma from host network with a temporary container:
  ```bash
  docker run --rm --net=host alpine:3.20 sh -lc 'wget -S -O - http://127.0.0.1:3001/ | head'
  ```
- For a push monitor, script should push `OK` only if:
  1. selected PC peer is active exit-node in Tailscale JSON;
  2. SOCKS IP is non-empty and differs from direct VPS IP;
  3. optional expected SOCKS IP matches if pinned.
- If the monitor runs every minute, set Kuma push interval with margin (e.g. 120s), otherwise minute-boundary jitter can create false `No heartbeat in the time window` flaps.

## Kuma automation notes

- Kuma v1 can be configured through its Socket.IO API from inside the container (`socket.io-client` is already installed in the image).
- Telegram notification provider fields: `telegramBotToken`, `telegramChatID`, optional `telegramMessageThreadID`.
- Uptime Kuma image may not have `wget`; to call its local push URL from Hermes, use an ephemeral container sharing Kuma's network namespace:
  ```bash
  docker run --rm --net=container:uptime-kuma alpine:3.20 \
    sh -lc "wget -q -O - 'http://127.0.0.1:3001/api/push/<token>?status=up&msg=OK' >/dev/null"
  ```

## Permissions pitfall

Kuma writes files in its volume as root. If Hermes needs to maintain local secret files (`admin.env`, `phasea_push.env`) under the same volume, fix only those files or the top-level service directory, not the whole `/opt/data` tree:

```bash
docker run --rm -v /opt/hermes/data/services/uptime-kuma:/mnt alpine:3.20 \
  sh -lc 'chown 10000:10000 /mnt/admin.env /mnt/phasea_push.env && chmod 600 /mnt/admin.env /mnt/phasea_push.env'
```

Keep bot tokens and push tokens out of the vault and reports; store them under `/opt/data/services/...` or `/opt/data/.env` with mode `0600`.

## QA contract

Phase is not fully done until the physical failure test passes:

1. Normal state: direct IP != SOCKS IP; Tailscale peer selected as PC exit-node; Kuma heartbeat `UP`.
2. User cuts Tailscale/Internet on the PC for 2–3 minutes.
3. Kuma sends Telegram DOWN alert.
4. User restores PC connectivity.
5. Kuma sends recovery / heartbeat returns UP.

If the physical cut is not performed, report `installed + heartbeat OK, but QA final missing`; do not advance to the next phase.

## Rollback

```bash
hermes cron pause <heartbeat_job_id>
/opt/data/tools/tailscale/tailscale --socket=/opt/data/tailscale-userspace.sock set --exit-node=<previous-node>
docker rm -f uptime-kuma
```

If the previous node was S25, use its MagicDNS name; do not route the host VPS globally as a rollback shortcut.
