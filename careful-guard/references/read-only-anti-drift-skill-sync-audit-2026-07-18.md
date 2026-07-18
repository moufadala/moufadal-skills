# Read-only anti-drift / skill-sync audit — 2026-07-18

Use this reference when validating cross-machine agent hygiene, shared skill sync, MCP availability, or audit scripts that run from inside the Hermes gateway container while host paths differ.

## Context

A PC-side Claude Code session installed an anti-drift layer and shared skills into the VPS. Hermes was asked to independently validate it with a strict STOP-list: read-only, no gateway/container restart, no manual `jobs.json` edits.

The first validation found several real faults even though the implementation looked plausible.

## Durable lessons

### 1. Host paths and Hermes runtime paths are different

Hermes often sees host `/opt/hermes/data` as container `/opt/data`.

A symlink that is valid on the host can be broken inside Hermes if it targets `/opt/hermes/data/...` absolutely. For skills loaded by Hermes, verify from the runtime path, not only the host path.

Good validation probes:

```bash
docker exec hermes-gateway sh -lc 'ls -l /opt/data/skills/<dir>/<skill>/SKILL.md'
docker exec hermes-gateway sh -lc 'for d in /opt/data/skills/<dir>/*; do test -f "$d/SKILL.md" && echo "$(basename "$d") ok" || echo "$(basename "$d") broken"; done'
```

Prefer relative symlinks such as:

```text
../../projects/moufadal-skills/<skill>
```

instead of host-absolute `/opt/hermes/data/...` targets.

### 2. Validate the actual skill loader, not only files on disk

After fixing skill paths, prove both layers:

- filesystem: every symlink resolves to a `SKILL.md` inside `hermes-gateway`;
- loader: `skills_list` shows the expected category and `skill_view(<name>)` works.

If a skill name collides, `skill_view("name")` may become ambiguous. Verify the explicit categorized form such as `skill_view("moufadal-pc/prompt-to-design")`.

### 3. Git remotes behind SSH aliases can make audit rules false-green

A repo remote like:

```text
git@github-skills:moufadala/moufadal-skills
```

may not match naive markers such as `github.com/moufadala/...`. Audit code should match the repo identity (`moufadala/moufadal-skills`) or include the approved alias marker, otherwise it may report “clone absent expected” while the repo exists and is dirty/diverged.

### 4. `dubious ownership` can make secret/skills/vault scans vacuous

When the audit runs as a different user than the repo owner, `git ls-files` can return zero because of Git safe-directory protection. A green secret scan with `tracked_files_scanned=0` is not evidence.

Pattern:

```bash
git -c safe.directory=* ls-files
```

For a fallback secret scan, fail non-green if:

```text
gitleaks absent AND tracked_files_scanned == 0
```

### 5. `bash -lc` PATH can create false red alerts

A command may exist for the agent process but be absent inside a login shell. If an audit script probes documented commands via `bash -lc`, set a known PATH or use absolute paths for critical tools such as Hermes:

```bash
export PATH="/opt/hermes/.venv/bin:/opt/hermes/bin:$PATH"
```

Do not classify `hermes: command not found` from one probe path as a real system failure until another runtime path is checked.

### 6. Read-only validation can still create audit artifacts

Under a read-only STOP-list, it is acceptable for the audit mechanism itself to write its own timestamped evidence under an artifacts directory if that is the audited contract. Do not restart services or edit scheduler state to “prove” a reload unless explicitly authorized.

## Acceptance criteria for future revalidation

- `--mode host`: green, and host doctor resolves critical tools by absolute path.
- `--mode hourly`: green, with non-vacuous evidence:
  - secrets scan has `tracked_files_scanned > 0` or gitleaks ran;
  - skills repo locate method is a real remote match;
  - clone aligned/clean if present.
- `--mode daily`: green, with Hermes probes no longer failing due to PATH.
- Runtime skill proof: every shared-skill symlink resolves inside `hermes-gateway`, and at least one representative new skill loads via `skill_view`.
- MCP proof: use an actual MCP initialize/tools probe or `hermes mcp list`, not only container presence.
- Exit-node decisions remain separate: prove selected exit-node and per-capability egress before changing host/global routing.
