# Static real-estate dashboards — listing history and price/status events

Use this reference after a static scraper-backed immo dashboard already has a clean product export and saved-search alerts. It captures the next class-level step: add historical state without prematurely migrating the whole stack to a backend database.

## Product decision

Do **not** migrate from SQLite/Postgres or add user accounts just to support price-change awareness. For a V1 static dashboard, add a small auxiliary history SQLite database fed from the generated `listings.json` export.

This enables:

- new listing baseline tracking;
- price changed events;
- disappeared listings;
- reappeared listings;
- source stability monitoring;
- later Telegram/email digest enrichment;
- a lightweight public/admin change journal for inspection without opening SQLite.

Keep it separate from the raw scraper DB and product enrichment DB unless there is a clear concurrency/API requirement.

## Minimal architecture

```text
artifacts/app/listings.json
  -> src/listing_history.py
  -> /opt/data/artifacts/<project>-alerts/history.sqlite
       listing_current
       listing_events
  -> src/search_alerts.py reads matching events for digest enrichment
  -> src/listing_changes.py exports artifacts/app/changes.json
  -> build_app.py embeds summary in listings.json.meta.recent_changes and links /changes.json
```

Tables:

- `listing_current`: one row per stable listing ID, with `first_seen_at`, `last_seen_at`, `active`, `rent_eur`, title, URL, source, region/commune, and raw JSON.
- `listing_events`: append-only events such as `new`, `price_changed`, `disappeared`, `reappeared`.

## Acceptance contract

- Do not mutate the raw scraper table.
- Read from the same JSON export the public UI uses, so history matches the visible product perimeter.
- Use stable listing IDs, not row order.
- First run initializes a baseline; do not send all baseline `new` events as user notifications unless explicitly requested.
- Events can be logged/stored before they are exposed in the user digest.
- The cron wrapper must keep stdout reserved for user-facing notification text only.
- For public/admin inspection, expose a small derived JSON (`changes.json`) rather than forcing the user to inspect SQLite.
- Exclude baseline `new` events from the public “recent changes” journal; include them only in an audit/count field so an empty change journal is explainable.

## CLI/script behavior

A useful `listing_history.py` should support:

```bash
python3 src/listing_history.py \
  --source artifacts/app/listings.json \
  --db /opt/data/artifacts/immo-alerts/history.sqlite \
  --snapshot-at 2026-06-24T00:00:00+00:00
```

Normal manual output can be JSON summary:

```json
{
  "counts": {
    "new": 735,
    "price_changed": 0,
    "reappeared": 0,
    "disappeared": 0,
    "unchanged": 0,
    "processed": 735
  },
  "active_current": 735,
  "event_counts": {"new": 735}
}
```

But in cron, redirect this summary to a logfile so it does not become a Telegram notification.

## Public/admin `changes.json` pattern

After history exists, add a deterministic exporter such as `src/listing_changes.py`:

```text
history.sqlite listing_events/listing_current
  -> artifacts/app/changes.json
```

Recommended payload shape:

```json
{
  "meta": {
    "ok": true,
    "db": "/opt/data/artifacts/immo-alerts/history.sqlite",
    "current_rows": 735,
    "active_rows": 735,
    "latest_event_at": null,
    "limit": 80,
    "note": "Baseline new events are intentionally excluded; this file exposes only price/status changes."
  },
  "summary": {
    "total_events": 0,
    "by_type": {},
    "all_history_counts": {"new": 735},
    "price_drops": 0
  },
  "changes": []
}
```

Rules:

- Include only user-meaningful event types in `changes`: `price_changed`, `disappeared`, `reappeared`.
- Count price drops separately from all price changes if the user cares mainly about opportunities.
- Keep `summary.all_history_counts` for auditability so `changes=[]` is not mistaken for a broken pipeline.
- Wire generation into the normal app build, not a separate manual step.
- Add a simple UI link (`journal changements`) before building a full panel; avoid extra UI complexity until real events exist.
- Mirror the summary into `listings.json.meta.recent_changes` so future UI work can read it without another fetch.

## Digest enrichment pattern

When enriching saved-search alerts from history:

- Compute `since` per saved search from the same state file used for anti-duplication.
- Filter price/status events through the saved-search predicate where possible; do not broadcast every global event to every search.
- Send price drops, reappearances, and useful disappearances; suppress price increases by default unless the user explicitly asks for market trend noise.
- Preserve the anti-spam invariant: if there are no new listings and no relevant events, cron stdout must be empty.

