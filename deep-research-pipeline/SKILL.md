---
name: deep-research-pipeline
description: "À utiliser quand l'utilisateur veut une recherche de qualité, actuelle et sourcée — un rapport « comme les meilleurs », des réponses sémantiques solides, ou quand une recherche web simple ne suffit pas. Impose un pipeline type Deep Research : cadrage, recherche décomposée, multi-sources, dédoublonnage, scoring de confiance des sources, vérification/critique des citations, synthèse finale."
version: 1.0.0
license: MIT
platforms: [linux, macos, windows]
---

# Deep Research Pipeline

## Trigger

Use this skill for any serious research where quality matters:

- “cherche”, “vérifie”, “fais une recherche approfondie”, “comme les top”, “meilleures réponses”, “sémantique”;
- **“recherche premium”**: activate Premium Research mode below, with Claude Research/Claude Code in the loop and, when credentials/API access exist, OpenAI Deep Research as an additional benchmark/source, not as a replacement for local evidence artifacts;
- product/technical decisions based on current external facts;
- reports that need citations, source trust, contradictions, or evidence;
- when Agent Reach/Exa is mentioned and the user expects more than simple search.

## Premium Research mode — Moufadal trigger: “recherche premium”

When Moufadal explicitly asks for **recherche premium**, do not run a single-engine Hermes search. Use a multi-agent research loop:

1. **Hermes frames the contract**: question, sub-questions, acceptance criteria, source classes, deadlines, and artifact directory.
2. **Local DeepResearch runner gathers auditable evidence**: Exa/Agent Reach + SearXNG breadth + GitHub/community/specialist channels when relevant, full-page fetch, dedupe, source trust, evidence notes, and raw artifacts.
3. **Claude Research / Claude Code pass is mandatory**: ask Claude to independently research/critique coverage, contradictions, missing source classes, weak evidence, and alternative interpretations. Claude is not allowed to validate its own synthesis; Hermes must reconcile against local artifacts.
4. **OpenAI Deep Research pass is optional but preferred when available**: if OpenAI API credentials and model access for `o3-deep-research` or `o4-mini-deep-research` are available, run it as an additional deep-research lane through the Responses API with web/file/MCP sources. Treat its output as another cited research artifact, not automatically as truth.
5. **Synthesis only after comparison**: compare local DeepResearch, Claude, and OpenAI lanes; preserve disagreements, mark weak/snippet-only sources, and cite every factual/current claim.
6. **Final QA**: run claim→citation checks, source-quality audit, and write dated Markdown/HTML reports under `/opt/data/artifacts/...`.

If OpenAI Deep Research API access is unavailable, say so plainly and continue with Hermes local DeepResearch + Claude. Do not pretend ChatGPT/consumer Deep Research was invoked if only the current Hermes GPT brain did normal tool-based research.

## Core principle

Do **not** equate “more search engines” with better answers. Top-tier research requires an auditable pipeline:

0. **Do not reinvent the wheel for research-stack implementation.** Before coding major retrieval/rerank/verification/benchmark bricks, search web/GitHub/docs/community for existing libraries and patterns, then write an `EXISTING_SOLUTIONS_RESEARCH.md` with adopt/adapt/reject decisions. See `references/build-vs-adopt-before-deep-research-implementation.md`.
1. Scope the question and split into sub-questions.
2. Search complementary channels: Exa semantic, SearXNG as an additive breadth channel, GitHub/community when useful, `web_search`/Jina for keyword and page reading, specialist skills for YouTube/GitHub/etc. Treat SearXNG as a complement to widen source discovery, not merely as a fallback; measure its unique URLs/domains and upstream engine health.
3. Fetch/read full pages, not only snippets.
4. Dedupe URLs/domains.
5. Score source trust: official/academic > docs/vendor > GitHub/issues > reputable press > community/UGC > unknown/SEO.
6. Rerank by relevance + trust + freshness.
7. Extract evidence notes with source id + URL + quote.
8. Synthesize **only from notes**; mark gaps as `non vérifié`.
9. Run a critique/citation-support pass before final answer.
10. Store artifacts under `/opt/data/artifacts/...`.

