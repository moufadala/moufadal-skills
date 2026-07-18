# Réunion vols + immobilier — operational watch lessons (2026-06-13)

Use when continuing RUN flight scraping or Réunion rental monitoring after pre-recon / prototype scrapers exist.

## Flight watch orchestration pattern

Build a small auditable runner above individual fragile scrapers rather than trusting each script's exit code:

- Write one run directory per execution with `health.txt`, `tasks.json`, per-task `stdout`, `stderr`, raw JSON, `SUMMARY.json`, and `report.md`.
- Maintain a stable symlink such as `/opt/data/artifacts/flight-watch/latest` for handoff / Telegram / Morning Brief.
- Classify per task as `prod-candidate`, `partial-price-artifact`, `blocked-antibot`, or `bug-local-or-blocked`.
- Parse full stdout/raw JSON, not only tails. Airline scripts often return exit 1 while the page contains fares, or exit 0 with no business-valid prices.
- Separate site protection from local runner defects: page blanche/app shell, bad local template path, screenshot tooling, profile conflict, timeout, and parser mismatch are not proof that the site is impossible.

## Kiwi fallback: prefer browser network capture over stale template replay

A previous direct `kiwi_direct_search.py` depended on a local captured request template and failed when the template path was stale. For production-like runs, prefer a live browser network capture (`kiwi_capture_live.py`) that opens Kiwi results and captures `SearchOneWayItinerariesQuery` responses.

Important parsing rule: Kiwi may render `price_amount` in a non-EUR display currency/locale (observed `Rp` / IDR), while `price_eur` is stable for comparisons. Classification and cheapest-price logic should prefer:

```python
value = offer.get('price_eur') or offer.get('price_amount')
```

Do not report a giant `price_amount` as euros.

## Air Austral: targeted rerun beats stale contradiction

If memory/artifacts disagree about Air Austral (e.g. earlier Cloudflare/403 notes but later price artifacts), run a targeted official smoke before deciding. On 2026-06-13, `airaustral_price_check_nosshot.py` for RUN↔CDG 2026-07-19/2026-07-26 returned official Amadeus results with fares and flights:

- outbound examples: RUN→CDG from about €375.02 / €380.02
- return examples: CDG→RUN from about €706.55
- page title: `Air Austral - Vols`

Treat Air Austral official as currently exploitable for that route/date until a fresh run disproves it.

## French Bee: HTTP 200 app shell is not production success — but avoid false negatives

French Bee official can generate an Amadeus `Override.action` and return HTTP 200 with a large HTML app shell, but still fail business extraction if:

- final URL has no `#/FPOW` / expected results state,
- screenshot is blank/white or DOM lacks business result text,
- parser returns `flights=[]` and `cheapest=null`,
- error is `no_cheapest_combo`.

Classify that as `bug-local-or-blocked`, not `prod-candidate`, even if historical runs succeeded.

However, a blank/app-shell first pass can be a **local wait false negative**. On 2026-06-13, adding console/pageerror capture plus a slower Amadeus wait fixed French Bee: `--render-timeout 180000 --extra-wait 45000`, then fallback `networkidle`, produced official results for RUN↔ORY 2026-07-19/2026-07-26:

- outbound BF705: BEE LIGHT+ €349.52;
- return BF704: BEE LIGHT+ €580.58;
- cheapest round trip: €930.10;
- final URL had `#/FPOW`, title `French bee - vols`, `pardon=false`.

So the root cause was not a hard anti-bot block; it was premature capture/extraction before Amadeus/Aria finished rendering after Akamai/Incapsula bootstrap. Keep the longer wait in `flight_watch.py` before declaring French Bee down.

## Real-estate watch handoff

For the Réunion rental watcher, keep the non-destructive lifecycle pattern and add a stable latest pointer:

- never delete rows during stabilization;
- mark stale only for sources actually refreshed successfully in the current run;
- report DB coverage and selected business listings in JSON + Markdown;
- maintain `/opt/data/artifacts/realestate/watch_runs/latest` pointing to the latest run.

This makes Morning Brief / Telegram handoff robust without re-discovering the newest artifact path each session.

## Final report shape for the user

The useful summary is compact and verdict-first:

- Vols: source → status → offers/prices → artifact → verdict (`official exploitable`, `indicative fallback`, `not prod today`).
- Immo: selected count, source count, coverage/quality, latest symlink, report path.
- Explicitly say when a source is not production-valid despite historical success.
