# Flight multisource scraper consolidation — final verdict pattern — 2026-06-21

## Trigger

Use this when consolidating a flight-scraper ecosystem after multiple partial runs: official airlines, aggregators, fragile airline probes, mobile/API probes, and sources mentioned by the user but not present locally.

## Durable lesson

A consolidation is not complete when the strongest two sources are green. The final artifact must answer three separate questions:

1. **Which sources are production-solid now?** Price proof + route/date/passenger coverage + replayable artifacts.
2. **Which sources are known but not production-solid?** Anti-bot, no-offer, local bug, timeout, missing script, or transient upstream.
3. **Which earlier failures were false negatives?** Especially proxy/SOCKS preflight failures and parser false positives.

If the user corrects scope with “there were plenty of others” / “Kiwi, Skyscanner, etc.”, keep any useful official run, but immediately add an inventory/aggregator track. Do not present the official-only result as the global answer.

## Required source tracks

- **Official solid track:** French Bee, Air Austral, or equivalent direct airline sources already known to return prices.
- **Aggregator solid track:** Kiwi/Skypicker GraphQL or direct replay, Kayak/Skyscanner/Trip.com where scripts/artifacts exist.
- **Fragile official track:** Air Mauritius, Corsair, or engines that may return no-offer, error pages, or anti-bot.
- **Absent/discovery track:** sources named by user or previous artifacts but no local script found; report `not-found-local-script` explicitly.

## Evidence gates for `solid`

A source can be called solid only when the run has:

- current preflight proof when proxy/mobile egress matters;
- structured or audited price evidence, not just regex over body text;
- route/date/passenger context;
- segment/flight or booking URL evidence when available;
- artifact path to stdout/JSON/report;
- non-price cases audited and reclassified.

For flight prices, ignore strings that occur inside error messages/status pages. Example pitfall: `Erreur 500` must not become `eur 500`.

## Classification taxonomy

Use these labels consistently across reports:

- `price-found`
- `no-offer`
- `validation-control-exercised`
- `network-preflight-failed`
- `transient-upstream-502` or another explicit upstream class
- `blocked-antibot`
- `bug-local-*`
- `bug-local-or-site-timeout` when timeout occurs before route verdict
- `not-found-local-script`
- `failed-unknown` only after stdout/stderr audit

## Reporting contract

Produce a compact final report with:

1. **Solid now:** e.g. Air Austral 54/54, French Bee hardened 29/30 business + 1 transient 502, Kiwi GraphQL/direct with prices and booking URLs.
2. **Not solid / gaps:** e.g. Kayak anti-bot, Skyscanner no local script, Corsair error-page/local bug, Air Mauritius no-offer vs timeout split.
3. **False negatives corrected:** e.g. initial French Bee failures caused by SOCKS `(97)` / empty preflight, not scraper failure.
4. **Next single useful action:** targeted replay of transient cases or specific bug-local fix; do not reopen every source blindly.

Keep Telegram summary short; put detailed matrices in Markdown/JSON artifacts.
