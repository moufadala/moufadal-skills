---
name: conversation-to-skill-review
description: "Décider quoi retenir durablement d'une interaction : mémoire, note de vault, correctif de skill, ou nouveau skill — avec preuve. À utiliser quand l'utilisateur demande ce qu'on peut apprendre d'une session, dit que l'agent a répété une erreur, veut mettre à jour la bibliothèque de skills, ou transformer un échange en comportement durable."
version: 1.0.0
license: MIT
platforms: [linux, macos, windows]
---

# Conversation to Skill Review

## Overview

Use this skill to turn repeated user corrections, project incidents, and Obsidian conversation-intelligence notes into durable behavior changes. The goal is not to create more skills by default; the goal is to choose the smallest durable intervention that prevents the same mistake from happening again.

Moufadal values proof-backed improvement. A good review distinguishes a stable workflow lesson from temporary task progress, then updates the right substrate: memory, Obsidian, an existing skill, or a new skill.

## When to Use

Use this skill when the user says or implies:

- “à partir de nos interactions…”
- “quels skills on peut créer ?”
- “mets à jour la skill library”
- “tu as encore refait la même erreur”
- “qu’est-ce qu’on peut améliorer dans Hermes ?”
- “testons Obsidian” in the context of behavior/skills
- “remember this workflow” or “don’t do that again” for a recurring agent behavior

Do not use it for:

- simple one-off preferences that belong directly in `memory`;
- project progress logs that will be stale within days;
- creating narrow one-session skills when an existing umbrella skill can be patched;
- sensitive raw transcript dumps, secrets, cookies, tokens, or `.env` content.

## Decision Ladder

Apply this ladder in order:

1. **Currently-loaded skill patch** — first check skills loaded/consulted in the session; if a writable one governs the lesson, patch that one.
2. **Existing skill patch** — preferred when a governing skill exists and failed to prevent the error.
3. **Existing umbrella reference** — add a short `references/` file when details/evidence are useful but too specific for SKILL.md.
4. **Central runbook / Operating Map update** — when the session changed durable Hermes/VPS operations (providers, gateway, toolsets, MCP, cron, proxy/scraping, dashboards, incidents, QA/reprise commands, or secret locations), update `/opt/data/vaults/moufadal-second-brain/70-Runbooks/HERMES Operating Map.md` as well as skills/memory.
5. **Graphify sync** — when Graphify is active and the change affects future orchestration, update `/opt/data/graphify/current/graph.json` or run the normal Graphify update path, then verify query/MCP visibility. Use `graphify-orchestration` for the exact pattern.
6. **New skill** — only when no existing skill clearly owns the workflow and the trigger is likely to recur.
7. **Memory** — for stable user/environment facts, not procedure.
8. **Obsidian note** — for project knowledge, decisions, source synthesis, or conversation intelligence.
9. **Do nothing** — only if the session was genuinely smooth and produced no correction, workflow, style, or technique signal.

**Active review rule:** when Moufadal explicitly asks to review a conversation and update the skill library, a no-op is exceptional. Most such sessions should produce at least one small patch, support file, or runbook update unless all relevant skills are protected or the interaction contains no durable learning.

## Workflow

### 1. Gather evidence first

Do not rely on vibes. Use at least one of:

- `session_search` for prior corrections or incidents;
- `read_file` / `search_files` inside `/opt/data/vaults/moufadal-second-brain` for Obsidian notes;
- `skill_view` for candidate skills to patch;
- actual artifact/log paths if the lesson came from a failed task.

If Obsidian notes are `draft-auto`, treat them as signal, not final truth. Cross-check with session history or current user confirmation before creating a durable rule.

### 2. Extract the lesson

For each candidate lesson, write:

- **Trigger:** what user wording or task context should activate it?
- **Failure prevented:** what bad outcome does it avoid?
- **Best substrate:** memory, Obsidian, patch skill, new skill, or nothing?
- **Owner skill:** which existing skill should own it if any?
- **Verification:** how will we know the fix works next time?

### 3. Prefer patching existing skills

Before creating a new skill, inspect nearby skills with `skills_list` and `skill_view`. Patch when the lesson is really a missing pitfall, missing trigger, or missing verification step.

