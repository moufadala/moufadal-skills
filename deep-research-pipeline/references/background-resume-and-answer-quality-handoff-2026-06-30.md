# Background resume + answer-quality handoff pattern (2026-06-30)

## When to use

Use this when a long DeepResearch benchmark or overnight run completed while the main Hermes turn was interrupted, and Moufadal asks to `/continue` or resume the task in background.

## Durable lesson

A completed retrieval benchmark is not automatically a completed research-quality benchmark. If the final metrics show all queries completed but `claims_total` or equivalent claim-verification counters are zero, report the run as:

> operationally validated for retrieval/evidence-pack execution, not validated for final answer quality or claim support.

Do not phrase it as “the module is validated” unless final answers, extracted claims, citation support, and a judge/human spot-check have been exercised.

## Recovery steps

1. Inspect the canonical run directories and symlinks, not only the truncated background notification.
2. Read the benchmark summary JSON/Markdown and capture the key counters: distinct queries, completed queries, fetch attempts/OK, unique domains, notes/claims, and proxy/SearXNG preflight.
3. Generate a deterministic background synthesis artifact under the parent Hermes ops run, with Markdown/HTML/JSON outputs.
4. In Telegram, keep the verdict short: what is validated, what remains open, and the paths to reports. Do not paste raw logs.
5. If continuing quality validation, inspect the quality benchmark script before running it. A script may import heavy modules or execute work at import time, so even `--help` can hang if it is not built with an argparse guard.
6. If the quality script has hardcoded previous benchmark paths, update/copy it only after identifying the current canonical benchmark directory. Do not run a stale P0 benchmark against the wrong artifact set and present it as V2 proof.

## Suggested final verdict language

- `Retrieval 60/60 validé opérationnellement.`
- `Qualité réponse/claims non validée: claims_total=0 / pas de boucle writer→claims→citation.`
- `Prochaine étape: benchmark qualité réponse séparé avec claims, citations, blind judge/human spot-check.`

## Minimal artifact set

```text
<ops-run>/background_resume_synthesis_<timestamp>/BACKGROUND_RESUME_REPORT.md
<ops-run>/background_resume_synthesis_<timestamp>/BACKGROUND_RESUME_REPORT.html
<ops-run>/background_resume_synthesis_<timestamp>/qa_resume.json
<benchmark-run>/benchmark_summary_final.json
<benchmark-run>/benchmark_report_final.md
```
