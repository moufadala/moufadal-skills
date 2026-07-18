# True-100 skill-library audit pass

Use this reference when a skill-library cleanup/audit pass reports residual warnings but the remaining work is safe, inferable, and reversible.

## Lesson captured

If the user asked not to stop until done, a partial report is not an acceptable stopping point unless a real user decision/blocker is required. Continue in background with `notify_on_complete` for bounded long-running work, then verify and report only after gates pass or a blocker genuinely needs the user.

## True-100 contract for skill cleanup

A pass can be called `100%` only when all of these are true:

1. Snapshot/rollback exists before edits.
2. Current audit inventory is regenerated after fixes.
3. Residual errors/warnings are either:
   - fixed, or
   - explicitly reclassified as false positives/intentional with the auditor policy updated so they no longer appear as warnings.
4. Quality gates pass after the final state, not only after the initial safe fixes.
5. Any background worker has exited; no silent unfinished process remains.
6. Final report points to evidence files: final audit, final inventory, gate logs, smoke logs, and rollback command.

## Pitfall

Do not label `partiellement terminé` and stop just because remaining items are less automatable. If they can be handled by a targeted safe pass, continue. Ask the user only for destructive decisions such as deleting duplicate runtime skill roots or changing protected/bundled skills.
