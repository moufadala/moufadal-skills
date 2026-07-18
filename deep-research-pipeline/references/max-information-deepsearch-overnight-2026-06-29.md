# Max-information DeepSearch overnight pattern (2026-06-29)

## Trigger

Use when Moufadal asks to finish DeepSearch/DeepResearch by a deadline and explicitly says not to lose information while still filtering garbage.

## User correction captured

Moufadal's priority is **maximum useful information intake**. Do not optimize retrieval by over-pruning. The right behavior is:

- filter or downgrade true waste;
- keep broad candidates, snippets, metadata, and blocked/fetch-failed records where useful;
- distinguish evidence strength instead of silently discarding weak evidence;
- preserve enough raw/structured artifacts so a later pass can recover missed value.

## Implementation pattern

1. Treat SearXNG as additive breadth, not fallback.
2. Expand with targeted `!bang` probes, but avoid known noisy defaults such as direct Reddit, Brave/Qwant when suspended, or any engine currently producing only rate-limit noise.
3. Preserve each candidate with status fields:
   - `candidate_kept`, `candidate_dropped`, or `candidate_downgraded`;
   - reason: duplicate, blocked, captcha, not-found, empty, low-signal, fetch-failed, snippet-only;
   - source type and channel/bang used.
4. Fetch pipeline should not be single-adapter:
   - try the current reader path;
   - add domain-specific/direct fetch fallback for open domains such as arXiv, StackOverflow/StackExchange, GitHub, docs, Wikipedia, and academic APIs when available;
   - if fetch still fails, retain snippet/metadata as weak evidence rather than losing the source.
5. Final synthesis and claim verification must separate:
   - fetched evidence = can support claims if quote matches;
   - snippet-only evidence = weak lead, may inform coverage but must be labeled;
   - blocked/garbage = retained in audit metrics, not used as support.
6. Benchmark acceptance should measure information preservation, not just final answer polish:
   - distinct queries, not rows;
   - candidates total and unique URLs/domains;
   - fetched_ok count;
   - snippet-only count;
   - dropped/downgraded count with reasons;
   - notes/claim-support count;
   - source-type mix.

## Overnight orchestration pattern

For a hard morning deadline:

- write a Definition of Done contract first;
- start a foreground/background orchestrator immediately;
- spawn parallel Claude analysis agents for: information preservation, fetch fallback, benchmark design, SearXNG noise/bang ordering;
- run one implementation pass after those analyses;
- run syntax/tests/smoke;
- run a crash-safe 50–60 distinct-query benchmark with partial JSONL writes and resume;
- schedule a resume cron and a pre-wakeup final-report cron;
- pause older duplicate final-report jobs to avoid conflicting Telegram summaries.

## Pitfalls

- Do not equate “cleaner results” with better DeepSearch if useful weak signals were discarded.
- Do not call the project complete if the benchmark has fewer than 50 distinct queries unless the report clearly says partial and gives blockers.
- Do not hide fetch failures by only showing successful notes; report `fetched_ok`, `snippet_only`, and `failed_or_downgraded` separately.
- Do not schedule a final report after the user's wake time when they asked for a 07:00-ready result; schedule the audit before wake-up.
