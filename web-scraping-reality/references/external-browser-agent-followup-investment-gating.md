# External browser-agent follow-up investment gating

Use when a ChatGPT Agent / Comet / browser-agent report produced at least one locally validated scraping lead and the user asks whether to invest more in that same agent.

## Decision rule

Invest more only when the first report produced **locally probed value**:

- source URLs that returned 200 from the VPS or user browser;
- visible list/detail pages with prices/items;
- corrected source inventory or prioritization;
- concrete pagination/detail-page questions that a browser agent can answer faster than Hermes.

Do **not** invest more just because the report is well-written. If the report lacks real navigation proof, screenshots/visual observations, actions performed, or locally verified claims, first send a corrected prompt with browser-proof gates.

## Best division of labor

- External browser agent: visual reconnaissance, opening pages, clicking pagination, opening detail pages, collecting representative examples, describing UI/filter states, locating obvious XHR/HAR hints if available.
- Hermes: VPS probes, reproducible implementation, lifecycle safety, deduplication, anti-bot replay validation, cron/QA.

## Follow-up prompt shape

For a promising vertical, ask for **deep bounded investigation**, not another broad panorama:

1. Start from Hermes-verified context; forbid repeating generic discovery.
2. Focus P1 sources only — the sources already confirmed accessible or high-value.
3. Require real-browser status at the top:
   - `Navigateur réel disponible: oui/non`
   - `DevTools/HAR disponible: oui/non`
   - `Screenshots disponibles: oui/non`
   - number of sources/pages/details actually opened.
4. For every P1 source require:
   - exact URL opened;
   - visual result;
   - number of visible listings/items;
   - 3 real examples with title/location/price/core fields/detail URL;
   - at least 2 detail pages opened if possible;
   - pagination mechanism and page 2/3 URL or load-more behavior;
   - anti-bot/cookie/CAPTCHA signals;
   - whether HTML/RSS/JSON-LD/XHR/HAR is needed;
   - next Hermes implementation action.
5. Separate strictly:
   - `observed in this browser session`;
   - `hypothesis to verify`;
   - `not tested`.
6. If no interactive browser was used, require the agent to stop with an explicit failure line instead of producing a substitute research report.

## Réunion real-estate case pattern

When the agent found useful Réunion real-estate leads, the right follow-up was not “search more everywhere”. It was a bounded deep dive on the locally confirmed P1 sources:

- FNAIM Réunion
- Superimmo
- 97immo
- DOMimmo
- Immo974
- OFIM
- Alter Immobilier
- Citya only if the correct Réunion rentals URL can be found quickly

The follow-up should extract implementation details: pagination, detail-page fields, residential-vs-commercial filters, examples, and whether HTML/RSS is enough. Deprioritize Bien’ici/SeLoger/Logic-Immo until the easy HTML/RSS sources are implemented or HAR evidence is available.

## Pitfalls

- Do not ask the external agent to “investigate more” broadly; that produces another polished but shallow report.
- Do not let the agent relabel inferred endpoints as observed endpoints.
- Do not promote DataDome/403 sources above confirmed HTML/RSS sources just because they are larger brands.
- Do not treat external screenshots/claims as production evidence until Hermes probes or replays the path.
