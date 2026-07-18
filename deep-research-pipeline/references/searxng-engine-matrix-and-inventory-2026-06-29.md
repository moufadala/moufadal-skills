# SearXNG engine matrix + inventory lesson — 2026-06-29

## Trigger

Use this when DeepResearch/SearXNG coverage is discussed, especially if Moufadal asks whether SearXNG is already integrated or asks for the full engine list.

## What was learned

SearXNG was already integrated in `/opt/data/scripts/deep_research_v2.py` as channel `searxng`, but the useful contract was not explicit enough. Moufadal corrected the target shape: configure a source-class matrix, not a vague list of bangs.

Canonical matrix for DeepResearch:

- General: Bing / Google / DuckDuckGo / Mwmbl
- Technical: GitHub / StackOverflow / HackerNews / GitLab
- Academic: Google Scholar / OpenAlex / Crossref / PubMed / arXiv
- Reddit: indirect only through `site:reddit.com`, never SearXNG's direct Reddit engine

Recommended profiles:

- `balanced` default: stable, lower-noise engines; keep Google/Scholar/Reddit indirect out unless required.
- `max` or `matrix`: full matrix for premium/overnight/diagnostic runs, including Google/Scholar and Reddit indirect.
- `fast`: low-latency subset for smoke checks.

## Operational checks

When asked “what engines do we have access to?”, do not answer from memory. Query SearXNG `/preferences` and archive the raw HTML + parsed inventory. In this session the inventory showed 248 configured engines and a default smoke query returned results from Bing/DuckDuckGo/Mwmbl with no unresponsive engines.

Useful artifact layout:

```text
/opt/data/artifacts/searxng-engines-<timestamp>/
  preferences.html
  search_smoke.json
  collection.log
  engines_inventory.md
  engines_inventory.json
```

## Pitfalls

- “Accessible/configured” does not mean “safe for high-throughput DeepResearch”. Google/Scholar/Brave/Reddit-style sources can exist in SearXNG and still CAPTCHA/rate-limit under repeated probes.
- Reddit direct may be present in SearXNG preferences, but the DeepResearch contract should route Reddit indirectly via `!ddg site:reddit.com ...` or `!bing site:reddit.com ...`.
- If importing a script module with dataclasses through `importlib.util.module_from_spec`, register it in `sys.modules[spec.name]` before `exec_module`; otherwise dataclasses can fail because `sys.modules.get(cls.__module__)` is `None`.

## Acceptance criteria before claiming the matrix is wired

- `ast.parse` or equivalent syntax check passes for `deep_research_v2.py`.
- A probe of `searxng_expanded_queries()` shows the expected profiles and labels.
- At least one live SearXNG JSON smoke is archived with result count and `unresponsive_engines`.
- For `max`/`matrix`, confirm that Reddit appears only as `site:reddit.com` indirect probes, not as the direct Reddit engine.
