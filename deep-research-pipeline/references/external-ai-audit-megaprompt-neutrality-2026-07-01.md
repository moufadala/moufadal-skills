# External AI audit mega-prompts — neutrality correction (2026-07-01)

## Signal

Moufadal corrected a generated mega-prompt because it over-oriented Claude/external AI toward Hermes' own analysis and strategy. His intended workflow: once he gives the mega-prompt and corpus to Claude/another IA, that external IA decides the analysis, priorities, strategy, rules, and conclusions independently.

## Durable lesson

When producing a mega-prompt for an external AI audit/research review:

- Do **not** make Hermes' preliminary analysis the frame to validate.
- Do **not** prescribe the exact findings or strategic direction unless the user explicitly asked for a constrained review.
- Make the raw corpus/evidence the priority source.
- Present Hermes' analysis as a secondary hypothesis, not a conclusion.
- Explicitly authorize the external AI to disagree with Hermes, ignore parts of Hermes' analysis, and decide its own structure if that improves the audit.
- Ask for evidence/proof/hypothesis separation, but avoid over-constraining the answer into Hermes' preferred taxonomy.

## Good prompt stance

Use language like:

> Tu es l'IA externe qui prend la décision finale. Ce prompt ne doit pas t'orienter vers une analyse déjà choisie par Hermes. Le corpus brut est la source prioritaire. L'analyse Hermes est une hypothèse de travail, pas une conclusion. Tu peux la contredire, l'ignorer partiellement ou la remplacer si le corpus montre autre chose.

## Bad prompt stance

Avoid language that says, implicitly or explicitly:

- “Voici les points d'analyse obligatoires” when those points encode Hermes' already-chosen interpretation.
- “Propose le protocole X/T0/T1/T2/T3” before the external AI has decided whether that framework is valid.
- “Évalue selon ces axes” if the user's goal is independent diagnosis rather than checklist completion.

## Minimal acceptance check

Before delivering an external-audit mega-prompt, ask:

1. Would a smart external AI feel free to disagree with Hermes?
2. Is the raw corpus clearly above Hermes' analysis in source priority?
3. Are required outputs limited to necessary deliverables, not pre-decided conclusions?
4. Does the prompt ask the external AI to decide, not just fill a template?
