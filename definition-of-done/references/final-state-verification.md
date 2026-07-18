# Finished means final-state verified

When Moufadal challenges a `partially done` status, the durable lesson is not to soften the wording; it is to avoid stopping before final-state verification when no user decision is needed.

## Checklist before saying finished/100%

- Final state, not intermediate state, has been audited.
- Quality gates/smokes ran after the last fix.
- Background jobs are exited or explicitly listed as still running.
- Remaining items are only true blockers, destructive decisions, or out-of-scope work.
- Evidence paths are included.
- Rollback/reprise command is provided if files/system state changed.

If any safe, reversible, inferable work remains, continue instead of asking for praise/approval or producing a premature final.
