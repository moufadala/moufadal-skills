# Session-history trigger calibration — 2026-07-03

## Source

This note condenses a 4-day local audit requested by Moufadal to calibrate when Hermes should do local retrieval, external search, or premium DeepResearch. The audit used session history and local artifacts, not web search, because the evidence needed was Moufadal's own interaction pattern.

Window inspected: roughly 2026-06-29 → 2026-07-03.

## Why this matters

Moufadal corrected Hermes that the issue is not only “search before build”. It is also choosing the right retrieval/search tier at the right time:

1. use known local context before guiding him through a domain already researched;
2. search externally when the wording or risk calls for it;
3. escalate to premium/Level 3 when he asks for DeepResearch/grosse analyse or when the decision is high-risk;
4. keep Telegram concise for small questions.

## Trigger families from history

### T0 — no external search

Use for trivial local checks, current-state commands, small reversible edits, or obvious answers that do not affect architecture or durable behavior.

Do not turn every mention of “research” into a giant report if the user asks a small follow-up or format clarification.

### T1 — local retrieval first

Trigger phrases / situations:

- “on avait déjà recherché”
- “normalement tu savais”
- “où on en est”
- a continuation of Android/S25, Obsidian/LifeOS, DeepResearch, skills, immo, scraping, or VPS topics already researched
- the user is about to perform manual steps and past blockers are known

Action:

- search memory/session history/Obsidian/runbooks/artifacts first;
- surface known pitfalls before the user struggles;
- only then search externally if local evidence is stale or insufficient.

Pitfall prevented: creating a narrow project-specific patch when the real issue is a class-level “known context activation failure”.

### T2 — external search required

Trigger phrases:

- “recherche web sourcée”
- “cherche sur le net”
- “cherche dans la communauté”
- “sources / citations / URLs”
- “ne réinvente pas la roue”
- “ça existe déjà ?”
- “outils/plugins/repos existants”
- “meilleures pratiques”
- architecture/tool/plugin choice where a wrong build-vs-buy decision can cost 30–60+ minutes

Action:

- run local inventory first when relevant;
- then external docs/community/repos search;
- return a short verdict `ADOPT | EXTEND | BUILD` with evidence and next smoke test.

### T3 — premium / Level 3 research

Trigger phrases:

- “DeepResearch” / “deepsearch premium”
- “recherche premium”
- “grosse analyse”
- “gros audit”
- “état de l’art”
- “au réveil” with expectation of complete overnight deliverable
- repeated correction about the same search/decision threshold
- high-risk VPS/Hermes/security/scraping/Android architecture decisions

Action:

- local inventory;
- external multi-source search;
- Claude Code critique/review when available;
- durable artifact under `/opt/data/artifacts/...`;
- concise Telegram summary with paths and QA evidence.

## Telegram output calibration

Moufadal wants visible calibration but not noise:

- During visible calibration, briefly state when the gate fires and list external query strings used.
- For T0/T1, keep the message short unless there is a real deliverable.
- For T2, give a compact verdict plus the evidence paths/links.
- For T3, create artifacts and avoid dumping logs into Telegram.

## Golden cases to add/maintain

1. “Cherche sur le net avant de choisir un plugin Obsidian” → T2.
2. “Ne réinvente pas la roue pour ce module” → T2 build-vs-buy.
3. “DeepResearch premium, au réveil je veux un rapport complet” → T3.
4. “Normalement tu savais que ça allait buguer, c’était dans nos recherches” → T1 local known-context retrieval first.
5. “Petite question” after a large project → concise T0/T1 answer, not Projet Clair.
