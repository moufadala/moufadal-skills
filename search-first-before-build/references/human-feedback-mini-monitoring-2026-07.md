# Human feedback mini-monitoring — search-first calibration (2026-07)

## Trigger

Use this when Moufadal asks to actively calibrate whether Hermes is launching internet/external search at the right time, not merely when the `search-first` gate exists.

## Pattern learned

A skill/rule is not enough when the user wants to teach the boundary. Add a short-lived visible feedback loop:

1. Announce the external-search decision in one line.
2. Log the decision with a compact reason.
3. Let Moufadal mark it as justified / too heavy / too late.
4. Convert repeated corrections into positive/negative golden cases.
5. Escalate to level 3 if the boundary remains ambiguous or high-risk.

## Decision log

Canonical log path used in this session:

```text
/opt/data/logs/search_first_calibration.jsonl
```

Recommended JSONL event:

```json
{"ts":"<UTC ISO>","task":"<short task>","external_search":true,"reason":"<necessity/utility/affordability>","level3_signal":false,"user_feedback":"pending"}
```

If feedback arrives later, append a new `feedback_update` event. Do not rewrite old lines; the point is to preserve traceability.

## Mini-monitoring summary

A useful summary should be mobile-sized and answer only:

- how many external searches were logged;
- how many feedbacks arrived;
- whether any level-3 signal appeared;
- the last 1–3 decisions with reasons;
- where the log lives.

Example wording:

```text
Mini-monitoring search-first — dernières 24h
- recherches externes annoncées/loggées: 2
- feedbacks reçus: 1
- signaux niveau 3: 0
Dernières décisions:
- architecture Obsidian — probablement déjà résolu ailleurs; repos/templates utiles
Log: /opt/data/logs/search_first_calibration.jsonl
```

## Important pitfall

Do not make this permanent by default. Mini-monitoring is useful during calibration windows; after the boundary is stable, keep only the log/golden cases and stop sending routine summaries unless Moufadal asks.
