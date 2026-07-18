# Research/report pipeline traceability for Moufadal

Use when Moufadal asks for benchmark/research reports, challenges why an item was omitted, or asks for “rapport complet HTML cliquable” with what was searched, filtered, scored, and displayed in Telegram.

## Required contract

A serious research/report deliverable must not only show conclusions. It must include a traceable path:

1. User request → interpreted research questions.
2. Skills loaded and why.
3. Search/query plan: exact query families, engines/tools, limits, proxy status if relevant.
4. Raw result inventory: counts by engine, statuses, errors, timestamps.
5. Filtering/deduplication: what was removed and why.
6. Scoring/ranking: score fields, weights, thresholds, examples.
7. Synthesis path: how evidence became final claims.
8. Telegram/output path: what was condensed, omitted, and linked to full artifacts.
9. QA: missing sections, proxy/network caveats, secret hygiene, links open.

## HTML report sections

For a clickable HTML report, include at minimum:

- `Résumé / Verdict`
- `Pipeline de bout en bout`
- `Requêtes et moteurs`
- `Résultats bruts et erreurs`
- `Tri, scoring, exclusions`
- `Ce qui a été omis ou perdu dans le pipeline`
- `Limites / fiabilité`
- `Artefacts et logs` with links/paths, not inline raw logs

If the user is novice or explicitly asks to understand, use pedagogical course mode: diagrams, glossary, and short explanations before raw technical detail.

## Omission investigation pattern

When the user asks “pourquoi tu n’as pas parlé de X ?”, do not answer from memory. Treat it as a pipeline audit:

- Was X absent from the original query plan?
- Was X found by a search engine but filtered out?
- Was X present in raw notes but omitted during synthesis/compression?
- Was X outside the chosen framing?
- Did a network/proxy failure make the search unreliable?

Report the answer as fact/hypothesis/unknown with artifact paths. If exact raw search logs are unavailable, say so and create better logging for the rerun rather than inventing a retrospective trail.

## Telegram discipline

Telegram should stay as steering UI. Put the complete traceability report in HTML/Markdown under `/opt/data/artifacts/...`, and send only concise status plus links. Do not paste raw JSON/logs into Telegram.
