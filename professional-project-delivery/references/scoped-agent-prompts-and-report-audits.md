# Scoped agent prompts and report audits

Use this when the user asks for GPT/agent prompts, PDF/report review, or a "mode goal" continuation around an existing watch/pipeline project.

## Core lesson

Do **not** expand the agent's scope just because the class of work has many possible sources. For Moufadal's watch/scraping projects, prompts must be limited to:

- sources already verified;
- sources explicitly in chantier/backlog;
- sources present in current scripts/config/artifacts.

If a source is out of scope, do not name it inside the prompt, even in a "do not test" list. Naming it can prime GPT Agent to go there. Use generic wording instead: `Ne teste aucun site hors périmètre. Si tu vois une source hors scope, note seulement "hors scope détecté" sans ouvrir/tester/nommer davantage.`

## Prompt generation checklist

1. Inspect current project artifacts/scripts/config first.
2. Build the source list from verified/current work, not from generic domain knowledge.
3. Include context per source: `already implemented`, `needs hardening`, `blocked`, `benchmark only`, `official`, `OTA`, etc.
4. Require evidence: HAR/Network, endpoint, payload, screenshot, status code, or raw response excerpt.
5. Require redaction of cookies/tokens/session IDs/anti-bot tokens.
6. Explicitly distinguish truth classes:
   - official source vs aggregator/benchmark;
   - live bookable price vs SEO/statistical price;
   - 5-passenger family price vs 1-adult price;
   - replayable API vs browser/session-only path.
7. Verify the final prompt contains no out-of-scope named sources before delivering.

## Report/PDF audit pattern

When the user provides a report/PDF and says "do everything" or "mode goal":

1. Extract the PDF to markdown/text and save it as an artifact.
2. Compare claims against the **current local state**: scripts, config, DB dry-runs, prior artifacts.
3. Treat the report as evidence, not truth. Mark outdated/inconsistent claims explicitly.
4. Run at least one grounding check when feasible, e.g. a dry-run of the relevant pipeline.
5. Produce:
   - concise audit summary;
   - QA report with commands/outputs;
   - updated scoped prompts if agent prompts are part of the workflow;
   - handoff HTML for substantial work.

## Example correction from RUN Watch

A broad prompt that included every plausible flight/immo website was wrong. The corrected prompts were limited to already verified/in-progress sources only. Also, a PDF marked 97immo/Citya as inconclusive, but local `realestate_watch.py --dry-run` proved the scrapers already extracted them, so the prompt changed from "discover" to "harden existing connector".