Create a new skill only if:

- the workflow has a distinct recurring trigger;
- it combines multiple tools/substrates in a way no current skill owns;
- it would reduce future user steering materially;
- it can be tested with realistic prompts.

### 4. Write or patch with a testable contract

Any new or patched skill should include:

- clear trigger phrases;
- counter-triggers;
- a short workflow;
- common pitfalls;
- verification checklist;
- links to related skills.

For important new skills, add 3 realistic eval prompts or at least state how the skill will be tested.

### 5. Report compactly

Telegram response should include:

- what evidence was inspected;
- what changed;
- why it matters;
- what was deliberately not changed;
- paths/skill names;
- rollback or reversal instruction if relevant.

Avoid raw session dumps and long logs.

## Common Patterns from Moufadal Interactions

These patterns often become skill candidates:

- user says the agent made a too-local fix after a general correction: first identify the class-level failure, patch the governing umbrella, and only then patch the domain skill if still useful. Do not turn a systemic workflow issue into a narrow one-project rule.
- user says existing research/Obsidian/memory was not used proactively: treat this as a **known-context activation failure**. Patch the relevant project/router/recovery skill so future sessions retrieve known steps, blockers, community issues, and likely next actions before the user rediscovers them.
- declaring “fini” before QA, runtime reload, or background completion;
- Telegram reports that include too much raw log detail;
- long-running tasks without process/job/run-dir ledger;
- Obsidian ingestion without distillation/indexing;
- Hermes/VPS stack changes not reflected in the central Operating Map;
- skill-library changes not reflected in Graphify when Graphify is the active project knowledge graph;
- searches or scraping conclusions without required proxy preflight;
- project continuations that ignore session_search or existing artifacts;
- scope removals that are not reflected in active indexes.

## Reference Notes

- `references/session-2026-07-03-known-context-activation-failure.md` — session-specific lesson: do not turn Moufadal’s systemic complaint about unused prior knowledge into only a domain-specific patch; treat it as known-context activation failure and patch class-level routing/recovery/review skills first.
- `references/session-2026-06-30-operating-map-and-active-skill-review.md` — session-specific lesson: active skill-review default plus the new central `HERMES Operating Map.md` as a durable update target for Hermes/VPS operations.
- `references/session-2026-07-01-adaptive-response-and-7d-audit.md` — session-specific lesson: adaptive Telegram reply tiers (T0/T1/T2/T3), Obsidian’s role in conversation alignment, and the 7-day audit artifact pattern.
- `references/session-2026-07-12-skill-source-of-truth-external-dirs.md` — session-specific lesson: when deciding neutral repo vs Hermes-native skills, inspect `skills.external_dirs`, active-name collisions, and whether a local skill is a thin wrapper or a strongly coupled operational overlay.

## Verification Checklist

Before saying the review is done:

- [ ] At least one durable source was inspected (`session_search`, Obsidian note, existing skill, or artifact).
- [ ] Existing skills were checked before creating a new one.
- [ ] Each proposed skill has an estimated utility and non-creation alternative.
- [ ] Any skill modification was verified with `skill_view` or file readback.
- [ ] The final response distinguishes created, patched, deliberately skipped, and still-open items.

## Pitfalls

1. **Creating one narrow skill per incident.** Prefer umbrella skills and references unless the trigger is clearly reusable.
2. **Saving stale project progress to memory.** Use Obsidian or artifacts instead.
3. **Treating draft-auto notes as gospel.** Cross-check before durable changes.
4. **Patching the wrong layer.** Style preferences may belong in delivery skills; technical procedures belong in domain skills.
5. **Stopping at analysis.** If the user says “vas-y fais-le”, create or patch the agreed skill and verify readback.
6. **Ignoring tool-scope instructions during review.** If the user says only memory/skill-management tools are allowed, obey that scope even if a generic tri-agent/Claude guard is also present. Do not attempt Claude Code, terminal, session_search, or file tools; use `skills_list`, `skill_view`, `skill_manage`, and `memory` only, then state that the Claude guard could not be applied because the explicit review scope forbade non-skill tools.
