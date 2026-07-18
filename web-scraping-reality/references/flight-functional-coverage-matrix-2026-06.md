# Flight scraping functional coverage matrix — RUN project lesson (2026-06)

## Trigger

Use this reference when continuing or auditing flight scrapers, especially when the user challenges whether the work is solid enough for functional/business requirements.

A few successful route/date probes are **not** enough to call a flight scraper robust. They prove technical feasibility, not product coverage.

## Core correction

Before claiming a flight scraping system is solid, build and run a coverage matrix across the dimensions a real user/business request can vary.

**Do not overfit to the user's examples.** When Moufadal gives routes/dates/passenger mixes, treat them as examples of a class unless he explicitly says “only these cases”. Extrapolate the implied product need: robust scrapers for real future use. First inventory all known/local flight sources, then split the work into tracks:

- **Working official sources:** consolidate deeply (broad matrix, edge cases, invalid inputs, artifacts).
- **Working aggregators/fallbacks:** smoke broadly and compare/cohere with official where possible.
- **Fragile/unproven sources:** run bounded classification probes and label `blocked-antibot`, `bug-local`, `not-found-local-script`, or `not-supported` — do not silently omit them.

Coverage axes:

- **OD pairs / airports:** not only RUN→Paris. Include likely RUN routes such as ORY/CDG, MRU, DZA, TNR, JNB, BKK, Mayotte, and French mainland cities when supported.
- **Direction:** outbound from RUN and reverse routes when relevant.
- **Trip type:** one-way, round-trip 7 nights, round-trip 14 nights.
- **Passenger mix:** 1 adult, 2 adults, 2 adults + 1 child, 2 adults + 2/3 children, and at least one infant case if the source supports it.
- **Cabin / fare family:** economy/loisirs, premium, business where the source exposes it; distinguish airline fare families such as BEE LIGHT+/SMART/FLEX from generic aggregator cabins.
- **Stops constraints:** direct only, max 1 stop, cheapest any stops.
- **Business filters:** max duration, overnight tolerance, same-carrier preference, price total vs per-passenger average, baggage/options if in scope.

## Evidence standard

For every case, preserve:

- query parameters: origin, destination, dates, trip type, passenger mix, cabin/filter constraints;
- source and method: official airline, aggregator GraphQL, browser capture, API replay;
- result classification: `price-found`, `no-offer`, `blocked-antibot`, `bug-local`, `not-supported`;
- price signals: total price, per-person average if relevant, fare family/cabin, currency;
- itinerary signals: segment list, direct/stops count, duration, carrier, flight numbers;
- artifacts: stdout/stderr, raw JSON/HTML, screenshot when browser rendered, and a summary report.

Do not call a route/source blocked if the failure is local infrastructure, e.g. an optional SOCKS proxy is down. Rerun direct or mark `bug-local/proxy-prereq`.

## Practical pattern validated

A useful split is:

1. **Inventory first** — before a long `/goal`/auto run, list all local and historical flight sources/scripts/artifacts, not just the ones used in the last successful example. Search for airline names and aggregator names (French Bee, Air Austral, Air Mauritius, Corsair, Kiwi, Kayak, Skyscanner, etc.) and create an explicit `included / not found / deferred` ledger.
2. **Aggregator broad pass** — use Kiwi/Skypicker, Kayak, Skyscanner if present, or equivalent to sweep many dates/passenger mixes quickly. Treat it as market coverage / fallback, not official truth.
3. **Official targeted pass** — validate representative routes and passenger/cabin combinations on French Bee, Air Austral, etc. Official probes are slower and anti-bot sensitive, so run fewer but preserve stronger artifacts.
4. **Coherence check** — compare aggregator vs official only on the same flight/route/date/passenger mix. Quantify EUR/% delta and classify aggregator results as `live exact`, `probably live`, `indicative`, or `non-conclusive`.
5. **Gap report** — explicitly list untested routes, cabins, infants, baggages/options, reverse directions, stop constraints, and sources without a local script.

## Minimum acceptance before saying “robust”

A flight scraper system is not robust until it has a passing campaign like:

- explicit source inventory including official airlines, aggregators/fallbacks, and absent/deferred sources;
- 10–12 OD pairs or a justified smaller route set;
- 4+ passenger mixes including children and one infant case if supported;
- one-way + round-trip variants;
- direct/max-1-stop/any-stop filtering where the source supports it;
- official validation for the routes where official airlines operate;
- aggregator/fallback smoke tests (e.g. Kiwi/Kayak/Skyscanner if local support exists) so broad market coverage is not forgotten;
- a dated `SUMMARY.json` + human-readable `report.md` with pass/fail counts and remaining gaps.

## Pitfalls

- Do not equate `RUN⇄Paris adult works` with business readiness.
- Do not hide missing coverage behind “anti-bot is hard”; classify the missing axis and the next highest-value test.
- Do not let `winners=[]` or empty offers stand without checking whether the date window was invalid, e.g. `last_return < start + nights`.
- Do not lose passenger evidence: include `adults`, `children`, and `infants` in final JSON outputs, not only in raw form data.
- When a proxy is optional and unavailable, rerun with explicit direct mode before calling the target blocked.
