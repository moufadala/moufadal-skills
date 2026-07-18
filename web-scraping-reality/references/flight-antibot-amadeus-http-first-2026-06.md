# Flight anti-bot / Amadeus HTTP-first notes — 2026-06

Use this when scraping airline booking flows from Réunion or similar Amadeus-backed sites.

## Core lesson

Do not treat all airline failures as the same browser/CAPTCHA problem. Split by the actual gate:

- CMS/Drupal/front site reachable but browser errors: try HTTP-first with TLS impersonation (`curl_cffi`) before more Playwright.
- Amadeus `plnext/.../Preload.action` or `Override.action` present: the winning path is often a POST on the airline front-end that generates a dynamic `ENC`, then a second request to Amadeus.
- Final `Pardon Our Interruption` usually means Akamai/Amadeus reputation/fingerprint gate, not a bad form payload.

## French Bee validated pattern

Scripts from the session:

- `/opt/data/scripts/frenchbee_http_first_probe.py`
- `/opt/data/scripts/frenchbee_parse_amadeus_forms_full.py`
- `/opt/data/scripts/frenchbee_post_replay.py`

Observed flow:

1. Playwright/Chromium showed `ERR_HTTP2_PROTOCOL_ERROR`; disabling HTTP/2 only produced timeout.
2. `curl_cffi` with Chrome impersonation fetched `https://re.frenchbee.com/fr/vol-reservation` successfully.
3. Parse form `amadeus-form-search-flights-page`.
4. POST fields such as:
   - `search_flights_from=RUN`
   - `search_flights_to=ORY`
   - `search_flights_travel_type=R`
   - `search_flights_departure_date=18/07/2026`
   - `search_flights_return_date=25/07/2026`
   - passenger counts + hidden `form_build_id`, `form_id`, language fields from the fresh GET.
5. The front site returned HTTP 302 to:
   - `https://vols.frenchbee.com/plnext/bf-dx/Override.action?...&ENC=...`
6. Following the Amadeus URL returned `Pardon Our Interruption`.

Verdict: payload generation was solved; remaining issue is the final Amadeus/Akamai gate. Next tests should reuse exact cookies/headers/referrer from GET/POST and open the generated URL in a real CDP/nodriver browser; if blocked, try residential/mobile proxy rather than rewriting form logic.

## Corsair hCaptcha/Imperva lesson

For Imperva/Incapsula + hCaptcha:

- `CAPSOLVER_API_KEY` present and extension loaded is only setup, not success.
- Simple `sitekey + pageurl` may fail with `ERROR_INVALID_TASK_DATA` / unsupported service.
- Before abandoning solve services, capture the real hCaptcha `/getcaptcha` payload (`rqdata`, enterprise data, n-data if present) from the iframe/network and test providers that support those parameters.
- If the payload cannot be captured or providers still reject it, classify as requiring residential/mobile proxy + anti-detect/persistent browser.

## Provider notes from docs/research

Keep the abstraction provider-neutral:

- 2Captcha / Anti-Captcha / CapMonster-style APIs may support hCaptcha with extra enterprise/rqdata-style parameters depending on service and site.
- Always log: provider, task type, sitekey, pageurl, extra payload fields, proxy/no-proxy, task response, token accepted/rejected.
- A token returned by a provider is not proof until injected/clicked and accepted by the target page.

## Artifact discipline

For every blocked airline keep:

- screenshot of browser-visible state;
- raw HTML for front page and form page;
- network log around form submit/captcha;
- replay script;
- `result.json` with status, URL, redirect location/title, and verdict.

Example durable report path from session:

- `/opt/data/artifacts/flight-scraping/antibot_research_20260604/rapport_obstacles_architecture_20260604.md`
