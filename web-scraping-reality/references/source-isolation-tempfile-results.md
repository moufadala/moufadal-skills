# Scraper source isolation — avoid Queue deadlocks with large payloads

## Pattern

When running one scraper per child process with per-source timeouts, avoid sending large listing payloads through `multiprocessing.Queue`. A child can block while flushing the queue, and the parent may report a false timeout even though scraping completed quickly.

## Safer implementation

- Child process writes its result to a temporary JSON file.
- Parent `join(timeout)` controls the hard timeout.
- If the child exits normally, parent reads the temp JSON.
- If timeout expires, parent terminates the child and records `timeout_after_Ns`.
- Only update DB/source state for sources that completed successfully.

## Acceptance contract

For multi-source scraper refreshes:

- source-level logs include duration, row count, and error/timeout;
- failed sources do not mark their old rows stale/inactive;
- backups exist before DB writes;
- dry-run works for one source and for a slow source;
- a freshness gate validates the post-refresh DB.

## When this matters

Use this when a source appears to timeout in the orchestration wrapper, but the same scraper succeeds quickly in an isolated diagnostic/probe. The orchestrator, not the target site, may be the bug.
