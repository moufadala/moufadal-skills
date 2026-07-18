# Deep Research V2 60-query benchmark: execution proof vs answer-quality proof

Session lesson from a fixed 60 distinct-query V2 benchmark run.

## What the run proved

A completed benchmark with:

- `queries_completed_v2=60/60`
- `status_complete=60`
- non-zero source/domain/evidence-note metrics
- generated final answer artifacts

is valid evidence that the runner is operational and more auditable than a simple discovery baseline.

It can support claims like:

- “V2 runs end-to-end without crashing on 60 distinct queries.”
- “V2 collects more unique sources/domains than the keyword baseline.”
- “V2 produces evidence packs and deterministic answer artifacts.”

## What it does NOT prove

Do not call the module “finished” or “premium answer-quality validated” when any of these are true:

- `avg_claims_total=0` — no structured final claims are being verified against citations.
- baseline rows have `avg_final_answer_chars=0` — the A/B is asymmetric and does not compare final answer quality.
- `avg_fetch_attempted` is very low, e.g. ~2, while `avg_sources_unique` is much higher — most discovered sources are not read.
- no blind human eval / external judge evaluated factuality, usefulness, hallucination, or citation support.

## Why `avg_claims_total=0` can happen intentionally

In V2, automatic conversion of evidence notes into claims may be disabled to avoid circular validation:

> evidence quote → generated claim from same quote → verify claim against same quote

That would produce fake “supported” labels. If no external or writer-generated claims are submitted back into `verify_claims()`, zero claims is safer than bogus claims — but it means the claim-verification loop is not complete.

## Required next gate

Before declaring V2 quality-complete:

1. Add a writer step that produces explicit final claims from the answer.
2. Submit those claims back through `verify_claims()` against the evidence pack.
3. Report supported / weak / unsupported claims separately.
4. Run a 10–15 query smoke with higher fetch depth, e.g. `fetch_top=5`.
5. Run a blind human or external answer-quality eval on real final answers.

## Reporting language

Use:

- “retrieval/evidence-pack benchmark passed”
- “operational run completed”
- “better raw material and auditability”

Avoid unless independently evaluated:

- “answers are better”
- “premium research quality is validated”
- “module finished”
