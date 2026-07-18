# Static real-estate clean search optimization

Use this after a scraper-backed immo portal has been rebooted into a clean V1 and Moufadal says to optimize it without adding clutter.

## Trigger signals

- The user says the clean portal “répond bien” and wants to stay on it.
- The user asks to “optimiser sans rajouter de fouillis”.
- The temptation is to add map, alerts, source health, admin panels, scores, or many filters.

## Principle

Optimize search behavior before adding visible features. The visible UI should remain a classic real-estate portal: search bar, a small set of primary filters, cards, detail modal/page, source link, save/hide.

## Research-backed default

Quickly check current category references before changing product behavior:

- Citya-style agency pages: location, budget/rent, surface.
- SeLoger-style portals: location, price, surface, number of rooms, property type, sort.
- General filter UX: keep frequent filters visible; hide or avoid rare/technical filters; distinguish filtering from sorting; expose active filters clearly.

Do not copy a repo or large UI. Use references to validate the product default.

## Low-clutter improvements that worked

1. Add only one first-level filter when it has strong search value:
   - `Pièces min.` with options `Toutes`, `Studio / 1+`, `2+`, `3+`, `4+`, `5+`.
2. Make the search bar parse common user language:
   - `T2` / `T 2` → exact rooms = 2.
   - `moins de 800`, `sous 800`, `budget 800`, `loyer 800`, `max 800` → budget max = 800.
   - `40m2`, `40 m²`, `40 metres` → surface minimum = 40.
   - `st denis` / `ste marie` → `saint denis` / `sainte marie`.
3. Keep technical internals hidden:
   - no source-health widgets on first screen;
   - no scraper debug;
   - no score explanations unless behind admin/back-office;
   - no alert cockpit unless the user explicitly moves to alerts.

## QA gate

Run public URL QA, not only local build checks:

- Public HTTPS loads current build.
- `listings.json` count matches expected export count.
- Search example `Saint-Denis T2 moins de 800` returns non-zero results.
- The first visible results satisfy:
  - Saint-Denis / matching locality;
  - exactly 2 rooms for `T2`;
  - price <= 800.
- Filter example `Pièces min. = 3` + `Budget max = 1200` returns non-zero results, and first cards obey rooms/price constraints.
- Browser console after interactions: 0 JS errors.
- Mobile visual check still shows header/search/filters/cards without overlap.

## Pitfalls

- Do not treat `T2` as a fuzzy text token only; it should constrain room count or the search will feel wrong.
- Do not add a map, alerts, or admin statistics just because they are available. Those are separate product phases.
- Do not expose “photo cache coverage” or source reliability on the public first screen; keep fallback photo UX clean and mention coverage only in QA/handoff.
- Do not optimize by cloning an open-source property portal. Extract patterns, then adapt to the current scraped export.
