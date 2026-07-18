# Flight aggregators RUN — Kayak/Kiwi/Trip.com terrain notes (2026-06)

Session context: flight-price scraping from Réunion (`RUN`) toward Paris (`ORY/CDG`) and regional destinations where direct airline sites were mixed or anti-bot heavy. User preference during this class of task: keep short progress updates during long Playwright/background runs and separate **site blocking** from **local tooling bugs**. Important workflow correction from user: once an aggregator works technically, do **coherence checks against official airline sources** before trusting the prices.

## Core lesson

For flight aggregators, do not stop at DOM scraping if a results page loads. Capture XHR/fetch and prefer direct API/GraphQL replay when possible.

Recommended order for aggregators:
1. Generate/open a structured results URL.
2. Accept cookies once.
3. Capture network while waiting for results.
4. Identify poll/search endpoints.
5. Save response bodies, not only URLs.
6. Build a direct API parser if replay works.
7. Use screenshots only as proof; avoid making screenshot success a dependency for extraction.
8. Validate price coherence against official airline sources on routes the airline actually serves.

## Coherence-validation workflow

When the goal is a reliable flight-price monitor, do not keep adding aggregators indefinitely after one or two work. Instead:

1. Pick routes that belong naturally to known carriers:
   - Air Austral: `RUN-DZA` (Mayotte), `RUN-TNR` (Madagascar/Antananarivo), also `RUN-CDG` where relevant.
   - French Bee: primarily `RUN-ORY` / Paris routes.
   - Corsair: primarily `RUN-ORY` / Paris routes, but often anti-bot heavy on official site.
2. Query aggregators for the same route/date/date-window.
3. Query official carrier scripts/pages for the matching route/date/date-window.
4. Compare:
   - cheapest aggregator price vs official price;
   - carrier shown by aggregator;
   - one-way vs round-trip mismatch;
   - live price vs SEO/static historical/average price;
   - suspiciously low values that may be monthly statistics rather than bookable fares.
5. Classify each source per route:
   - `live/bookable-looking`, `static SEO estimate`, `carrier filter/aggregate`, `blocked`, `no result`, `incoherent`.

Use this before declaring an aggregator “trusted”. A scraper can be technically successful and still commercially unreliable.

## Kayak pattern

Validated direct URL examples:

```text
https://www.kayak.fr/flights/RUN-ORY/2026-07-12/2026-07-18?sort=bestflight_a
https://www.kayak.fr/flights/RUN-CDG/2026-07-12/2026-07-18?sort=bestflight_a
```

Observed endpoints:

```text
POST https://www.kayak.fr/i/api/search/dynamic/flights/poll
GET  https://www.kayak.fr/a/api/display/V1/flights/list?searchId=...
POST https://www.kayak.fr/i/api/xsell/v1/results
POST https://www.kayak.fr/s/horizon/flights/results/GetFlightPriceAlertDriveByAction
```

The `/i/api/search/dynamic/flights/poll` response contained multi-MB JSON with:
- `tripId`
- `price`, `currency`, `localizedPrice`
- leg/segment IDs
- approximate departure/arrival times
- fare/baggage/refund details

Examples seen for `RUN-CDG` round-trip July 2026:
- Air France around `1 037–1 057 €`
- Air Austral around `1 127 €`
- Air Mauritius around `1 152 €`
- Corsair around `1 324 €`
- lower filter/global prices around `919–957 €`

Pitfalls:
- Kayak pages are heavy; Chromium can crash during `page.screenshot()` or `body.inner_text()` even after network success.
- Treat `Target crashed` at screenshot/DOM extraction as a **local tooling/resource problem**, not a site block.
- Capture API response bodies before screenshots/DOM extraction.
- Store complete bodies; truncating at 2 MB may cut valid JSON.

## Momondo pattern

Momondo is effectively Kayak-family/r9cdn terrain.

Validated direct URL shape:

```text
https://www.momondo.fr/flight-search/RUN-CDG/2026-07-19?sort=bestflight_a
```

Observed endpoints mirror Kayak:

```text
POST https://www.momondo.fr/i/api/search/dynamic/flights/poll
GET  https://www.momondo.fr/a/api/display/V1/flights/list?searchId=...
POST https://www.momondo.fr/i/api/xsell/v1/results
POST https://www.momondo.fr/s/horizon/flights/results/FlightDateGraphsAction
POST https://www.momondo.fr/s/horizon/flights/results/GetFlightPriceAlertDriveByAction
```

