# French Bee hardened rerun after mobile proxy recovery — 2026-06-21

## Trigger

Use this when a flight scraper campaign produced `network-preflight-failed` / empty SOCKS output while the user later says the Android/Tailscale exit node is back online and asks to rerun “maximum tests” / make it “very solid”.

## Durable lesson

Do **not** rerun the entire broad campaign blindly. First prove the mobile egress is active, then replay the failed proxy-dependent cases plus a bounded hardening matrix. Classify previous failures as network false negatives only if per-case artifacts show SOCKS preflight failure, not site/anti-bot/no-offer.

## Required preflight before rerun

```bash
printf 'direct='; curl -4 -sS --max-time 8 https://api.ipify.org || true; echo
printf 'socks='; curl -4 -sS --max-time 20 --socks5-hostname 127.0.0.1:1055 https://api.ipify.org || true; echo
/opt/data/tools/tailscale/tailscale --socket=/opt/data/tailscale-userspace.sock exit-node list
```

Pass condition:

- direct VPS IP differs from SOCKS IP;
- SOCKS IP is non-empty;
- no `curl: (97)` / SOCKS CONNECT failure;
- exit node shows selected.

If this fails, stop and mark `network-preflight-failed`; do not create scraper verdicts.

## Rerun pattern

1. Load prior corrected summary, e.g. `CORRECTED_SUMMARY.json`.
2. Select only French Bee cases whose corrected classification starts with `network-preflight-failed`.
3. Add bounded hardening cases rather than only replaying old failures:
   - RUN→ORY and ORY→RUN;
   - one-way and roundtrip;
   - 7/10/14 nights;
   - summer and holiday windows;
   - 1ADT, 2ADT, 2ADT+children, 2ADT+children+infant;
   - invalid controls after proxy is known-good.
4. Run French Bee **sequentially**. Do not parallelize Chrome/Playwright profile-based airline scrapers; it creates false negatives.
5. For every case, write:
   - `preflight.json`;
   - `stdout.txt`;
   - `stderr.txt`;
   - `case_result.json`;
   - global `progress.json`, `SUMMARY.json`, `REPORT.md`.
6. Re-check direct vs SOCKS during long runs if the user’s phone may move or lose signal.

## Example campaign shape

A successful hardened rerun used 33 French Bee cases:

- 16 previously failed network cases;
- 15 extra hardening cases;
- 2 validation controls.

The first results immediately converted previous network false negatives into `price-found`, proving the original failures were proxy availability, not scraper/anti-bot failures.

## Classification rules

- `network-preflight-failed`: per-case preflight SOCKS empty/same-as-direct/curl SOCKS error.
- `price-found`: actual price strings or JSON price fields in stdout.
- `validation-control-exercised`: invalid input path reached after proxy OK. Count these separately from business cases; do not include invalid controls in the price-found denominator.
- `transient-upstream-502`: upstream booking engine returned an explicit 502/Bad Gateway page while proxy preflight was OK and nearby cases succeeded. Do not misclassify this as anti-bot or no-offer; mark as targeted replay candidate.
- `blocked-antibot`: visible captcha/hCaptcha/Imperva/Akamai/Pardon/access-denied evidence.
- `timeout`: process timeout with proxy OK.
- `failed-unknown`: only after stdout/stderr audit rules out the above.

## Final audit pattern from the 2026-06-21 rerun

After the background process exits, audit every non-price case before reporting:

1. Re-read per-case `preflight.json`, `stdout.txt`, `stderr.txt`, and `case_result.json`.
2. Reclassify generic `failed-unknown` into specific buckets whenever stdout/stderr contains proof.
3. Recompute the denominator as **valid business cases only**; validation controls are out-of-denominator.
4. Patch the Markdown report if wording drifts from corrected counts.

Concrete outcome observed: 33 total cases → 29 `price-found`, 3 `validation-control-exercised`, 1 `transient-upstream-502`; denominator = 30 valid business cases, so verdict = 29/30 prices, not 29/31 or 29/33.

## User-facing reporting

For Moufadal, keep updates compact but evidence-backed:

- say proxy proof first;
- give process/session id and artifact root;
- report `completed/total`, counts, and first concrete prices;
- avoid claiming “all solid” until the campaign finishes and artifacts are audited.