## Local P0 runner

A reproducible lightweight runner is installed at:

```bash
/opt/data/scripts/deep_research_runner.py
```

It uses Agent Reach/Exa, Jina Reader, optional GitHub search, deterministic dedupe/source scoring/rerank, evidence-note extraction, and writes a Markdown + HTML handoff.

### Basic use

```bash
/opt/data/scripts/deep_research_runner.py "<question de recherche>" --max-results 8 --fetch-top 10 --github
```

Outputs:

```text
/opt/data/artifacts/deep-research/<timestamp>_<slug>/
  query.txt
  research_state.json       # structured source/score/evidence data
  research_report.md        # report + synthesis contract
  research_report.html      # mobile-readable static viewer
  raw/                      # raw doctor/search/fetch evidence
```

### Explicit sub-questions

```bash
/opt/data/scripts/deep_research_runner.py "<question>" \
  --subquestion "official docs and primary sources" \
  --subquestion "GitHub issues and real-world failures" \
  --subquestion "benchmarks and evaluation methods" \
  --github
```

## QA command

Run before claiming the pipeline works:

```bash
python3 /opt/data/tests/test_deep_research_runner.py
```

Expected: JSON with `ok: true`, a `smoke_out_dir`, and non-zero source metrics.

## How to use the runner inside final research

1. Run the P0 runner for retrieval/evidence.
2. Read `research_report.md` and `research_state.json`.
3. If the question is important, ask Claude Code for a critique pass over the report/evidence:

```bash
claude -p 'Critique ce research pack: <path>. Vérifie couverture, sources faibles, contradictions, claims non supportés. Réponds en JSON.' --allowedTools 'Read' --max-turns 5 --output-format json
```

4. Hermes writes the final answer using only cited evidence or explicit `non vérifié` labels.
5. Save final artifacts and report Telegram with paths, not raw logs.

## Acceptance criteria for serious research

- At least 2 complementary retrieval channels when relevant, or an explicit reason why only one was usable.
- Full-page fetch for key sources.
- Dedupe + trust score + relevance score visible in artifacts.
- Evidence notes include quote + URL + source id.
- Final answer has citations for factual/current/numeric claims.
- UGC/community evidence is labeled weak unless corroborated.
- Contradictions and missing evidence are surfaced.
- QA command passes or failure is reported honestly.

## Benchmarking and claims discipline

A 20-query internal benchmark on 2026-06-29 showed DeepP0 improves retrieval/auditability versus Hermes `web_search`: more unique sources/domains, more high-trust/GitHub/academic candidates, fetched pages, and evidence notes. However Claude and Codex audits agreed this **does not prove final answer quality**. When reporting benchmark results, say: “better retrieval and auditability / better raw material for answers”, not “objectively better answers”, unless an external judge or human eval has scored final synthesized responses.

For V2 completion, do **not** reuse a broad P0/P1 benchmark as proof. The benchmark must exercise the actual V2 runner end-to-end: hybrid/community retrieval, dedupe, authority scoring, rerank, evidence extraction, claim/citation verification, final answer generation, reports, and optional critique hooks. If external providers are unstable, bound them with timeouts/non-fatal fallback and run a stable-channel proof separately. Report the result as “operationally complete with caveats” unless blind answer-quality eval and external-channel integrations are also proven. See `references/v2-operational-completion-20260629.md`.

Benchmark artifact pattern:

```text
/opt/data/artifacts/deep-research-benchmark/<timestamp>/benchmark_report_final.md
/opt/data/artifacts/deep-research-benchmark/<timestamp>/benchmark_summary_final.json
```

Matrix fetch-smoke runner for the specific post-discovery gate:

```bash
/opt/data/scripts/deepsearch_matrix_fetch_smoke.py --limit 10 --max-results 4 --fetch-top 4 --timeout 6
```

