# Deep Research V2 — operational completion pattern (2026-06-29)

Session learning: when Moufadal asks to “reprendre deepsearch” or challenges whether Deep Research is really done, do not treat a broad P0/P1 benchmark as proof of the full V2 pipeline. The benchmark must exercise the actual V2 runner and the later-stage capabilities: hybrid/community retrieval, dedupe, authority scoring, rerank, evidence extraction, claim/citation verification, final answer generation, and optional critique hooks.

## Acceptance evidence that counted

- Unit tests for both core V2 and completion-specific behaviours:
  - final writer output
  - date/freshness and contradiction flags in claim verification
  - critique stub behaviour
  - normalize, dedupe, authority, rerank, notes, claims, SQLite cache
- A/B benchmark that runs V2 end-to-end, not just baseline retrieval.
- Benchmark report states its discipline honestly: retrieval + evidence-pack benchmark, not blind human answer-quality proof.
- External audit pass from Claude Code with caveats captured in the final report.
- Progress file updated with a non-100% status when important caveats remain.

## Useful implementation pattern

- Keep Exa/unstable channels bounded by timeout and non-fatal fallback; do not let one provider block the benchmark.
- For stable proof, run a benchmark with reliable channels first, then label Exa/Reddit as caveats if they are rate-limited or unauthenticated.
- A deterministic heuristic writer is acceptable as an operational baseline if clearly labeled; do not oversell it as LLM-quality synthesis.
- Claim verification can start with quote overlap + freshness/date + contradiction flags, as long as weak support is explicitly surfaced.
- Optional Claude critique should be a hook (`none` by default) when benchmark cost/latency matters.

## Final-report wording to preserve

Use wording like: “operationally complete for the no-user-help scope, with explicit caveats.” Avoid “100% finished” unless blind answer-quality evaluation, stable external-channel integration, and desired neural/LLM rerankers are also proven.

## Caveats to keep visible

- Reddit public access may require OAuth/cookies.
- Exa can rate-limit/hang; bounded timeout + fallback is robustness, not proof of Exa availability.
- Neural rerankers such as BGE/Cohere are not active unless dependencies/credentials are present.
- A/B retrieval/evidence benchmarks are not human answer-quality evaluations.
- A run can be operationally useful while still having partial cases; record count and impact instead of hiding them.
