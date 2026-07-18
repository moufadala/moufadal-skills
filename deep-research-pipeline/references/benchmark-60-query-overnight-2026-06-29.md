# 60-query benchmark correction — 2026-06-29

## Trigger

Use this when Moufadal asks whether the research module is really better, complains that the benchmark was not done, or asks to run the 50–60 query benchmark overnight.

## Core correction from the session

Moufadal corrected a framing error: a strategic multi-theme research pack is **not** the deliverable when the goal is to validate the research module. Do not answer with project research summaries when the active purpose is benchmark/evaluation.

Also: `20 queries × 3 methods = 60 rows` is **not** the requested “50–60 requêtes”. The requirement means 50–60 distinct user-like queries, each evaluated across the methods.

## Acceptance contract for a serious benchmark

A serious Deep Research module benchmark should include:

1. 50–60 distinct queries, not rows.
2. Equal or clearly documented retrieval budgets across compared methods.
3. Baseline method, Exa/Agent Reach-only method, and DeepP0 method.
4. Crash-safe/resumable writes after each query/method pair, e.g. `rows_partial.json`.
5. Full final artifacts: rows JSON/CSV, summary JSON, Markdown report, HTML report, raw evidence/logs.
6. Explicit claim discipline: retrieval/auditability is not the same as final answer quality.
7. A final audit pass that checks actual counts (`queries_expected`, `queries_completed_deep`, `rows_total`) before reporting.
8. If run overnight, use durable cron and a morning final-audit job, not a promise.

## Implementation pattern used

- Main script: `/opt/data/scripts/research_stack_benchmark_60.py`
- Wrapper: `/opt/data/scripts/run_deep_research_benchmark_60.sh`
- Contract artifact: `/opt/data/artifacts/deep-research-benchmark/overnight_contract_20260629.md`
- Expected benchmark root: `/opt/data/artifacts/deep-research-benchmark/20260629Tnight_60q/`

Important reusable features:

- `rows_partial.json` written atomically after each method.
- Resume by rerunning the same command with the same `--out-root`.
- Jina reader retry/backoff and bot/captcha marker rejection in `deep_research_runner.py`.
- Abort on repeated Exa/mcporter failures rather than fabricating success.
- HTML/Markdown reports must include “what this benchmark does NOT measure”.

## Telegram reporting discipline

When reporting to Moufadal:

- Lead with whether the 50–60 distinct-query benchmark is actually done, scheduled, partial, or blocked.
- Separate “research reports produced” from “module benchmark result”.
- Do not say “terminé” if the benchmark is only scheduled.
- Give clickable artifact links when available, but do not let links replace the benchmark verdict.
- Use plain language: “meilleure matière première vérifiable” rather than “objectivement meilleures réponses” unless final-answer eval supports it.

## Pitfalls

- Do not count method rows as queries.
- Do not use a P1-lite 8-pair answer-quality result as production proof.
- Do not answer with a strategy synthesis when the user asked for module evaluation.
- Do not hide rate limits; partial report is acceptable, fake completion is not.
