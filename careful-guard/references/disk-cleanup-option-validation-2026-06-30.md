# Disk cleanup option validation — 2026-06-30

## Pattern captured

When Moufadal asks what to validate for disk cleanup, present cleanup as explicit options with exact targets, estimated gain, and risk. If he replies with a shorthand matching an option (`a`, `A`, `b`, `B`, `A+B`), treat it as explicit approval for that listed option only.

## Safe execution pattern that worked

1. Inventory first with `df -h`, `du -xh --max-depth`, and archive/snapshot discovery.
2. Group deletion candidates by risk:
   - Option A: old archives/snapshots/backups, low risk.
   - Option B: generated daily stages/backups, medium-low risk.
   - Option C: broader project/research artifacts, higher context risk.
3. Wait for user validation of a specific option.
4. Create a run directory under `/opt/data/artifacts/disk-cleanup/<run-id>/`.
5. Write the exact target paths once to `targets.txt`.
6. Generate `precheck.md` containing `df`, per-target `du -sh`, and safety notes.
7. Run assertions before deletion:
   - every target is under the intended base directory;
   - live app/current production path is excluded;
   - names match the option pattern when possible.
8. Delete by reading the previously written `targets.txt`; do not recompute globs at deletion time.
9. Write `deletion.log` and `result.md` with after-`df`, live-artifact checks, and removed-target checks.
10. Smoke test affected public services after cleanup.

## Concrete smoke checks used

- Immo public app: `curl -k -L -sS -o /tmp/immo_smoke.html -w 'HTTP=%{http_code} SIZE=%{size_download} URL=%{url_effective}\n' https://immo.148.230.103.174.sslip.io/`
- IPTV playlist: `curl -k -L -sS -o /tmp/iptv_smoke.m3u -w 'HTTP=%{http_code} SIZE=%{size_download} URL=%{url_effective}\n' https://iptv-moufadal.148.230.103.174.sslip.io/moufadal-tv.m3u`

## Result of this session

- Option A deleted old immo archives/snapshots and freed about 3 GB.
- Option B deleted old generated immo daily stages/backups and freed about 6 GB more.
- Total visible gain: `/opt/data` moved from about 61 GB used / 36 GB free to 51 GB used / 45 GB free.
- The live app path `/opt/data/projects/reunion-immo-search/artifacts/app` stayed present and public smoke tests returned HTTP 200.

## Pitfalls

- Do not delete `artifacts/app` unless the user explicitly asks to remove the live app.
- Do not treat a broad category like “old snapshots” as approval to delete every matching directory. Approval applies only to the listed option targets.
- After direct deletion, rollback is not real; report that honestly and rely on preserved live artifact checks rather than pretending snapshots can be restored.
