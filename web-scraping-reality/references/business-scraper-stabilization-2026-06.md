# Business scraper stabilization pattern (immobilier / watchlists)

Session-derived pattern for turning raw scrapers into usable business modules without breaking the existing stack.

## When to use

Use when the user asks for scrapers to be “stabilisés”, “optimisés”, “nettoyés”, “métier”, “fonctionnent parfaitement”, or wants overnight autonomous cleanup/testing.

## Proven loop

1. **Inventory first**
   - Find existing scripts/artifacts/DB before creating anything.
   - Classify sources by real status: OK, transient failure, blocked, untested.

2. **Dry-run each source independently**
   - Compile scripts.
   - Run every scraper in dry-run mode if available.
   - Parse stdout as JSON and record counts, by-source coverage, and errors.
   - Do not trust a source-level runner just because it exits 0: inspect per-source `errors`.

3. **Add an orchestrator instead of rewriting source scrapers**
   - Keep source scrapers small and independently testable.
   - Orchestrator responsibilities: backup DB, run sources, normalize report outputs, query DB, score listings, write JSON/Markdown reports.
   - Always save artifacts under a timestamped run directory plus a `latest_*` symlink.

4. **Backup before refresh**
   - Copy SQLite DB to a run-local timestamped backup before any write refresh.
   - Never delete rows during stabilization.

5. **Stale lifecycle: only mark sources actually touched**
   - Mark old rows `is_active=0` only for sources that produced valid results in the current run.
   - If a sub-source fails with 429/403/CAPTCHA while the wrapper exits 0, do **not** mark that source inactive.
   - Preserve history; business reports should query `is_active=1` by default.

6. **Business filters before “top picks”**
   - Exclude irrelevant categories by default for residential rental alerts: bureau/bureaux, local commercial, commerce, fonds de commerce, terrain, box, garde-meuble, parking.
   - Exclude chambre/colocation by default unless explicitly requested.
   - Add guardrails for implausible parsed prices (example: min rent 450€ for Réunion residential) to avoid stale parser false positives.

7. **Deduplicate at business level**
   - Source IDs are not enough. Aggregators often repeat the same listing with different IDs/titles.
   - Dedup report candidates by normalized city + rent + surface + rooms, then keep the highest-scored/most complete row.

8. **Score, don’t just sort newest**
   - Useful fields: budget bands, surface bands, rooms, €/m², image present, description present.
   - Report the flags that explain the score.

9. **Retest transient sources later**
   - For 429/rate limits, schedule a delayed retry in an overnight runner.
   - Generate multiple business report variants from the final DB: budget 900, budget 1200, T2+ etc.

## Report shape preferred by this user

- Verdict/status first.
- Counts by source and quality metrics.
- Top listings as compact bullets with source, city, rent, surface, score, URL.
- Put full details in artifacts, not a long chat wall.

## Pitfalls

- Do not mark a source stale just because a wrapper script ran; inspect nested errors.
- Do not let technically cheap categories (box, office, room share) dominate residential rankings.
- Do not overwrite or prune historical DB rows during cleanup unless user explicitly approves.
- Do not treat scraper success as business success until selected listings look plausible.
