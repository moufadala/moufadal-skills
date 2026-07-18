# Static real-estate dashboard — shareable/saved search via URL state

## When this applies

Use this pattern for static or mostly-static real-estate dashboards where:
- filters already exist client-side;
- users need to save/share a search;
- there is no backend/account system yet;
- the next tempting ideas are map/email alerts/contact forms.

## Decision rule

Before building maps or true alerts, make searches restorable from the URL.

This gives a real product improvement without backend debt:
- bookmarkable saved searches;
- shareable search links;
- reproducible QA URLs;
- a clean bridge to future Telegram/email alerts because the URL encodes the matching contract.

## Recommended implementation

1. Keep localStorage for the user’s local browsing state.
2. Add a URL marker such as `?immo=1` to indicate that query params should override localStorage.
3. Encode only product state, not transient UI state:
   - regions / zones / communes;
   - property type / furnished / source;
   - rent min/max;
   - surface min;
   - rooms / bedrooms min;
   - search text;
   - active tab;
   - sort.
4. Use compact, readable parameters, e.g.:
   ```text
   ?immo=1&r=Sud&rentMax=900&surfaceMin=50&tab=sameBudgetElsewhere&sort=priceAsc&q=saint
   ```
5. Add a visible `Copier recherche` action on desktop and mobile.
6. On render, call a URL sync function so the address bar remains restorable after filter changes.
7. Preserve unrelated query params when possible, but remove stale dashboard-state params before writing new ones.

## QA gate

Minimum browser QA:
- Open a hand-crafted URL with several filters; verify input values, checkboxes, tab, sort and result count.
- Click `Copier recherche`; verify no JS error/dialog blocker.
- Reload or reopen the URL; verify the same result count and heading.
- Verify fresh/reset state still works.
- Verify public HTML and JSON endpoints still return 200.

Add a static regression test that checks tokens such as:
- `copySearch` / `copySearchUrl`;
- `stateFromUrl`;
- `encodeStateToParams`;
- the URL marker (`immo` or equivalent).

## What not to do too early

- Do not build a map until latitude/longitude or address coverage is proven. A partial map makes a clean portal look broken.
- Do not promise email alerts from a static site. True alerts need server-side saved searches + matching + notification delivery.
- Do not treat `mailto:`/basic contact links as a real lead-capture feature.
- Do not migrate the DB to support this; URL state is client-side and reversible.

## Repeat optimization handoff

When this URL-state pass is part of a repeated "recherche → planification → optimisation" request, pair it with the broader clean-portal iteration QA in `references/static-real-estate-clean-portal-iteration-qa.md`: public HTTPS checks, representative hydrated URLs, reset behavior, mobile 390px overflow, performance timing, schema fallback coverage, and a compact evidence-first final reply.

## Future bridge

When ready for real alerts, persist these URL/search specs in a small config/table and run a cron matcher against newly seen canonical listings, then deliver only new matches via Telegram/email.