Artifacts:

```text
/opt/data/artifacts/deepsearch-matrix-fetch-smoke/<timestamp>/
  summary_final.json      # totals: queries, sources, pages_fetch_attempted/ok, notes/citations
  rows_final.json         # per-query metrics + top URLs + unresponsive counts
  report_final.md/html    # user-readable report
  raw/**/searxng.raw.txt  # raw SearXNG packets with unresponsive_engines
```

Use this when the remaining proof is: “not just discovery; fetch_top > 0; measure sources found, pages actually fetched, exploitable citations, and SearXNG engines becoming unresponsive.”

If benchmarking again, include variance/distribution, latency cost, external answer-quality judge, and claim → citation verification. Avoid spectacular percentages on near-zero baselines (e.g. GitHub +5300%) without raw values.

**Strict benchmark caveat learned 2026-06-29:** a 60-query run is not valid final proof if it benchmarks P0 while the active implementation is V2, if baseline methods return 0/60 OK, or if the winning method has near-zero evidence output (`avg_notes_total=0`, almost no fetched sources). Treat such a run as “scheduler/execution proof only”, not A/B quality proof. A valid benchmark must include the actual current runner (V2 or later), working comparable baselines, real output quality metrics, and evidence/answer-quality scoring.

**V2 claim-gap caveat learned 2026-06-29:** even a clean `60/60` V2 run with `status_complete=60`, generated answers, and improved source/domain coverage is still only an operational retrieval/evidence-pack proof if `avg_claims_total=0`, the baseline does not generate answers, or only ~2 pages are fetched per query. This often means automatic note→claim conversion was correctly disabled to avoid circular “quote verifies itself” support, but the real writer→claims→verification loop is not complete. Do not declare answer quality or the module “finished” until explicit final claims are generated, verified, and spot-judged. See `references/v2-60q-benchmark-claim-gap-2026-06-29.md`.

P1-lite answer-quality benchmark artifact pattern:

```text
/opt/data/artifacts/answer-quality-benchmark/<timestamp>/answer_quality_report.md
/opt/data/artifacts/answer-quality-benchmark/<timestamp>/summary.json
/opt/data/artifacts/answer-quality-benchmark/<timestamp>/judge_decoded.json
```

A P1-lite run on 2026-06-29 showed DeepP0 winning 8/8 against the web_search baseline, but Codex audit rejected a strong production claim: n=8, selected/project-specific queries, baseline often catastrophically off-topic, asymmetric source budgets, deterministic evidence summaries rather than real Telegram answers, one LLM judge, no human spot-check. Report this only as “promising answer-quality signal”, not proof. For a real answer-quality claim, run 50–60 randomly sampled real Telegram queries with equal retrieval/source budgets, real end-to-end answers, at least one blind human spot-check, confidence intervals, and failure-case analysis.

**Important Moufadal correction:** when the active goal is to validate the research module, do not substitute a polished research pack or strategy synthesis for the benchmark. `20 queries × 3 methods = 60 rows` is not the requested “50–60 requêtes”; the benchmark must contain 50–60 **distinct queries**. If the benchmark is only scheduled or partial, say so directly and do not declare the module finished. See `references/benchmark-60-query-overnight-2026-06-29.md`.

**V2 validation correction:** before any “module validé” claim, repair the actual V2 completion contract: report `unique_domains`, make `status=complete` depend on explicit `complete_checks`, disable quote→claim→same-quote circular validation, run a smoke with `fetch_top > 0`, then launch the 50–60 distinct-query V2 benchmark. If another DeepSearch cron is already running, schedule the fixed benchmark after it rather than colliding with it. Before launching/resuming, preflight `/opt/data` free space; a V2 run that crashes while writing raw channel files with `No space left on device` is an infrastructure capacity failure, not a retrieval-quality verdict. See `references/v2-completion-gates-and-cron-chaining-2026-06-29.md` and `references/disk-pressure-and-resume-guard-2026-06-29.md`.

