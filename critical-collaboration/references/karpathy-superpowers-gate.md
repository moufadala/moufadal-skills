# Karpathy/Superpowers lightweight project gate

Use this as a compact decision/checklist when Moufadal asks whether Hermes is applying the “Karpathy / Superpowers” style to serious work.

## Source pattern captured from session

- Article/video theme: AI coding skills are reusable instruction packs for agents; useful when they prevent common agent failure modes, not when blindly enabled everywhere.
- Karpathy-inspired principles:
  - think before coding;
  - simplicity first: minimum code/process that solves the problem;
  - surgical changes: avoid broad unrelated edits;
  - goal-driven execution: define success criteria;
  - loop until verified by a real artifact.
- Superpowers-style principles:
  - structured brainstorm/spec/plan/implementation/review;
  - clarifying questions when the answer is genuinely personal/business or blocked;
  - TDD/spec-driven execution for non-trivial builds;
  - independent review/fresh context for important work.

## Hermes adaptation

Do **not** turn every task into a heavy Superpowers workflow. For trivial tasks, answer or execute directly.

For serious projects, apply this lightweight gate before approving or building:

1. **Simplify:** What is the smallest reversible step that proves the direction?
2. **Quantify:** What number/count/benchmark/comparison will show progress?
3. **Classify facts:** What is verified, inferred, or unknown?
4. **Acceptance criteria:** What exact output/log/test/screenshot makes this done?
5. **Surgical scope:** Which files/services/sources are in-scope and out-of-scope?
6. **Skill routing:** Which existing skills should be loaded for this class of work?
7. **Independent validation:** Is Claude Code/subagent/fresh-context review needed, or are Hermes tools enough?
8. **Artifact:** What durable proof should be saved under `/opt/data/artifacts/...` or in the repo?
9. **Stop/change condition:** What result tells us to stop coding and validate/research/switch approach?

## Response pattern

When useful, state explicitly:

- “J’applique ici le gate Karpathy/Superpowers : simplifier, quantifier, vérifier.”
- “Ça vaut le coup seulement si le critère suivant est vérifié…”
- “La meilleure prochaine étape n’est pas de coder, c’est de prouver X avec Y.”

## Pitfall

Do not claim the gate is always fully applied. If a previous project only used part of it, say so: “utilisé partiellement/implicitement, pas systématiquement”. Then encode the missing piece into the plan or skill library.
