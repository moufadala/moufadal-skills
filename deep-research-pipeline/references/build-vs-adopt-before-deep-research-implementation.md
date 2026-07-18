# Build-vs-adopt reconnaissance before Deep Research implementation

## Trigger

Use this when Moufadal asks to improve, implement, or benchmark a research/retrieval stack: hybrid retrieval, BM25/keyword search, semantic search, reranking, citation verification, claim checking, community retrieval, benchmark/eval runners, or report generation.

## User correction captured

Moufadal explicitly corrected the workflow: **do not reinvent the wheel every time**. Before implementing a serious research module, first search the web/GitHub/docs/community for existing libraries, patterns, and prior art, then decide what to adopt, adapt, or build.

## Required reconnaissance before coding major bricks

Create an `EXISTING_SOLUTIONS_RESEARCH.md` artifact with clickable links and a short decision for each category:

1. **Hybrid retrieval / keyword search**
   - BM25 libraries (`rank-bm25`, SQLite FTS5, Tantivy, Lucene-style engines, Meilisearch/Typesense when service complexity is acceptable).
   - Existing RAG retrievers and query fusion patterns.

2. **Semantic search / web retrieval**
   - Existing Agent Reach/Exa/Jina/SearXNG integrations already present on the VPS.
   - GitHub code/issues search patterns before writing ad hoc scrapers.

3. **Reranking**
   - Local cross-encoder/BGE-style rerankers if dependencies are realistic.
   - API rerankers such as Cohere only when credentials are available.
   - Deterministic fallback reranker: exact phrase, BM25 score, source authority, freshness, domain diversity.

4. **Citation / claim verification**
   - Existing claim-evidence evaluation patterns.
   - LLM-as-judge should be audit-backed and should emit weak/unsupported flags rather than binary truth.

5. **Community/dev sources**
   - Hacker News, StackOverflow/StackExchange API, GitHub issues/repos, Reddit public read-only if accessible without private cookies.
   - V2EX is supplementary, not representative of the global dev community.

6. **Benchmark/evaluation**
   - Prior internal benchmark artifacts and scripts.
   - Existing eval frameworks or simple A/B harnesses before inventing a bespoke metric.

## Decision format

For each candidate solution:

```text
- Candidate: <name/link>
- What it solves: <retrieval/rerank/cache/eval/etc.>
- Fit for this VPS: adopt / adapt / reject / later
- Reason: <dependencies, credentials, complexity, quality gain>
- Smoke test: <small command/test or why not run now>
```

## Implementation rule

Only after this reconnaissance should the agent code. If it builds custom logic, the report must say why existing solutions were insufficient or too heavy for the current P0/P1 goal.

## Final report requirement

The final HTML/Markdown handoff must include a section `Existing solutions checked` linking to `EXISTING_SOLUTIONS_RESEARCH.md`, so Moufadal can verify we did not invent everything from scratch.
