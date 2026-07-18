# Static real-estate dashboards — saved-search alert engine

Use this reference after a static immo dashboard already has clean listings, canonical/default views, and shareable URL state. It captures the safer next product step: alerts based on saved searches, without prematurely adding a backend/email stack.

## Product decision

For real-estate portals, a saved search is a set of filters/location that the user can revisit and optionally receive updates for. Alert value should start with **new listings matching saved criteria**. Price-drop/status alerts can come later if historical snapshots are available.

Do **not** jump directly to a full account/email backend for a V1 static scraper-backed dashboard. Prefer a small server-side matching script that reads the generated JSON/export and emits a notification-ready digest only when new matching listing IDs appear.

## When to use

Use this pattern when:
- the dashboard has bookmarkable/shareable URL state;
- listing IDs are stable enough across builds;
- there is a generated JSON export (`listings.json` or equivalent);
- the user wants progress toward alerts/monitoring;
- recurring notifications are acceptable only if silent when nothing changed.

Avoid if:
- IDs are unstable or regenerated randomly each run;
- duplicates/canonicalization are not solved;
- there is no reliable refresh/build pipeline yet;
- the user has not approved recurring delivery.

## Minimal architecture

```text
project/
  config/saved_searches.json       # named searches + filters + public base URL
  src/search_alerts.py             # reads export, matches searches, updates seen state
  tests/audit_search_alerts.py     # dry-run + anti-spam regression
/opt/data/artifacts/<project>-alerts/seen.json
```

The alert script should support:
- `--dry-run`: inspect matches without writing state;
- first real run bootstraps `seen.json` silently;
- `--notify-initial`: optional override to emit current matches on first run;
- `--verbose`: print JSON control output when no notification is emitted;
- normal mode: print a Telegram-ready digest only when new matching IDs exist; empty stdout means no message for `cron no_agent=True`.

## Matching contract

Default filters to mirror the static UI:
- region(s);
- zones / communes;
- property type;
- furnished status;
- rent min/max;
- surface min;
- rooms/bedrooms min;
- free-text query if supported;
- sort order.

For immo dashboards with canonicalization, alerts should usually ignore non-canonical listings:

```python
if item.get("db_is_canonical") is False:
    return False
```

This avoids sending near-duplicates or suspect/commercial items after the clean-default product work.

## URL state integration

Each saved search should produce the same restorable public URL that the dashboard understands, e.g. `?immo=1&r=Nord&rentMax=1000&surfaceMin=60`. QA must open at least one generated URL and verify that the browser restores filters and count.

## Anti-spam QA gate

A useful regression test should use a **temporary state file** and assert:
1. `--dry-run` returns JSON with configured searches and non-empty match counts.
2. First non-dry run creates the state file but prints nothing.
3. Second run with `--verbose` reports `new: 0`.
4. Search URLs include the dashboard state marker (`immo=1` or project equivalent).
5. Public dashboard/build QA still passes after adding the alert script.

Example command bundle:

```bash
python3 tests/audit_search_alerts.py
python3 src/search_alerts.py --dry-run
python3 src/search_alerts.py
python3 src/search_alerts.py --verbose
python3 src/build_app.py
python3 tests/audit_app_features_v*.py
bash deploy/qa-public.sh
```

## Cron pattern

Only schedule recurring delivery after user approval. Use `cron no_agent=True` if the script already prints the exact message text:
- non-empty stdout = deliver digest;
- empty stdout = stay silent;
- non-zero exit = alert that the watchdog broke.

Schedule it **after** the scrape/build pipeline, not before, so it sees the latest export. If an existing daily pipeline runs at `HH:MM`, schedule the alert job a few minutes later and document the dependency in the QA report.

Recommended wrapper contract:

```bash
#!/usr/bin/env bash
set -euo pipefail
umask 077
exec 9>/tmp/immo_saved_search_alerts.lock
flock -n 9 || exit 0
cd /path/to/project
python3 src/search_alerts.py   # stdout must be reserved for the user-facing digest only
```

Important: wrapper operational logs (`start`, `exit=0`, paths, timestamps) must go to stderr or a logfile, **not stdout**. In `no_agent=True`, any stdout is delivered to the user, so even harmless log lines become notification spam.

For Hermes cron, a good job shape is:
- `script`: wrapper name under the scripts directory;
- `no_agent=True`;
- `deliver='origin'` for user-facing alerts;
- a prompt explaining stdout semantics, even though prompt is ignored by script-only mode.

## Product visibility

Do not hide the alert capability only in server scripts. If the dashboard is already public, add a small, non-intrusive indicator sourced from the same config/export metadata, e.g. `Alertes prêtes: 2 recherches surveillées après le refresh quotidien.` QA should verify this text in the public browser and that console JS remains clean.

## Next step: listing history

After saved-search alerts are stable, the next useful product capability is usually historical tracking, not a backend migration. See `references/static-real-estate-listing-history.md` for the auxiliary SQLite pattern that records `new`, `price_changed`, `disappeared`, and `reappeared` events from the same public `listings.json` export.

## QA additions for productionized alerts

Beyond the anti-spam unit test, verify:
1. Wrapper direct execution returns `rc=0` and `stdout_len=0` when there are no new matches.
2. Cron job is listed as active with the intended schedule after the existing scrape/build run.
3. The real `seen.json` has counts matching current searches.
4. Public `listings.json` embeds `meta.saved_search_alerts` or equivalent.
5. Browser page shows the alert readiness indicator and has 0 console errors.
6. Report includes rollback commands, e.g. `hermes cron pause <job_id>` and `hermes cron remove <job_id>`.

A manual `cronjob(action='run')` may only enqueue/re-schedule a job depending on scheduler timing; do not treat a short wait without log movement as proof of failure. The stronger proof is active cron listing + wrapper direct execution + silent stdout + scheduled next run.

## Pitfalls

- Do not notify all current matches on first run unless the user explicitly asks; bootstrap `seen` silently.
- Do not call it “email alerts” unless there is actual email subscription/unsubscribe handling.
- Do not include suspect/commercial/debug listings by default.
- Do not create a cron just because the script exists; recurring user-facing delivery is a product decision.
- Do not let wrapper logs leak to stdout in `no_agent=True`; stdout is the notification channel.
- Do not use transient row order as identity; use stable source/listing IDs.
