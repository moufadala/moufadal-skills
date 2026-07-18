# Feasibility-first multisite scraping

Use when the user’s goal is an operational result, not primarily anti-bot research.

## Trigger phrases

- “le goal c’est que ça marche”
- “teste les sites les plus faisables”
- “pas les plus gros / pas les plus durs”
- user frustration after the agent drifts toward technically interesting blockers

## Rule

Do not start with the hardest protected sites just because they are the unresolved ones. First rank all sources by probability of a live, verifiable result.

## Ranking method

For each candidate site/source, score:

1. Has a fresh working script or historical end-to-end artifact?
2. Can it return live prices/data now from the VPS?
3. Is the blocker a normal dynamic UI or hard anti-bot?
4. Does a deterministic command already exist?
5. Can a smoke test finish in <5 minutes?

Then choose the highest-probability source, not the most interesting one.

## Output expected before deeper work

- ordered feasibility ranking;
- first site/source selected;
- exact smoke-test command;
- result proof: title/final URL/prices/data/artifact path;
- first-try and fallback probability;
- next stabilization step.

## Pattern from Reunion flights session

Air Austral outranked French Bee/Corsair because it had a live working command and Amadeus price extraction:

```bash
python3 /opt/data/scripts/airaustral_price_check.py RUN MRU 2026-07-15 2026-07-22
```

A small cheapest-window smoke test also succeeded:

```bash
/opt/data/labs/browser-use-poc/venv/bin/python /opt/data/scripts/airaustral_cheapest_window.py RUN MRU 2026-07 --weeks 1 --step-days 3 --limit 3
```

French Bee had a historical success but needed restabilization; Corsair had Imperva/hCaptcha and was last for a “make it work” goal.

## Pitfall

Do not over-apply the earlier rule “push broken sites first.” That rule is correct for blocker research, but wrong when the user asks for the most feasible path to a working result.