Use Momondo as a secondary corroboration source, not a totally independent source from Kayak. Same crash/resource pitfalls apply.

## Kiwi / Skypicker GraphQL pattern

For family round-trip scans (e.g. 2 adults + children over a date window), use the dedicated note `references/kiwi-family-roundtrip-graphql-2026-06.md`: capture/replay `SearchReturnItinerariesQuery`, patch `passengers`, null stale session tokens, sort by `priceEur.amount`, and validate the booking URL in browser.

Validated results URL example:

```text
https://www.kiwi.com/en/search/results/reunion-france/paris-france/2026-07-19/no-return/
```

Observed endpoint:

```text
POST https://api.skypicker.com/umbrella/v2/graphql?featureName=SearchOneWayItinerariesQuery
```

Also observed:

```text
RecentSearchesQuery
useQuickNavPricesQuery
```

The browser-loaded Kiwi page may choose a surprising market/currency, e.g.:

```json
"options": {
  "currency": "idr",
  "market": "id",
  "partnerMarket": "id",
  "locale": "en"
}
```

Direct replay works by patching variables before POST:

```json
"options": {
  "currency": "eur",
  "market": "fr",
  "partnerMarket": "fr",
  "locale": "fr"
}
```

Validated one-way `Réunion -> Paris`, `2026-07-19`, EUR/FR:
- Cheapest: `368 €`, `11h55`, Corsair `SS711`, `RUN -> ORY`, direct
- Best: `370 €`, `11h35`, Air Austral `UU971`/`UU975`, `RUN -> CDG`, direct
- Fastest: `382 €`, `11h20`, French Bee `BF705`, `RUN -> ORY`, direct
- Further examples: Air France `AF643/AF647` around `572 €`

Relevant fields in GraphQL response:
- `data.onewayItineraries.metadata.topResults.{best,cheapest,fastest}`
- `data.onewayItineraries.itineraries[]`
- itinerary fields: `price.formattedValue`, `price.amount`, `priceEur.amount`, `duration`, `sector.sectorSegments[]`
- segment fields: `source.station.code`, `destination.station.code`, `source.localTime`, `destination.localTime`, `carrier.name`, `carrier.code`, `code`, `cabinClass`
- `bookingOptions.edges[0].node.bookingUrl` can be made absolute with `https://www.kiwi.com`.

## Trip.com pattern

Trip.com is a useful corroboration/SEO-data source for RUN routes, but distinguish static route intelligence from live bookable fares.

Validated route URL shape:

```text
https://fr.trip.com/flights/airport-run-cdg/
https://fr.trip.com/flights/airport-run-dza/
https://fr.trip.com/flights/airport-run-tnr/
```

Observed accessible page for `RUN-CDG`:
- title: `... dès 341 € | Trip.com`
- no CAPTCHA/robot wall in the tested run;
- visible route metadata, monthly/day-of-week statistics, recommended carriers, direct flight schedule.

Example visible fields for `RUN-CDG`:
- Air Austral from `341 €`
- Air France from `542 €`
- Air Mauritius from `574 €`
- Corsair International from `904 €`
- schedule example `UU975`, `RUN -> CDG`, `19:55 -> 05:30`, `11 h 35 m`
- page also showed `Vol aller le moins cher` and `Billet aller-retour le moins cher` fields.

Observed APIs:

```text
POST https://fr.trip.com/restapi/soa2/21273/GetRouteInfo
POST https://fr.trip.com/restapi/soa2/27147/run
POST https://fr.trip.com/restapi/soa2/14571/getCityByIp
POST https://fr.trip.com/restapi/soa2/24884/json/getConfiguration
POST https://www.trip.com/restapi/soa2/18088/getAppConfig.json
```

Pitfall: Trip.com route pages can expose estimated or historical route statistics (“prices based on average/latest Trip.com data”) rather than current bookable fare quotes. Treat as a candidate/coherence signal until `/GetRouteInfo` or booking-search API responses are parsed and matched to dates.

## Expedia pattern

Tested `https://www.expedia.fr/Vols` returned a robot challenge page:

```text
Robot ou pas robot ?
Vous êtes humain, n’est-ce pas ?
Nous ne sommes pas sûrs que vous soyez un humain ou un robot.
```

Classify Expedia as low priority unless a different access path or human/HAR capture is available.

### Local fallback validated 2026-06-11

If `/opt/data/scripts/kiwi_direct_search.py` fails because the historical template capture is missing (`kiwi_api_capture_20260604/.../result.json`), use the live network-capture fallback instead of stopping:

