# Static real-estate clean portal — iterative optimization + QA loop

## When this applies

Use this after a clean static real-estate portal is already published and Moufadal asks to "refaire", "optimiser", or repeat research/planning/optimization. The goal is not to add dashboard complexity; it is to run another product-quality pass while preserving the clean portal contract.

## Product rule

For each optimization cycle, explicitly repeat:

1. **Recherche / benchmark** — what standard property portals and user workflows suggest.
2. **Planification** — one small improvement that increases decision/search value without clutter.
3. **Implémentation** — reversible code/data change.
4. **Publication** — deploy the exact public artifact users will open.
5. **QA publique** — browser/curl evidence, not only local build success.

If the previous pass already added natural-language search and a high-value filter, good next passes are usually:
- shareable/restorable URL state and `Copier recherche`;
- debounce/performance for client-side filters;
- mobile layout hardening;
- schema fallback hardening for regenerated exports.

## Low-clutter optimization sequence

Prefer this order before maps, accounts, alerts, source-health panels, or admin UI:

1. Search semantics: `T2`, `moins de 800`, `40m2`, local spelling aliases.
2. One classic filter if missing: rooms/min pieces, budget, surface, type, city.
3. URL-state saved search: query params hydrate filters and sort; reset clears URL.
4. Copy/share action: one visible button, no account system.
5. Filter performance: precomputed searchable text per listing plus input debounce; keep explicit submit/button immediate.
6. Mobile polish: verify 390px viewport for header, filters, cards, and horizontal overflow.
7. Data schema guard: when rebuilding from scraped/exported JSON, accept both canonical and legacy field names (e.g. `property_type` then `type`) before falling back to generic labels.

## QA checklist for every repeat pass

Run this against the **public HTTPS URL**, not just local files:

- `curl -4` HTML, `listings.json`, and `coverage.json` return 200.
- Listing count matches expectation in both JSON and page summary.
- A representative URL hydrates state, for example: `?immo=1&q=Saint-Denis+T2+moins+de+800&sort=price_asc`.
- Result count and first visible cards obey the parsed constraints: city/sector, rooms, price, sort.
- A multi-field URL hydrates individual controls: city, max price, min surface, rooms, sort.
- Reset clears UI state and returns the URL to the base route.
- `Copier recherche` does not trigger JS errors; if clipboard confirmation is not visible in automation, verify the button exists and console remains clean.
- Browser console after interactions: 0 JS errors.
- Mobile emulation around 390px: `document.scrollingElement.scrollWidth <= window.innerWidth` or no meaningful horizontal overflow/offenders.
- If performance changed: measure repeated filter/apply calls and report average/max.
- Regenerated coverage preserves property types, cities, photos, and important counts.

## Pitfalls

- Do not call an optimization pass complete after a local build only; the public container may still serve the previous artifact.
- Do not add source/debug/admin health UI to the clean public portal just because the underlying scraper has quality signals. Keep those secondary or separate.
- Do not treat a copy-to-clipboard visual confirmation as required in browser automation; clipboard APIs may be restricted. Console-clean plus stable URL/button is sufficient unless the user specifically asks for a toast.
- Watch for CSS grid/flex min-content overflow on mobile panels. A minimal `min-width:0` on grid children/panels can fix 5–15px horizontal overflow without redesigning the UI.
- Watch for data-schema fallback regressions after rebuilding. If all types collapse to `Bien`, inspect whether the source uses `type` instead of `property_type` and patch fallback order.
- If deployment tooling lacks `rsync`, use a reversible copy strategy with backup + `shutil.copytree`; capture this as a deployment workaround only, not as a permanent claim that rsync is unavailable.

## Final response shape

Keep the user-facing reply compact and evidence-backed:

- what the two cycles changed;
- public URL;
- exact QA facts: listing count, representative query result count, URL hydration, reset, mobile overflow, JS errors;
- report path and rollback backup path;
- explicitly state that no dashboard/debug clutter was added.
