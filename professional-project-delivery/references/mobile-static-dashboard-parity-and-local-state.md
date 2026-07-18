# Mobile static dashboard parity + local-state QA

Use this reference when turning a static/data dashboard into something the user can actually use on phone.

## Trigger

The user complains that the desktop version has functions missing on mobile, or that a dashboard is only “40% usable”. Treat that as a product/QA failure, not a styling request.

## Implementation pattern

For a static dashboard with embedded JSON:

1. Preserve all top-level datasets through every post-build step.
   - If `build_app.py` embeds `{listings, suspects}`, a later image-cache/minifier/publisher must re-embed both, not just `listings`.
   - Add a deterministic audit that compares public JSON files against embedded JSON counts.
2. Put key actions both in desktop UI and in visible mobile controls.
   - Mobile top controls should include the state-changing views/actions, not hide them in a footer or horizontal-only overflow.
   - Prefer wrapping controls over horizontal scrolling for critical actions.
3. For usable real-estate/listing dashboards, include:
   - save/favorite/shortlist state;
   - hide/dismiss and restore flow;
   - copy/share/source actions;
   - suspects/excluded listings view;
   - similar/duplicate listings view;
   - missing-field/trust badges.
4. Store local-only state explicitly and label the limitation.
   - Example localStorage keys: `immoSavedIds`, `immoHiddenIds`.
   - Be honest that localStorage is per browser/device, not account sync.

## QA contract

Do not stop at screenshots. Verify with browser JS and public fetches:

- embedded dataset counts equal `/listings.json` and `/suspects.json` counts;
- no console errors;
- mobile top buttons visible: filters/all/saved/hidden/suspects/reset/example;
- tabs include all desktop categories and wrap visibly on phone;
- save flow increments saved count and saved tab shows the card;
- hide flow removes from normal results, hidden tab shows it, restore label appears;
- duplicate/similar tab count matches exported duplicate records and is not accidentally constrained by default filters;
- suspects tab shows excluded records and modal source link is populated;
- copy/share buttons execute fallback paths without throwing.

## Pitfalls

- A post-build image-cache step may silently rewrite embedded JSON from only one data file and drop secondary datasets like `suspects`.
- A “Similaires” tab can accidentally inherit default residential filters and show far fewer records than its tab count.
- A mobile screenshot may look acceptable while critical buttons are merely off-screen in horizontal overflow. Check DOM and viewport layout, and prefer wrap for essential controls.
- Do not claim “100% finished” for a static dashboard if saved state is local-only, dedup is heuristic, or source data remains incomplete. Say “usable static V1” and list backend/product limits.