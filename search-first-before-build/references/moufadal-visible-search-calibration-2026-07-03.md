# Moufadal visible search-first calibration — 2026-07-03

Use this reference when a Moufadal task activates `search-first-before-build` and the decision is visible calibration of external search/tool use.

## User corrections captured

Moufadal clarified that for durable/impactful decisions he wants the agent to search before acting, but not blindly:

- Threshold: external search is expected when a wrong decision may cost roughly **30 min to 1 h or more**, adjusted by task criticality.
- Always-sensitive domains: architecture, automation durable, security, VPS/Hermes, skills, agents, scraping, Android/S25, Obsidian/LifeOS, immo, business, and serious projects.
- Emergency/service-down mode: start with obvious local, reversible checks; if the cause is unclear or the fix takes ~15 minutes, switch to search-first and explain with concrete examples.
- Visible calibration window: for a short calibration period, announce when the gate triggers and show the **brief search queries used**.
- Level 3 meaning: Claude Code critique + second external-search loop + evidence-backed verdict before a high-risk decision.

## Required user-facing pattern during visible calibration

Keep Telegram concise, but include the queries. Example:

```text
Gate search-first activé : décision durable sur skills/Hermes.
Recherche externe justifiée : mauvais choix = dette durable >30–60 min.
Requêtes :
- Hermes Agent SOUL.md skills docs
- AI agent tool use calibration external search best practices
Verdict : EXTEND — patcher les skills existants, pas créer un god-skill.
```

Do not paste raw search logs. Show 2–4 short query strings max.

## Logging pattern

When appending to `/opt/data/logs/search_first_calibration.jsonl`, include a `queries` list when external search happened:

```json
{"external_search":true,"reason":"...","queries":["query 1","query 2"],"level3_signal":true,"user_feedback":"pending"}
```

The mini-monitor can then report decisions with queries instead of forcing the user to infer what was searched.

## Pitfalls

- Do not use “I researched” without showing the actual query strings during calibration.
- Do not let a 4-day calibration phrase become a permanent noisy behavior. After the window, keep the permanent rule but drop routine query display unless the user asks or risk is high.
- Do not treat “search-first” as “always web-search first.” Local session/memory/skills/artifacts come first; external search follows when necessity + utility + affordability justify it.
