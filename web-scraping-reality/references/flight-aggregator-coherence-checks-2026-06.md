# Flight aggregator coherence checks — RUN routes (2026-06)

Use when validating flight aggregators against official airline sources for Réunion routes. Goal: determine whether aggregator prices are directionally reliable, not just whether the scraper runs.

## Workflow correction from user

Do not keep expanding to new sites once Kiwi/Kayak work. For route monitoring, validate **coherence**:

1. Pick routes tied to a known official carrier.
   - Air Austral: RUN→DZA (Mayotte), RUN→TNR (Antananarivo), RUN→MRU, sometimes RUN→CDG.
   - French Bee: RUN↔ORY/Paris.
   - Do **not** use Corsair official as a reference until its official site is solved end-to-end; if it appears in aggregators, treat it as observed aggregator data only.
2. Query aggregators for the same route/date.
3. Query official carrier for comparable one-way or round-trip dates.
4. Compare order of magnitude and carrier/flight number, not just absolute lowest price.
5. Mark suspicious cases explicitly: static route page, cached price, sponsored ad, different cabin/baggage, one-way vs round-trip mismatch.

## Validated local patterns

### Kiwi / Skypicker GraphQL

- Browser discovery revealed `POST https://api.skypicker.com/umbrella/v2/graphql?featureName=SearchOneWayItinerariesQuery`.
- Original request can come back with wrong market/currency, e.g. `currency: idr`, `market: id`.
- Replaying the captured GraphQL request directly with:
  - `currency: eur`
  - `market: fr`
  - `partnerMarket: fr`
  - `locale: fr`
  returned clean EUR results without browser.
- Response structure: `data.onewayItineraries.metadata.topResults`, `data.onewayItineraries.itineraries[].sector.sectorSegments[].segment`.
- Extract: price, `priceEur`, duration, source/destination station codes, local times, carrier code/name, flight number, cabin, booking URL.

### Kayak / Momondo family

- Direct URLs can work:
  - Kayak: `https://www.kayak.fr/flights/RUN-DZA/2026-07-19?sort=bestflight_a`
  - Momondo: `https://www.momondo.fr/flight-search/RUN-CDG/2026-07-19?sort=bestflight_a`
- Both expose similar endpoints:
  - `/i/api/search/dynamic/flights/poll`
  - `/a/api/display/V1/flights/list?searchId=...`
  - `/i/api/xsell/v1/results`
- Browser/DOM and screenshot may crash on heavy pages. Prefer response-body capture of `/flights/poll`; do extraction before screenshot and make screenshots optional.
- For RUN→DZA one-way, Kayak showed Air Austral direct `15:50–17:00`, 2h10, `288 €`; official Air Austral outbound same date showed `UU276`, `248,20 €`, coherent (+~40 €).

### Trip.com route pages

- Static route pages can be useful for route/price sanity checks:
  - `https://fr.trip.com/flights/airport-run-cdg/`
- Accessible without CAPTCHA in tests; page exposed EUR route-level prices, carrier list, and schedule snippets.
- Endpoints observed:
  - `/restapi/soa2/21273/GetRouteInfo`
  - `/restapi/soa2/27147/run`
  - `/restapi/soa2/14571/getCityByIp`
- Treat Trip.com route pages as indicative unless an endpoint replay returns live offer details for the exact date.

## Official Air Austral comparison pattern

Existing script pattern: `airaustral_price_check.py ORIGIN DEST YYYY-MM-DD YYYY-MM-DD`.

Important fix: screenshot timeouts are local tooling failures, not necessarily site failures. Use a no-screenshot variant or extract body text before screenshot.

Validated examples:

- RUN→DZA, 2026-07-19/2026-07-26 official Air Austral:
  - outbound `UU276`, `15:50–17:00`, 2h10, `248,20 €`
  - return `UU277`, `11:10–14:20`, 2h10, `200,75 €`
  - approximate RT: `448,95 €`
- RUN→TNR, 2026-07-19/2026-07-26 official Air Austral:
  - outbound `UU611`, `11:00–11:40`, 1h40, `239,34 €`
  - return `UU612`, `12:40–15:05`, 1h25, `331,20 €`
  - approximate RT: `570,54 €`

## Reporting style for this user

During long scraping runs, give short progress updates: site/route, process id if relevant, artifact paths, and distinguish clearly:

- site blocking: CAPTCHA/robot/Cloudflare/403;
- local tooling issue: Chromium crash, screenshot timeout, Playwright route handler bug;
- data quality issue: cached/static price, sponsored listing, wrong currency, different cabin.

When the user says a source is out of scope (e.g. Corsair), remove it from the comparison immediately instead of continuing to mention or test it.