# Real-estate portal clean UX reboot

Use this reference when a real-estate dashboard/listing app becomes cluttered, over-personalized, or technically impressive but not usable.

## Trigger signals

- User says the app is a “fouillis”, “not usable”, or “only 40% usable”.
- UI has many tabs/chips/debug states/special filters visible at first level.
- The product started from a custom personal search and drifted away from standard real-estate portal expectations.
- The user asks to “forget my personalized search” and rebuild like the best property sites.

## Correction

Do not keep patching the existing clutter. Treat it as a product-direction failure, not a missing-button failure.

1. **Stop feature stacking.** Archive/snapshot the current public artifact before broad replacement.
2. **Research/benchmark first.** Check current real-estate UX patterns (Zillow/Redfin/Realtor, Airbnb card patterns, SeLoger/Bien’ici/Leboncoin conventions, mobile property search best practices).
3. **Write a clean product contract before coding.** Explicitly say what is first-level vs secondary.
4. **Reboot in a clean workspace** when the old implementation is structurally confused. React/Vite is justified when the app needs real client state: filters, favorites, hidden items, detail modal, sharing, saved state.
5. **Keep data, simplify presentation.** Preserve source listings and rollback path, but do not expose scraper/debug concepts as primary navigation.

## Default clean real-estate UX contract

First-level UI should be limited to:

- Search bar: city, district, property keyword.
- Four essential filters: location, budget, type, surface/rooms.
- Sorting: recommended, price, surface, recent.
- Photo-first cards: price, location, surface, rooms/bedrooms, source, main image.
- Actions: save/favorite, hide, share/copy, source link.
- Detail modal/page: gallery, description, trust/missing fields, similar/duplicate hints, original URL.

Do **not** put these at first level by default:

- 10+ tabs.
- Custom personal preference logic.
- Scraper/debug labels.
- Suspect/excluded lists as primary navigation.
- Scoring details unless they are explainable and useful to the seeker.
- Excessive chips/filters.

## Data handling lessons

- Normalize city/commune labels before exposing them as location filter options. Avoid raw postal codes, room labels, source titles, or listing fragments as filter choices.
- Keep suspect/commercial/excluded counts for transparency, but place them as secondary information unless the user explicitly wants an audit view.
- If replacing a static public directory with a Vite build, keep a timestamped backup of the previous `artifacts/app` and record rollback commands.
- If the Vite public build needs JSON/images from the old app, copy them into the new app’s `public/` directory before build and verify public `/data.json` from both canonical URLs.

## QA acceptance

Minimum proof before saying it is better:

- `npm run build` passes.
- Public canonical URL loads the new title/H1, not the old app.
- `/data.json` returns expected listing counts from canonical and alternate host.
- Browser console has no JS errors after interactions.
- Browser interaction test covers search/chip/filter drawer, save, hide, detail modal/source.
- Mobile screenshot shows a simple real-estate portal, not a debug dashboard.
- Final handoff includes backup/rollback path and honest limits (no map, localStorage-only favorites, imperfect source data, etc.).
