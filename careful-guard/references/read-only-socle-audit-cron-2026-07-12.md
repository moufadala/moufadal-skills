# Read-only socle audit cron pattern (2026-07-12)

Use this when Moufadal asks for a durable audit/watchdog whose scope is **audit and report only**: no repair, no config mutation, no push/fetch/checkout, no edits to other agents' state.

## What worked

- Classify the setup itself as the only allowed mutation: creating local audit scripts/artifacts/cron jobs. Keep audited targets read-only.
- Split cadence by risk/cost:
  - hourly: secrets scan + skills repo alignment + vault git hygiene;
  - daily: shared tools/MCP/runbook coherence + documented version-divergence checks;
  - daily morning digest: aggregate dated artifacts.
- Use script-only cron jobs with `no_agent=true` when the output contract is deterministic:
  - empty stdout = silent green;
  - non-empty stdout = concise red alert;
  - separate digest job prints the daily summary.
- Write dated redacted artifacts under `/opt/data/artifacts/<audit-name>/...` and cite paths in alerts.
- Verify with a manual smoke run before reporting job IDs.
- Add a rollback block with exact `hermes cron remove <job_id>` commands.

## Secret-safe reporting rules

- Prefer `gitleaks --redact` if installed; otherwise scan tracked files with conservative filename/content patterns.
- Never print matched lines or secret values. Findings should include only `path` + `reason` + counters.
- Re-scan produced artifacts/digests for secret-like assignments before claiming they are safe.

## Git read-only hygiene

Allowed examples:

```bash
git status --porcelain=v1
git branch --show-current
git rev-parse --abbrev-ref --symbolic-full-name '@{u}'
git rev-list --left-right --count HEAD...@{u}
git diff --name-status --find-renames
```

Avoid in this class of audit unless explicitly authorized:

```bash
git fetch
git pull
git checkout
git diff        # content diff can expose secrets
git show        # content can expose secrets
```

## Repo identity pitfall

When checking a named shared repo, match the **exact remote**. Do not accept similar names.
Example: for `moufadala/moufadal-skills`, do not treat `moufadala/hermes-quality-skills-reports` as equivalent just because the name contains `skills`.

## Reporting style

Final report should include:

- created job IDs and schedules;
- current verdict per block (`🟢 OK`, `🔴 écart`, `ℹ️ info`);
- proof artifact paths;
- manual smoke output summary;
- rollback commands.

Do not repair red findings in the same mission when the user explicitly asked for lecture seule.