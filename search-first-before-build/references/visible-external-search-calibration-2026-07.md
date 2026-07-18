# Visible external-search calibration — 2026-07

## Triggering correction

Moufadal clarified that the useful calibration point is not merely “I used search-first”, but specifically **when Hermes decides to perform an internet/external search**.

During a calibration period, Hermes should make the external-search decision visible so Moufadal can say whether it was justified or too heavy.

## Durable rule

When a task enters `search-first-before-build`, split the gate into two visible layers:

1. **Local-first check** — sessions, artifacts, skills, scripts, runbooks, project files.
2. **External-search decision** — repos, docs, packages, forums/community, official changelogs.

Only announce the external layer when it is actually being launched or seriously considered.

## Recommended phrasing

```text
Recherche externe justifiée selon moi : [raison courte]. Je vérifie repos/docs/community avant de coder; tu pourras me dire si c'était trop tôt ou utile.
```

Keep it short. The point is calibration, not a long explanation.

## What to do with feedback

If Moufadal says the external search was justified:
- keep the trigger boundary;
- optionally promote the example into a positive SkillOps/golden case if it is representative.

If Moufadal says it was not justified:
- record the boundary as a negative example;
- patch this skill or the golden set if the pattern is likely to recur.

## Positive examples from the calibration

External search is usually justified for:
- architecture/template design, e.g. Obsidian vaults, dashboards, UX systems;
- non-trivial integrations, e.g. MCP, plugins, provider APIs;
- scrapers/anti-bot/proxy/auth flows where community/docs often reveal traps;
- generic/non-differentiating modules likely solved by existing packages or repos;
- user phrases such as “ça existe déjà ?”, “cherche les repos”, “ne réinvente pas”, “comment les autres font”.

## Negative examples

External search is usually not justified for:
- typo or wording fixes;
- reading/summarizing a known local file;
- giving a simple local command;
- rollback or emergency fix with a clear local cause;
- a small patch where the surrounding code is already understood.

## Mini-monitoring log

During the calibration period, each external-search decision should also be logged to:

`/opt/data/logs/search_first_calibration.jsonl`

Recommended event:

```json
{"ts":"<UTC ISO>","task":"<short task>","external_search":true,"reason":"<necessity/utility/affordability>","level3_signal":false,"user_feedback":"pending"}
```

If Moufadal later says the search was justified or not justified, append a second event with `event:"feedback_update"`; do not rewrite history. A daily mini-monitor reads this log and sends a compact summary.

## Level-3 escalation

Moufadal liked the proposed “niveau 3” but did not want it executed yet. Treat it as a later escalation, after calibration signals or high project risk.

Propose level 3 proactively when one of these concrete triggers appears:

- 3 user corrections on external-search timing within a short calibration window;
- repeated ambiguity about whether external search is useful or too heavy;
- high-stakes project decision: durable architecture, recurring automation, agent routing, security, VPS reliability, scraping/anti-bot;
- the current verdict is likely `BUILD`, but local/external evidence is weak, outdated, or contradictory;
- an incident shows Hermes reinvented something, missed a repo/template/skill, or searched too late;
- the likely cost of a bad decision is several hours of work, production debt, data exposure, or service breakage.

Recommended phrase:

```text
Je pense que le niveau 3 est justifié ici : [signal concret]. Le niveau 2 suffit pour exécuter, mais une revue Claude + seconde recherche réduira le risque de construire la mauvaise chose.
```

Do not jump to level 3 by default; propose it, let Moufadal approve/refuse, then record his feedback if the boundary needs adjustment.
