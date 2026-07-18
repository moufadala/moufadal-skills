# Flight coherence comparisons — RUN routes (2026-06)

Use this reference when the user asks whether aggregators are coherent with official airline prices for Réunion routes.

## User expectation

For aggregator comparisons, do not stop at a minimum price. Push toward the full offer detail:

- all visible offers/prices, not only cheapest;
- airline, flight number, departure/arrival times;
- direct vs stops, stop count and stop airports when available;
- cabin/fare family when visible;
- baggage/conditions when available;
- official vs aggregator price delta in EUR and percent;
- whether the aggregator price is live/bookable or only an indicative/average “à partir de”.

Reports must be compact: short bullets, grouped by route/source, no long narrative unless the user explicitly asks for a full analysis.

## Session findings

### Air Austral official as reference

Air Austral official scraper can serve as source of truth for regional routes.

Validated examples:

- RUN-DZA roundtrip 2026-07-19 → 2026-07-26
  - outbound UU276 RUN→DZA 15:50→17:00 direct 2h10, Loisirs 248.20 EUR
  - return UU277 DZA→RUN 11:10→14:20 direct 2h10, Loisirs 200.75 EUR
  - approx total 448.95 EUR
- RUN-TNR roundtrip 2026-07-19 → 2026-07-26
  - outbound UU611 RUN→TNR 11:00→11:40 direct 1h40, Loisirs 239.34 EUR
  - return UU612 TNR→RUN 12:40→15:05 direct 1h25, Loisirs 331.20 EUR
  - approx total 570.54 EUR

Local workaround discovered: if Air Austral extraction times out at `Page.screenshot`, use or create a no-screenshot variant that extracts HTML/text before attempting screenshots. The problem is local rendering/screenshot overhead, not necessarily source failure.

### Kayak

- RUN-DZA one-way 2026-07-19 matched the Air Austral official flight:
  - UU276 / 15:50→17:00 / direct / 2h10 / 288 EUR on Kayak.
  - Compared to Air Austral official outbound 248.20 EUR: +39.80 EUR, about +16%.
  - Coherent but not identical; quote the delta, do not just say “coherent”.
- RUN-TNR DOM extraction crashed locally (`Locator.inner_text: Target crashed`) with no CAPTCHA/robot signal. For Kayak on heavy pages, prefer API capture (`/i/api/search/dynamic/flights/poll`) over DOM.

### Trip.com

Trip.com route pages are useful as coherence/route intelligence, not source of truth until a live booking API is parsed.

- RUN-DZA page showed title “dès 194 €”, Air Austral “à partir de 226 €”, and schedule UU276 15:50→17:00. Official outbound was 248.20 EUR. Coherent order of magnitude, but likely indicative/average/starting price.
- RUN-TNR page showed Air Austral “à partir de 428 €”, Kenya Airways “à partir de 364 €”, Air Mauritius “à partir de 491 €”, and UU611 schedule. Official Air Austral roundtrip was ~570.54 EUR. Coherent but indicative.

### Kiwi

Kiwi/Skypicker GraphQL is technically strong and can force EUR/FR. In this session it was validated mostly on RUN→Paris, not yet DZA/TNR. Extend carefully for regional routes if route IDs are known/captured.

### French Bee

French Bee official was validated previously for RUN↔ORY/Paris, but the regional DZA/TNR coherence campaign did not compare French Bee. For future Paris tests, explicitly compare French Bee official RUN→ORY against Kiwi/Kayak RUN→ORY/Paris and quote deltas.

### Corsair

User explicitly excluded Corsair from future effort because official Corsair was not validated. If Corsair appears in aggregators, record only as an observed aggregator offer if relevant; do not spend official-site time or use it as a reference.

## Recommended comparison campaign shape

1. Pick multiple dates, not one date only (e.g. 3 weekly windows).
2. Run official sources first:
   - Air Austral: DZA/TNR/MRU/CDG when relevant.
   - French Bee: ORY/Paris only.
3. Run aggregators next:
   - Kiwi direct/GraphQL where route is supported.
   - Kayak API capture, not DOM, for heavy pages.
   - Trip.com as indicative cross-check.
4. Normalize every offer to a common schema:
   - source, route, trip_type, date(s), price_total, currency, airline(s), flight_number(s), departure/arrival, duration, stops, cabin/fare, baggage, booking_url, capture_ts, confidence.
5. Report compactly:
   - route/date;
   - official price;
   - aggregator price;
   - delta EUR and percent;
   - matching flight/hours yes/no;
   - verdict: exact/live, coherent-but-indicative, non-conclusive, blocked.
