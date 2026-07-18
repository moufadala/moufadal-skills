# Réunion immo — residential quality gate and Queue pitfall

## Trigger

Use when refreshing or QA-ing the Réunion rental DB, especially before presenting a dashboard/top list as residential housing.

## Lessons captured

### 1. Fresh DB is not enough

A DB can be fresh and still polluted by non-residential items. Add a non-destructive quality gate that separates:

- `residential_candidate`;
- `suspect_non_residential`;
- `unknown_residentiality`.

For the current VPS pipeline the reusable gate is:

```bash
/opt/data/scripts/immo_residential_quality_gate.py
```

Default behavior should be non-destructive and export a CSV subset for consumers:

```text
immo_residential_candidates.csv
```

Dashboard/product layers should default to the residential subset unless the user explicitly wants commercial properties.

### 2. Avoid over-aggressive text filters

Do not reject a residential listing just because the long description contains incidental words like `parking`, `bureau`, or `agent commercial`.

Prefer strong signals from:

- title;
- `property_type`;
- URL/category;
- exact long-description phrases such as `local commercial`, `local professionnel`, `locaux commerciaux`.

### 3. Multiprocessing Queue false timeouts

When a child scraper returns many listings, sending the full payload through `multiprocessing.Queue` can fill the pipe and block the child before `join()`, creating a false timeout. For large source payloads, write the child result to a temporary JSON file and let the parent read it after `join()`.

## Reporting contract

When reporting immo refresh quality, include both:

- freshness: latest timestamp, rows, coverage;
- residential quality: active count, residential candidates, suspect count, unknown count, top suspect sources.
