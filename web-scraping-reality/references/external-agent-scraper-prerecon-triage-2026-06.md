# External agent prerecon triage — scrapers vols/immo Réunion (2026-06)

Use this when the user brings back a ChatGPT Agent / Perplexity / browser-agent PDF report intended to unblock scrapers. Treat it as **external prerecon**, not ground truth.

## Workflow

1. **Extract the report first**
   - For local PDFs use `/opt/data/bin/pdfx <pdf> --out-dir <artifact_dir>/pdf_extract --render-if-short`.
   - Keep `extracted.md`, `report.json`, and the source PDF path in the triage artifact.

2. **Triage claims into three buckets**
   - `confirmed_by_local_artifact`: matches existing logs/scripts/fixtures.
   - `plausible_but_unverified`: technically coherent, needs HAR/cURL/NetLog/screenshot.
   - `contradicted_or_overstated`: live probe or prior postmortem disagrees.

3. **Probe only the highest-value claims**
   - Do not spend time validating every link.
   - For scrapers, prioritize claims that name a concrete endpoint, payload, mobile API, HAR replay path, or anti-bot bypass.
   - Archive probe outputs even when they fail.

4. **Correct the implementation order**
   - If a report says “endpoint accessible” but VPS probe returns 403/429/captcha, do **not** start coding HTTP replay.
   - Reclassify the finding as “capture target”: ask for HAR, Copy-as-cURL, NetLog Android raw bytes, screenshots, cookies/headers redacted.

5. **Deliver a verdict, not a summary**
   - Answer explicitly: “Did it find something?”
   - Separate: new useful lead / already known confirmation / wrong or overclaimed / next artifact required.

## Réunion flights lessons from this session

- Air Austral: ChatGPT Agent’s useful lead was `ajaxResa.php?method=getCryptData2` producing an Amadeus `Override.action` URL with `SITE=BAUKBNEW`, `EMBEDDED_TRANSACTION=FlexPricerAvailability`, `ENCT=1`, dynamic `ENC`, and a critical `d` parameter. Local VPS probe on `d=` returned `HTTP 403`, so this is a **capture target**, not a solved HTTP endpoint. Ask for HAR/Copy-as-cURL of the real `ajaxResa.php` call with populated `d`.
- French Bee: external reports mostly confirm the known path: Drupal/front → Amadeus `Preload.action` / `Override.action` with dynamic `ENC`; production work should stabilize CDP/headful profile, HAR/screenshot/cookie artifacts, and parser QA rather than rediscovering the endpoint.
- Air Mauritius: page-cache/deals can be `official_cached` or `marketing_cache`; never publish them as `official_live`. Live booking still needs Android NetLog/mitmproxy/HAR around `availability`, `offer`, `price`, `fare`, `booking`, `search`, `MK`.
- Kiwi/Tequila: keep `confidence=indicative`; useful for comparisons only. Beware currency/display transformations and require official-source coherence checks.
- Kayak/Skyscanner/Google Flights/Corsair: useful external report outcome may be “do not scrape UI”; require official API/access or a very concrete HAR before investing.

## Réunion immobilier lessons from this session

- Validate agent site claims with small live probes before implementation.
- Example corrections: a report classed Logic-Immo/PAP as accessible, but VPS probes returned 403; FNAIM report URL 404’d, while `https://www.fnaim.re/locations/1` was valid.
- Prefer implementing confirmed low-friction HTML sources first, while anti-bot/BFF sources wait for HAR/NetLog.

## Output artifact template

Create `TRIAGE_<DOMAIN>_CHATGPT_AGENT.md` with:

```md
# Triage du rapport ChatGPT Agent — <domain>

## Verdict court
- Did it find something?
- New useful lead:
- Not yet solved because:

## Extraction PDF
- pages:
- chars:
- scanned/image?:

## Findings by source
### <source>
- New lead:
- Confirmed by:
- Contradicted by:
- Required capture:
- Implementation decision:

## Corrected priority order
1. ...

## Next artifacts to ask from user
- HAR:
- Copy-as-cURL:
- NetLog Android:
- screenshots:
```
