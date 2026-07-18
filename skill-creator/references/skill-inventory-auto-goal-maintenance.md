# Skill Inventory Auto-Goal Maintenance

Use this reference when Moufadal asks to “faire le max”, “auto goal”, “reprendre tous les skills”, or clean up the skill system without leaving tool-sprawl.

## Contract

The goal is not to rewrite every skill. The goal is to make the skill registry healthier while preserving rollback:

1. Snapshot all readable `SKILL.md` files before edits.
2. Audit all roots: `/opt/data/skills`, `/opt/data/home/.claude/skills`, `/opt/data/home/.agents/skills`.
3. Fix low-risk structural issues first: missing frontmatter fields, name/folder mismatches, oversized skill loader limits.
4. Quarantine duplicates or mismatched legacy directories instead of deleting them.
5. For generic stub skills, reduce triggering by changing descriptions to legacy/deprecated routing notes; do not delete unless the user explicitly approves.
6. Treat external installed skills such as Claude `.claude/skills/notebooklm` and `.agents/skills/notebooklm` as intentionally duplicated unless proven otherwise.
7. Rerun the audit after every batch and report remaining blockers.

Use P1/P2/P3 to avoid tool-sprawl:
- **P1**: usage pilots on high-impact skills. Pick 5–8 candidates, inspect at least 3 deeply, patch only obvious safe improvements to triggers, pitfalls, verification, examples, references, and report-quality guidance.
- **P2**: consolidation proposals. Identify overlaps, generic stubs, duplicate content and oversized files. Apply only non-destructive routing/pointer fixes; everything else becomes `approval-needed`.
- **P3**: future instrumentation. Define recurring trigger evals, telemetry, dashboards and deprecation governance, but do not run heavyweight evals for every skill in a cron/autonomous pass.

For final handoffs, prefer the Hermes Report V1 template for maintenance reports and keep `skill-creator/eval-viewer/generate_review.py` for actual skill eval review. Do not build custom report stacks unless the output is becoming a durable app.

## Commands / artifact pattern

Use an artifact directory such as:

```text
/opt/data/artifacts/skill-creator-audit-<timestamp>/
```

Save:

- `skills_inventory.json`
- `AUDIT_RAW.md`
- `duplicates.json`
- pre-edit snapshot manifest
- metadata-fix report
- quarantine path if any
- eval workspaces and viewer HTML when evals are involved

## Safe fixes

- Add missing `version`, `author`, `license` frontmatter when absent.
- Rename a skill directory to match `name:` only if no target directory exists and all contents move together.
- If old mismatch directories reappear or both old/new exist, move the old mismatch directory to an artifact quarantine path, not `rm -rf`.
- Split a `SKILL.md` over loader limits into `references/*.md` and leave a clear pointer in the main skill.

## Blockers

If a skill is root-owned/unreadable and the current process lacks permission, do not pretend it was fixed. Record the exact `stat`/`chmod` output and the required targeted host command. Do not run broad ownership changes.

## Verification

Before final report:

```bash
python3 <artifact_dir>/audit_skills.py
python3 - <<'PY'
import json
from collections import Counter
from pathlib import Path
j=json.loads(Path('<artifact_dir>/skills_inventory.json').read_text())
print(j['summary'])
print(Counter(e for s in j['skills'] for e in s.get('errors', [])))
PY
```

For Skill Creator evals, generate the static viewer with:

```bash
python3 /opt/data/skills/software-development/skill-creator/eval-viewer/generate_review.py \
  <workspace>/iteration-N \
  --previous-workspace <workspace>/iteration-N-1 \
  --skill-name "..." \
  --benchmark <workspace>/iteration-N/benchmark.json \
  --static <artifact_dir>/pilot-evals-review-final.html
```

## Final report

Include:

- before/after error counts;
- exact files changed or quarantined;
- eval pass-rate trend;
- blockers with exact command needed;
- rollback path;
- what was deliberately not deleted and why.
