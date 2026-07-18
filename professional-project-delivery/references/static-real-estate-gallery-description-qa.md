# Static real-estate app: galleries, descriptions, and trust QA

Use this when turning a scraped real-estate dataset into a static/public dashboard or mobile web app.

## Why this matters

A public URL and correct JSON count do not mean the product is usable. Users evaluate an immo app by:

- whether results match the real database/filter rules;
- whether descriptions are real source descriptions or synthetic placeholders;
- whether photos load reliably;
- whether multi-photo listings can be browsed;
- whether mobile shows results before a wall of filters.

## Acceptance criteria to add

- **DB → JSON → UI truth:** deterministic scenario counts against the DB/export and UI.
- **Description status:** every listing has a visible quality label such as `Description source` or `Synthèse depuis titre + champs`; report counts per source.
- **Photo principal cache:** listing cards use local `/thumbs/...`, not hotlinks, and browser QA verifies `naturalWidth > 0`.
- **Gallery support:** if `local_image_urls.length > 1`, show `+N photos` on the card and modal navigation with `1/N` counter.
- **Mobile first:** first result card should appear quickly in a phone viewport; filter controls should be a drawer/bottom sheet, not a full pre-results wall.

## Implementation pattern

1. Generate/export the app normally.
2. Enrich listings with `image_urls[]` from raw source payloads, selecting the exact listing record first.
3. Cache all image URLs locally and patch:
   - `local_image_url`
   - `local_image_urls[]`
   - `photo_cached`
4. Patch both external JSON (`listings.json`) and embedded JSON in `index.html`, if present.
5. Add UI:
   - card badge `+N photos`;
   - modal photo arrows;
   - counter `1/N`;
   - keyboard/mobile next/prev.
6. QA in browser:
   - open a multi-photo listing;
   - click next;
   - assert image URL changed, counter changed, and image loaded;
   - capture screenshot.

## Important pitfall

Do not scan a whole raw SERP JSON and attach all image URLs to every listing. Select the exact listing object by source ID or canonical URL first. Otherwise you create fake galleries with unrelated photos.

## Reporting language

Be precise:

- “Photo principale locale: 495/495”
- “Galeries locales >1 photo: 15 listings”
- “Description source: 152; synthetic summaries: 343”
- “Source X details blocked by DataDome 403; needs CDP/HAR/proxy phase”

Do not say “all photos/descriptions fixed” unless both gallery and description-source gates pass.
