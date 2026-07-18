---
name: karpathy-project-gate
description: "Porte légère à passer au démarrage/reprise d'un projet sérieux : simplifier, quantifier, cadrer l'exécution, router vers les bons skills, exiger des artefacts vérifiés — sans imposer un processus lourd à une tâche triviale. À utiliser quand l'utilisateur lance ou reprend un projet et se demande s'il est bien cadré ou si c'est du bricolage."
version: 1.0.0
license: MIT
platforms: [linux, macos, windows]
---

# Karpathy/Superpowers Project Gate

## Overview

This skill is a lightweight Hermes adaptation of community patterns from popular AI coding-agent skills:

- Karpathy-inspired rules: think before coding, keep it simple, make surgical changes, stay goal-driven, verify with real evidence.
- Superpowers-style methodology: clarify/specify, plan, execute with discipline, test/review, and use independent validation for serious work.
- Matt Pocock-style clarification: use a “Grill me” pass when ambiguity would materially change the implementation, business outcome, UX, data source choice, or definition of success.

The goal is **not** to turn every request into a heavyweight process. The goal is to stop common agent failures: rushing into code, expanding scope, inventing success, skipping QA, not asking enough up-front questions, or agreeing too easily.

## When to Use

Use this skill when Moufadal asks to:

- start a new serious project, scraper, dashboard, website, automation, research dossier, or business workflow;
- continue or audit prior project work;
- decide whether a direction is worth building;
- optimize an implementation workflow;
- check whether Hermes is applying “Karpathy”, “Superpowers”, “simplify/quantify/verify”, or similar rules;
- run multi-step work where a bad assumption could waste time or produce a fake win.

Do **not** use the full gate for tiny one-shot tasks like quick calculations, simple file reads, or direct factual answers. For trivial tasks, execute directly and verify normally.

## Source Validation Snapshot

Community-aligned patterns verified before creating this skill:

- The AWS/DEV article on popular AI coding skills describes skills as Markdown instruction packs loaded only when relevant, not globally forced on every task.
- `multica-ai/andrej-karpathy-skills` emphasizes:
  - think before coding;
  - simplicity first;
  - surgical changes;
  - goal-driven execution;
  - explicit success criteria and verification loops.
- `obra/superpowers` emphasizes:
  - not immediately writing code;
  - extracting/validating a spec;
  - implementation planning;
  - TDD/YAGNI/DRY;
  - subagent execution and review for larger work.
- `mattpocock/skills` emphasizes:
  - grilling sessions to reduce misalignment;
  - shared language / `CONTEXT.md` to reduce verbosity and preserve domain terms;
  - small composable skills rather than one framework owning everything.
- `addyosmani/agent-skills` emphasizes:
  - lifecycle routing: define → plan → build → verify → review → ship;
  - assumptions surfacing;
  - pushback when warranted;
  - simplicity, scope discipline, and evidence-based verification.
- Spec-driven development references from Augment/DeepLearning.AI emphasize:
  - specs as active constraints, not passive docs;
  - project constitution / feature specs for complex or multi-session work;
  - plan–implement–verify loops to reduce “vibe coding” drift.

Hermes adaptation: use a **compact gate** by default; escalate to full spec/review/TDD only when the task is large, risky, costly, or hard to reverse.

## Grill Me / Clarification Pass

Use this pass when Moufadal’s answer would materially change the project direction, implementation, UX, data source, monetization, scope, or acceptance criteria.

The default should be **2–5 sharp questions**, not a long questionnaire. Ask fewer if only one decision is blocking. Ask more only for a genuinely new project.

### When to grill

Ask questions before execution when:

- the request contains business/personal preferences that cannot be inferred from public research;
- multiple valid directions exist and choosing silently could waste hours;
- the success criteria are vague, e.g. “fais mieux”, “optimise”, “rends premium”, “aspire ce site”;
- the task affects public output, money, user acquisition, security, credentials, production services, or destructive changes;
- the user’s intended audience, tone, budget, risk tolerance, or go/no-go threshold is unknown;
- Hermes is about to build downstream work before the upstream proof is solid.

### How to grill

Use direct questions that expose tradeoffs:

