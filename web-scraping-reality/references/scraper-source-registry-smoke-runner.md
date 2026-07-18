# Scraper source registry + smoke runner pattern

Use this as the reusable checklist when a scraping project has multiple fragile sources or when the user signals that exploration is scattered.

## Minimal registry fields

- `id`: stable source identifier, not a run timestamp.
- `project`: vertical or product area (`flights`, `immo`, `catalogues`, etc.).
- `priority`: lower number runs first.
- `method`: `api_direct`, `browser_network_capture`, `rss_html_dry_run`, `db_report`, `local_watchdog`, etc.
- `proxy_policy`: `direct`, `never`, `tailscale_mobile`, `self_check`, `auto_script_default`.
- `enabled`: false for known-broken/local-template-missing sources.
- `quick`: true for cheap health gates.
- `timeout_seconds`: short bounded timeout.
- `command`: exact smoke command, with placeholders like `{run_dir}` and `{tailscale_socks}`.
- `success_json_paths`: paths expected in parsed stdout JSON.
- `classification_rules`: map common outcomes to `prod-candidate`, `needs-hardening`, `blocked-antibot`, `bug-local`, `low-value`.

## Runner requirements

A good smoke runner must:

1. Be non-destructive by default: dry-run or DB-report only unless explicitly running a production refresh.
2. Archive per-source `stdout.txt`, `stderr.txt`, `meta.json`, and parsed JSON when available.
3. Write global `SUMMARY.json` and `REPORT.md`.
4. Capture command, exit code, timeout, duration, proxy policy, and artifact directory.
5. Distinguish:
   - `bug-local`: bad path, missing template, proxy not passed to browser, dependency/venv issue.
   - `blocked-antibot`: 403/Cloudflare/CAPTCHA with correct routing and browser evidence.
   - `needs-hardening`: partial success or brittle parser.
   - `prod-candidate`: representative smoke returns usable structured items.
6. For browser/Playwright through phone/Tailscale, pass proxy explicitly (`--proxy` or `chromium.launch(proxy=...)`), never rely only on `ALL_PROXY`.
7. Parse machine output defensively: many scrapers print human logs or Python dicts before the real JSON. Prefer a contract where the scraper prints one final JSON object on the last line, and make the runner scan stdout from the bottom for the last valid JSON line before falling back to blob extraction. Do not let earlier log lines like `{'clicked': True}` make a successful scraper look like `needs-hardening`.
8. When promoting a source, update the registry `command`, `artifact_requirements`, `last_verified_*`, and classification together; stale artefact paths or old disabled commands create false negatives in later gates.

## Promotion gate for browser DOM scrapers

Before a source becomes `prod-candidate`, require:

- representative count of structured items, not just “page loaded”;
- key fields parsed with sanity bounds (e.g. price/surface/URL for real estate);
- sample rows checked against page semantics to catch text-flattening bugs;
- final JSON summary parsable by the smoke runner;
- artefact path stored in the registry.

## User-facing report shape

Keep it compact:

- Files created/changed.
- Command to run the quick gate.
- Real test results and artifact paths.
- Any source disabled and why.
- One recommended next step.

## Pitfall

Do not leave an obsolete direct API scraper enabled just because the browser fallback works. If a template/HAR path is missing, classify it as `bug-local`, disable it in the registry, and document the regeneration step.
