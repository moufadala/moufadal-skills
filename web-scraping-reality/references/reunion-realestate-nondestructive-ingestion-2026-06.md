# Réunion real-estate scraper hardening — non-destructive ingestion pattern

Context: session implementing a production-ish rental watcher for La Réunion across HTML/RSS sources. This reference captures reusable scraper/lifecycle patterns, not the one-off run narrative.

## Durable technique

### 1. Source-by-source lifecycle, never global stale
When an orchestrator refreshes multiple sources, mark old listings inactive only for sources that were successfully fetched and parsed in the current run.

Required per-source result shape:

```json
{
  "source_status": {
    "zimo": {"ok": true, "count": 96},
    "superimmo": {"ok": false, "count": 0, "error": "HTTP 503"}
  },
  "by_source": {"zimo": 96}
}
```

Safe stale rule:

```python
for source, status in source_status.items():
    if status.get("ok") and status.get("count", 0) > 0:
        mark_not_seen_as_inactive(source, refresh_started_at)
```

Pitfall: if source A succeeds and source B 403s/timeouts, a global `seen_last_at < run_started_at` update will create false disappearances for source B.

### 2. Treat partial success as normal
A multi-source scraper should return `ok=true` for the runner if at least its process completed and produced structured JSON, while recording per-source failures in `errors`/`source_status`. The orchestrator then decides lifecycle per source.

### 3. IRI / Unicode URL handling
French real-estate URLs may contain raw Unicode path segments (`la-réunion`). Python `urllib.request` can fail with `UnicodeEncodeError` in the request line. Normalize before `Request`:

```python
from urllib.parse import urlsplit, urlunsplit, quote
parts = urlsplit(url)
url = urlunsplit((
    parts.scheme,
    parts.netloc,
    quote(parts.path, safe='/%'),
    quote(parts.query, safe='=&?/%'),
    parts.fragment,
))
```

### 4. Rent parsing order
Avoid parsing the first number in the entire HTML page; related listings, rooms, postcode, fees, or surface often appear before the actual rent.

Preferred order:
1. title / structured metadata
2. description / OpenGraph description
3. explicit `loyer|prix ... €` snippets
4. full page fallback only if constrained to plausible rent range

Example helper:

```python
def parse_rent_eur(text):
    candidates = []
    for m in re.finditer(r'(?:loyer|prix)[^0-9€]{0,40}([0-9][0-9\s.,]{1,8})\s*(?:€|eur)?', text, re.I):
        candidates.append(m.group(1))
    for m in re.finditer(r'([0-9][0-9\s.,]{1,8})\s*(?:€|eur)', text, re.I):
        candidates.append(m.group(1))
    for raw in candidates:
        val = to_int_price(raw)
        if val and 250 <= val <= 6000:
            return val
    return None
```

### 5. WordPress/JS embedded listing URLs
Some real-estate sites do not expose plain anchors; URLs can be escaped inside JSON blobs, e.g. `https:\/\/domain\/post_type_annonces\/...`. Search escaped forms and unescape before fetching.

### 6. QA gates before declaring production-ish
Run these minimum checks:
- `python -m py_compile` on modified scripts, using `PYTHONPYCACHEPREFIX=/tmp/...` if script directory is not writable.
- Dry-run scrapers and inspect `by_source`, `source_status`, and `errors`.
- Real refresh against DB with backup path recorded.
- Lifecycle unit/smoke test proving blocked source remains active while touched source can mark stale rows inactive.
- Browser-open generated HTML artifact or screenshot to verify dashboard renders.

## Example lifecycle smoke test

```python
res = mark_stale_not_seen(db, '2026-06-01T00:00:00+00:00', ['zimo'])
states = dict(con.execute('select source_site||":"||source_id,is_active from rental_listings'))
assert states['superimmo:old'] == 1  # untouched/blocked source preserved
assert states['zimo:old'] == 0       # touched stale row inactivated
assert states['zimo:new'] == 1       # fresh touched row active
```
