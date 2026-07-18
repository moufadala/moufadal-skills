# SeLoger CDP probe → registry entry, not production activation (2026-06-15)

## Context
During a Réunion real-estate scraping campaign, the user challenged whether SeLoger had really been tested. The active smoke run did not include SeLoger, even though prior probes had seen VPS HTTP `403`/DataDome. A live CDP probe later loaded a real SeLoger Réunion rentals page, but parsing was unreliable.

## Durable lesson
For multi-source scraping campaigns, a hard site must not disappear from the report just because it is not production-ready. Register it explicitly as a known source with a disabled/needs-hardening state, evidence path, and next action.

## Evidence pattern
Minimum evidence for a `needs-hardening` registry entry:

- page title or URL proving the real target loaded;
- screenshot path, especially if cookie/consent modal blocks content;
- count of visible text/listing/price candidates;
- examples of bad parsed fields if the parser is not trustworthy;
- explicit reason why ingestion remains disabled;
- next gate required to promote to `prod-candidate`.

## SeLoger-specific observations from this session

- HTTP direct from VPS had historical `403`/DataDome signals.
- CDP/browser profile could load `Maisons et appartements à louer – La Réunion`.
- Screenshot showed a real SeLoger results page but blocked by Usercentrics cookie modal.
- Text extraction found candidates/prices, but parser mixed fields: impossible examples such as tiny surfaces attached to large prices.
- Correct verdict: `needs-hardening_not_prod_candidate`, not `blocked` and not `done`.

## Promotion gate before enabling ingestion

Promote only after a DOM-card extractor passes all of these:

1. dismiss/remove Usercentrics modal;
2. extract card-scoped fields, not whole-page text windows;
3. require URL/title/city/rent/surface/rooms where available;
4. reject impossible rents/surfaces with explicit QA rules;
5. dedupe and compare against the existing DB to estimate unique value;
6. write raw snapshot + screenshot + normalized JSON as artifacts;
7. only then set `enabled: true` in the scraper source registry.

## Reporting rule
When the user asks “tu l’as fait ?”, answer with three separate states:

- `in registry / not in registry`;
- `live-probed / not live-probed`;
- `production-ingested / not production-ingested`.

Do not collapse “page loaded” into “scraper done”.
