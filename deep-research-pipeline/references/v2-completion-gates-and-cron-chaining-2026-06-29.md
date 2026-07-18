# DeepResearch V2 completion gates + cron chaining lesson — 2026-06-29

## Trigger

Use this when validating or repairing DeepResearch V2 after a user rejects a “tomorrow / next action” plan and expects the module finished overnight.

## Lesson

Do not declare a DeepResearch module validated just because discovery, scheduling, or a P0 benchmark ran. For V2, the validation must exercise the actual V2 runner and the current completion contract.

## Required V2 fixes before “module validé”

1. **`unique_domains` metric**
   - Compute distinct normalized domains from ranked sources.
   - Report it in every per-query `metrics` block and benchmark row.

2. **Stricter `status=complete`**
   - `complete` must require more than `sources_total >= 4` and one note.
   - Minimum machine checks should include: enough sources, enough domains, at least one fetch attempt, at least one fetched/snippet evidence item, enough evidence notes, and at least one working channel.
   - Persist a `complete_checks` object so the failure mode is visible.

3. **No circular claims**
   - Do not turn extracted evidence notes/quotes into claims and then verify them against themselves.
   - If no user/API claims are provided, the V2 runner may produce evidence notes and a synthesis, but `claims` should remain empty or explicitly externally generated.
   - Claim verification metadata should state automatic claims are disabled.

4. **Real 50–60 distinct-query benchmark after the fix**
   - Use 50–60 unique query strings, not `20 queries × 3 methods` rows.
   - Set `fetch_top > 0`.
   - Track `fetched_ok`, `fetch_attempted`, `notes_total`, `unique_domains`, completion status, and unresponsive/failed engines.
   - Treat a partial run as partial; do not massage it into a final PASS.

## Cron sequencing pattern

If another DeepSearch cron/run is already active, do not create a conflicting benchmark at the same time. List existing cron jobs, identify the in-flight or next DeepSearch run, and schedule the corrected V2 benchmark after it. For example:

```text
existing DeepSearch cron -> fixed V2 60q benchmark -> final report/audit cron
```

For long runs, add a script-only watcher/finalizer that is quiet on success and emits only a compact result or failure digest.

## Smoke proof before overnight benchmark

Before launching the full 50–60q benchmark, run one V2 query with `fetch_top > 0` and verify:

- syntax/import passes;
- `metrics.unique_domains` exists;
- `complete_checks` exists;
- weak evidence leaves `status=partial` when checks fail;
- `claims` does not contain quote-derived circular claims.

## Reporting language

Say: “V2 patched and benchmark launched/scheduled” until the 50–60 distinct-query run finishes and artifacts prove the gates. Do not say “module validé” while benchmark or replay is still running.