## Pitfalls

- **Over-orienting external AI audit mega-prompts.** When generating a corpus + mega-prompt for Claude/another IA to review Hermes, do not force Hermes' own analysis, taxonomy, or strategy onto the reviewer. The external AI should decide independently once Moufadal gives it the prompt and corpus. Raw corpus/evidence must outrank Hermes' preliminary analysis; frame Hermes' analysis as a hypothesis that can be contradicted or ignored. See `references/external-ai-audit-megaprompt-neutrality-2026-07-01.md`.
- **Obvious-solution tunnel vision on solution-landscape questions.** When Moufadal asks “quelles solutions/options ?” for tools, remote access, agents, or infrastructure, do not stop at the generic stack you already know. Run a landscape search and explicitly check for native product capabilities before recommending workarounds. Example: controlling a home Claude environment from Android is not only RustDesk/Tailscale/SSH; Claude Code has an official `claude remote-control` path for mobile/web access to a local session. See `references/solution-landscape-correction-claude-remote-control-2026-07-01.md`.
- **Source-primary recovery after web-fetch failures.** In Premium Research / AutoResearch audits, if the runner discovers an authoritative GitHub repo but web fetch returns HTTP 451/blocked content, do not leave the report relying only on mirrors/blogs. Try `git clone --depth 1` or another source-primary path, record commit hash and key README/program lines in the run artifacts, then patch the report to distinguish fetch limitation from recovered primary proof. See `references/autoresearch-premium-audit-source-primary-recovery-2026-07-02.md`. 
- **Networking/VPN architecture answers must name the actual user-facing app and traffic path.** If recommending Tailscale/VPS/VPN/proxy combinations, do not say vague things like “open a remote browser” without explaining whether the user opens Chrome/Firefox locally, a remote browser stream, or a proxy-configured app. Verify official constraints (Android one-VPN limit, Tailscale split tunneling semantics, provider Linux/headless support) and separate global routing from isolated per-container/per-app routing. See `references/tailscale-vps-vpn-routing-patterns-2026-07-01.md`.
- **Thin Last30days output on niche/community topics is not the end of the investigation.** If Last30days returns only a Reddit snippet or zero YouTube/web items, supplement with exact-query searches and `yt-dlp --flat-playlist` YouTube probes, then label strict-window evidence vs near-window context and snippet-only sources. See `references/last30days-thin-community-topic-recovery-2026-06-30.md`.
- **Last30days on GitLab-hosted app projects needs forge-specific recovery.** If the user asks for app news plus open issues/MRs and the authoritative project is on GitLab, run Last30days for public/social signal, then query GitLab releases/tags/issues/MRs directly; do not rely on sparse GitHub or web results. See `references/last30days-gitlab-app-project-recovery-2026-07-01.md`.
- **Niche/community press-coverage checks need an “absence detected” audit, not a blunt “no press exists” claim.** For city/country press questions, run Last30days per geography, DeepResearch subquestions, and Google News RSS regional probes; classify every hit as current/in-zone, out-of-period, out-of-zone, social-not-press, or off-topic before synthesizing. See `references/press-coverage-absence-for-niche-community-events-2026-06-30.md`.
- **Reinventing the research stack before reconnaissance.** When asked to implement better research, first check existing libraries/frameworks/APIs and prior internal scripts. Build custom code only for the gaps, and include an `Existing solutions checked` section in the final report.
- **Collapsing neighboring research questions.** When researching agent/tool/search behavior, explicitly separate at least: (A) build-vs-buy/search-first before coding, and (B) tool-use calibration / when to call web search. A source about avoiding code reinvention does not automatically prove a rule for live web-search routing. If a critique lane identifies a missing high-relevance source, fetch it before synthesis rather than defending the first pack. See `references/agent-tool-call-calibration-research-2026-07.md`.
- Exa snippets are not enough for a strong conclusion; fetch the page.
- Evidence notes must come only from `fetched_ok=true` sources. Do not extract final evidence from snippets/search output when fetch failed.
- GitHub search syntax/JSON fields differ for repos vs issues; use the installed runner instead of ad hoc shell pipelines.
- Jina Reader may return readable 404/“page not found” content instead of a hard error; reject those pages as failed fetches.
- Jina Reader may fail on blocked/JS pages; report fetch errors and use browser/specialist tools only if the source is important.
- Do not unlock social cookies/personal accounts just to increase coverage unless the task requires that source class and Moufadal approves.
- Never fabricate a “citation support” verdict. The P0 runner extracts candidate quotes; Hermes/Claude still must verify that the quote actually supports the final claim.
- If Claude Code critique hits `max_turns`, log it and continue with deterministic artifacts; do not imply Claude validated the design. For background-completion recovery, parse summary/rows files yourself, write a deterministic audit, optionally run a compact one-turn Claude critique, and remove stale resume jobs that could collide with the canonical fixed benchmark.

