# Kiwi family round-trip GraphQL scan — RUN ⇄ Paris (2026-06)

## Trigger

Use this when the user asks for cheap family flight tickets over a date window, especially Réunion (`RUN`) ⇄ Paris, with passenger mix such as adults + children and a fixed trip length.

## Key finding

Kiwi's browser results page exposes a usable GraphQL request for round trips:

```text
POST https://api.skypicker.com/umbrella/v2/graphql?featureName=SearchReturnItinerariesQuery
```

The one-way `SearchOneWayItinerariesQuery` script is not enough for this task. Capture or reuse a `SearchReturnItinerariesQuery` request, then patch variables.

## Browser URL probe

A working round-trip URL shape observed:

```text
https://www.kiwi.com/en/search/results/reunion-france/paris-france/YYYY-MM-DD/YYYY-MM-DD/
```

Example observed for `2026-06-15` / `2026-06-29`:

```text
https://www.kiwi.com/en/search/results/reunion-france/paris-france/2026-06-15/2026-06-29/
```

This page emitted `SearchReturnItinerariesQuery` and showed return-trip cards. A malformed variant using an underscore (`YYYY-MM-DD_YYYY-MM-DD`) can produce confusing flexible-date behavior; prefer the slash-separated two-date URL.

## Request variables to patch

Patch these fields from the captured request:

```json
{
  "search": {
    "itinerary": {
      "source": {"ids": ["AutonomousTerritory:RE"]},
      "destination": {"ids": ["City:paris_fr"]},
      "outboundDepartureDate": {"start": "YYYY-MM-DDT00:00:00", "end": "YYYY-MM-DDT23:59:59"},
      "inboundDepartureDate": {"start": "YYYY-MM-DDT00:00:00", "end": "YYYY-MM-DDT23:59:59"}
    },
    "passengers": {
      "adults": 2,
      "children": 3,
      "infants": 0,
      "adultsHoldBags": [0, 0],
      "adultsHandBags": [0, 0],
      "childrenHoldBags": [0, 0, 0],
      "childrenHandBags": [0, 0, 0]
    }
  },
  "options": {
    "currency": "eur",
    "locale": "fr",
    "market": "fr",
    "partnerMarket": "fr",
    "sortBy": "PRICE",
    "serverToken": null,
    "searchSessionId": null
  }
}
```

Important: do **not** replay stale `serverToken` or `searchSessionId`; null them before direct replay.

## Response extraction

The response root is:

```text
data.returnItineraries.itineraries[]
```

Useful fields:

- `priceEur.amount` — normalized EUR total for all passengers.
- `price.formattedValue` — display currency; may be non-EUR if the browser guessed another market.
- `duration` — total seconds for both legs.
- `outbound.sectorSegments[].segment` — outbound segments.
- `inbound.sectorSegments[].segment` — return segments.
- `bookingOptions.edges[0].node.bookingUrl` — relative or absolute booking URL.
- `lastAvailable.seatsLeft` — availability hint.

If `bookingUrl` is relative, prefix with `https://www.kiwi.com`.

## Validation pattern

For a result worth showing to the user:

1. Scan the whole requested date window with the patched GraphQL request.
2. Sort by `priceEur.amount`, not by localized display price.
3. Keep total family price and average per person.
4. Preserve direct/stopover info separately for outbound and inbound.
5. Open the best `bookingUrl` in a browser and verify:
   - title matches the route/dates;
   - URL contains `passengers=A-C-I` (e.g. `2-3-0`);
   - body contains the expected itinerary and final displayed price.
6. State limitations clearly: Kiwi price is volatile, bags are not included unless explicitly configured, and this GraphQL passenger shape accepts `children=N` but not detailed child ages in the observed request.

## Session result example

For `RUN ⇄ Paris`, 2 adults + 3 children, 14 nights, departures `2026-06-15` through `2026-07-27` with return no later than `2026-08-10`, the direct GraphQL scan tested 43 dates with 0 API errors. Best observed result:

- Total: `4332.00 EUR` for 5 passengers (`866.40 EUR/person` average).
- Dates: `2026-07-06 → 2026-07-20`.
- Outbound: Air Austral `UU975`, `RUN 19:55 → CDG 05:30 +1`, direct.
- Return: French Bee `BF704`, `ORY 08:00 → RUN 21:05`, direct.
- Booking page validation: title `Saint-Denis - Paris, 6–20 juillet`, URL contained `passengers=2-3-0`, body showed `4 332 €`.

## Pitfalls

- The old legacy `/flights` API may return `404`; do not depend on it.
- Existing one-way Kiwi scripts (`SearchOneWayItinerariesQuery`) are insufficient for family A/R windows.
- Kiwi may render prices in IDR in browser text; use `priceEur.amount` for reporting.
- Date phrase interpretation matters. For “2 semaines entre demain et 10 août”, use a reasonable default and state it: departure tomorrow or later, return 14 days later, return not after 10 August. If that interpretation changes the search materially, label it.
- Same-city Paris airport mixing is common (`CDG` outbound, `ORY` inbound). Call it out explicitly; many users care.
