# Static real-estate clean portal reboot V1

Use when a scraper-backed real-estate dashboard has become cluttered/buggy and the user asks to restart from a classic property-search experience over the existing scraped DB.

## Trigger

- User calls the current app a `fouillis`, says it bugs, or wants to “partir depuis le début”.
- Goal is not a new scraper first; goal is a usable search portal over the already-scraped listings.
- Existing app exposes source/debug/suspect/internal state too prominently.

## Product stance

Do not keep adding tabs to the old dashboard. Build a small clean V1 in a parallel workspace and publish reversibly.

Default V1 contract:
- search-first page, like a normal property portal;
- first-level filters: location, budget, type, surface/rooms, sort/region if useful;
- photo-first cards with clean fallback;
- detail modal/page with description, metadata, and source link;
- save/favorite/hide can be localStorage-only;
- no debug/source-health/suspect internals on the landing screen;
- galleries only if multi-photo extraction/cache is proved; otherwise state “primary photo only”.

## Data audit before build

From the public/static export, measure:
- listing count;
- field coverage: city/commune, region, type, price, surface, rooms, bedrooms, description, source URL;
- primary photo coverage and local cache coverage separately;
- gallery coverage (`image_urls[]`, `local_image_urls[]`) separately;
- source distribution if useful, but keep it out of the main consumer UI.

For the Reunion immo stack, local thumbnails may be named from `sha256(image_url)` prefixes. If `listings.json` has `image_url` but no `local_image_url`, try matching `sha256(url)[:24|32|40|64] + .jpg/.jpeg/.webp/.png` against `artifacts/app/thumbs/` before concluding the photo cache is absent.

## Implementation pattern

- Create a separate output directory such as `artifacts/app_clean_v1/` rather than editing the existing app in place.
- Copy/reuse thumbnail assets into that directory.
- Export a simplified `listings.json` for the consumer UI; leave raw fields and QA/debug fields in the old/admin artifacts.
- Add `coverage.json` or a QA note with data counts and photo limits.
- Treat missing local primary photos as a normal product state: use external source image if present, then a clean visual fallback if it fails.
- Add query token expansion for common property shorthand: `T2` should also match `2`, `2 pièces`, `2 p.`; `Saint-Denis T2` should not require the exact phrase.

## Reversible publication

Before switching the public container:
- back up the previous app directory with a timestamp;
- publish the clean app by overriding the static app directory/env (`HERMES_APP_DIR` and Docker host path equivalent if the local stack uses host-mounted volumes);
- keep the old source app/artifact path untouched for rollback.

## QA gates

Minimum gates before saying “ça marche”:
- HTTP public URL returns the new clean HTML, not the old dashboard;
- public `listings.json` count equals expected export count;
- canonical and compatibility hostnames work, with IPv4 forced when a known stale/bad AAAA exists;
- browser title and visible counters match the export;
- search example such as `Saint-Denis T2` returns non-zero relevant results;
- filters combine correctly, e.g. budget max + surface min;
- detail modal opens and source URL is present;
- console has zero JS errors after interactions;
- mobile viewport/visual check has no blocking overlap/illegible layout;
- photo QA reports primary-local, primary-external, and fallback-needed counts separately.

## Reporting

Final response should be compact and honest:
- URL(s);
- what changed in product terms;
- exact data counts;
- QA proof;
- rollback/backup path;
- remaining limitation: primary-photo cache and galleries are separate problems, not solved by a clean UI alone.
