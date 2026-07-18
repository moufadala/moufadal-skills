# P0 runner implementation notes — 2026-06-29

Session lesson from upgrading Agent Reach/Exa into a Deep Research-style pipeline.

## Durable technique

The useful P0 pattern is not another search provider. It is a reproducible artifact pipeline:

```text
question → sub-questions → Exa/GitHub retrieval → URL dedupe → source type/trust score → relevance rerank → full-page fetch → evidence notes → report/HTML/state JSON → QA smoke
```

Local files created in this session:

- `/opt/data/scripts/deep_research_runner.py`
- `/opt/data/tests/test_deep_research_runner.py`

Useful smoke commands:

```bash
python3 /opt/data/tests/test_deep_research_runner.py
/opt/data/scripts/deep_research_runner.py "deep research citation verification" --max-results 3 --fetch-top 5 --github
```

## Important implementation pitfalls

1. **Do not extract evidence from snippets when fetch failed.** Evidence notes must come only from sources where `fetched_ok=true`; otherwise the report can quote stale snippets or malformed search output as if they were verified page content.

2. **Reject reader “not found” pages.** Jina Reader may return a readable 404/page-not-found document instead of an HTTP failure. Treat content containing markers like `page not found`, `404 not found`, or `not found url source` near the start as `fetched_ok=false`.

3. **GitHub search JSON fields differ by type.** `gh search repos` does not support the same JSON fields as `gh search issues`. For repos use fields like `url,fullName,description,stargazersCount,updatedAt`; for issues use `url,title,repository`.

4. **Claude Code critique can consume max turns.** If Claude reaches `max_turns` while exploring, log it and continue with deterministic Hermes artifacts rather than pretending Claude validated the design.

5. **Metrics are coverage/discipline metrics, not final truth.** `sources_total`, `fetched_ok`, and `notes_total` prove the pipeline ran and produced inspectable evidence. They do not prove every final synthesized claim is entailed by sources.

## Next P1 upgrades

- Add a benchmark over ~20 real Moufadal queries comparing old search vs Agent Reach vs Deep Research runner.
- Add claim-to-citation verification: quote substring match first, then optional LLM/NLI judge for entailment.
- Add optional channel adapters only when they add source class value, not just more noise.
