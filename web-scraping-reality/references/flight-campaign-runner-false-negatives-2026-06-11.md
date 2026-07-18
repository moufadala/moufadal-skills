# Flight campaign runner false negatives — RUN routes (2026-06-11)

## Trigger

Use this note when a broad flight scraping campaign reports `winners=[]` or low `ok_hints`, but per-task stdout may still contain live fares.

## What happened

Two consecutive `flight_scraping_campaign_v4_20260611.py` runs launched 79 bounded tasks across French Bee, Air Mauritius, Air Austral, Kayak, and Kiwi.

The JSON summary initially reported no winners in one run:

```json
{
  "winners": [],
  "by_family": {
    "kiwi": {"exit0": 1, "ok_hints": 0},
    "airmauritius": {"exit0": 0, "ok_hints": 0},
    "airaustral": {"exit0": 16, "ok_hints": 0}
  }
}
```

Manual inspection showed this was wrong:

- Kiwi stdout contained top-level `"ok": true`, 22 API itineraries, and `price_eur` values.
- Air Mauritius stdout had `Air Mauritius - vols` plus fare text like `EUR301,70` despite script `exit_code=1`.
- Air Austral stdout had `Air Austral - Vols` / `Air Austral - Calendrier` plus fare arrays such as `à partir de €375,02`.
- French Bee failures were mostly runner/local concurrency issues (`profile already in use`, `TargetClosed`, missing headed/Xvfb context), not proof that the site path was invalid.

## Durable rule

Do not trust a campaign-level `winners=[]` until you inspect representative stdout files and parse full stdout, not just the tail.

Also do not trust a narrow `winners>0` as proof of product readiness. A few successful user-provided examples prove feasibility only. Before saying the flight scraper suite is consolidated, ensure the campaign includes all discovered source families or explicitly labels them `not-run`, `not-found-local-script`, `blocked-antibot`, `bug-local`, or `deferred`.

## Recommended runner logic

When summarizing a task:

1. Read the full stdout file for success signals; use tail only for human preview.
2. Count top-level JSON `ok: true` as success even if the regex did not find `€`.
3. Detect price patterns beyond European suffix form:
   - `"price": 349.52`
   - `"price_eur": "374.985907"`
   - `EUR301,70`
   - `€375,02`
   - `à partir de €375,02`
4. Treat rendered fare pages as partial wins even if the child script exits non-zero:
   - title/text contains `Air Mauritius - vols` and `EUR...`
   - title/text contains `Air Austral - Vols` or `Air Austral - Calendrier` and `€...`
5. Separate source blockages from local runner bugs:
   - site/blockage: Cloudflare 403, `Pardon Our Interruption`, CAPTCHA/bot page, no prices in HTML/API
   - local runner: browser profile already in use, `TargetClosed`, missing Xvfb/headed browser, per-task stdout parser bug

## French Bee concurrency pitfall

French Bee’s working path uses a headed/persistent Chromium profile. In broad campaigns, keep French Bee concurrency at `1` unless each task has an isolated `user-data-dir` and valid Xvfb/headed context.

Observed false-negative errors when concurrency was too high:

- `BrowserType.launch_persistent_context: Opening in existing browser session`
- `TargetClosedError`
- headed browser launched without XServer

## Compact user-facing report shape

For this user, after a broad flight campaign, report:

- verdict first: `winners=[] is reliable` or `winners=[] is false negative`
- top live fares with source/route/date/price/duration
- source classification: `official live`, `aggregator live`, `partial official`, `bot/challenge`, `local runner bug`
- exact artifact path to the compact report
- runner fixes applied or still needed
