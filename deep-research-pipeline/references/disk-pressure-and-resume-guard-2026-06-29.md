# DeepSearch disk-pressure and resume guard — 2026-06-29

## What happened

A fixed 60-distinct-query DeepSearch V2 benchmark resumed correctly, then crashed after several queries with:

```text
OSError: [Errno 28] No space left on device
```

The failing write was not a retrieval bug: `deep_research_v2.py` was writing raw channel output (`raw_dir / f"{channel}.raw.txt"`). The root cause was VPS artifact pressure, mainly large immo generated backups and app copies under `/opt/data`.

## Durable lesson

For 50–60 query DeepSearch validation, preflight disk and artifact size before launch. A crash-safe benchmark can still fail if raw/evidence files cannot be written. Do not classify this as a V2 quality failure or a provider failure; classify it as infrastructure capacity failure, then resume from artifacts after cleanup.

## Preflight checklist

Before launching or resuming a long DeepSearch benchmark:

```bash
df -h /opt/data
# inspect likely large artifact roots; use project-specific cleanup rules before deleting anything
```

Recommended minimum free space for a 50–60 distinct-query multi-channel run: several GB, preferably >10 GB when raw pages/snippets, HTML reports, and parallel agents are enabled.

## Recovery sequence

1. Inspect `benchmark_summary_partial.json`, `benchmark_rows_partial.json`, and `run.log` rather than trusting a truncated background notification.
2. If the log shows `No space left on device`, stop retrying immediately; retries will only produce more partial/corrupt artifacts.
3. Apply the relevant project cleanup skill/safety gate. For immo-heavy disks, use `reunion-immo-active-watch` + `careful-guard` and ask before broad deletion of old generated backups.
4. Remove only temporary/smoke directories created by the current recovery without asking if they are clearly disposable and scoped.
5. After cleanup, relaunch the canonical fixed benchmark into a new run dir; keep the failed partial run as evidence unless retention pressure requires explicit cleanup.
6. In the final report, distinguish:
   - implementation bugs fixed earlier;
   - infrastructure failure due to disk;
   - benchmark progress before crash;
   - whether a fresh complete run exists.

## Reporting discipline

Do not say “DeepSearch failed again” without classifying the failure. Say for example:

- “V2 resumed; current blocker is disk capacity, not the previous `urlparse` bug.”
- “The partial run reached N/60 distinct queries; no final benchmark exists yet.”
- “Cleanup approval is needed because the free space is locked in old generated artifacts.”
