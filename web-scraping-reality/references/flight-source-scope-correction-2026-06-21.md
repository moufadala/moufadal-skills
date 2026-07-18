# Flight scraper source-scope correction — 2026-06-21

## Trigger

During a RUN flight scraper consolidation, the initial execution narrowed too quickly to the two strongest official sources (French Bee + Air Austral). The user corrected the scope: the working set also included aggregators and other prior probes such as Kiwi, Kayak, Skyscanner, Air Mauritius, Corsair, and mobile probes.

## Durable lesson

For flight scraper consolidation, do not treat examples or recently-green sources as the full scope. Build a source inventory first from local scripts, artifacts, registry, and prior runs, then split execution into tracks:

1. **Official/validated track** — sources already known to produce prices, e.g. French Bee / Air Austral.
2. **Aggregator track** — Kiwi, Kayak, Skyscanner, Trip.com, etc.; include both direct replay and browser/mobile capture if present.
3. **Fragile official track** — Air Mauritius, Corsair, other airline sites with anti-bot or booking-engine errors.
4. **Discovery/absent track** — sources mentioned by user or previous artifacts but no local script found; classify explicitly as `not-found-local-script`, not silently omitted.

## Classification pitfalls observed

- **False positive price regex:** `Erreur 500` can be misparsed as `eur 500`. Price extraction must ignore error titles/status pages and prefer structured fields like `ok=true`, `prices=[]`, body title, and booking-page status.
- **Bug-local vs site-block:** Kiwi direct replay failed because a captured template file was missing; this is `bug-local-missing-template`, not a Kiwi site block.
- **No-offer vs failure:** Air Mauritius reaching booking engine and returning “aucune disponibilité / 66002” is `no-offer`, while homepage timeout before search is `bug-local-or-site-timeout`.
- **Skyscanner omission:** If no local Skyscanner script exists, write that as an explicit line in the report instead of leaving it out.

## Reporting pattern

For user-facing summaries, lead with the corrected source coverage:

- official track status;
- aggregator track status;
- fragile official status;
- absent/not-found sources;
- bugs local to fix next.

Keep the summary compact, but cite artifact paths and corrected reports. If an initial report contains false positives, create a corrected summary/Markdown artifact rather than only explaining the correction in chat.
