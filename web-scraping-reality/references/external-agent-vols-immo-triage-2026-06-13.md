# External agent reports — vols RUN + immobilier Réunion triage (2026-06-13)

Use this reference when the user provides browser-agent/ChatGPT Agent PDFs for both Réunion flight and real-estate scraping.

## Session artifacts

- Source PDFs:
  - Vols: `/opt/data/cache/documents/doc_2306dd813d48_rapport_vols_RUN.pdf`
  - Immo: `/opt/data/cache/documents/doc_6f4adb07c802_rapport_investigation_approfondie_immo_reunion.pdf`
- Triage artifact: `/opt/data/artifacts/external_reports_triage_20260613T174916Z/TRIAGE_RAPPORTS_VOLS_IMMO.md`
- PDF extraction:
  - Vols: 5 pages, ~17k chars, text PDF, no OCR needed.
  - Immo: 8 pages, ~18k chars, text PDF, no OCR needed.

## Core lesson

Treat these reports as **browser-real prerecon**, not production proof. They contain useful visual/navigation evidence but no HAR, Copy-as-cURL, NetLog, or DevTools export. Therefore:

- visible price/result = useful lead;
- URL/path seen in address bar = plausible capture target;
- no network artifact = not a solved API scraper;
- local VPS probe can override or downgrade claims when it sees 403/503/captcha.

## Flights RUN triage outcome

- **French Bee**: strongest official target. External report saw RUN→ORY on 2026-07-28 with prices `344,52 €` and `470,52 €` through `vols.frenchbee.com/plnext/bf-dx/Override.action`. Decision: stabilize existing CDP/headful Amadeus runner, screenshots/HTML/parser QA; do not rediscover the endpoint from scratch.
- **Air Mauritius**: external report confirms `booking.airmauritius.com/plnext/AirMauritiusDX/Override.action` followed by Imperva/hCaptcha. Decision: do not burn time on more Playwright desktop; ask for Android NetLog/API mobile or HAR/Copy-as-cURL around the real search.
- **Air Austral**: contradictory evidence. External report/VPS homepage probe show Cloudflare 403, but a prior local campaign extracted `à partir de €375,02`. Decision: do not mark dead; retest the exact route/script that produced prices and classify as conflict `homepage-blocked vs route-price-artifact`.
- **Corsair**: hCaptcha; keep out of P0 unless explicitly testing solver/profile-human path.
- **Kiwi/Skyscanner/Trip/Kayak/Google Flights**: useful for comparative/indicative pricing only. Require HAR/XHR capture and official-source coherence checks before treating as production pricing.

## Real-estate Réunion triage outcome

The immo PDF materially changes priority: do not limit the product to Bien’ici/SeLoger. Prefer the low-friction HTML/RSS sources first.

Confirmed or high-value sources:

- **FNAIM** `/locations/1`: VPS HTTP 200, price/surface visible; HTML direct candidate.
- **97immo** `/immobilier/location/la-réunion`: VPS HTTP 200, price/surface visible; HTML direct candidate, with possible non-blocking captcha/contact noise.
- **OFIM RSS** `/rss.xml`: VPS HTTP 200, rich RSS; filter `Location` and residential types.
- **Alter Immobilier** `/nos-biens-a-louer/`: VPS HTTP 200, price/surface visible; HTML direct candidate.
- **Citya** `/annonces/location/appartement/la-reunion-974`: VPS HTTP 200, price/surface visible; HTML direct candidate.
- **Immo974** `/locations`: VPS HTTP 200, price/surface visible; contact reCAPTCHA does not block listing read.
- **DOMimmo**: HTTP 200 and rich details but dynamic enough to classify as `needs-light-hardening`; use CDP/HAR if HTML detail parsing is insufficient.
- **Superimmo**: browser-agent saw 516 annonces, but VPS probe returned HTTP 503 anti-bot. Treat as promising but not direct HTML until CDP/HAR/profile test succeeds.

## Corrected implementation order

### Immo first when the goal is useful production value

1. Build/verify a non-destructive lifecycle wrapper before adding many sources:
   - per-source `run_status`: `success`, `partial_success`, `blocked_403`, `blocked_429`, `captcha`, `timeout`, `parse_error`, `empty_but_valid`;
   - only `success`/`empty_but_valid` can stale/inactivate old listings;
   - blocked/timeout/parse-error never stale old data;
   - archive raw HTML/JSON snapshots per source.
2. Add confirmed HTML/RSS adapters: FNAIM, 97immo, OFIM RSS, Alter, Citya, Immo974.
3. Add DOMimmo with light CDP/HAR hardening if needed.
4. Add Superimmo only after resolving 503 via CDP/HAR/profile.
5. Keep Bien’ici/SeLoger hardening as valuable but not the only core path.

### Flights after immo unless the user explicitly prioritizes flights

1. Kiwi live cron for indicative RUN→PAR prices.
2. French Bee official runner hardening.
3. Air Austral targeted rerun to resolve evidence conflict.
4. Air Mauritius Android NetLog/API mobile capture.

## Output style for this user

After processing such reports, deliver a short verdict first:

- “Did it find something?”
- “What is newly useful?”
- “What is contradicted/overclaimed?”
- “What exact artifact is needed next?”

Then provide the path to the durable triage artifact. Avoid a long PDF summary unless asked; the user wants decision and next implementation order.