## Multi-theme strategic research packs

When Moufadal asks for several broad strategic axes at once, do **not** collapse them into a single mega-query. Run one DeepP0 pack per theme, create a top-level manifest, synthesize with a Claude pass, then run a Codex tone/claim audit before the Telegram final. Preserve caveats: collected sources are not all verified, evidence notes are candidate quotes, and channels must be reported honestly. See `references/multi-theme-research-pack-2026-06-29.md` for the reusable pattern, file layout, QA checks, and Telegram delivery shape.

## Pre-wakeup clickable HTML delivery

For overnight or long-running research/benchmark/code-review work, especially when Moufadal asks for results at wake-up, the expected deliverable is not a pile of Telegram text. Produce a **mobile-readable clickable HTML index** of all recent reports, results, and evidence files, then send the link around 07:00 Réunion. Index recent artifacts from `/opt/data/artifacts`, convert Markdown to HTML when useful, copy files into a web-served mirror, and verify the exact public URL plus at least one internal artifact link before claiming it is ready. Keep the mirror retention bounded because exhaustive overnight runs can create thousands of files. See `references/prewake-clickable-html-report-index-2026-06-29.md`.

## Off-topic pack recovery for course/report deliverables

When a premium/course report depends on DeepP0/runner packs, do not trust pack metrics alone. A pack can show `fetched_ok` and evidence notes while the actual source titles/quotes are unrelated GitHub issue noise. Before synthesizing, inspect representative source titles and notes. If packs are noisy or empty, recover with direct authoritative sources (official docs, GitHub repos, arXiv/papers, vendor docs, pragmatic tool docs), then document the weak automated pack and the stronger replacement sources in `QA_REPORT.md`. See `references/off-topic-pack-recovery-for-course-reports-2026-06-30.md`.

## Implementation notes

