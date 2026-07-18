---
name: specification-par-exemples
description: "À utiliser quand une demande de fonctionnalité est floue : intention métier vague, entrées en langage naturel, cas limites cachés, ou « ça doit marcher comme tel autre produit ». Transforme la demande en spécification légère par l'exemple — critères d'acceptation, questions de clarification là où l'ambiguïté demeure, puis portes de QA exécutables avant de coder."
version: 1.0.0
license: MIT
platforms: [linux, macos, windows]
---

# Spécification par exemples

## Overview

Use this skill to avoid the classic AI-development failure mode: building a plausible UI or feature too quickly, then discovering that the real user cases do not work.

The goal is not to create a heavy enterprise cahier des charges. The goal is a **mini cahier des charges vivant**: concrete examples, acceptance criteria, edge cases, and verification gates that can be turned into tests.

In engineering language, this combines:

- **Spécification fonctionnelle**: what the product must do for the user.
- **Critères d'acceptation**: what proves the feature is correct.
- **Specification by Example / BDD**: examples drive implementation and tests.
- **A-TDD**: acceptance tests are defined before or alongside implementation.

## When to Use

Use this when:

- Moufadal says a feature is buggy, incomplete, or “pas pris en compte tous les cas”.
- The request includes natural language, search, filters, ranking, matching, scoring, alerts, dashboards, or business rules.
- The user compares the expected UX to another product, e.g. “comme Unia”.
- The feature has ambiguous inputs such as bare numbers, shorthand, synonyms, accents, typos, or hidden state.
- The cost of a wrong implementation is wasted iteration, user frustration, or false confidence.

Do not use this for trivial one-line edits where the expected behavior is fully explicit and low-risk.

## Core Workflow

### 1. Capture the business intent

Restate what the user is trying to accomplish in plain language. Separate facts from assumptions.

Example:

- Bad: “Add better search.”
- Good: “The user wants to type natural French immo phrases and get listings matching family size, furnishing, target quartiers, and budget without learning filter syntax.”

### 2. Build the example table before coding

Create concrete examples. For each example, define:

- **Input**: what the user says/types/clicks.
- **Expected intent**: structured interpretation.
- **Expected behavior**: visible result, filter, ranking, message, or UI state.
- **Must not happen**: common wrong interpretation.
- **Verification**: how to prove it: unit test, browser QA, API response, screenshot, log.

Template:

```markdown
## Acceptance examples

Example: [short name]
Input: `...`
Expected intent:
- field: value
Expected behavior:
- ...
Must not happen:
- ...
Verification:
- ...
```

### 3. Generate families, not only examples

Do not force Moufadal to enumerate every variant. Infer technical variants yourself.

Common families:

- Synonyms: `T4` / `F4`, `appartement` / `appart`.
- Accents: `beauséjour` / `beausejour`.
- Separators: hyphen, space, apostrophe, punctuation.
- Singular/plural and typo tolerance.
- Word order variations.
- Negative terms: `non meublé`, `sans parking`.
- Ambiguous numbers: budget, surface, room count.
- Zero-result cases: recognized intent but no matching data.
- Hidden state: localStorage, cookies, previous filters, masks/favorites.
- Page ordering: important sections must not be buried.
- Mobile/browser behavior.

### 4. Ask only useful clarification questions

Ask Moufadal only when the ambiguity is truly business/product-level and cannot be inferred.

Good questions:

- “Quand tu tapes `900` seul, veux-tu que le système demande `≤`, `≥`, `=`, `autour`, ou qu'il applique une valeur par défaut ?”
- “Si un quartier reconnu n'a aucun résultat, tu préfères zéro résultat clair ou élargissement automatique à la commune ?”

Bad questions:

- “Quels accents et variantes dois-je tester ?” — infer and generate them.
- “Quels fichiers dois-je modifier ?” — inspect the repo.

### 5. Create the product oracle

For non-trivial features, create a durable oracle file or equivalent test artifact that encodes expected behavior.

Possible artifacts:

- `tests/acceptance_cases.json`
- `tests/audit_user_cases.py`
- `docs/functional-spec.md`
- browser QA script
- fixture dataset with expected outputs

The oracle should cover:

- exact user-reported failures;
- generated variants;
- negative cases;
- ambiguous cases;
- regression cases for previously fixed bugs.

### 6. Implement against one source of truth

Avoid scattered logic where UI chips, summary line, counters, and filtering each parse differently.

Prefer:

1. parse input → structured intent object;
2. chips/summary derive from intent;
3. filtering/ranking derive from intent;
4. tests assert both intent and visible behavior.

### 7. Verify at the real boundary

Before claiming done, run verification at the boundary the user experiences:

- public URL, not just local file;
- browser console, not just build success;
- real data, not toy fixtures only;
- screenshot/DOM/log/test output as evidence.

## Output Format for a Spec Pass

When asked to plan or repair a fuzzy feature, respond with this structure before coding unless urgency requires a tiny hotfix:

```markdown
## Mini spécification fonctionnelle

Objectif utilisateur:
- ...

Hypothèses:
- ...

Questions nécessaires:
- ...

Familles de cas:
- ...

Exemples d'acceptation:
1. Input: `...`
   Attendu: ...
   Ne doit pas: ...
   Vérification: ...

Contrat de sortie:
- Tests à créer/mettre à jour
- QA navigateur/API
- Artefacts attendus
```

If the user has already said “go” or the ambiguity is low, proceed to implement after writing the spec internally/briefly and create the tests.

## Common Pitfalls

1. **Coding from vibe.** A natural-language request is not enough when many hidden cases exist.

2. **Over-asking.** Do not dump 20 questions on Moufadal. Infer what is technically inferable; ask only product choices.

3. **Testing tokens instead of behavior.** A feature flag or function name proves nothing. Test what the user sees and what the system returns.

4. **No negative cases.** The “must not happen” column is often where bugs hide.

5. **No public QA.** Passing local tests is insufficient for deployed dashboards/apps.

6. **Spec as static document only.** The spec must become executable tests or audit gates, otherwise it will drift.

## Verification Checklist

- [ ] User intent restated in business language.
- [ ] Assumptions and product ambiguities separated.
- [ ] Concrete examples written before or alongside implementation.
- [ ] Variants generated beyond the user's exact examples.
- [ ] Acceptance criteria include “must not happen”.
- [ ] Tests/audits created or updated.
- [ ] Implementation uses a single intent/source-of-truth where possible.
- [ ] Real boundary QA completed with evidence.
- [ ] Remaining limitations stated without overclaiming.
