# DeepResearch V2 answer-quality benchmark: claim extraction + Claude judge retry

Session lesson from 2026-06-30.

## Trigger

Use this when validating DeepResearch/V2 answer quality after a retrieval benchmark, especially when the remaining gap is `writer → claims → citation verification → blind judge`.

## What happened

A V2 60-query retrieval benchmark passed operationally, but `claims_total=0`, so it did **not** prove final answer quality. A P1-lite answer-quality script was added to:

1. load the latest V2 benchmark rows;
2. collect V2 final answers and baseline answers;
3. extract explicit claims from cited answer bullets;
4. run a heuristic claim→citation support pass;
5. run a blind A/B Claude judge;
6. refresh the public clickable reports index.

## Important pitfall: preserve answer line breaks

Claim extraction was bullet/line based. A first run normalized the whole answer with whitespace collapse, which turned multiline cited bullets into a single line and produced false `deep_claims=0`.

Correct pattern:

```python
# Keep line breaks for bullet/line-based claim extraction
deep_answer = ((state.get("final_answer") or {}).get("answer") or "").strip()
```

Avoid this before claim extraction:

```python
deep_answer = normalize((state.get("final_answer") or {}).get("answer") or "")
```

Normalize individual claims/quotes after line splitting, not the entire answer before splitting.

## Important pitfall: judge failure can be transient

Claude judge inside the script returned a 401, but an immediate smoke test succeeded, and a manual retry against the same blind packet succeeded. The durable lesson is **retry the judge after a fresh smoke**, not “Claude is broken”.

Recovery pattern:

1. Read `judge_claude_raw.json` and confirm the actual error.
2. Run a live smoke: `claude -p 'Réponds exactement CLAUDE_OK' --allowedTools 'Read' --max-turns 1 --output-format json`.
3. If smoke passes, rerun only the judge over `judge_packet_blind.json` rather than rerunning retrieval/answer generation.
4. Decode winners with `answers_with_mapping.json`.
5. Patch `summary.json`, `judge_decoded.json`, and the Markdown/HTML report.
6. Refresh the public report index.

## Interpretation discipline

A good P1-lite result is a **signal**, not a production claim. Example successful retry:

- sample: 12 queries;
- DeepResearch won 11/12 blind A/B pairs;
- average score Deep 7.5 vs baseline 4.42;
- but claim support was mixed: Deep 120 claims, 60 supported / 60 unsupported by heuristic overlap.

Report as:

> DeepResearch V2 has a positive answer-quality signal, but final production validation still needs 50–60 query evaluation, stronger claim→citation verification, and preferably human spot-check.

Do **not** report as:

> DeepResearch V2 answer quality is fully validated.

## Artifacts pattern

```text
/opt/data/artifacts/answer-quality-benchmark/<timestamp>_v2_claims/
  summary.json
  answer_quality_report.md
  answer_quality_report.html
  judge_packet_blind.json
  judge_claude_raw.json
  judge_claude_retry_raw.json
  judge_decoded.json
  answers_with_mapping.json
  raw/q##_evidence.json
```
