# VPS adversarial audit + targeted permission hardening (2026-07-08)

Use this reference when Moufadal asks to “audit under another angle”, “do not stop until fixed”, or when a previous Docker/runtime audit passed but security/ops drift may remain.

## Pattern that worked

1. Treat the second pass as a different threat model, not a repeat of Docker checks:
   - container/host boundary (`/.dockerenv`, PID 1, namespace limitations),
   - sensitive file and directory permissions,
   - cron script existence and paused/error jobs,
   - runtime smoke after any permission change,
   - Graphify/MCP/cockpit/watchdog reachability,
   - dirty Git repos and missing project markers,
   - logs with recent errors, storage/backups/rollback evidence.
2. Collect read-only evidence into a fresh run dir before any mutation.
3. Ask Claude Code for adversarial review, but parse print-mode JSON strictly. If it hits `error_max_turns`, retry once with a compact no-tool synthesis prompt from already-collected facts rather than treating the failed run as proof.
4. Apply only safe, reversible fixes; keep metadata backups for every permission change.
5. Run a final audit after the last mutation and require `issues: []` or explicitly list remaining blocked/non-actionable items.

## Permission hardening pitfall

Do **not** harden files by a broad filename regex like `token|secret|credential` across `/opt/data` or `$HOME`.

That catches false positives such as:
- Python packages: `tokenizers`, `pydantic_settings/sources/providers/secrets.py`, `pygments/token.py`;
- Node modules and SDK examples;
- docs and skills that mention “secrets” but are not secret material.

Over-hardening those to `0600`/`0700` can break imports and CLI tools. In the session this broke `pydantic_settings`; the regression was caught by an import smoke and restored from permission metadata.

## Safer permission scope

Prefer a narrow allowlist of real state paths:

- `~/.claude/*auth*`, `~/.claude/*credential*`, `mcp-needs-auth-cache.json`;
- `~/.hermes/auth.json`, `~/.hermes/.env`, profile equivalents;
- `/opt/data/config.yaml` if it contains tokens or provider headers;
- project-specific `secrets/`, `.env`, API key files;
- Graphify secret directories and cron/auth JSON files.

Recommended modes:

- secret files: `0600`;
- secret directories: `0700` when the runtime user owns and traverses them;
- do **not** make a root-owned parent directory `0700` if Hermes scripts need to traverse it. Protect files inside instead, or fix ownership first.

## Docker helper path mapping

When Hermes sees `/opt/data/...`, Docker bind mounts must usually use host path `/opt/hermes/data/...`.

Example for a root-owned file visible to Hermes as `/opt/data/.claude/mcp-needs-auth-cache.json`:

```bash
docker run --rm \
  -v /opt/hermes/data:/data \
  --entrypoint /bin/sh alpine:3.22 \
  -lc 'chmod 600 /data/.claude/mcp-needs-auth-cache.json'
```

Using `-v /opt/data:/data` from inside the Hermes container may point at the wrong filesystem and produce false “No such file” results.

## Mandatory post-fix smoke checks

After permission hardening, verify at least:

```bash
python3 -c 'import tokenizers, yaml, pydantic_settings; print("PY_IMPORTS_OK")'
claude -p 'Réponds exactement CLAUDE_OK' --allowedTools 'Read' --max-turns 1 --output-format json
/opt/data/scripts/morning_brief.py --help
hermes mcp test graphify
hermes cron list
```

If any smoke fails, treat it as a regression caused by the hardening until disproven. Restore false positives from the permission metadata backup, then re-run the smoke.

## Reporting standard

Final report should include:

- initial findings and what was corrected;
- explicit false positives/regressions and their restoration;
- final audit JSON path with `issues: []` or remaining issues;
- backup/rollback path for permission metadata;
- honest limit: token rotation requires user approval unless active compromise is proven, because it can break Hermes/Claude authentication.
