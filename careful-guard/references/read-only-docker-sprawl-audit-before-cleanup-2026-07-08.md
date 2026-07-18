# Read-only Docker sprawl audit before cleanup (2026-07-08)

## When this applies

Use this when Moufadal says the VPS has “too many Docker containers”, asks whether Docker is a mess, or wants cleanup/rationalization of live containers.

## Core lesson

Do **not** equate container count with the root problem. Twenty containers is not automatically bad. The real issue is usually operational drift:

- preview/artifact containers left running indefinitely;
- public host ports outside Traefik;
- floating image tags such as `latest` / `alpine`;
- missing memory limits;
- inconsistent restart policies;
- unclear canonical vs preview services;
- old public routes still reachable.

Run a read-only audit first, then ask for explicit approval before any `docker stop/rm/restart/prune`.

## Safe read-only evidence bundle

Create a dated artifact directory:

```bash
RUN_DIR=/opt/data/artifacts/architecture-docker-audit/$(date -u +%Y%m%dT%H%M%SZ)
mkdir -p "$RUN_DIR/raw" "$RUN_DIR/scans"
```

Collect state without mutation:

```bash
docker ps -a --no-trunc --format '{{json .}}' > "$RUN_DIR/raw/docker_ps_all.jsonl"
docker images --digests --format '{{json .}}' > "$RUN_DIR/raw/docker_images.jsonl"
docker network ls --format '{{json .}}' > "$RUN_DIR/raw/docker_networks.jsonl"
docker volume ls --format '{{json .}}' > "$RUN_DIR/raw/docker_volumes.jsonl"
docker stats --no-stream --format '{{json .}}' > "$RUN_DIR/raw/docker_stats.jsonl"
docker inspect $(docker ps -aq) > "$RUN_DIR/raw/docker_inspect_all.json"
docker inspect $(docker network ls -q) > "$RUN_DIR/raw/docker_network_inspect_all.json"
docker system df -v > "$RUN_DIR/raw/docker_system_df.txt" 2>&1 || true
```

Optional bounded logs:

```bash
mkdir -p "$RUN_DIR/raw/recent-logs"
for c in $(docker ps --format '{{.Names}}'); do
  docker logs --tail 80 "$c" > "$RUN_DIR/raw/recent-logs/$c.log" 2>&1 || true
done
```

## Risk classifier to apply

Flag containers for review when they have:

- `HostConfig.RestartPolicy.Name` empty or `no`;
- `HostConfig.Memory == 0` for persistent services;
- published host bindings beginning with `0.0.0.0:`;
- `Config.Image` ending with `:latest` or `:alpine` for durable infra;
- preview-like names: `cand-*`, `*-preview-*`, old dated reports, one-off file servers;
- Traefik routes that still publish old candidates.

Classify results as:

- **P0/P1:** public direct port, vulnerable public reverse proxy, sensitive dashboard exposure.
- **P2:** memory/restart policy/tag hygiene, preview rationalization.
- **Cleanup candidate:** likely obsolete preview, but never delete without user approval.

## Scanner pattern

Install scanners in a sandbox path, not globally, unless explicitly asked:

```bash
TOOLS=/opt/data/tools/security-audit/bin
mkdir -p "$TOOLS"
# Install exact release assets for gitleaks/trivy into $TOOLS, then smoke with --version.
```

Use:

- `gitleaks detect --no-git --redact=100` for projects/scripts; report counts and top files/rules, not secret values.
- `trivy image --scanners vuln --severity CRITICAL,HIGH` for public-facing base images first (`traefik`, `nginx`, `searxng`, custom services).
- OpenCodeReview only as an LLM code-review layer; it does not replace Docker/security scanners.

## Reporting rule

Final report should separate:

1. “Count is a symptom” verdict.
2. Exact read-only evidence paths.
3. P0/P1/P2 risks.
4. Mutations requiring approval.
5. Rollback/reprise commands.

Never include raw secrets, full `.env`, or unredacted scanner findings in Telegram.

## Approval boundary

These actions remain **Red** and require explicit current-turn approval:

- `docker stop`, `docker rm`, `docker restart`, `docker compose down`, `docker system prune`;
- deleting volumes/images/logs/artifacts;
- changing Traefik, UFW, published ports, restart policies, memory limits;
- exposing dashboards/scanners publicly.

Safe first correction candidate is usually to propose a target list, not execute it.