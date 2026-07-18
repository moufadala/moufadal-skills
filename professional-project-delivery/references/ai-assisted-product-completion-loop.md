# AI-assisted product completion loop

Use this when Moufadal reports that a product still has many obvious bugs, that progress is too slow, or asks whether the problem is prompt, methodology, missing planning, or missing QA.

## Durable lesson

The failure pattern is usually not that the user failed to provide a perfect prompt. The agent shipped from a plausible implementation plus structural audits, while the product needed a **behavioral oracle**: examples, generalized cases, and acceptance tests that represent how a real user will use it.

For AI-assisted delivery, the loop must be:

1. Reproduce at least a few of the user's exact complaints on the public/staged artifact.
2. Convert exact complaints into bug families, not one-off strings.
3. Write or update an acceptance contract before coding.
4. Add red behavioral tests/evals for the families.
5. Implement the smallest durable fix in the parser/state/model/pipeline, not just the visible symptom.
6. Run red→green tests, hard regression gates, and public/browser QA.
7. Reply with concise accountability: what was broken, what now passes, what remains.

## Example: natural search/product parser

If the user says queries like `F4`, `non meublé`, quartier names, or bare numbers fail, do not ask them to enumerate every possible phrase. Generalize:

- alias family: accents, spaces, hyphens, plurals, quartier variants;
- synonym family: `Tn = Fn`, studio/T1/F1;
- negation family: `non meublé`, `pas meublé`, `sans meubles`;
- ambiguous numeric family: bare `900` needs an operator choice rather than silently assuming max;
- visibility family: if a summary announces price drops, price-drop cards/tabs must be immediately visible.

The implementation should produce one structured intent object. Chips, understood line, counters, and filtering must all derive from the same object. Separate ad-hoc parsers for display and filtering create false passes.

## Acceptance-bank sources

Build cases from:

- the user's exact examples;
- real data values in the product dataset;
- domain grammar and local vocabulary;
- metamorphic variants: accent/no accent, singular/plural, hyphen/space, word order, synonyms;
- later analytics/search logs when available.

## Communication under frustration

When the user says there is “du laisser-aller” or “on avance à pas de fourmis”, do not defend previous audits. Say clearly whether the process failed, show one or two reproduced facts, and explain the stronger loop now being applied. The next response should prioritize action and evidence over reassurance.

## External practice anchors

Useful community practices to cite/translate into the project contract:

- Specification by Example / Acceptance Test-Driven Development: examples become executable acceptance criteria.
- BDD / Given-When-Then: user-visible behavior defines success.
- Story mapping: group complaints into user journeys and slices.
- Evals: use datasets/metamorphic tests so AI-built features do not rely on manual spot checks.
