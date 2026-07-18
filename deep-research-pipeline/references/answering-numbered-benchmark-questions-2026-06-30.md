# Answering numbered benchmark questions

When Moufadal asks something like “réponds aux questions 1 5 6 8 10…” after a DeepResearch benchmark, treat the numbers as likely **indices in the benchmark query list**, not as a new questionnaire, unless the immediate context clearly says otherwise.

Important disambiguation: if the latest user message itself contains or quotes a numbered question menu (for example Obsidian/second-brain questions 1–35), that explicit menu wins. Do not answer benchmark rows just because an older task involved benchmarks. In that case, route to the relevant domain skill, e.g. `obsidian/references/answering-numbered-second-brain-questions.md`.

## Recommended recovery pattern

1. Locate the canonical benchmark artifact directory first, preferably the latest `benchmark_summary_final.json` / `benchmark_rows_final.json` under `/opt/data/artifacts/deep-research-benchmark/`.
2. Filter rows to the active method, usually `deep_research_v2`, before indexing. Do not mix baseline rows with V2 rows.
3. Use 1-based indexing: question `1` = first V2 row.
4. For each requested number, extract:
   - query text;
   - status;
   - sources/domains;
   - fetched pages;
   - evidence notes;
   - artifact path;
   - generated answer section from `research_report_v2.md` if present.
5. Answer in concise numbered sections, with a clear caveat if `claims_total=0` or if the run is retrieval/evidence-pack only.
6. Include the canonical summary/rows paths at the end rather than pasting raw JSON.

## Pitfall learned

Do not over-search the whole session/filesystem for “question 35” once benchmark artifacts are identified. The fastest reliable route is: summary JSON → rows JSON → method filter → requested 1-based indices → per-run Markdown report.

## Output discipline

For Telegram, avoid dumping all raw report text. Summarize each requested benchmark question in 3–6 bullets or a short paragraph, then link the artifact path. Always distinguish:

- `60/60 complete` as an operational retrieval/evidence-pack result;
- true answer-quality validation only if claims are generated, verified, and judged.

## Quality gate before answering

When converting benchmark rows into user-facing answers, do a quick retrieval-quality triage per requested index:

- If `claims_total=0`, say the run is evidence-pack/retrieval only, not validated factual answers.
- If top URLs are off-topic, generic homepages, random arXiv papers, or channel failures dominate, label the item `faible confiance` and do **not** present the generated writer text as a reliable answer.
- For low-confidence rows, prefer a short diagnosis plus the correct next step (rerun with better query/channel, fetch official docs/API directly) over a polished but unsupported answer.
- If the user asked for numbered answers after an ambiguous previous task, use the number range as a discriminator: numbers beyond a small local questionnaire (for example 19, 20, 30, 34, 35) usually indicate benchmark row indices; still state the interpretation once at the top.
- When supplementing a weak row with live authoritative docs, clearly separate `benchmark result said` from `fresh verification says` so the benchmark evaluation is not silently rewritten.