# Read-only socle audit recalibration + doc↔reality drift — 2026-07-12

## Context

Moufadal asked to recalibrate a read-only Hermes cron audit of the shared vault/agent architecture. Audited targets stayed read-only; the only allowed mutation was the audit script itself, with backup + rollback.

This extends the class-level pattern in `read-only-socle-audit-cron-2026-07-12.md`.

## Durable lessons

### 1. Repository absence can be the expected architecture

Do not assume every source-of-truth repository should be cloned on the VPS. For `moufadal-skills`, the PC is the source of truth and Hermes already has critical skills natively. A VPS clone would be a duplicate/anti-pattern.

Audit rule pattern:

- Green/info when the expected remote clone is absent on this host.
- Red only if a clone exists on this host and is dirty, ahead/behind, diverged, or has unpushed commits.
- Match exact remotes; do not treat similarly named repos as equivalent.

### 2. A living vault is not expected to be clean

The Obsidian vault on the VPS is a live workspace with autosave jobs. `git status` being non-empty is not automatically an incident.

Audit rule pattern:

- Red: ahead/behind/divergence from origin; pending file path looks secret-like; mass deletion/rename; likely structural move directly on `main`.
- Green/info: normal pending files from autosave/live work.
- Output filenames only, never file content or diff hunks.

### 3. Doc↔reality drift checks must be deliberately narrow

Daily runbook/ADR drift checks are useful, but they can become unsafe if they run arbitrary code blocks.

Safe extraction pattern:

- Scan only runbooks/ADR docs.
- Freshness (`last_verified`, `last_verified_utc`, `timestamp`) older than 30 days is info/reminder, not red.
- Execute only fenced `bash|sh|shell|console` blocks explicitly marked `QA`, `Commande QA`, `lecture seule`, or `read-only`.
- Never execute unmarked blocks, text fences, restart/reprise/deploy/destructive commands, credential repair commands, pipes to shell, redirections, `git push/reset/clean/checkout`, `rm`, `cp`, `chmod`, `chown`, `kill`, `docker restart`, etc.
- Treat refused commands as info with reason, not red.
- Commands that are read-only but too slow/flaky for daily automation (e.g. `hermes doctor || true`) should be refused or moved to manual QA.

### 4. Avoid false contradictions

Operational text near a QA command may mention “broken”, “fallback”, “cassé”, or historical failures. Do not infer that a successful probe contradicts the doc unless the doc has an explicit expected-negative assertion such as `expected=KO`, `statut=rouge`, or “doit échouer”.

A non-zero probe exit is red drift/failure. A zero exit is red only if it contradicts an explicit expected-negative assertion.

### 5. Subprocess output should be robustly decoded

For audit probes, use UTF-8 with `errors='replace'` or equivalent. A command like `docker exec ... wget ... | head` can return bytes that trigger strict decode failures; that is an audit-wrapper bug, not necessarily service drift.

### 6. Verification before declaring the audit clean

Definition-of-done for this class:

- Backup path recorded.
- Diff saved.
- Script compiles/smokes.
- Direct hourly + daily runs executed.
- Actual cron jobs manually run via scheduler.
- Latest artifacts inspected for per-block verdicts.
- Output/artifacts scanned for secret-like values.
- Rollback command provided.

## Example resulting verdicts from the calibrated run

- Hourly A/B/C: green; pending vault files listed by name only.
- Daily D/E/F: green; F scanned runbooks/ADR, ran explicit safe QA probes, refused unsafe commands, and found no drift.
