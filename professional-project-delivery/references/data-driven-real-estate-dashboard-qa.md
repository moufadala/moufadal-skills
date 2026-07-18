# Data-driven real-estate dashboard delivery notes

Use this reference for local/static dashboards built from scraped or database-backed real-estate data.

## Product pattern from the Réunion immo search session

A good deliverable was not just a list of cards. It needed:

- A written acceptance contract before build.
- A generated JSON dataset from the source database.
- A self-contained HTML/JS app.
- Faceted filters with dynamic counts.
- A default search that matches the user's concrete scenario.
- Variant tabs so strict filters do not hide useful nearby options.
- Photo-first cards and a full-size modal/gallery.
- Browser QA with actual DOM interaction and screenshot.

## UX pattern

For property search interfaces, prefer:

- Left-side or sticky filter rail on desktop.
- Search bar + quick chips for priority zones.
- Counts on every facet option.
- Main stats: visible result count, strict match count, variant count.
- Tabs/segments for: strict match, targeted zones, same budget/surface elsewhere, furnished variants.
- Region/sector facets when the geography matters: Nord / Est / Ouest / Sud, commune, granular zone/district. Do not hide the geography only inside a title.
- Cards where the immediate scan fields are: photo, rent, surface, rooms/bedrooms, region, sector/commune, source, and a short description/excerpt.
- A visible “why this appears” or explainable score summary for decision dashboards, e.g. `Nord · zone prioritaire · budget cible · surface confortable`.
- Description quality labels: show source text when available; when missing, generate only a factual synthesis from title + extracted fields and mark it as such. Do not silently present synthesized text as a real source description.
- Click-through modal with large photo, region/sector/source metadata, description, reason/score explanation, and source link.

## QA pitfalls

- If embedded JSON is placed in `<script type="application/json">`, do **not** HTML-escape quotes into `&quot;`; `JSON.parse(el.textContent)` needs raw JSON. Only escape `</` to avoid closing the script tag.
- A page that visually renders a hero but shows `0` cards may still have a silent JS exception; inspect DOM counts and console/runtime state.
- Do not validate a listing dashboard only because HTTP returns 200, the DOM exists, or one browser path loads. For scraped/data-backed search, first prove DB → export JSON → UI scenario counts. If the user doubts results, stop styling and run a deterministic truth audit.
- Mobile UX must be measured, not eyeballed. Record header height, first-card top, first-card height, total scroll height, and whether filters appear before results. A filter rail that is fine on desktop can make mobile unusable if the first result appears after thousands of pixels.
- On mobile, show results first and put filters in a drawer/bottom sheet or collapsible panel. Keep cards compact enough to compare quickly; do not force the user to scroll photos or a huge filter wall before seeing results.
- Vision review can mistake pale/gray interiors for placeholders. Confirm real image loading with `img.complete && img.naturalWidth > 0`.
- External listing photos are fragile product dependencies. Even when URLs exist, hotlink protection, latency, or third-party domains can leave images pending/failed. Cards must remain useful without photos; if photos are product-critical, build a local thumbnail cache/proxy and add `photo_ok/photo_failed` QA. Use `references/static-real-estate-photo-cache.md` for the full implementation pattern.
- Do not confuse “primary photo cached for every listing” with “all gallery photos cached”. If the user asks to “aspirer toutes les photos”, clarify in the artifact/report whether V1 caches the primary card image only or opens detail pages to cache full galleries.
- Filter counts must reflect the result after toggling that option under the current filter state, not a generic unfiltered count.
- Preserve raw DB truth separately from the active presentation set; if the product requires photos, exclude or separate incomplete listings rather than silently injecting dubious fallback images.

## DB/product-data pattern

When the raw scraper DB has enough rows but weak product semantics, do not migrate storage engines first. Keep the raw table as source of truth and add a non-destructive product enrichment layer: normalized commune/zone/region, residential/commercial status + reasons, duplicate key/group/canonical flags, quality score, missing fields, trust flags, and product-facing views. Then make the export consume that layer and add a deterministic DB enrichment audit before browser QA.

## Recommended acceptance checks

- Build command exits 0 and writes HTML + JSON.
- Export count from DB is logged.
- Deterministic truth audit compares source DB rows, exported JSON IDs, duplicate IDs/URLs, required fields, and scenario counts.
- Browser opens the exact public artifact URL the user will use, with cache-bust/reset if the app persists state.
- Mobile viewport QA is run separately from desktop QA; record first result position and filter drawer behavior.
- Clear-all produces the full exported result count.
- Default search result count is non-zero or explicitly explained.
- Text search on a priority zone works.
- Region/commune/sector filters are exercised with at least one non-default case, e.g. clear all → region Sud → search Saint-Pierre → open modal.
- Coverage counts are computed for key product fields: descriptions, description source/synthesis status, region, sector/location label, decision summary.
- A card click opens the modal.
- Cards remain readable when images fail or are pending.
- Visible images have natural dimensions greater than 0; if not, report this as a media reliability blocker and propose local thumbnail caching.
- Console is checked after real interactions, not only on first load.
- Screenshot saved for handoff.
