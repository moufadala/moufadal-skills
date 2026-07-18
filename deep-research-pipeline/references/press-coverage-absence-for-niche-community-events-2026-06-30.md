# Press coverage absence checks for niche/community events — 2026-06-30

## When this applies

Use this pattern when Moufadal asks whether “la presse” or public media are talking about a niche/community event across specific geographies, especially when Last30days or the DeepResearch runner returns little or nothing.

Example class: Ashara Mubaraka / Dawoodi Bohra coverage in USA, London, Paris, Marseille.

## Durable lesson

For niche community topics, an answer of “nothing found” must be audited by geography and source class before it is safe to report. Treat it as **absence detected in the queried channels**, not proof that coverage does not exist.

## Recommended workflow

1. Run Last30days with separate queries per geography, not only a single broad query.
   - Global topic + all zones.
   - One query per city/country.
   - Include both English and local-language terms when relevant (`press`, `presse`, city names, community names).
2. Run DeepResearch local with explicit subquestions per geography.
3. Add a deterministic Google News RSS probe across regional editions:
   - US edition (`hl=en-US&gl=US&ceid=US:en`)
   - UK edition (`hl=en-GB&gl=GB&ceid=GB:en`)
   - France edition (`hl=fr&gl=FR&ceid=FR:fr`)
4. Dedupe by title/source and classify each hit:
   - relevant/current/in-zone;
   - out-of-period;
   - out-of-zone;
   - community/social but not press;
   - off-topic false positive.
5. If results are sparse, run a critique pass (Claude Code is useful) asking specifically for:
   - coverage by geography;
   - supported conclusions;
   - gaps;
   - overinterpretation risks.
6. Final wording must separate:
   - “press coverage found”;
   - “community/social signal found”;
   - “historical context only”;
   - “absence detected, not absolute absence.”

## Pitfalls

- Do not count Reddit/social posts as press coverage unless the user asked for community chatter too.
- Do not use old Google News hits (e.g. 2015/2020/2024/2025) as evidence for a current-year event; label them as historical context only.
- Do not infer a city result from a source that only mentions the city in an unrelated way or is actually about another location.
- Do not report a broad “no coverage exists” claim. Say: “No relevant coverage was detected in the open sources queried.”
- For events tied to a lunar/religious calendar, explicitly consider that coverage may appear during or after the event, not before.

## Minimal artifact set

Save a dated research folder with:

- raw Last30days outputs per query;
- DeepResearch report, even if empty, for auditability;
- Google News RSS JSON and a short human-readable probe output;
- final Markdown/HTML report;
- optional Claude critique JSON/text.

## Suggested final phrasing

> Je n’ai pas trouvé de couverture presse pertinente et récente dans les zones demandées. C’est une absence détectée dans les canaux ouverts interrogés, pas une preuve absolue qu’il n’existe rien dans WhatsApp, X, Instagram, presse locale non indexée ou médias communautaires privés.
