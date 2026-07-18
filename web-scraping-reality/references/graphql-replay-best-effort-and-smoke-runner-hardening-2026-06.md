# GraphQL direct replay + browser fallback + smoke runner hardening (2026-06)

## Pattern learned

For fragile web scrapers where a browser capture has already exposed a usable XHR/GraphQL request, prefer a **best-effort wrapper**:

1. Try a fast direct replay from the last captured request template.
2. Require parsed business data, not just HTTP 200.
3. If replay fails or returns no offers/items, launch a bounded browser capture with explicit proxy settings.
4. Save the newly captured winning request back as the replay template.
5. Emit one JSON result with:
   - `mode_selected`: e.g. `graphql_direct_replay` or `browser_capture_fallback`
   - `attempts`: command, exit code, ok flag, item/offer count
   - `result.json` in the run directory
6. In daily/cron jobs, call the wrapper, not the browser script directly.

## Why it matters

This avoids burning Chromium/Playwright on every run while keeping a recovery path when short-lived headers/tokens expire.

## Registry guidance

When a wrapper covers both direct replay and browser capture:

- keep the wrapper source enabled as `prod-candidate` or equivalent;
- mark the standalone browser capture source disabled/manual to avoid duplicate expensive runs;
- document `proxy_policy`, `artifact_requirements`, `qa_gates`, and `next_action` in the registry;
- inspect `mode_selected` in QA reports to know whether the run stayed on fast path or used fallback.

## QA gates

A best-effort replay wrapper should pass these checks:

- direct replay succeeds in a few seconds when template is fresh;
- parsed items/offers count is greater than zero;
- browser fallback passes proxy explicitly to Playwright/Chromium (`launch(proxy=...)` or equivalent), not only `ALL_PROXY`;
- fallback refreshes the template only from a captured request that produced usable data;
- smoke report archives stdout, stderr, parsed JSON, command, duration, and classification.

## Smoke runner hardening

Multi-scraper smoke runners should set `PYTHONDONTWRITEBYTECODE=1` for subprocesses. This avoids false `PermissionError` failures when a shared scripts directory has a root-owned `__pycache__` or a read-only cache path. Treat bytecode cache write failures as local harness noise, not site blocking.

Do not encode a permanent claim that Python/cache is broken; encode the mitigation in the runner.

## Example implementation shape

```python
attempts = []
direct = run(direct_cmd, timeout=70)
attempts.append(attempt_summary(direct))
if direct.exit_code == 0 and has_items(direct.json):
    payload = direct.json
    payload["mode_selected"] = "graphql_direct_replay"
    payload["attempts"] = attempts
    write_result(payload)
    return 0

browser = run(browser_cmd_with_explicit_proxy, timeout=150)
attempts.append(attempt_summary(browser))
if captured_request_exists:
    refresh_template_from_capture()

payload = browser.json or {"ok": False}
payload["mode_selected"] = "browser_capture_fallback"
payload["attempts"] = attempts
payload["template_refreshed"] = refreshed
write_result(payload)
return 0 if has_items(payload) else 2
```