```bash
python3 /opt/data/scripts/kiwi_capture_live.py --date 2026-07-19 --out-dir /opt/data/artifacts/.../kiwi_capture
```

This opens the Kiwi results URL, captures `SearchOneWayItinerariesQuery` responses, stores `captures.json`/`result.json`, and extracts `price_eur`, carriers, flights, duration. In the 2026-06-11 run, the page returned IDR formatted prices but valid `priceEur` fields, so report EUR from `price_eur` when `price_formatted` is non-EUR.

## Progress reporting pattern for the user

For long scraping runs:
- **Do not block the Telegram line.** If the run is multi-site, anti-bot/browser-heavy, or likely >30–60s, launch it as a background process with `notify_on_complete=true` (or a bounded parallel runner) before deep analysis. The user may keep sending steering messages while it runs.
- Start message: what is being tested, route/date, script path, PID/session ID if backgrounded.
- Progress messages: short, factual, no long explanations.
- Run independent targets in parallel when safe; write per-target stdout/stderr/status files under one artifact directory, then summarize after completion.
- On failure: state whether it is site-side (`CAPTCHA`, `403`, robot page) or local tooling (`Target crashed`, Playwright route bug, resource pressure, artifact write permissions).
- On success: list artifact paths and the concrete extracted values.
- When the user says “tiens-moi au courant” or corrects that the conversation line is being blocked, immediately switch to background/parallel execution and acknowledge the session ID.

## Mobile airline reconnaissance addendum (2026-06-14)

When the user asks whether mobile airline sites may be easier, test them — but distinguish **API discovery** from **price extraction**.

Observed RUN⇄Paris mobile probe:

- French Bee mobile/home: `curl` with iPhone UA returned 200 on `https://www.frenchbee.com/fr`, but Playwright mobile hit `ERR_HTTP2_PROTOCOL_ERROR`; treat as tooling/protocol issue, not proven site block. Current robust path remains `frenchbee_solver.py` (Drupal form → Amadeus `Override.action` → headful render).
- Air Austral mobile: `https://m.air-austral.com/` returned the same Cloudflare Turnstile 403 as desktop from VPS; mobile does **not** bypass Cloudflare locally.
- Kiwi mobile: still GraphQL (`api.skypicker.com/umbrella/v2/graphql`) and useful as OTA benchmark, not official airline source.
- Corsair mobile: high-value discovery path. `https://www.flycorsair.com/fr?fsopen=true` exposes a mobile form and public bundle with IBE aliases `ORI`, `DES`, `DEP`, `RET`, `TRIP`, `CABIN`, `ADT`, `CHD`, `INF`, `APPSMOBILE`, `IS_PRICE_ALL_PASSENGER`, plus endpoints `https://vols.corsair.fr/Booking/Research`, `https://vols.flycorsair.com/?TRIP=J`, `https://mybooking.corsair.fr/plnext/corsair_DX/Override.action`, `FlexPricerAvailability`. A direct family URL like `https://vols.flycorsair.com/Booking/Research?ORI=RUN&DES=ORY&DEP=20260714&RET=20260728&TRIP=R&CABIN=eco&ADT=2&CHD=3&INF=0&CLT=fr&SC=FALSE&APPSMOBILE=TRUE&IS_PRICE_ALL_PASSENGER=TRUE` reaches the booking host but returns an Incapsula resource shell; needs human/agent HAR after challenge or browser with valid session.
- Air France mobile: local probe inconclusive (`ERR_HTTP2_PROTOCOL_ERROR` / timeout); lower priority until a real HAR is available.

Artifacts from the probe live under `/opt/data/artifacts/flight-search-family-test/mobile_probe/20260614T062506Z/` and `/opt/data/artifacts/flight-search-family-test/corsair_mobile_ibe/20260614T062844Z/`.

## Durable takeaway

For RUN flight monitoring, Kiwi GraphQL direct is currently the cleanest class of source when available: no browser, EUR can be forced, structured JSON. Kayak is a strong secondary source but needs browser-assisted capture or careful replay of heavier internal poll JSON. Momondo is useful but not independent from Kayak. Trip.com is promising for route/carrier/price intelligence and REST endpoints, but must be coherence-checked against official carrier results before being treated as live pricing truth. For official airline mobile paths, Corsair mobile is the strongest next target for HAR/API discovery; Air Austral mobile remains Cloudflare-blocked from VPS; French Bee official headful remains the most reliable live official price source.
