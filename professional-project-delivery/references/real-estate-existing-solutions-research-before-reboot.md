# Real-estate existing-solutions research before rebuilding

Use this reference when Moufadal challenges a messy immo dashboard/portal and asks to check whether the thing already exists in repos, communities, GitHub, or open source before rebuilding.

## Trigger signals

- “Fais une grosse recherche avant.”
- “Quelqu’un a déjà fait ça.”
- “Regarde les repos, communautés, GitHub.”
- Current immo UI is called a “fouillis” and the desired direction is a classic portal/search experience over scraped data.

## Required sequence

1. **Acknowledge the correction and stop coding.** The next step is research/validation, not another UI patch.
2. **Search by families, not by one exact phrase:**
   - classic real-estate portal/listing/search UIs;
   - scraper/aggregator/notifier projects;
   - structured extraction/detail/photo tools;
   - topic/community inventories.
3. **Use GitHub and web together:**
   - `gh search repos "real estate"`, `"real-estate"`, `"property listings"`, `"zillow clone"`, `"real estate scraper"`, `"immobilier scraper"`, `"seloger scraper"`, `"bienici scraper"`;
   - `gh search code` for concrete implementation terms such as `PropertyCard`, `saved search`, `favorites`, `SeLoger scraper`, `image management`;
   - web extraction for README summaries and GitHub topic pages.
4. **Separate project classes:**
   - UI portals / listing apps: useful for UX and feature conventions;
   - aggregators/notifiers: useful for architecture, jobs, dedupe, alerts;
   - extraction tools: useful for detail pages, photos, normalized fields;
   - full platforms: useful but often too heavy for V1.
5. **Evaluate reuse honestly:** do not recommend cloning a popular repo just because it has stars. Check maturity, license, data source assumptions, paid APIs, geography, framework debt, and whether it solves scraped-data ingestion.
6. **Write a compact durable research artifact** under `/opt/data/artifacts/...md` with links, stars/license where available, useful ideas, limits, and a recommendation.
7. **Translate research into a V1 contract:** classic search-first portal over our DB, not a cluttered debug dashboard.

## Strong patterns found in prior research

- `orangecoding/fredy`: self-hosted real-estate finder, multi-provider jobs, dedupe, Web UI, Telegram/Slack/email/Discord/ntfy notifications. Excellent architecture reference for search jobs and alerts, but Germany-focused and not a photo-first public portal.
- `flathunters/flathunter`: rental search bot with Telegram/Slack and Selenium/browser scraping. Good alerting pattern; AGPL license requires caution.
- `DEENUU1/property-aggregator`: FastAPI + scraper CLI + PostgreSQL + Celery/Redis, favorites, saved filters, notifications, tests. Strong backend architecture analogue, but geography/source-specific and heavier than a simple V1.
- `bradtraversy/property-pulse`: Next.js rental listing/search app with bookmarks, sharing, gallery, responsive UX. Good product/UI reference, but generic/tutorial stack.
- `RealEstateWebTools/property_web_scraper`: structured extraction from rendered HTML with many portal mappings including SeLoger; useful for enrichment if we can supply rendered HTML. It is not a JS renderer by itself.
- `PropertyWebBuilder`: mature Rails real-estate website builder; useful as a reference, usually too heavy to adopt for a focused V1.

## Recommended conclusion pattern

Say explicitly:

- “Oui, ça existe déjà en morceaux.”
- “Je ne recommande pas de cloner un repo entier.”
- “On doit reprendre les patterns prouvés: portail classique pour l’UX, aggregator/notifier pour l’architecture, extraction tool pour détails/photos, notre DB comme source de vérité.”

## V1 product contract after research

- One clean search screen.
- First-level filters only: location/sector, budget, type, surface/rooms.
- Sort: recommended, price, surface, recent.
- Photo-first cards: price, location, surface, rooms/bedrooms, source, primary image.
- Actions: save/favorite, hide, share/copy, source link.
- Detail modal: gallery only if actually available, source description if present, missing fields clearly labeled.
- No scraper/debug/suspect internals on the first screen.
- Be explicit about photo scope: primary thumbnail vs full gallery.

## Pitfalls

- Do not keep patching a cluttered dashboard after Moufadal asks for a classic portal reboot.
- Do not treat repo stars as product fit.
- Do not silently import license risk such as AGPL.
- Do not promise “all photos” when the scraper only has primary images or hotlinked URLs.
- Do not jump to a heavyweight Rails/Next/Postgres clone when the immediate need is a V1 that works over the existing scraped DB/export.
