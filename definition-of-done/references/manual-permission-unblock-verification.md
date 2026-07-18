# Manual permission unblock verification pattern

Use this when a task is blocked because the user must perform a host/root/manual action, then confirms it was done.

## Pattern

1. Treat the user's confirmation as a signal to **verify immediately**, not as completion by itself.
2. Re-run the exact blocked check from the agent environment, not only a generic `ls` or narrative check.
3. Re-run the higher-level audit/test suite that previously failed because of the block.
4. Save a small machine-readable proof artifact when the task is part of a larger delivery.
5. Only then change status from `blocked by external action` to `corrected/complete`.

## Example from a skills audit

A root-owned skill file was unreadable from Hermes. The user changed host permissions from the host-mounted path. The correct completion sequence was:

- verify permissions from Hermes path;
- re-run the skills/routing audit script;
- confirm `flagged=0` and route tests pass;
- update the final status and attach the audit log/proof.

The durable lesson is not the specific host path or chmod command. The durable lesson is: **manual unblocks must be followed by the same failing check plus the parent audit before declaring done**.
