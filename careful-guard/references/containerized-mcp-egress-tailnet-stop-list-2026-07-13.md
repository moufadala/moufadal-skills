# Containerized MCP egress + tailnet exposure — STOP-list pattern (2026-07-13)

## Trigger

Use this reference when repairing a host-run MCP/API service that must use a proxy or sidecar that exists only inside a Docker network, especially when the service is exposed to the tailnet with `tailscale serve`.

## Durable lesson

If a service runs on the **host** and points to `127.0.0.1:<proxy-port>`, while the working proxy actually lives inside a container, the fix is usually **not** to publish the proxy on the host. Prefer the proven in-network route:

```text
new service container on existing Docker network
  -> existing proxy/gateway DNS name:port
  -> existing egress path
```

For Moufadal's VPS class, this avoids touching the known-good gateway/SearXNG path and keeps the proxy private.

## Safe preflight before any mutation

Run only read-only checks first:

1. Pull/read the relevant vault/runbooks/specs.
2. Inspect the current service owner and route:
   - systemd status / process / listening port;
   - `tailscale serve status`;
   - existing Docker networks and container membership.
3. Prove the proposed in-network egress from a disposable container on the target network:

```bash
docker run --rm --network <network> --entrypoint sh <image-with-curl> -lc \
  'curl -x http://<gateway-container>:<relay-port> -4 -sS --max-time 20 https://api.ipify.org'
```

4. If Hermes is itself containerized but has Docker access, host facts can be collected read-only via:

```bash
# Read host filesystem without mutating it
docker run --rm -i -v /:/host:ro --entrypoint python3 <image> - <<'PY'
from pathlib import Path
# inspect exact files, redact secrets before printing
PY

# Query host namespace without changing host state
docker run --rm --privileged --pid=host --net=host --entrypoint sh <image> -lc \
  'nsenter --target 1 --mount --uts --ipc --net --pid sh -lc "tailscale serve status; systemctl status <service> --no-pager"'
```

Do not interpret missing `tailscale`, `systemctl`, or `ss` inside the Hermes container as host absence; verify host namespace first when needed.

## STOP-list before container recreation

Before `docker compose up -d --build`, `docker run -d`, service restart, or `tailscale serve` change, stop and ask Moufadal to approve an explicit list containing:

- exact files to create/patch;
- exact image/container names;
- exact port binding;
- exact Tailscale route change;
- exact resources explicitly excluded from mutation.

For live shared proxy/search paths, exclusions should name the protected containers and commands, e.g.:

- no `tailscale serve reset`;
- no restart/recreate of the existing gateway/proxy container;
- no restart/recreate of SearXNG or other working consumers;
- no host publication of private proxy ports;
- no deletion of the old server/stdio fallback until the new path is proven green.

## Blue/green shape

Prefer a parallel container on a new localhost port, then switch only the tailnet route after QA:

```text
old host service: 127.0.0.1:8770  (kept as rollback)
new container:   127.0.0.1:8771 -> container:8770
QA new container
if green and approved: tailscale serve --bg --http=80 http://127.0.0.1:8771
```

QA must include a real domain payload through the new path, not only a health check. For a transcript MCP, prove both:

- egress identity via the intended proxy/gateway;
- actual MCP tool call returning transcript text via local StreamableHTTP.

This keeps rollback simple:

```bash
tailscale serve --bg --http=80 http://127.0.0.1:<old-port>
docker compose -f <new-compose-file> down
cp -a <backup> <patched-file>
```

Keep the old backend alive until the remote client confirms the end-to-end tailnet path.

## Build/runtime pitfalls observed

- If the image build cannot reach PyPI, avoid declaring the architecture bad. A bounded workaround is copying a known-good venv into the image, but verify interpreter links and console scripts.
- Copied venvs may point to host paths such as `/usr/bin/python3.12`. Either use image Python with `PYTHONPATH` or add a compatible symlink, then smoke the actual CLI used by the service.
- `tailscale serve --http=PORT http://127.0.0.1:NEW` can fail if the listener already exists. Never use `tailscale serve reset` for this. Snapshot `tailscale serve status --json`, remove only the target listener with `tailscale serve --http=PORT off`, then recreate it with `--bg`. Without `--bg`, the route may disappear when the command exits or times out. See `references/tailscale-serve-scoped-route-update-2026-07-13.md`.

## Documentation anti-drift

After the fix is proven, supersede the old runbook section with a dated banner and proof commands/results. Do not silently erase the old diagnosis; mark it superseded so future sessions do not chase the old false culprit.
