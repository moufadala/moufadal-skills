# Proxy-PASS benchmark completion audit pattern — 2026-06-30

## Context

A long background process launched a DeepResearch V2 benchmark only after the residential/Tailscale proxy gate passed. The process completed with exit code 0 and empty stderr. The right response was not to trust the notification blindly, but to inspect the run directory, gate file, benchmark summary, rows, and then run an independent critique pass.

## Durable pattern

When a benchmark is scheduled/started behind a proxy gate and later completes in background:

1. Inspect the wrapper run directory first:
   - `run.stdout`
   - `run.stderr`
   - proxy/preflight gate JSON
2. Confirm the gate explicitly:
   - `gate=PASS`
   - `proxy_status=PASS`
   - direct IP differs from proxy IP
   - SearXNG/docker service is OK when SearXNG evidence is in scope
3. Inspect the actual benchmark artifact directory named in stdout, not just the wrapper.
4. Read the final summary and report:
   - `benchmark_summary_final.json`
   - `benchmark_report_final.md/html`
   - `benchmark_rows_final.json`
5. Create a deterministic Hermes audit artifact with row-level checks and weak-row detection.
6. Ask Claude Code for a compact critique over the gate, summary, report, and Hermes audit.
7. Report separately:
   - **validated**: proxy gate, completion, retrieval/evidence-pack metrics;
   - **not validated**: answer-quality, claim→citation support, blind human evaluation.

## Concrete metrics from the observed run

The successful rerun showed:

- proxy gate: PASS;
- V2 completion: 60/60 distinct queries;
- rows: 120 total, baseline + V2;
- V2 average unique sources: 15.98 vs baseline 6.73;
- V2 average unique domains: 9.10 vs baseline 4.07;
- V2 average fetched_ok: 1.97 / 2;
- V2 average notes_total: 5.03;
- V2 average final_answer_chars: ~1952;
- weak V2 rows with `fetched_ok < 1` or `notes_total < 1`: 0;
- `claims_total`: 0.

## Interpretation discipline

Do say:

- “proxy-gated rerun completed”;
- “V2 retrieval and evidence-pack generation validated for this run”;
- “better raw material than the keyword baseline.”

Do **not** say:

- “the module answers better”;
- “quality is validated”;
- “production-grade research is proven.”

The blocker is `claims_total=0`: final answers exist, but the benchmark does not prove that each final claim is explicitly supported by citations.

## Claude critique lesson

Claude’s critique highlighted useful caveats to preserve in future reports:

- `claims_total=0` is blocking for quality certification.
- The baseline is asymmetric if it does not fetch pages, extract notes, or generate final answers.
- `top5_score` can improve only marginally even when source/domain volume improves a lot; watch reranking quality.
- A strict `fetch_attempted=2` cap is useful for bounded benchmark cost, but may under-cover complex topics.
- A blind human spot-check remains necessary before strong answer-quality claims.

## Recommended next validation step

Implement/run the full writer → explicit claims → claim-to-citation verification loop, then perform a blind human evaluation on 10–20 representative queries before claiming answer quality.