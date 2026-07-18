# Reproducible dashboard/container fix after public verification — 2026-07-08

## Trigger

Use this pattern when a VPS/Docker/public-dashboard task is reported as “fixed”, but a later external check or user challenge shows the runtime is repaired without being reproducibly deployed.

Typical signal from Moufadal: “Donc pas fini ? Ça sert à quoi ? On en est où ? Prend du recul”.

## What happened

A public verification found two issues after an apparently complete VPS/Obsidian cockpit update:

1. Wrong public IPTV hostname was tested (`iptv.*`), while the canonical route was `iptv-moufadal.*`.
2. Hermes dashboard returned HTTP 500 on `/` because BasicAuth was being auto-redirected through the OAuth route `/auth/login?provider=basic`; BasicAuth is password-only and should land on `/login` / `/auth/password-login`.

A runtime patch fixed behavior and an image snapshot was committed, but the active container still showed the old `Config.Image`. That meant the fix was real but not production-finished: a container recreate or upstream/config patch was still required.

## Durable workflow

1. **Do not defend the previous “done”.** Acknowledge the gap: runtime fixed is not the same as reproducible production state.
2. **Define the real completion criterion:**
   - active container `Config.Image` points to the patched/immutable image;
   - endpoint returns expected HTTP status after restart/recreate;
   - logs show no relevant error after the latest mutation;
   - rollback/recreate commands exist;
   - Obsidian/report state no longer says “remaining action”.
3. **Snapshot first:** `docker inspect <container> > before.inspect.json`, save `docker ps`, labels, networks, env count, mounts, entrypoint/cmd, restart policy. Do not print env values in reports.
4. **Recreate one container only** with same labels/network/mounts/restart policy and the patched image. Watch for entrypoint/cmd duplication; if original has `Entrypoint=["bash"]` and `Cmd=["-lc", "exec ..."]`, use `--entrypoint bash <image> -lc 'exec ...'`, not `bash bash -lc ...`.
5. **If recreate fails, diagnose immediately** (`docker logs`, `docker inspect .State.ExitCode`) and either fix the command or roll back; do not leave restart-looping containers.
6. **Verify externally after the final recreate:** `curl -k -L` canonical public URLs, not just localhost/container-internal checks.
7. **Only then clean rollback containers**, keeping inspect/rollback artifacts.
8. **Update Obsidian/report** with the final reproducible state and commit/push if the vault is synced.

## Evidence pattern

Save:

- `before.inspect.json`
- redacted recreate command
- recreate logs
- final `docker inspect` showing `Config.Image=<patched tag>`
- public `curl -L` proof
- log grep showing no recurrence of the original error
- `ROLLBACK.md`

## Pitfalls

- A committed image snapshot is not enough if the running container still uses the old image tag.
- Public route names matter; verify the canonical hostname from Traefik labels before declaring a 404.
- Docker `Config.Image` is part of the Definition of Done for reproducibility.
- Do not leave stopped rollback containers around after a verified recreate unless they are intentionally retained and documented; inspect JSON is usually enough.