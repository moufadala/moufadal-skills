# Static immo dashboard — clean default + transparent excluded-data export

## Session-derived pattern

When publishing a public static real-estate dashboard from scraped listings, do not silently discard records that were filtered out for product quality. Keep the user-facing default clean, but export the excluded/suspect records as a separate auditable artifact.

## Recommended shape

- `listings.json`: clean default dataset used by the public UI.
- `suspects.json`: excluded records with structured reason fields.
- UI footer/drawer/tab: link to the suspects export, but keep it out of the default search flow.
- Handoff: include counts for input, public listings, suspects, source distribution, and top exclusion reasons.

## Classification discipline

For “residential / non-commercial” filters, avoid over-aggressive keyword rejection:

- Strong signals from `title`, `property_type`, and `url` can exclude: local commercial/professionnel/médical, bureaux, box, parking/garage, garde-meuble, terrain, entrepôt.
- In long descriptions, reject only explicit phrases such as `local commercial`, `local professionnel`, or `locaux commerciaux`.
- Do not reject a listing merely because a residential description mentions incidental parking, a home office/bureau, or an `agent commercial`.

## QA contract

Before reporting success:

1. Rebuild the static app and its JSON exports.
2. Run the repo’s filter/audit tests.
3. Re-run image cache if the JSON changed.
4. Verify public URLs:
   - `/`
   - `/listings.json`
   - `/suspects.json`
5. Browser-check:
   - hero counts match JSON;
   - suspects link resolves;
   - `fetch('/suspects.json')` returns expected count;
   - no console errors.
6. Run the broader portfolio/status gate when this dashboard is part of a larger system.

## Why this matters

This avoids two bad outcomes:

- polluting the default user experience with commercial/irrelevant listings;
- losing auditability and making users distrust the filter.
