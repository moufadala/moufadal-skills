# Real-estate scraper app gates: DB truth, photos, galleries, descriptions

Use this reference when a scraped real-estate dataset is published as a user-facing app/dashboard. It captures a session lesson: HTTP/DB scraping success is not enough; the user judges the product by mobile UX, result trust, photos, descriptions, and gallery behavior.

## Non-negotiable gates before saying “it works”

1. **Truth chain audit**
   - Compare source DB rows → exported JSON rows → UI filter counts.
   - Write a deterministic audit script with scenario counts: clear-all, default search, key communes/zones, budget/surface combos.
   - If results look sparse, distinguish: data coverage issue vs restrictive default filters vs UI hiding the logic.

2. **Mobile-first dogfood**
   - Use a real phone viewport measurement.
   - Record: first result card top offset, card height, filter panel height, JS console errors, screenshot.
   - Result cards must appear quickly; do not put a full filter wall before the first listing on mobile.
   - Preferred pattern: results first + visible count + filter bottom sheet/drawer + compact cards.

3. **Photo gate**
   - Hotlinked photos from portals are not reliable enough for a serious dashboard.
   - Build a local photo cache under the static app (e.g. `/thumbs/`) and patch each listing with `local_image_url`.
   - Validate image content type, minimum size, HTTP status, and final browser load.
   - If the app embeds data in HTML as well as serving `listings.json`, patch both; otherwise browser UI may still use stale external URLs.
   - Prefer `loading="eager"` for the small initial result set when lazy loading gives false pending images in mobile/browser QA.

4. **Gallery gate**
   - Users expect to navigate 2–3+ photos when available, like real estate sites.
   - Extract `image_urls[]` from raw source payloads where available; cache into `local_image_urls[]`.
   - Add UI affordances: card badge `+N photos`, modal/gallery arrows, counter `1/N`, keyboard/mobile navigation.
   - QA must prove image changed, counter changed, and new local image loaded.

5. **Description quality gate**
   - Track `description_status`: e.g. `Description source` vs `Synthèse depuis titre + champs`.
   - Do not imply all descriptions are source-quality if many are generated summaries.
   - Report per source: count with real descriptions vs synthetic summaries.

## Pitfalls from the session

- **Do not scan aggregate raw files blindly.** Some sources store a whole SERP/page raw JSON for many listings. If you walk all image URLs in that file and attach them to one listing, you create bogus 100+ photo galleries. First select the exact listing object by source ID or canonical URL, then extract images.
- **Patch embedded data too.** Static apps may have both `listings.json` and `<script id="embeddedData">…</script>`. After post-processing JSON for local images/galleries, update the embedded JSON or rebuild in the correct order.
- **Photo principal ≠ galerie.** `495/495 listings have a local principal photo` is not the same as “all galleries are complete.” Say exactly what was cached: principal images only, or multi-photo galleries where available.
- **Anti-bot detail pages remain separate work.** If a portal listing detail returns DataDome/403 while SERP/listing data was partially collected, classify description/gallery enrichment for that source as a dedicated CDP/HAR/mobile-proxy phase, not as done.

## Suggested artifact set

- `tests/audit_filters.py` — DB/export/UI truth scenario counts.
- `scripts/cache_listing_images.py` — idempotent local image cache + manifest + embedded JSON patch.
- `scripts/enrich_listing_galleries.py` — exact-record raw extraction into `image_urls[]`.
- `artifacts/photo-cache-report.md` — URL counts, success/fail reasons, cache size.
- `artifacts/gallery-report.md` — multi-photo listing counts by source and QA scenario.
- Browser screenshot showing mobile modal with gallery counter and source description.

## Report wording

Use precise claims:

- “Photo principale locale: 495/495”
- “Galeries locales >1 photo: 15 listings, source: Bien’ici”
- “Description source: 152; synthèse: 343”
- “Seloger detail enrichment blocked by DataDome 403; needs CDP/HAR/proxy-mobile phase”

Avoid vague claims like “all photos/descriptions are fixed” unless gallery and source-description gates are actually satisfied.
