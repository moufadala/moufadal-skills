# Shell-generated report quoting and runtime reload pitfall

Session pattern captured 2026-07-01 during a Hermes runtime audit.

## Problem

When generating Markdown reports from shell with an unquoted heredoc, Markdown backticks and command snippets can be interpreted by the shell before the file is written. This can silently corrupt the report and may execute rollback/example commands embedded in the report.

Bad pattern:

```bash
cat > "$REPORT" <<EOF
- Smoke: PASS (`CLAUDE_OK`)
Rollback:
```bash
hermes config set compression.threshold 0.5
```
EOF
```

Because `EOF` is unquoted, command substitution inside backticks runs. In the captured session this corrupted `qa-report.md` and temporarily reverted `compression.threshold`.

## Safer patterns

Prefer Hermes `write_file` for reports/artifacts when content contains Markdown code spans or shell snippets.

If shell is required, use a quoted heredoc delimiter:

```bash
cat > "$REPORT" <<'EOF'
- Smoke: PASS (`CLAUDE_OK`)
Rollback:
```bash
hermes config set compression.threshold 0.5
```
EOF
```

For mixed dynamic + literal content, write dynamic values separately or use Python with explicit string construction and no shell interpolation.

## QA gate

After generating the report:

1. Read the report back.
2. Assert that expected code snippets remain literal.
3. Re-check any config values mentioned in rollback examples, because an unquoted heredoc may have executed them.
4. Rewrite the report with `write_file` if corruption is found.

## Runtime reload note

For Hermes/gateway prompt or config edits, writing files is not the same as runtime completion. The current gateway session can keep old prompt/config snapshots. Mark status as `partiellement terminé` until restart/new session is verified, and include rollback/restart commands.