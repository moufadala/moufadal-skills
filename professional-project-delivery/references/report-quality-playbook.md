# Report Quality Playbook — evidence-rich HTML reports

Use this reference when Moufadal asks for reports, research synthesis, eval viewers, QA handoffs, dashboards, or “progress on reports”. The goal is not prettier HTML; the goal is **decision value + verifiable evidence + low tool-sprawl**.

## Core lesson

Moufadal strongly values interactive HTML reports/viewers with tabs such as `Résumé`, `Output`, `Benchmark`, `Sources`, `Evidence`, `Failures`, and `QA`. This should be treated as a professional delivery standard for substantial work, not a cosmetic extra.

Default recommendation:

```text
self-contained static HTML + Markdown notes + JSON/source map + QA proof
```

Do **not** reach for React/Vite by default. React/Vite is justified only when the report becomes a durable app with complex state, reusable components, many filters, large data volume, or recurring publication. For simple tabs/KPIs/filtering, vanilla HTML/CSS/JS is the right default because it is portable, Telegram-friendly, archivable, and avoids tool-sprawl.

## Report types and when to use them

1. **Executive brief** — decision in 2 minutes: verdict, options, risks, proof.
2. **Evidence ledger** — commands, logs, sources, screenshots, pass/fail, artifact paths.
3. **Eval viewer** — input, output, expected behavior, rubric, score, judge reason, failures.
4. **Benchmark dashboard** — versions/runs, pass rate, variance, regressions, failure clusters.
5. **Incident postmortem** — impact, timeline, causes, recovery, action items.
6. **Decision memo** — options, criteria, cost, risk, recommendation, missing proof.
7. **Product QA report** — acceptance contract, browser QA, console, screenshots, bugs fixed/remaining.
8. **Research notebook** — consulted sources, extracts, hypotheses, uncertainties.
9. **Artifact manifest** — files, role, size, how to open, QA status.
10. **Source map** — URLs, consulted vs search-only, reliability, extracted facts, impact on decision.

## Default artifact structure

For substantial work:

```text
/opt/data/artifacts/<topic>-<YYYYMMDD>/
  index.html or report.html
  data/
    report-data.json
    source-map.json
  notes/
    research-notes.md
    decision-memo.md
  qa/
    qa-report.md
    screenshots/
  raw/
    command-outputs.txt
```

For small work:

```text
report.html
source-map.json
qa-report.md
```

## Recommended HTML tabs

Default order:

1. `Résumé` — verdict, decision, risks.
2. `Evidence` — proofs, commands, source links, artifact paths.
3. `Output` — full generated output or inspected result.
4. `Benchmark` — metrics, comparisons, before/after.
5. `Failures` — failed cases, limits, blockers.
6. `Sources` — consulted sources vs failed/search-only sources.
7. `Next` — concrete next actions.
8. `Raw` — JSON/logs only when useful.

## Quality rules

A report is good if:

- it answers a clear question;
- the verdict is visible within 10 seconds;
- sources are separated into consulted/extracted vs merely found;
- data shows provenance, freshness, and confidence;
- failures and limits are visible, not hidden;
- next actions are concrete;
- a machine-readable file exists when data is non-trivial;
- QA proves the HTML opens and expected tabs/sections exist;
- browser console is checked for interactive reports.

For each item/case/card when applicable, include decision-grade fields:

- stable `id` or label;
- source/provenance link;
- timestamp/freshness;
- status: pass/fail/blocked/unknown;
- score or priority with explanation;
- key evidence excerpt or output snippet;
- recommended action;
- owner/lane if operational;
- rollback path if a system change was made.

Use this relevance score to avoid pretty-but-useless reports:

- decision usefulness: 20
- verifiable evidence: 20
- provenance clarity: 15
- scanability/mobile: 15
- real QA: 15
- minimal tooling: 10
- reversibility/next actions: 5

## Anti-patterns

- Beautiful dashboard with no decision question.
- Average score without failed examples.
- Source list that mixes extracted sources and search-result-only links.
- “It works” without command/browser/screenshot proof.
- Adding React/Vite/Quarto/Observable just to get tabs or cards.
- Giving many artifact paths without an index or manifest.

## Tool decision matrix

- **Static HTML/CSS/JS**: default V1. Best for Telegram/mobile, archive, handoff, light interaction.
- **React/Vite**: durable app or complex state/components only.
- **Quarto**: reproducible research/data reports with citations/PDF needs.
- **Observable Framework**: recurring data apps/dashboards where build tooling is accepted.
- **Jupyter**: exploration/workbench, not final client handoff by default.
- **Streamlit**: internal dynamic prototype; needs server/runtime.
- **Grafana/Metabase**: recurring operational metrics, not one-off project reports.
- **W&B/MLflow**: recurring experiment tracking; avoid for occasional evals.

## Reusable Hermes Report V1 template

For future one-off reports, do not rebuild the report shell from scratch. Start from the bundled lightweight template and QA script in this skill:

```text
professional-project-delivery/
  templates/hermes-report-v1.html               # static HTML/CSS/JS with premium tabs/cards
  scripts/validate_hermes_report_v1.py          # no-dependency QA gate
  references/hermes-report-v1-bundle.md         # source-map contract + scoring rules
```

On Moufadal’s VPS there may also be a convenience copy under `/opt/data/templates/hermes-report-v1/`, but the skill-bundled files are the portable source of truth.

Use this template when no more specialized viewer exists. Keep `skill-creator/eval-viewer/generate_review.py` for skill eval reviews because it already has the right workflow. Use React/Vite only after the tool decision matrix justifies a durable app.

Minimum implementation loop:

1. Create `/opt/data/artifacts/<topic>-<YYYYMMDD>/`.
2. Fill `report.html` from `report.html.template` with only non-empty tabs.
3. Write `source-map.json` with consulted vs failed/limited sources.
4. Add `qa-report.md` or validation log.
5. Run:

```bash
python3 /opt/data/templates/hermes-report-v1/validate_report.py \
  /opt/data/artifacts/<topic>/report.html \
  --source-map /opt/data/artifacts/<topic>/source-map.json
```

## Verification gate

Before final reply for a substantial report:

```text
- files exist and sizes are non-zero;
- HTML contains expected sections/tabs;
- browser opens artifact when browser QA is relevant/available;
- click at least one non-default tab for interactive reports;
- console has no blocking JS errors when browser QA is relevant/available;
- source-map distinguishes consulted vs failed/limited sources;
- validate_report.py returns pass for Hermes Report V1 bundles;
- final message gives artifact path, QA proof, limits, and next step.
```