## Cron integration pattern

If an alert wrapper already runs after the scrape/build pipeline, prepend the snapshot step:

```bash
cd /path/to/project
python3 src/listing_history.py >>"$LOG" 2>&1
python3 src/search_alerts.py
```

Rules:

- `listing_history.py` output goes to logs.
- `search_alerts.py` stdout remains the notification channel.
- Verify wrapper direct execution with `stdout_len=0` when nothing new should be delivered.

## Deterministic audit

Use a temporary JSON export and temporary SQLite DB. The audit should simulate:

1. first snapshot creates N `new` events;
2. second snapshot changes one rent and removes one listing;
3. assert `price_changed == 1` and `disappeared == 1`;
4. third snapshot restores the removed listing;
5. assert `reappeared == 1`;
6. inspect SQLite directly for required event types.

Add a separate `changes.json` audit with a temporary history DB:

1. insert baseline `new` events and useful events (`price_changed`, `disappeared`, `reappeared`);
2. assert baseline `new` does **not** appear in `changes[]`;
3. assert old/new prices are present for `price_changed`;
4. assert price drops are counted;
5. assert `all_history_counts.new` remains visible for audit.

Suggested QA bundle:

```bash
python3 -m py_compile src/listing_history.py src/listing_changes.py src/search_alerts.py
python3 tests/audit_listing_history.py
python3 tests/audit_listing_changes.py
python3 tests/audit_search_alerts.py
python3 tests/audit_db_enrichment.py
python3 src/build_app.py
python3 tests/audit_filters_v3.py
python3 tests/audit_app_features_v4.py
bash deploy/qa-public.sh
/opt/data/scripts/immo_saved_search_alerts.sh >/tmp/immo_alert_out.txt
printf 'wrapper_stdout_len=%s\n' "$(wc -c </tmp/immo_alert_out.txt)"
```

Also verify the deployed JSON endpoints directly:

```bash
curl -fsS https://<public-host>/changes.json
curl -fsS https://<alternate-host>/changes.json
```

## Pitfalls

- Do not call baseline `new` events “fresh alerts”; they are historical initialization.
- Do not expose baseline `new` events as “recent changes” in public/admin JSON; that creates a false 700+ item change log.
- Do not interpret `changes=[]` as failure when `all_history_counts` shows only baseline `new` events.
- Do not expose price-drop alerts before testing event filtering against saved searches; otherwise the digest becomes noisy.
- Do not treat missing IDs or unstable regenerated IDs as reliable history; first verify identity stability.
- Do not log operational wrapper lines to stdout under Hermes `no_agent=True` cron; stdout is the user notification channel.
- Do not track all raw scraper rows if the public app only shows a product-filtered export; mismatched perimeters confuse counts.
- Do not overbuild a UI panel before there are real price/status events; start with JSON + one visible link, then add UI once the data proves useful.

## Next product step

Once history exists, enrich the saved-search digest with:

- new matching listings;
- price drops on matching/currently saved listings;
- reappeared listings;
- optional disappeared notices only if they help the user, not as daily noise.

After `/changes.json` is wired, the next useful UX increment can be a lightweight `/changes.html` even before real price/status events exist, **if** it is framed as a readable inspection surface rather than a new product surface. Keep the JSON contract stable for QA and automation, and have the HTML render a clear empty-state when only baseline `new` events exist.

Recommended `/changes.html` contract:

- generated by the same `src/listing_changes.py` or app build path as `changes.json`;
- links back to `/` and to `/changes.json`;
- shows summary counts: useful changes, price drops, baseline `new` excluded, active listings tracked;
- filters by event type: all / price changes / disappeared / reappeared;
- includes text search over title/location/source;
- renders cards with event label, date, title, location/source, price transition if any, and source link;
- when `changes=[]`, display an explicit empty state explaining that baseline `new` events are intentionally excluded;
- dashboard link should point to `/changes.html`, with `/changes.json` retained for machine inspection.

QA additions for this increment:

```bash
python3 -m py_compile src/listing_changes.py tests/audit_listing_changes.py src/build_app.py
python3 tests/audit_listing_changes.py
python3 src/build_app.py
curl -fsS https://<public-host>/changes.html | grep -E 'Journal|Aucun changement|Baisse de prix'
```

Also open both the dashboard and `/changes.html` in browser QA and verify console JS has zero errors. The audit should use a temporary history DB with a synthetic price drop so the HTML card path is tested even if production currently has no real changes.
