# Flight scraping RUN — Air Mauritius, Google Flights, Skyscanner reality notes

Date: 2026-06-04

## Why this exists

For flight-price monitoring from La Réunion (RUN), avoid shallowly touching many airline sites. Keep a per-source inventory of what was actually tested, what remains, and the next uncertainty-reducing test.

## Air Mauritius — current technical state

Representative test: RUN → MRU, 18/07/2026 → 25/07/2026, 1 adult.

Actually validated:

- Homepage/form loads with Playwright.
- Origin/destination selection works: `RUN` → `MRU`.
- Datepicker can be driven with DOM labels like `Sat Jul 18 2026` and `Sat Jul 25 2026`.
- Search button redirects to Amadeus DX:
  - `https://booking.airmauritius.com/plnext/AirMauritiusDX/Override.action?...`
- Final page is not results: it is Imperva + hCaptcha with French text `NOUS VOUS PRÉSENTONS NOS EXCUSES POUR CETTE INTERRUPTION...` and incident/IP metadata.

Useful artifact pattern:

- screenshot after search: verify visually that it is hCaptcha/Imperva, not flight results;
- `result.json`: final URL/title/body text;
- `network_events.json`: confirm `Override.action` navigation and challenge resources;
- do not conclude “selector problem” once Override.action is reached.

Implication:

- Air Mauritius is a solved-form / blocked-results target.
- Next real test is challenge handling: clean CDP profile + CapSolver extension/API + possibly residential/mobile proxy.
- Distinguish:
  - CapSolver key present;
  - extension loaded;
  - hCaptcha detected;
  - task actually created/solved;
  - token accepted by Imperva/Air Mauritius.

Probability guidance:

- Playwright-only: low once final Imperva appears.
- CDP + CapSolver on VPS datacenter: medium-low to medium.
- Persistent human-like profile + residential/mobile proxy: materially better.

## Google Flights reality

There is no practical free unlimited official Google Flights API for this workflow.

Options:

- Direct Google Flights scraping: high bot-detection cost; avoid as production target unless specifically researching Google.
- SerpApi `engine=google_flights`: structured and practical, but it is paid scraping-as-a-service / externalized scraping, not official unlimited access.
- If using SerpApi, state quota/cost and whether `SERPAPI_API_KEY` is active; `deep_search=true` can improve parity with browser results at higher latency/cost.

## Skyscanner reality

Skyscanner has an official Travel API, but it is partner/business access, not a public unlimited API.

Options:

- Official Skyscanner Travel API: best if accepted; requires application/established business context.
- Internal web endpoints / HAR replay: possible reconnaissance path, but Cloudflare/fingerprinting can make production unreliable.
- Third-party/RapidAPI wrappers: validate freshness, quota, and result quality before building around them.

Known/community endpoint family seen in recon:

- `skyscanner.net/g/conductor/v1/fps3/search/`

Treat this as HAR/replay research input, not a stable contract.

## Prioritization pattern for RUN flight sources

Prefer finishing one source to a clear state before widening:

1. Source already working end-to-end: stabilize and parameterize.
2. Source with API/XHR replay likely: run HAR capture + curl replay.
3. Source where form works but results hit anti-bot: document and only continue if CapSolver/proxy budget is acceptable.
4. Big protected aggregator/direct site: use for validation, not initial production scraper.

Current terrain ranking from this session:

- French Bee: end-to-end feasible via Amadeus/Override flow; good production candidate.
- Air Austral: strong candidate; existing scripts suggest highest next production ROI.
- IndiGo: worth next reconnaissance for RUN → MAA; likely SPA/API/HAR path, medium odds.
- Air Mauritius: form solved, final anti-bot unresolved.
- Corsair: hard due to Imperva/hCaptcha/page issues.
- Air France: likely hard direct target; prefer community/API/comparator validation before coding.
