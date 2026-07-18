# Obsidian conversation review + numbered-question routing (2026-06-30)

## Triggering incident

During an Obsidian/second-brain workflow, Moufadal pasted a numbered list of Obsidian questions and then asked: `Réponds aux questions 1 5 6 8 10 19 20 30 34 35`.

The agent initially bound those numbers to a stale benchmark/deep-research question set from previous context instead of the immediately preceding Obsidian list. Moufadal corrected: `Non questions pour Obsidian`.

Later, Moufadal asked: `A partir de mes interactions avec toi. Y a til des skills qu'on peut créer ? A quel point ca va être utile. Vas y testons obsidian`.

The useful pattern was:
1. Treat the immediately preceding user-provided numbered list as the active referent for bare numbers unless the user explicitly names another corpus.
2. Use Obsidian conversation-intelligence notes as a first-class evidence source for skill-library review, but label `draft-auto` notes as signals, not final truth.
3. Cross-check with session history when possible before turning patterns into durable skills.
4. Prefer updating class-level umbrellas (`definition-of-done`, `professional-project-delivery`, `agent-self-improvement`, `obsidian`, `skill-creator`) over creating narrow one-session skills.
5. Capture candidate skills as a distilled Obsidian note when not yet ready to create a skill.

## Durable lesson

When reviewing a session for skill updates, user corrections about *routing the source of a question* are skill signals. A wrong source binding can make the answer look competent but irrelevant.

## Recommended skill-library behavior

- If the user asks to answer numbered questions, first resolve the source list from the latest surrounding conversation, not from older artifacts or active todos.
- If multiple numbered corpora exist, state the assumed corpus briefly before answering or ask only if ambiguity materially changes the answer.
- If the user says `testons Obsidian`, read/write concise distilled notes in the vault and report the evidence path.
- For skill candidates extracted from interactions, score utility and recommend create-vs-patch. Do not create a flat list of narrow skills by default.

## Session artefact created

A distilled note was written in the Obsidian vault:

`/opt/data/vaults/moufadal-second-brain/60-Distilled/Skill candidates depuis interactions Hermes.md`

It identified high-value candidates:
- `finish-real-qa-gate` — best handled by strengthening `definition-of-done`.
- `telegram-project-delivery` — best handled by `professional-project-delivery` / Telegram delivery rules.
- `conversation-to-skill-review` — best candidate if a new class-level skill is needed.
- `long-task-ledger` — candidate for long-running autonomous missions.
- `scope-pause-qa` — mostly belongs under `obsidian`.
- `proxy-first-research-scraping` — belongs under scraping/search skills.