```text
Avant d’exécuter, je te grille sur les 3 choix qui changent vraiment le résultat :
1. Public cible exact : ... ?
2. Critère de réussite : ... ?
3. Limite à ne pas franchir : ... ?
```

Good question types:

- **Goal:** “Quel résultat réel doit changer après ce livrable ?”
- **Audience:** “C’est pour toi, des clients, des investisseurs, ou un usage interne ?”
- **Success metric:** “On juge ça au nombre d’items récupérés, au taux de conversion, à la clarté, au gain de temps, ou autre ?”
- **Constraint:** “Qu’est-ce qui est interdit : coût, délai, risque légal, complexité, changement prod ?”
- **Preference:** “Tu préfères rapide/prototype ou propre/public ?”
- **Stop condition:** “À quel résultat on abandonne cette piste ?”

### When not to grill

Do not ask questions just to look rigorous. Execute directly when:

- the missing info is searchable or testable by Hermes;
- the task is small and reversible;
- the user already gave clear acceptance criteria;
- asking would block unnecessarily and a safe default exists.

If a safe default exists, state it and proceed:

```text
Je pars sur le défaut raisonnable : prototype vérifié avant polish. Je te demanderai seulement si le test terrain contredit cette direction.
```

## Non-Negotiable Minimal Gate

For serious work, do **not** turn this skill into ceremony. The mandatory core is only three questions:

1. **DONE:** What does done look like, and how will we know?
2. **ASSUMPTION:** What assumption would cause rework if wrong?
3. **PROOF:** What is the smallest reversible proof before bigger work?

Everything else in this skill is optional scaffolding. If these three are answered and the next step is safe, execute.

Compact pattern:

```text
Gate rapide :
- DONE = ...
- Hypothèse risquée = ...
- Preuve minimale = ...
```

## Pre-Build Product Gate — 6 forcing questions

Use this YC-office-hours style gate before coding a new product, significant feature, automation, dashboard, or business workflow when no clear spec/acceptance contract exists yet. Do **not** run it for bugfixes, tiny edits, or when Moufadal already supplied a concrete spec.

Ask fewer questions if the answer is obvious or researchable. The point is useful pressure, not ceremony.

1. **Problem:** What exact painful problem are we solving, in one sentence?
2. **User:** Who has this problem now, and what do they do without our solution?
3. **Hidden premise:** What assumption would make the whole build a waste if false?
4. **No-code alternatives:** What are 2–3 simpler ways to test this before building software?
5. **10-star version vs V1:** What would make this excellent, and what is the smallest reversible V1 that proves it?
6. **Success signal:** In 7–30 days, what evidence says this was worth doing?

Output a compact design note:

```text
Product gate:
- Problem = ...
- User/current workaround = ...
- Riskiest premise = ...
- No-code/smaller tests = ...
- V1 acceptance = ...
- Success signal = ...
```

Feed the result into `specification-par-exemples` or `professional-project-delivery` before implementation.

## Additional Community Patterns Worth Applying

### Autoresearch loop for measurable improvements

Use this pattern when the user asks for autonomous optimization, overnight improvement, or “advance without me” **and** the target has an objective metric. This is the useful Karpathy/autoresearch lesson: not a new tool by default, but a constrained loop.

Only run the loop if all five are true:

1. **Metric exists:** one primary number or binary gate, e.g. build passes, bundle KB, Lighthouse score, error count, extracted item count, HTTP success rate.
2. **Command exists:** a repeatable command measures it without subjective judgement.
3. **Baseline saved:** record the metric before changes.
4. **Atomic hypothesis:** one small change per iteration.
5. **Keep/revert rule:** keep only if the metric improves or no regression occurs on mandatory gates.

Default artifact:

```text
/opt/data/artifacts/<topic>/autoresearch-loop.md
```

Each row should include: timestamp, hypothesis, files touched, command, before, after, decision, rollback note.

Do **not** use this loop for vague taste work like “make it premium” unless you first define a quality checklist and visual QA evidence. Do not run it on production services, secrets, auth, DNS, routing, or destructive cleanup without explicit approval and rollback.

### A. Assumptions I’m Making

