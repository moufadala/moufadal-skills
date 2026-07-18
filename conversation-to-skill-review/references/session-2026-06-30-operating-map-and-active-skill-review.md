# Session note — Operating Map + active skill review (2026-06-30)

## What happened

Moufadal first prioritized skill-library changes, then asked for a central Obsidian runbook:

- create `conversation-to-skill-review` first;
- patch `definition-of-done` only if needed;
- create `long-task-ledger`;
- do not create `telegram-project-delivery` yet;
- create central document `70-Runbooks/HERMES Operating Map.md` and keep it updated.

Later he explicitly requested an active conversation review and skill-library update, with the rule that most sessions should produce at least one skill update.

## Durable lessons

1. **Skill review should be active, not passive.**
   If the user asks to review a session and update skills, default to patching at least one relevant loaded/class-level skill unless the whole session was truly smooth and produced no workflow/style/technique signal.

2. **Prefer loaded skills first.**
   In this session the relevant loaded skills were `conversation-to-skill-review`, `definition-of-done`, `obsidian`, and `hermes-agent`. Because protected skills must not be edited, the right writable owner is `conversation-to-skill-review` for the review behavior, plus references instead of touching protected setup docs.

3. **Operating Map is a durable substrate.**
   For Hermes/VPS stack changes, the central Obsidian runbook is now a durable destination alongside memory and skills:
   `/opt/data/vaults/moufadal-second-brain/70-Runbooks/HERMES Operating Map.md`

4. **Do not turn transient tool symptoms into permanent negative rules.**
   The runbook recorded SearXNG/CDP loopback anomalies as “reverify/preflight” rather than “broken forever”.

## Future trigger

When a session changes durable Hermes/VPS operations — providers, gateway, toolsets, MCP, cron, proxy/scraping, dashboards, incident fixes, QA/reprise commands, or secret locations — include “update Operating Map?” in the skill-review decision ladder.

## Suggested test prompt

> Review the conversation above and update the skill library. Be ACTIVE. Also check whether any central docs/runbooks should be updated.

Expected behavior:

- load/use `conversation-to-skill-review` if available;
- patch a governing writable skill or support file;
- update `HERMES Operating Map.md` when stack state changed;
- do not edit protected bundled/hub skills;
- final response says what was patched and what was intentionally not touched.
