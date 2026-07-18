# RUN Watch resume/full-run pattern — 2026-06-14

Context: after a terse `Continue`, recent session recovery showed a daily RUN Watch job had been created and a quick daily run existed. The right continuation was not only to report the cron state: the obvious safe next step was to run the full variant once, with French Bee included, then verify artefacts.

## Pattern

1. Recover recent context and cron state.
2. Read latest `telegram_summary.txt`, `manifest.json`, and coherence report before claiming anything.
3. If daily cron is deliberately quick (`--flight-quick`) but a full run is safe and was implied by previous work, launch one manual full run without changing cron.
4. After the full pipeline, run `flight_coherence_check.py` against the produced `flight_run_dir`.
5. Verify dashboard in browser/snapshot and console, not only file existence.
6. If vision analysis provider fails after screenshot capture, do not treat it as dashboard failure: use browser snapshot/console as QA evidence and retain the screenshot path as visual artefact.

## Concrete commands

```bash
STAMP=$(date -u +%Y%m%dT%H%M%SZ)
RUN_DIR="/opt/data/artifacts/reunion-watch/${STAMP}_full_resume"
mkdir -p "$RUN_DIR"
PYTHONUNBUFFERED=1 python3 /opt/data/scripts/reunion_watch_pipeline.py \
  --run-dir "$RUN_DIR" \
  --flight-dates 2026-07-19 \
  --return-date 2026-07-26 \
  --max-price 1200 \
  --min-price 450 \
  --min-rooms 2 \
  --limit 15

FLIGHT_RUN_DIR=$(python3 - <<PY
import json
from pathlib import Path
m=json.loads(Path('$RUN_DIR/manifest.json').read_text())
print(m['flight_run_dir'])
PY
)
python3 /opt/data/scripts/flight_coherence_check.py --flight-run-dir "$FLIGHT_RUN_DIR" --out-dir "$RUN_DIR"
```

## Acceptance evidence from the session

- Full run artefact: `/opt/data/artifacts/reunion-watch/20260614T042416Z_full_resume`.
- Vols: 3/3 `prod-candidate` (Kiwi, Air Austral, French Bee).
- French Bee full scraper still worked: BF705 outbound 349.52 EUR + BF704 return 580.58 EUR = 930.10 EUR roundtrip.
- Air Austral vs Kiwi coherence: 2 exact comparisons, 0 aberrants; deltas 0.88% and -0.45%.
- Immo: 15 selected across 12 sources.
- Browser QA: dashboard title/summary/3 flight cards/immo section present; console JS errors = 0.

## Pitfall

Keep the scheduled daily cron lightweight unless the user explicitly asks otherwise. A manual full run can include French Bee, while the daily `no_agent` cron can stay quick (`--flight-quick`) to avoid slow/noisy daily execution.