Inspired by production-grade agent-skills workflows: before non-trivial execution, surface assumptions explicitly instead of silently filling gaps.

Use when assumptions could change implementation or business outcome:

```text
Hypothèses que je prends si tu ne corriges pas :
1. ...
2. ...
3. ...
Je continue avec ces hypothèses sauf si tu me corriges maintenant.
```

Do not overuse this for small tasks. Use it when the cost of a wrong assumption is real.

### B. Shared Language / Project Context

For recurring projects, create or update a small project context/glossary so Hermes and subagents stop rediscovering the same terms.

Use when:

- a project has domain-specific vocabulary;
- explanations become long or repetitive;
- multiple sessions or agents will work on it;
- naming consistency matters in code, dashboard, scraper fields, or business docs.

Preferred artifacts:

- `CONTEXT.md` only if it can stay short, with max 5 fields:
  - goal;
  - success_metric;
  - out_of_scope;
  - owner / decision maker;
  - last_updated.
- `ADR-YYYY-MM-DD-<decision>.md` for important architecture/product decisions;
- project-specific `AGENTS.md` when the repo/workdir should steer future agents.

Keep these short. A stale 50-page context doc is worse than none. If `CONTEXT.md` is older than the current project state or not maintained, treat it as a hint, not truth.

### C. Phase Check, Not Waterfall

Borrow the useful part of lifecycle skill packs without installing a huge framework. This is **not** a rigid waterfall sequence. It is a quick diagnostic to avoid doing the wrong kind of work too early:

```text
DEFINE → do we know what outcome matters?
PLAN   → is the next slice small and verifiable?
BUILD  → are we implementing only that slice?
VERIFY → what proof/log/test/screenshot closes the loop?
REVIEW → is there complexity/security/performance risk worth checking?
SHIP   → if public/prod, is deploy/handoff/rollback covered?
```

If the current phase is obvious, do not recite all phases. Use the phase check only when sequencing is unclear.

This prevents errors like building UI before data acquisition is proven, or polishing code before the acceptance contract is clear.

## The Gate

Before approving or building, answer these nine checks briefly.

### 1. Simplify

Ask: what is the smallest reversible step that proves the direction?

Prefer:

- smoke test before full pipeline;
- one representative page/source before broad scraping;
- prototype before polished UI;
- one verified endpoint before abstraction;
- manual proof before automation.

Avoid:

- speculative architecture;
- generic frameworks for one-off work;
- building UI before data acquisition is proven;
- normalizing data before acquisition robustness is measured.

### 2. Quantify

Define at least one number that proves progress.

Examples:

- pages tested: `3/3`;
- records expected vs recovered: `270/270`;
- tests passing: `18/18`;
- HTTP success rate: `95%+`;
- max runtime: `< 60s`;
- price/card match rate: `100%`;
- lighthouse/accessibility target if relevant.

If no useful metric exists, state why and choose a binary artifact check instead.

### 3. Classify facts

Separate:

- **verified:** backed by log, curl, screenshot, test, browser observation, source, or file;
- **inferred:** plausible but not directly proven;
- **unknown:** still needs a test, source, or user choice.

Never present inferred as verified.

### 4. Acceptance criteria

Turn the request into a concrete done condition.

Good examples:

- “A dated report exists under `/opt/data/artifacts/...`, with raw logs and a clear go/no-go.”
- “The public URL loads on mobile and desktop, screenshot saved, no console errors.”
- “The scraper returns at least N items with prices and titles from source X, and rerun behavior is logged.”
- “Tests fail first for the bug, then pass after the fix.”

Bad examples:

- “It should work.”
- “Looks good.”
- “Implemented.”

### 5. Surgical scope

State what is in-scope and out-of-scope.

Rules:

- Touch only files/services needed for the task.
- Do not refactor adjacent code unless directly required.
- Do not broaden source lists without user authorization or evidence.
- If unrelated problems are discovered, report them separately.

### 6. Skill routing

Load the skills that match the work class before acting.

Common routes:

