# Authorized generated-artifact cleanup pattern

Session lesson from 2026-06-30 Réunion.

A long benchmark failed because `/opt/data` filled up. User authorized option `1`: clean old generated Immo artifacts and relaunch DeepSearch.

## Safety classification

- Level: Red/Yellow boundary — broad deletion, but limited to generated artifacts.
- Allowed scope: `/opt/data/projects/reunion-immo-search/artifacts/` generated app backups and daily stage replays.
- Preserved explicitly: current `artifacts/app`, code, production DB, recent reports.

## Robust command pattern

1. Generate a target list file under an artifact/report path.
2. Count it and estimate size.
3. Delete exactly the listed paths, not a newly-expanded glob.
4. Append before/after `df -h` and errors to the report.

Why: in the session, the initial preview pipeline accidentally wrote report output rather than a reusable `.targets` file. The safe fix was to create the `.targets` file explicitly, then delete exactly that list.

## Report fields to keep

```text
created_utc=...
created_reunion=...
scope=...
target_count=...
target_size=...
removed_count=...
errors=...
df_before=...
df_after=...
```

## Pitfall

If cleanup is broad and there is no simple rollback, say so plainly. Do not pretend deleted generated artifacts have an easy rollback unless a snapshot/archive exists.
