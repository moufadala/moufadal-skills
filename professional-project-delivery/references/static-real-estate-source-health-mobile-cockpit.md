# Static real-estate dashboards: source health, mobile map filters, and saved-search cockpit

Use this pattern when a scraper-backed static real-estate dashboard already has a working JSON export, filters, saved-search URL state, alerts/history, and the user asks to “finish P0/P1/P2”, “take a step back”, or questions whether the database should change.

## Core judgement

Do **not** migrate the database just because the product now needs health/admin UX. For small/medium scraper-backed dashboards, first prove whether the engine is the bottleneck:

- row count and export size;
- active vs exported items;
- duplicate/canonical counts;
- missing field coverage;
- freshness per source;
- public dashboard performance and browser console.

If volume/concurrency is modest, keep the raw scraper DB stable and add static operational layers:

- `source_health.json/html` for freshness and source trust;
- `saved_searches_admin.json/html` for alert cockpit and dry-run counts;
- auxiliary history SQLite for non-spammy price/status events;
- generated dashboard links to these pages.

The better next step is often fixing stale sources, not changing DB technology.

## P0 — Source health layer

Create a non-destructive exporter that reads the DB and latest scraper smoke summary. Output both machine and human artifacts:

- `artifacts/app/source_health.json`
- `artifacts/app/source_health.html`

Recommended JSON contract:

```json
{
  "ok": true,
  "generated_at": "...",
  "db_path": "...",
  "latest_smoke_summary": {"path": "...", "by_source": {}},
  "summary": {
    "source_count": 13,
    "status_counts": {"fresh": 10, "stale": 3},
    "severity_counts": {"ok": 10, "high": 3},
    "stale_or_attention_critical": ["seloger"]
  },
  "sources": [
    {"source": "zimo", "active_rows": 127, "last_seen_at": "...", "age_hours": 12.3, "status": "fresh", "severity": "ok"}
  ]
}
```

Implementation details:

- Classify `fresh`, `aging`, `stale`, `empty`, `unknown` with explicit thresholds.
- Treat “stale” as “investigate”, not as “delete/disable rows”.
- Be schema-tolerant: scraper DBs may not have `fetched_at`; inspect columns before querying optional fields.
- Carry smoke coverage separately from DB freshness: a source can have old rows but still appear in smoke reports, or vice versa.
- Link `/source_health.html` and `/source_health.json` from the main dashboard.

## P1 — Mobile UX and lightweight map filters

For static dashboards, prefer a lightweight region/commune map panel before full geocoding. Exact map markers are fragile when source addresses are incomplete.

Recommended behavior:

- show region/sector tiles with counts from canonical non-hidden listings;
- click a region tile to set `state.region=[region]`;
- **reset conflicting narrower filters** (`zones=[]`, `commune=[]`) when the map changes region;
- allow clicking the active tile again to clear region;
- run both dirty-state and fresh-state QA, because persisted localStorage filters can create zero-result false negatives.

Pitfall: adding a region tile on top of existing default zones can yield `0` results (e.g. default Nord zones + clicked Sud). The map click must reset narrower filters or clearly show that filters are being intersected.

Mobile QA gates:

- emulate a narrow viewport (e.g. 390x844);
- verify mobile actions are visible;
- filters are closed by default and open as a drawer;
- map tiles are tappable;
- after tapping a region, visible count is plausible and localStorage has clean state.

## P2 — Static saved-search cockpit and smart alerts

When the dashboard is static/public and there is no auth admin, do **not** expose server mutation. Build a safe cockpit that inspects and prepares configuration:

- `saved_searches_admin.json`: dry-run counts, sample matches, alert policy;
- `saved_searches.html`: human cockpit with links, JSON draft builder, copy/download buttons;
- production config changes still happen through file deployment or reviewed patch.

Alert digest improvements:

- keep first-run/bootstrap silent;
- emit only useful new canonical matches and selected history events;
- do not send price increases by default;
- include why/score/source context in each line so Telegram alerts are decision-useful;
- make thresholds configurable (`min_score`, `notify_price_increases`) without code patches.

Anti-spam QA:

- run the wrapper and assert `stdout_len=0` when no new useful result exists;
- dry-run saved searches and record match counts;
- test event digest with a fixture for price drop/status events;
- verify `seen` state is not corrupted.

## Public QA checklist

After build, verify local and public artifacts:

```bash
python3 -m py_compile src/*.py scripts/*.py tests/*.py
python3 tests/audit_source_health.py
python3 tests/audit_saved_search_admin.py
python3 tests/audit_search_alerts.py
python3 tests/audit_listing_history.py
python3 tests/audit_listing_changes.py
python3 src/build_app.py
bash deploy/qa-public.sh
```

Then browser-check the exact public URL:

- dashboard loads with console OK;
- source health page shows source KPIs and rows;
- saved-search cockpit parses its JSON draft and shows real counts;
- mobile viewport renders mobile controls and drawer;
- map click updates count and persisted state cleanly;
- `source_health.json`, `saved_searches_admin.json`, `changes.json`, `listings.json` all return HTTP 200.

## Handoff stance

Be direct in the final recommendation:

- “DB stays” if freshness/product semantics are the real bottleneck.
- Name stale sources explicitly.
- Separate delivered P0/P1/P2 from remaining scraper repair work.
- Include exact URLs and QA outputs, not just descriptions.
