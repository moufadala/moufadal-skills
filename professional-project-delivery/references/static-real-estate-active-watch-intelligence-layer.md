# Static real-estate active watch + intelligence layer

Use this when a clean static real-estate portal already works and Moufadal asks for the next serious layer: active watch, deduplication, photo quality, custom alerts, Réunion localization, and opportunity scoring — without cluttering the main search page.

## Trigger

- The public portal is already usable/searchable.
- User asks for daily/bi-daily refresh, source-break alerts, new/disappeared/price-drop reporting, dedup, premium photos, saved alerts, map/localization, or opportunity score.
- User explicitly wants separate page/tab/button and says not to overload the main page.
- User asks for research first because data loss, restitution loss, or noisy deduplication is unacceptable.

## Product rule

Do **not** turn the clean search page back into a dashboard. Add intelligence as separate surfaces:

- `changes.html/json` — watch report: new, disappeared, price changes, source health.
- `source_health.html/json` — operational/source freshness view.
- `dedup.html/json` — probable duplicate groups and merge candidates.
- `locations.html/json` — geographic interpretation and mapping readiness.
- `opportunity.html/json` — score rankings and explanations.
- `alertes_cours.html` or equivalent — pedagogical explanation of custom-alert implementation.
- one small `Analyse` button/card action is acceptable if it opens an existing modal/popup; no heavy inline analysis on cards.

## Architecture pattern

Keep raw listings immutable and add non-destructive product layers:

```text
raw scraper DB/export
  -> normalized static listings.json
  -> history.sqlite              # active/inactive, first/last_seen, price events
  -> changes.json/html           # public digest, avoid baseline spam
  -> source_health.json/html     # source status/freshness/errors
  -> dedup_groups.json/html      # candidate groups, no deletion
  -> locations.json/html         # inferred commune/region/quality
  -> opportunity.json/html       # explainable score and warnings
```

Never delete listings during dedup. Use soft grouping/canonical candidate only:

- keep every listing ID and source URL;
- score similarity with commune/zone/title/type/price/surface/rooms;
- show confidence and reasons;
- preserve multiple source links;
- only later, if needed, let the UI collapse group display while keeping expand-all.

## Active watch / alert implementation

1. Build/update history first:
   - `first_seen`, `last_seen`, `active`, `last_snapshot_at`;
   - price fields normalized from all possible schema names (`rent_eur`, `price`, etc.);
   - location/source fields normalized from all possible schema names (`commune`, `city`, `source_site`, `source`).
2. Generate changes from history:
   - baseline `new` events stay in audit counts but are hidden from public/Telegram first-run spam;
   - show disappeared and price changes;
   - include all-history counts for accountability.
3. Source health alerts:
   - classify required/important/optional sources;
   - alert on newly broken critical sources or changed failure state;
   - cooldown repeated failures;
   - stdout empty means silent OK for script-only cron.
4. Saved search alerts:
   - bootstrap `seen` silently;
   - emit Telegram digest only for newly matching canonical IDs;
   - include search URL and top matches.
5. Cron:
   - run after the refresh pipeline;
   - add a smaller health watchdog every few hours if the user wants fast source-break alerts;
   - prefer `no_agent=True` scripts with empty stdout as silence.

## Photo quality pattern

Distinguish three states clearly:

- primary photo cached locally;
- external photo only;
- no photo/fallback.

For premium galleries, do not overclaim if the current export only has primary images. `582/586 local primary photos` is good UX but not “all photos”. Full galleries usually require per-source detail-page extraction and local caching:

- extract `image_urls[]` from detail pages/source raws;
- cache into `local_image_urls[]`;
- verify image load with `naturalWidth` or equivalent browser QA;
- show `+N photos` or carousel only after gallery data exists.

## Réunion localization pattern

For La Réunion, simple North/South/East/West is not enough. Add a compact local ontology before mapping:

- intercos: CINOR, CIREST, TCO, CIVIS, CASUD;
- communes;
- common aliases and quartiers;
- quality label: high / medium / low, because many listings lack exact address.

Priority Nord / Nord-Est ontology:

- Saint-Denis — CINOR / Nord: Saint-Denis, Sainte-Clotilde, Moufia, Bellepierre, La Bretagne, Bois de Nèfles Sainte-Clotilde.
- Sainte-Marie — CINOR / Nord: Duparc, La Convenance, Beauséjour, Grande Montée.
- Sainte-Suzanne — CINOR / Nord: Quartier Français, Bagatelle, Deux Rives, Bocage.
- Saint-André — CIREST / Est: Cambuston, Champ Borne, Ravine Creuse, centre-ville.
- Bras-Panon — CIREST / Est: Rivière du Mât.
- Saint-Benoît — CIREST / Est: Bras-Fusil, Beaulieu, Sainte-Anne.

Map display rule: if address precision is missing, plot approximate commune/quartier centroid and label precision; do not pretend exact geolocation.

## Opportunity score pattern

Make it explainable and conservative:

- price/m² vs observed median for inferred sector/type;
- photo/local-gallery quality;
- surface-per-room sanity;
- completeness of title/location/rooms/surface;
- duplicate risk;
- warnings for missing fields, strange prices, suspiciously poor data.

UI rule: use a modal/popup opened by `Analyse`; keep the card clean. The modal should answer:

- score / label;
- why this may be interesting;
- what to verify;
- location confidence;
- duplicate/source context.

## QA gates

Minimum before delivery:

- py_compile all new scripts;
- synthetic/history regression tests for listing history, changes, source health, and search alerts;
- run scripts against current `listings.json` and inspect counts;
- public HTTP checks for every new HTML/JSON endpoint;
- browser console = 0 errors on main page and at least one new subpage;
- verify `Analyse` modal opens and contains score/reasons;
- verify cron job state if jobs were created/resumed;
- final report with counts and honest limits.

## Pitfalls

- Do not schedule noisy Telegram alerts on first run; bootstrap `seen` and suppress baseline.
- Do not use a single schema assumption (`rent_eur`, `source_site`, `commune`) if exports have evolved; normalize aliases.
- Do not call primary-photo coverage “premium gallery”. Premium requires multiple local photos where source allows.
- Do not collapse duplicates destructively; dedup starts as signal, not data deletion.
- Do not add map/scoring/source-health panels to the first screen; keep separate pages or a modal.
- Do not trust subagent claims about publication; verify endpoints yourself.
