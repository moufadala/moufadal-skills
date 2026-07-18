# Daily scraper gate + proxy propagation pattern (2026-06)

## Trigger

Use when a scraping project already has a mobile/residential/Tailscale proxy and a registry/smoke runner, but the production/daily pipeline still risks bypassing the proxy or running without a preflight gate.

## Durable lesson

A working proxy smoke is not enough. The proxy must be propagated through every orchestration layer that eventually launches the browser, and the scheduler must run a quick gate before the business daily job.

For Playwright/Chromium, a daily shell exporting `ALL_PROXY` is not a reliable contract. Add an explicit CLI argument all the way down:

```text
daily.sh -> pipeline.py --kiwi-proxy ... -> flight_watch.py --kiwi-proxy ... -> kiwi_capture_live.py --proxy ... -> chromium.launch(proxy={...})
```

Archive the generated task list/manifest and verify it contains the final `--proxy socks5://127.0.0.1:1055` command. Do not rely on source inspection alone.

## Implementation checklist

1. **Patch the leaf scraper first**
   - Leaf browser scraper accepts `--proxy` or `PLAYWRIGHT_PROXY`.
   - It passes the proxy to `chromium.launch(proxy={"server": proxy})`.

2. **Patch the family orchestrator**
   - Add an explicit `--<source>-proxy` argument, e.g. `--kiwi-proxy`.
   - Append `--proxy <value>` to the leaf command only when set.
   - Write a `tasks.json`/manifest containing the exact command.

3. **Patch the business pipeline**
   - Add the same proxy argument to the pipeline layer.
   - Pass it to the family orchestrator.
   - Persist the pipeline manifest with command arrays.

4. **Patch the daily shell/cron wrapper**
   - Pass the stable proxy endpoint explicitly, e.g. `--kiwi-proxy socks5://127.0.0.1:1055`.
   - Avoid VPS-wide proxy environment unless explicitly required and verified.

5. **Add a quick gate before the daily job**
   - Script should run the registry quick smoke.
   - Success must be silent if used with cron `no_agent=true`.
   - Failure should print a compact alert with artifact path and tail log.
   - Schedule it shortly before the business daily, not after.

6. **Verify through the scheduler path**
   - Shell-smoke the script.
   - If the scheduler expects scripts under a specific directory, place the wrapper there as well as any profile-local script directory.
   - Check cron `last_status`; if it is `error`, fix the wrapper path before adding more jobs.

7. **End-to-end proof**
   - Run the full pipeline manually once with the proxy argument.
   - Verify `manifest.json`/`tasks.json` contains the proxy at the leaf command.
   - Verify business output still works: dashboard/report/telegram summary generated, source counts nonzero.

## Common pitfall: wrapper path mismatch

A script can pass in shell but fail under Hermes cron if the scheduler resolves relative script names under `/opt/data/scripts/` while the wrapper was written under `.hermes/scripts/` or vice versa. The durable fix is not “cron is broken”; create the wrapper in the scheduler-resolved script directory and then force/list a cron run to confirm `last_status=ok`.

For RUN Watch specifically, keep `/opt/data/scripts/reunion_watch_daily.sh` and `/opt/data/.hermes/scripts/reunion_watch_daily.sh` byte-identical when the cron wrapper is expected to mirror the source script:

```bash
install -m 755 /opt/data/scripts/reunion_watch_daily.sh /opt/data/.hermes/scripts/reunion_watch_daily.sh
cmp -s /opt/data/scripts/reunion_watch_daily.sh /opt/data/.hermes/scripts/reunion_watch_daily.sh
```

Then rerun the business QA or equivalent wrapper-sync check before declaring the daily path fixed.

## Common pitfall: root-owned `__pycache__` false negatives

If smoke/daily runners execute many Python scrapers under `/opt/data/scripts`, a root-owned or non-writable `__pycache__` can create misleading failures like `Permission denied: ... .pyc`. Do not classify this as a scraper/site failure.

Durable mitigation for orchestrators and cron wrappers:

```bash
export PYTHONDONTWRITEBYTECODE=1
export PYTHONPYCACHEPREFIX="${PYTHONPYCACHEPREFIX:-/tmp/pycache-hermes}"
python3 -B /opt/data/scripts/scraper_smoke_runner.py --quick --max-workers 2
```

Also pass the same environment into subprocess-based orchestrators (`subprocess.run(..., env=env)`), because setting it only in the parent shell may not protect leaf scrapers launched by Python runners.

## Verification ladder after patching a daily scraping path

After changing proxy propagation or runner hardening, verify in this order:

1. Direct family run, e.g. `flight_watch.py --skip-frenchbee --kiwi-proxy socks5://127.0.0.1:1055`.
2. Inspect the family `tasks.json`; require the leaf command to contain `kiwi_best_effort.py ... --proxy socks5://127.0.0.1:1055`.
3. Run the business pipeline quick mode and inspect `manifest.json`; require the pipeline command to contain `--kiwi-proxy` and the nested flight `tasks.json` to contain leaf `--proxy`.
4. Run the quick gate script used by cron; success should be silent for `no_agent=true` jobs and should write an artifact log with counts.
5. Run business QA if present; fix wrapper sync / dashboard / summary regressions before reporting completion.

## Reporting to the user

Use a compact but accountable format:

- conflict found/fixed;
- files patched;
- exact run directories;
- counts (`6/6 prod-candidate`, `2/2 prod-candidate`, etc.);
- proof path showing the proxy argument in the final task list;
- remaining caveat: a successful anti-bot run is evidence for this run, not a permanent guarantee.
