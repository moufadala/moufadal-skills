# Tailscale Serve — scoped route update without reset (2026-07-13)

## When this applies

Use when a live `tailscale serve` route must be moved from one local backend port to another while preserving other published routes on the same node.

Concrete class: a tailnet-only MCP/HTTP service is blue/greened from `127.0.0.1:OLD` to `127.0.0.1:NEW`, while another route such as SearXNG on `:8443` must remain untouched.

## Lesson

`tailscale serve --http=80 http://127.0.0.1:NEW` may fail with:

```text
listener already exists for port 80
```

Do **not** fix this with `tailscale serve reset`; it deletes every Serve route on the node.

The safe scoped pattern is:

```bash
# Snapshot first
tailscale serve status
tailscale serve status --json > /path/to/serve-status-before.json

# Remove only the listener being changed, then recreate it in background mode
tailscale serve --http=80 off
tailscale serve --bg --http=80 http://127.0.0.1:NEW

# Verify all expected routes, not just the changed one
tailscale serve status
tailscale serve status --json
```

Important: without `--bg`, `tailscale serve` runs in the foreground. If the controlling command times out or exits, the route can disappear even though it briefly printed the desired proxy. Always use `--bg` for persistent gateway changes.

## Rollback pattern

If the downstream client test fails, immediately restore the old listener only:

```bash
tailscale serve --bg --http=80 http://127.0.0.1:OLD
```

Then verify:

```bash
tailscale serve status
```

## Verification checklist

- The changed route points to the new port.
- Unrelated routes are still present, e.g. `:8443 -> 127.0.0.1:8888`.
- Old backend is still listening if it is the rollback path.
- New backend is listening and logs real requests.
- End-to-end client test passes before deleting or stopping the old backend.