- serious deliverable: `professional-project-delivery`;
- project strategy or prioritization: `critical-collaboration`;
- code review / independent QA: `requesting-code-review`;
- plan writing: `writing-plans`;
- TDD: `test-driven-development`;
- scraping: `web-scraping-reality` plus stack-specific scraping skills;
- Hermes configuration: `hermes-agent`;
- design/UI: `claude-design` and `popular-web-designs`.

If no skill is relevant, say so explicitly.

### 7. Independent validation

Decide whether Hermes tools are enough or whether to ask another agent/fresh context.

Use independent validation when:

- the decision is strategic, costly, or hard to reverse;
- Claude Code produced the main artifact and should not self-validate it;
- security, prod, payments, auth, destructive operations, or public-facing deliverables are involved;
- the task spans many files or multiple systems.

For simple bounded tasks, Hermes direct verification is enough.

### 8. Artifact

Choose the proof to save or produce.

Acceptable artifacts:

- logs;
- screenshots;
- curl responses;
- test output;
- git diff;
- browser console output;
- dated Markdown report;
- HTML/PDF deliverable;
- raw data sample;
- before/after comparison.

No artifact means no strong success claim.

### 9. Stop/change condition

Define when to stop coding and switch approach.

When a stop condition triggers, do **one** of these explicitly:

- **halt and report** with raw evidence;
- **ask Moufadal** if it is a business/product decision;
- **switch approach** if a better verified path exists;
- **rollback/revert** if the change created harm;
- **escalate to review** if the risk is technical and non-obvious.

Do not silently continue past a stop condition.

Examples:

- “If Playwright still fails after 15 minutes on anti-bot, stop and inspect API/mobile/NetLog.”
- “If source returns fewer than expected items twice, write a go/no-go report instead of building downstream parsing.”
- “If tests reveal unrelated failures, isolate them and do not refactor broad areas.”
- “If a business choice is required, ask Moufadal instead of guessing.”

## Compact Response Pattern

For serious work, start with a short pre-flight like this:

```text
J’applique le gate Karpathy/Superpowers léger :
- Objectif : ...
- Critère quantifié : ...
- Chemin minimal : ...
- Preuve attendue : ...
- Skills à charger : ...
- Stop condition : ...
```

Then execute. Do not stop at the pre-flight if tools can make progress.

## Escalation Levels

### Level 0 — Direct execution

Use for trivial tasks.

- No formal pre-flight.
- Still verify if factual/system/file claims are made.

### Level 1 — Lightweight gate

Default for serious but bounded work.

- 5–8 bullet pre-flight.
- Tool-backed execution.
- One artifact or clear log.

### Level 2 — Professional delivery

Use for public-facing dashboards, courses, business docs, or serious reports.

- Load `professional-project-delivery`.
- Define acceptance contract.
- Produce durable artifact.
- QA with browser/tests/logs/screenshots.

### Level 3 — Independent review / TDD / subagents

Use for high-risk code or multi-system changes.

- Load review/TDD/planning skills.
- Ask Claude Code or another worker to critique/find blind spots when appropriate.
- Verify independently before claiming success.

## Common Pitfalls

1. **Over-applying Superpowers.** Heavy spec/review for a tiny task wastes tokens and slows work.
2. **Skipping the proof.** A file existing is not the same as a working artifact.
3. **Quantifying after the fact.** Choose the metric before building.
4. **Pretending all facts are verified.** Keep verified/inferred/unknown separate.
5. **Letting one agent grade itself.** For important work, use fresh validation or direct tool evidence.
6. **Broad refactors disguised as fixes.** Every changed line should trace to the user’s request.
7. **Building downstream before acquisition is proven.** Especially in scraping, prove robust source acquisition before extraction polish.
8. **Asking Moufadal questions that are searchable.** Research public facts; ask only for personal/business decisions.

## Verification Checklist

Before finalizing a serious task:

- [ ] Relevant skills were loaded.
- [ ] Objective and acceptance criteria are explicit.
- [ ] At least one metric or binary proof is defined.
- [ ] Verified/inferred/unknown are separated where relevant.
- [ ] Scope stayed surgical.
- [ ] A real artifact/log/test/screenshot/diff exists.
- [ ] Independent validation was used or explicitly judged unnecessary.
- [ ] Stop/change condition was respected.
- [ ] Remaining risks are stated without overselling.
