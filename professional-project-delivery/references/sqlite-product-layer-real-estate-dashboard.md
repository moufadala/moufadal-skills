# SQLite product-layer pattern for small real-estate dashboards

Use this when a real-estate/watch dashboard is backed by a small SQLite scraper database and the user asks whether the database itself should change.

## Decision heuristic

Do **not** migrate away from SQLite just because the UI/data quality feels messy. First separate:

- **storage engine problem**: too much data, concurrent writers, complex backend/API needs, heavy geo/search workload, user accounts, high write contention;
- **product data model problem**: raw scraper rows are incomplete, duplicated, misclassified, missing normalized city/region/type/trust fields.

For V1 dashboards with hundreds or a few thousands of active listings, SQLite is usually fine. The better move is often a non-destructive product-enrichment layer above the raw scraper table.

## Acceptance contract

Before changing the app, require this contract:

- keep the raw scraper table immutable/non-destructive;
- add enrichment tables/views, not ad-hoc fixes only in React/JS;
- export from the product view, not directly from raw rows;
- prove DB -> export -> public URL -> browser consistency;
- keep suspect/debug/non-canonical items visible somewhere, but not in the clean default view.

## Implementation pattern

Recommended shape:

```text
raw table, e.g. rental_listings
  -> listing_product_enrichment
  -> rental_listings_product view
  -> rental_listings_canonical_residential view
  -> static app export/listings.json
```

Useful enrichment fields:

- `city_normalized`, `zone_normalized`, `region`;
- `property_type_normalized`;
- `residential_status`, `residential_reasons_json`, `is_residential`;
- `duplicate_key`, `duplicate_group_size`, `duplicate_group_rank`;
- `canonical_source_site`, `canonical_source_id`, `is_canonical`;
- `quality_score`, `missing_fields_json`, `trust_flags_json`.

## UX pattern

Default UI should be clean and canonical:

- main tab/list = canonical residential listings only;
- separate tab = similar/non-canonical duplicates;
- suspects/commercial/out-of-scope records excluded from the main user flow but inspectable;
- card counts should be based on the same exported JSON the public UI uses;
- if localStorage or filters can hide items, test fresh-state and dirty-state separately.

## QA gates

Run a deterministic DB audit plus public/browser QA:

```bash
python3 tests/audit_db_enrichment.py
python3 src/build_app.py
python3 tests/audit_filters_v3.py
python3 tests/audit_app_features_v4.py
bash deploy/qa-public.sh
```

Browser checks:

- public URL loads the current build, not an old artifact;
- embedded/exported listings count matches the expected product view;
- canonical/similar tab counts are coherent;
- opening a card/modal works;
- images load (`naturalWidth > 0` where applicable);
- console has zero blocking JS errors.

## Pitfalls

- Do not claim “database migration needed” before measuring row counts, data completeness, duplicate groups, and concurrency needs.
- Do not solve data quality purely in frontend filters; centralize reusable classification/normalization in DB/export code.
- Do not silently drop duplicates: canonicalize the main view and expose similar/non-canonical records separately.
- Do not normalize ambiguous missing cities by guesswork. Only add mappings when the text/URL/source gives reliable evidence.
- Watch aggregator contamination: a source scoped to Réunion can still emit off-island URLs/items. Add explicit trust flags such as `outside_reunion_url` and exclude them from the main product view.
- Reconcile count differences by stating the perimeter: raw active rows vs enrichment rows vs residential candidates vs exported-with-photo rows vs UI canonical rows.
