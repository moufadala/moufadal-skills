# V2 answer-quality background benchmark pattern — 2026-06-30

## Trigger

Use this when a DeepResearch V2 benchmark has already proven retrieval/execution (for example 60/60 rows) but still has `claims_total=0`, and Moufadal asks to “lance toutes les actions recommandées en background” or asks to advance validation without waiting.

## Lesson

A clean V2 retrieval benchmark is not enough to claim answer quality. The next safe autonomous step is a **P1-lite answer-quality background pass**:

1. Reuse the latest V2 benchmark artifact directory, not stale P0 artifacts.
2. For each sampled V2 run, read `research_state_v2.json` and use its `final_answer.answer` plus `notes`.
3. Extract explicit claims from answer bullets that include `[source: URL]` citations.
4. Verify claim→citation support separately. A pragmatic first pass can use lexical overlap against fetched evidence notes, but must label this as heuristic, not human/NLI proof.
5. Build a strengthened baseline by fetching top baseline URLs, so the comparison is not unfair snippet-only search.
6. Randomize A/B labels and ask Claude Code/Claude CLI for a blind judge when available.
7. Write durable artifacts: `summary.json`, `judge_decoded.json`, `answers_with_mapping.json`, `raw/q*_evidence.json`, `answer_quality_report.md/html`.
8. Refresh the public clickable report index after the benchmark artifacts are created.

## Concrete script pattern from this session

A reusable background script was created at:

```bash
/opt/data/scripts/answer_quality_benchmark_v2_background.py
```

Typical launch:

```bash
BENCH_DIR=/opt/data/artifacts/deep-research-benchmark/<latest_v2_60q> \
AQ_SAMPLE_N=12 \
python3 /opt/data/scripts/answer_quality_benchmark_v2_background.py
```

Run it as a Hermes background process with `notify_on_complete=true` for immediate continuation work.

## Reporting discipline

Say:

- `retrieval/exécution validé` when 60/60 V2 rows exist;
- `answer-quality en cours de validation` while the background pass runs;
- `signal P1-lite` after a small sample;
- **not** “module terminé” or “réponses objectivement meilleures” until claims are explicitly verified and at least one blind/human spot-check or stronger judge pass exists.

## Pitfalls

- Do not rerun hours of retrieval just to validate answer quality if `research_state_v2.json` already contains final answers and notes.
- Do not reuse `answer_quality_benchmark.py` blindly if it points at an older P0 directory; inspect the script’s hardcoded `PREV`/artifact paths first.
- Do not let Claude judge its own visible mapping: write a blind packet without the A/B mapping, keep mapping only in an audit file.
- Heuristic lexical support is a triage gate, not a final factuality proof.
