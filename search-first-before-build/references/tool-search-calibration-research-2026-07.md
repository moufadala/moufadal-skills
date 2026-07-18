# Tool-search calibration research — 2026-07

## Why this reference exists

Moufadal corrected that the most useful calibration point is not only “search before building”, but specifically **when Hermes decides to launch an internet/external search**. A later research pass showed this maps to a known agent problem: tool-use calibration / unnecessary tool calls / over-delegation.

## Distinguish two problems

1. **Build-vs-buy / search-first before coding**
   - Question: does a repo, package, MCP server, template, skill, or local artifact already solve this?
   - Typical output: `ADOPT / EXTEND / COMPOSE / BUILD`.
   - Sources: `shimo4228/search-first`, `mturac/skill-hunter`, Skills Agents / SkillForge search-first.

2. **Tool-search calibration / when to use web search**
   - Question: should Hermes call web/search at all, or answer from internal knowledge + current context + local files?
   - Typical output: visible justification for external search during calibration.
   - Sources: epistemic necessity, When2Tool, To Call or Not to Call, SMARTCAL, tool correctness evals.

Do not collapse these into one generic “research first” rule. A build task may need prior-art search; a conversation answer may only need local context.

## Practical Hermes gate before external search

Use this lightweight triad before launching web/external search:

```text
Necessity: can I answer reliably without external search?
Utility: will external search likely improve correctness/completeness?
Affordability: is the gain worth latency, cost, noise, and source-verification burden?
```

If all three are strong → external search is justified. Announce it during calibration:

```text
Recherche externe justifiée selon moi : [necessity/utility/affordability in one short reason]. Je vérifie repos/docs/community avant de coder; tu pourras me dire si c'était trop tôt ou utile.
```

If necessity is weak → do not search. If utility is unclear but the decision is high-risk → propose level 3.

## Level-3 triggers from the research

Propose level 3 when:

- repeated user corrections show the search threshold is still miscalibrated;
- a `BUILD` verdict is likely but prior-art evidence is weak or contradictory;
- the project risk is high: durable architecture, agent routing, security, VPS reliability, scraping/anti-bot, recurring automation;
- a previous incident shows Hermes reinvented, missed a repo/template/skill, or searched too late;
- the cost of a wrong tool/build decision is multiple hours, production debt, data exposure, or a service breakage.

Level 3 should mean: independent Claude critique/research, second external search loop, stronger source comparison, and golden-set update if the boundary should persist.

## Sources and what to extract

- `Position: Agent Should Invoke External Tools ONLY When Epistemically Necessary` — https://arxiv.org/html/2506.00886v2
  - Use as normative criterion: external tools only when internal reasoning/current context is insufficient.

- `LLM Agents Already Know When to Call Tools - Even Without Reasoning` / When2Tool — https://arxiv.org/html/2605.09252 and https://github.com/Trustworthy-ML-Lab/when2tool
  - Tool-augmented agents over-call tools; the paper reports Probe&Prefill reducing tool calls by 48% with 1.7% accuracy loss, and 20–56% fewer API calls on Search-o1 without accuracy degradation.
  - Hermes cannot use hidden-state probes directly, but can collect labeled examples and golden cases.

- `To Call or Not to Call` — https://arxiv.org/pdf/2605.00737
  - Best framing for web-search calls: necessity, utility, affordability.

- `SMARTCAL` — https://aclanthology.org/2024.emnlp-industry.59.pdf
  - Tool-abuse / overconfidence and multi-agent self-verification; useful analogy for level 3.

- `The Confidence Dichotomy` — https://arxiv.org/pdf/2601.07264
  - Web search is an evidence tool and can increase overconfidence because retrieved information is noisy; deterministic verification tools can ground reasoning better.

- Braintrust / LangSmith / DeepEval / Promptfoo docs
  - Support golden datasets, online feedback → offline eval loops, and tool correctness metrics (`tools_called` vs `expected_tools`).

## Pitfalls

- Do not treat “I searched the web” as proof; web search is noisy evidence, not deterministic verification.
- Do not use search-first for micro-actions: typo, local file read, simple log command, obvious rollback.
- Do not wait for Moufadal to ask about level 3 when the signals are already present; propose it and let him approve/refuse.
- Do not store every single correction as a new skill. Promote recurring boundaries into this skill’s golden cases or references.

## Suggested eval prompts

Positive external-search cases:

- “Crée une architecture Obsidian par domaines; vérifie les vaults/templates existants.”
- “Ajoute un serveur MCP; regarde d’abord s’il existe un serveur ou pattern maintenu.”
- “On va construire un scraper fragile; cherche d’abord scripts locaux, repos et limites anti-bot.”

Negative external-search cases:

- “Corrige cette typo.”
- “Lis ce fichier et résume-le.”
- “Donne-moi la commande pour afficher les logs Docker.”
- “Rollback le dernier patch évident.”