- See `references/benchmark-60-query-overnight-2026-06-29.md` for the corrected 50–60 distinct-query benchmark pattern: rows are not queries, use crash-safe partial writes/resume, schedule overnight with a morning audit, and separate research-pack delivery from module evaluation.
- See `references/benchmark-60q-resume-and-rate-limit-guard.md` for the benchmark resume lesson: diagnostic P0/Exa smoke failures must be recorded but must not abort the 50–60 distinct-query benchmark by default.
- See `references/background-resume-and-answer-quality-handoff-2026-06-30.md` for the interrupted/background-resume pattern: inspect canonical artifacts, write deterministic Markdown/HTML/JSON synthesis, report `60/60 retrieval validé` separately from `answer quality/claims non validée`, and inspect quality benchmark scripts before running stale or heavy `--help` paths.
- See `references/answering-numbered-benchmark-questions-2026-06-30.md` for the pattern when Moufadal asks “réponds aux questions 1 5 6…” after a benchmark: treat numbers as 1-based benchmark query indices, filter to the active method rows, extract each per-run Markdown answer, and preserve the `claims_total=0` caveat.
- See `references/v2-answer-quality-claim-benchmark-retry-2026-06-30.md` for the P1-lite answer-quality benchmark recovery pattern: preserve answer line breaks before bullet-based claim extraction, retry Claude judge after a fresh smoke instead of rerunning retrieval, decode blind A/B winners, and report positive signals separately from production-grade validation.
- See `references/v2-answer-quality-background-benchmark-2026-06-30.md` for the next-step pattern after a V2 60q retrieval benchmark with `claims_total=0`: launch a background P1-lite pass that extracts final-answer claims, verifies claim→citation heuristically, strengthens the baseline with fetched URLs, runs a blind Claude A/B judge when available, and refreshes the public report index.
- See `references/proxy-pass-benchmark-completion-audit-2026-06-30.md` for the completion-audit pattern after a proxy-gated benchmark finishes in background: inspect wrapper stdout/stderr and gate JSON, inspect the canonical benchmark summary/rows, write a deterministic Hermes audit, run a compact Claude critique, and report retrieval/evidence validation separately from answer-quality validation.
- See `references/searxng-as-additive-channel-and-mobile-proxy-2026-06-29.md` for the SearXNG correction: use it as an additive breadth channel in DeepResearch, proxy it through the mobile/Tailscale bridge when useful, and score unique contribution plus upstream engine health instead of treating it as a binary fallback. Runtime lesson 2026-06-29: do not keep CAPTCHA/noisy engines in the high-throughput default just to preserve apparent coverage; default to `DEEP_RESEARCH_SEARXNG_PROFILE=balanced`, reserve `max`/manual bangs for premium or overnight runs, and disable Google/Startpage/Brave/Reddit direct when they cause repeated unresponsive noise.
- See `references/searxng-engine-matrix-and-inventory-2026-06-29.md` for the explicit DeepResearch SearXNG matrix contract: general = Bing/Google/DuckDuckGo/Mwmbl; technical = GitHub/StackOverflow/HackerNews/GitLab; academic = Google Scholar/OpenAlex/Crossref/PubMed/arXiv; Reddit = indirect `site:reddit.com` only. Also covers how to inventory all configured SearXNG engines via `/preferences` and the importlib/dataclasses pitfall when probing `deep_research_v2.py` functions.
- See `references/p0-runner-implementation-notes-2026-06-29.md` for the session-specific P0 runner lessons: fetched-only evidence, Jina not-found rejection, GitHub field differences, and P1 benchmark/claim-verification upgrades.
- See `references/deepsearch-background-completion-recovery-2026-06-29.md` for the recovery pattern when a long DeepSearch/background benchmark completes: inspect artifacts instead of trusting truncated notifications, classify pre-patch runs as throughput evidence only, build deterministic audit files if Claude hits `max_turns`, fix the `urllib.parse.urlparse` V2 crash pattern, and prune stale resume crons before tracking the canonical fixed 60-query run.
- See `references/disk-pressure-and-resume-guard-2026-06-29.md` for the disk-capacity guard: preflight `/opt/data` before 50–60 query multi-channel runs, classify `No space left on device` during raw/evidence writes as infrastructure capacity failure, clean only scoped/user-approved heavy artifacts, then relaunch into a fresh run dir.

- See `references/max-information-deepsearch-overnight-2026-06-29.md` for Moufadal's explicit correction: optimize DeepSearch for maximum useful information intake, filter/downgrade garbage without silently losing candidates/snippets/metadata, distinguish fetched evidence from snippet-only evidence, and use parallel overnight Claude agents + crash-safe 50–60 query benchmarking before a pre-wakeup final report.
- See `references/premium-research-claude-openai-loop-2026-06-29.md` for the “recherche premium” contract: local DeepResearch + mandatory Claude critique/research lane + optional native OpenAI Deep Research API lane when actual API access exists; never conflate Hermes GPT tool-based research with OpenAI’s native deep-research models.
