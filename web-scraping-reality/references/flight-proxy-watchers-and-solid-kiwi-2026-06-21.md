# Flight scraping — proxy watcher noise + solid Kiwi/official evidence (2026-06-21)

## Trigger
Use this note when working on RUN flight scrapers with Tailscale userspace SOCKS (`127.0.0.1:1055`), Kiwi GraphQL, and official airline consolidation campaigns.

## Lessons captured

### 1) `magicsock` watcher output is not a scraper verdict
Tailscale logs like:

```text
magicsock: adding connection to derp-15
magicsock: closing connection to derp-15 (idle)
magicsock: disco: node [...] now using 80.x.x.x:port
```

are normal path/DERP maintenance noise. Do **not** pause or reclassify a scraper because of this alone.

Required verification before any conclusion:

```bash
printf 'direct='; curl -4 -sS --max-time 8 https://api.ipify.org; echo
printf 'socks='; curl -4 -sS --max-time 12 --socks5-hostname 127.0.0.1:1055 https://api.ipify.org; echo
pgrep -af 'tailscaled --tun=userspace-networking' || true
```

Verdict rule:
- `direct != socks` and `socks` is a mobile/residential IP → proxy path is alive.
- `direct == socks` or SOCKS fails → `network-preflight-failed`, not a scraper/site verdict.

### 2) When the user corrects source scope, expand inventory, but keep a `solid-only` layer
If the user says “there were Kiwi, Skyscanner, and others”, do not keep narrowing to the last two winning official scrapers. Inventory all local/prior sources:

- official airlines: French Bee, Air Austral, Air Mauritius, Corsair;
- aggregators: Kiwi, Kayak, Skyscanner;
- discovery/mobile probes.

But the output must separate:

- **solid**: structured JSON with price + segments + carrier + booking URL, or a functional matrix with per-case artefacts;
- **non-solid**: anti-bot, timeout, missing local template, no local script, parser gap;
- **in progress**: background runs still producing cases.

Do not treat a broad inventory as a success report. Produce a durable `REPORT_SOLID_ONLY.md` when some sources are noisy.

### 3) Fix `bug-local` before declaring a source weak
Observed Kiwi pitfall: `kiwi_direct_search.py` pointed at a stale `/opt/hermes/data/.../result.json` capture. The durable fix was to use the maintained replay template under `/opt/data/artifacts/kiwi-direct-replay/latest_template/request.json`, accepting both current `{url, method, headers, post_data}` and older `{responses:[...]}` capture shapes.

After patching, verify with canonical Kiwi IDs, not ad-hoc strings:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/pycache-hermes \
python3 /opt/data/scripts/kiwi_direct_search.py \
  --date 2026-07-15 \
  --source-id AutonomousTerritory:RE \
  --dest-id City:paris_fr \
  --limit 5 \
  --out-dir /opt/data/artifacts/flight-functional-coverage/kiwi-direct-fixed-$(date -u +%Y%m%dT%H%M%SZ)
```

Expected solid evidence shape:
- `itineraries_count_api` > 0;
- `offers[].price_formatted`;
- `segments[].carrier`, `flight_number`, `from`, `to`, `departure_local`;
- `booking_url`.

### 4) Known false-positive: `Erreur 500` parsed as `eur 500`
For Corsair and similar probes, never classify a price solely by a broad regex over stdout/stderr. If page/title says `Erreur 500`, JSON says `ok=false`, or `prices=[]`, correct the classification to `bug-local-site-error` / `site-error`, not `price-found`.

### 5) Background official matrix status reporting
For long official campaigns, compact progress should include:

```text
completed / total
counts by classification
sources count
routes count
last case id
```

Example classifications to preserve:
- `price-found`
- `no-offer`
- `blocked-antibot`
- `bug-local-*`
- `network-preflight-failed`

Do not stop at “still running”; read `progress.json` and case files if available.
