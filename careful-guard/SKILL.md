---
name: careful-guard
description: "Garde-fou avant une action potentiellement destructrice, irréversible, affectant une prod, ou de large portée : rm/rmdir, git reset/force-push, DROP/TRUNCATE, suppression d'artifacts/logs/backups, chmod/chown sur de gros arbres, arrêt de services, suppression de volumes Docker, édition de credentials, ou modif hors du projet courant. Barrière de sécurité avant l'appel d'outil."
version: 1.0.0
license: MIT
platforms: [linux, macos, windows]
---
# Careful Guard

## Overview

This skill is the multi-project safety gate for Moufadal's VPS. It adapts the useful GStack ideas behind `/careful`, `/freeze`, and `/guard` into one Hermes workflow.

The goal is not to make work slow. The goal is to prevent beginner-hostile accidents: deleting the wrong project, force-pushing protected history, wiping a database, breaking a live dashboard, or editing outside the intended workspace.

Important limitation: a SKILL.md is an agent workflow, not a kernel-level sandbox. It does not mechanically block tools by itself. Hermes must actively apply this checklist before issuing dangerous tool calls. If a future hard hook exists, this skill defines the policy it should enforce.

## When to Use

Load and apply this skill before any action involving:

- `rm`, `rmdir`, `shred`, `truncate`, broad `find -delete`, cleanup scripts, or deletion of logs/artifacts/backups;
- `git reset --hard`, `git clean`, `git push --force`, history rewrite, branch deletion, or merge bypass with admin privileges;
- SQL `DROP`, `TRUNCATE`, destructive migrations, DB file replacement, or bulk deletes;
- `docker rm`, `docker volume rm`, `docker compose down -v`, service restarts affecting live projects;
- recursive `chmod`, `chown`, `mv`, `cp --remove-destination`, or ownership repair over `/opt/data`, `/opt/hermes`, project roots, skills, memories, cron, or config;
- edits outside the active project directory during project work;
- credential, token, `.env`, Traefik, gateway, cron, or production deployment changes;
- control of a personal phone or browser session where input events could touch banking, payment, identity, authenticator, messaging, purchasing, posting, or other sensitive user actions.

Do not use the full protocol for harmless reads, status checks, tests, or targeted edits in one known file. Still keep normal verification discipline. For phone-control diagnostics, safe read-only checks and explicitly bounded probes are green/yellow, but clicks, typing, app launches, purchases, messages, permission prompts, or sensitive confirmations are red unless the user authorized that exact action in the current turn.

## Safety Levels

Classify the planned action before executing:

### Green — safe, proceed with normal verification

Examples: `git status`, `pytest`, `read_file`, `curl` health check, non-recursive edit to one source file.

### Yellow — reversible but needs snapshot or scope check

Examples: editing several files, replacing a generated artifact, restarting one non-critical service, moving files inside a project.

Required:
- confirm active project path;
- create a small backup or rely on git if tracked;
- state rollback command.

### Red — destructive or production-affecting

Examples: `rm -rf`, DB DROP/TRUNCATE, force-push, deleting Docker volumes, broad chown/chmod, branch protection bypass, production config rewrite.

Required:
- stop and explain exact risk;
- show target path/resource;
- create backup or prove one exists;
- ask for explicit user approval unless the user already explicitly authorized that exact destructive action in the current message;
- execute only the minimal scoped command;
- verify result and rollback path.

## Freeze Boundary Pattern

For project work, set a mental edit boundary:

```text
Active project: /opt/data/projects/<project>
Allowed edits: project files + declared artifact directory
Disallowed unless explicitly approved: ~/.hermes, /opt/data/skills, /opt/data/scripts shared by other projects, Docker volumes, unrelated projects
```

Before writing outside the boundary, say why it is necessary and whether it affects other projects. Prefer a project-local helper over a shared global script unless the user asked for cross-project reuse.

## Pre-Destructive Checklist

Before a Red action, answer these in your own reasoning and expose them briefly to Moufadal:

1. **Target:** exact path, branch, DB table, container, or service.
2. **Scope:** why only this target, not a broader glob/tree.
3. **Backup:** snapshot path, git branch, DB dump, Docker image, or explicit reason no backup is needed.
4. **Rollback:** exact command to restore.
5. **Proof needed after:** status/test/curl/screenshot/log that proves the action worked.
6. **Approval:** explicit user authorization when action is destructive or bypasses a guardrail.

## Safe Command Patterns

Prefer scoped commands:

```bash
# Better than rm -rf artifacts/*
rm -rf /opt/data/projects/my-project/artifacts/app.tmp

# Better than chmod -R a+rX /opt/data
chmod -R a+rX /opt/data/projects/my-project/artifacts/app

# Better than force-push to main
git push --force-with-lease origin feature-branch
```

For database work:

```bash
sqlite3 db.sqlite '.backup /opt/data/backups/db-YYYYMMDD.sqlite'
sqlite3 db.sqlite 'BEGIN; ...; COMMIT;'
```

For Git history rewrites, follow `github-pr-workflow` history rewrite warnings and do not force-push without explicit approval.

## Common Pitfalls

1. **Using broad cleanup because it is faster.** Cleanup is where agents destroy unrelated work. Narrow the target first.
2. **Thinking git protects untracked artifacts.** Generated dashboards, DB files, logs, and screenshots may be untracked; create explicit backups.
3. **Bypassing branch protection because CI is green.** Review requirements are intentional safety policy unless Moufadal explicitly asks to bypass.
4. **Editing shared skills/scripts while working on one project.** Shared changes affect future sessions and other projects; mark them as cross-project and verify triggers.
5. **Assuming a skill can mechanically block tools.** This is policy guidance until a runtime hook enforces it. The agent must self-apply it.

6. **Cleanup reports can be safer than memory.** When the user authorizes generated-artifact cleanup, write a small report with exact target patterns, count/size, before/after disk state, and preserved resources. This makes broad cleanup auditable without turning it into a stale memory entry.
7. **Dry-run target generation must be reused for deletion.** Generate a target list file once, review/count/size it, then delete exactly that list. Avoid recomputing broad globs differently between preview and execution.
8. **Container diagnostics are not host diagnostics.** Before concluding that VPS-level tools like `tailscale`, `systemctl`, `sudo`, or host networking are absent/broken, prove whether Hermes is running inside a container (`/.dockerenv`, Docker-like hostname, PID 1 such as `s6-svscan`). If it is isolated, stop host-level repair attempts and tell Moufadal to open a true SSH root/admin session on the VPS host. Do not install Tailscale inside the Hermes container to “repair” the host node; see `references/hermes-container-vs-host-tailscale-adb-diagnostic-2026-07-01.md`.
9. **Tailscale host changes must preserve existing prefs and Serve routes.** For single-setting changes such as enabling Tailscale SSH on the real VPS host, use `tailscale set --ssh=true` / `tailscale set --ssh=false`, not `tailscale up`, because `up` can reset omitted exit-node/routes/proxy preferences. Snapshot `tailscale debug prefs` before/after, redact keys/profile fields, and verify the safe diff shows only `RunSSH` changed. For `tailscale serve` changes, never use `tailscale serve reset` unless the user explicitly asked to wipe every route on the node. If changing one listener that already exists, direct `tailscale serve --http=PORT http://127.0.0.1:NEW` may fail with `listener already exists`; the scoped safe pattern is snapshot `tailscale serve status --json`, run `tailscale serve --http=PORT off`, then recreate only that listener with `tailscale serve --bg --http=PORT http://127.0.0.1:NEW`. Do not omit `--bg`: foreground Serve can vanish when the tool command times out. Verify unrelated routes are still present and keep the old backend alive until end-to-end client QA passes; rollback is `tailscale serve --bg --http=PORT http://127.0.0.1:OLD`. See `references/tailscale-serve-scoped-route-update-2026-07-13.md`. If Hermes is containerized but has privileged Docker/nsenter access to the host, target PID 1 with an explicit entrypoint (for example `docker run --rm --privileged --pid=host --net=host -v /:/host --entrypoint /usr/bin/nsenter <image> --target 1 --mount --uts --ipc --net --pid sh -lc 'tailscale set --ssh=true'`); never run it in the userspace Tailscale node. For SSH usernames, inspect host users first: if only `root` exists, test `root@vps-hermes-host`; prefer creating a dedicated user later and enforcing it through Tailscale SSH ACLs. See `references/tailscale-ssh-host-activation-2026-07-06.md`.
9a. **Per-capability exit-node proof is not the same as host routing.** When the requirement is “PC exit-node for one capability, datacenter for the rest”, prefer an existing Tailscale userspace SOCKS node and switch only that node’s exit-node with `tailscale --socket=/opt/data/tailscale-userspace.sock set --exit-node=<pc>`, never `tailscale up --exit-node` on the host. Prove the boundary with direct `ifconfig.co` vs `--socks5-hostname 127.0.0.1:1055`, and prove the selected peer with `status --json` (`ExitNode=true`). If PC and phone share the same residential IP, IP equality alone is not proof; pair it with Tailscale selected-node state. For Uptime Kuma heartbeat, bind Kuma to host loopback, use a push monitor with a margin above cron cadence, and do not call the phase done until a real PC cut/recovery Telegram alert is observed. See `references/tailscale-userspace-exit-node-heartbeat-phase-a-2026-07-14.md`.
10. **Docker-published localhost can be a false negative from Hermes.** A service published as `127.0.0.1:PORT->...` on the Docker host may not be reachable at `127.0.0.1:PORT` from inside the Hermes container. Before restarting or “fixing” it, verify with `docker inspect` port bindings, `docker exec <container> curl/wget http://127.0.0.1:<internal-port>/`, and/or the container/network IP. Classify the result as path/namespace ambiguity if the service is healthy inside its container.
11. **Docker container count is a symptom, not the diagnosis.** When Moufadal says there are “20 containers” or Docker is a mess, do a read-only sprawl audit before cleanup. Classify preview/artifact containers, public direct ports, floating tags, memory limits, restart policies, and canonical vs old public routes. Use sandboxed scanners where useful, but keep every stop/rm/restart/prune/Traefik/port change behind explicit approval. See `references/read-only-docker-sprawl-audit-before-cleanup-2026-07-08.md`.
12. **Adversarial VPS audits need targeted permission hardening, not broad chmod.** If a first Docker/runtime audit passes and Moufadal asks to audit “under another angle”, change threat model to security/ops/resilience: sensitive permissions, cron script existence, logs, backups, namespace boundary, Graphify/MCP and cockpit smokes. When hardening secrets, do not use broad filename regexes like `token|secret` across package trees: they catch `tokenizers`, `pydantic_settings`, Node SDK examples, and can break imports. Scope to real auth/config/secrets paths, record permission metadata first, use `/opt/hermes/data` as the Docker host mount for Hermes-visible `/opt/data`, then run runtime smokes. See `references/vps-adversarial-security-audit-permission-hardening-2026-07-08.md`.
13. **Runtime patch is not production-finished if Docker still points at the old image.** When a public/dashboard fix is applied inside a running container and an image snapshot is committed, continue until the active container is recreated from the patched immutable image and `docker inspect` shows `Config.Image=<patched tag>`. Verify canonical public URLs from Traefik labels, not guessed hostnames; a wrong URL can create false 404s while the real service is healthy. Save inspect/recreate/rollback artifacts and remove restart-loop or stale rollback containers after verification. See `references/reproducible-dashboard-container-fix-after-public-verification-2026-07-08.md`.
13a. **Hermes gateway Python deps need both live-runtime and clean-image proof.** When adding Python dependencies to `hermes-gateway` for skills or tools, do not treat `uv pip install` inside the running container as durable. Snapshot first, then build a clean derived image from the original tag and retag the service image for future recreate. Verify both Python entrypoints that may exist in Hermes images: the live terminal runtime `/usr/bin/python3.13` and the image/default venv `/opt/hermes/.venv/bin/python3`; installing only one can create a false pass. If a provider smoke test such as Cloudflare image generation fails with moderation/HTTP error, run a bland alternate prompt before blaming dependencies. See `references/hermes-gateway-python-deps-durable-image-2026-07-16.md`.
14. **Taildrop to Windows is delivery, not execution.** When recovering a remote Windows PC where Hermes can Taildrop files but has no shell, do not assume the helper can choose or run the right script. Modern Tailscale for Windows usually places received files in `C:\Users\<user>\Downloads` (older versions may use Desktop). Provide one friendly-named `.bat` launcher and tell the helper to double-click that file only; the `.ps1` is just the engine and may open in VS Code instead of running. If a screenshot shows VS Code with `INSTALL_*.ps1`, correct course: close VS Code, return to Downloads, run the `.bat` / Run as administrator. For `.bat` launchers invoking Claude Code on Windows, use `call claude ...` because npm-installed `claude` may be `claude.cmd` and otherwise the batch may stop after the first Claude invocation.
15. **Temporary Windows OpenSSH rescue is a red action, not a convenience script.** If Moufadal explicitly asks for broader PC access to repair remote-control failures, create a reversible OpenSSH setup: dedicated key, no password reliance, firewall scoped to known Tailscale VPS IPs, logs on Desktop, and rollback that removes the temporary account/key/firewall rule. Prefer a dedicated non-admin rescue account such as `hermes_rescue` with `Match User` + `%ProgramData%\ssh\...authorized_keys` over repeatedly fighting existing/admin account ACL quirks. Explain the real risk: acceptable for temporary repair via Tailscale, not zero-risk and not a permanent default. Verify with Tailscale ping, TCP port 22, then SSH using the dedicated key before claiming access. See `references/windows-taildrop-openssh-rescue-2026-07-09.md`.
16. **Non-technical helper time is the bottleneck in Windows remote rescue.** When a spouse/helper is clicking files on the PC, budget for one robust launcher, not iterative debugging by screenshots. Use one ASCII-only `.cmd`, success marker, Desktop log, rollback, and include all anticipated keys/paths up front. If a ProgramData `Match User` authorized-keys file is used, remember non-admin SSH later may not be able to add a Termux/S25 key; either include that key in the first admin run or verify a user-profile key path works. Do not claim a newly added key works until a real login with that key succeeds. UAC elevation from SSH is not a fallback; it can require an interactive desktop and fail headlessly. See `references/windows-remote-rescue-helper-fatigue-termux-2026-07-09.md`.
17. **Read-only audit cron jobs still need a mutation boundary.** When Moufadal asks for “audit and report only”, the only allowed mutation is the audit mechanism itself (scripts, artifacts, cron job); audited repos, vaults, MCP configs, other agents, and shared runbooks stay read-only. Use script-only cron for deterministic alerts: empty stdout means silent green, non-empty stdout means a concise red ping, and a separate digest job prints the daily summary. For secret/vault audits, output paths + reasons + counters only, never matched lines or values; prefer `gitleaks --redact` if present and fall back to conservative pattern scans if absent. Match exact repo remotes for named shared repos; do not treat similarly named repos as equivalent. Verify manually before reporting job IDs and provide exact `hermes cron remove <id>` rollback commands. See `references/read-only-socle-audit-cron-2026-07-12.md`.
18. **Recalibrate audit rules to the architecture, not generic cleanliness.** Absence of a repo clone can be expected if another machine is the source of truth; do not turn that into a red incident unless a local clone exists and is dirty/diverged/unpushed. A living Obsidian vault can have normal autosave changes; red should be reserved for divergence, secret-like pending paths, mass deletion/rename, or structural moves on main. For daily doc↔reality checks, scan runbooks/ADR freshness as info, and execute only fenced QA/read-only commands with an explicit allowlist; refuse reprise/restart/destructive/credential commands as info. Avoid false drift from nearby historical words like “broken/fallback”; only non-zero probes or explicit expected-negative contradictions are red. See `references/read-only-socle-audit-recalibration-doc-reality-2026-07-12.md`.
19. **Containerized MCP/proxy repairs need blue/green tailnet discipline.** When a host-run MCP/API service cannot reach a proxy that exists only inside a Docker network, do not “fix” it by publishing private proxy ports or touching the known-good gateway/search stack. First prove the in-network route from a disposable container on the target network, then present a STOP-list before any container recreation or `tailscale serve` mutation. Prefer a parallel new container on a new localhost port, keep the old host/stdin fallback alive, switch only the single tailnet route after QA, and never use `tailscale serve reset` for a one-route repair. If Hermes runs inside a container, host evidence can be gathered read-only via Docker bind-mount `/host:ro` and `nsenter` into PID 1; missing host tools inside Hermes are not proof they are missing on the host. See `references/containerized-mcp-egress-tailnet-stop-list-2026-07-13.md`.
19a. **Read-only anti-drift audits must prove both host and runtime perspectives.** When auditing shared skills, cron, MCP, or Hermes runtime from a containerized Hermes session, explicitly distinguish: host paths such as `/opt/hermes/data/...`, runtime paths such as `/opt/data/...`, and Docker bind mounts. A symlink that is valid on the host can be broken inside Hermes if it targets a host-only absolute path; verify with the actual skill loader (`skill_view`/`hermes skills list`) before claiming “active after reload”. For git remotes, do not require literal `github.com` in the URL: SSH aliases like `git@github-skills:owner/repo` are valid, so match the `owner/repo` identity or resolve the SSH config. Secret scans must fail-loud or downgrade when the scanner is absent and zero files were scanned; a green result with `tracked_files_scanned=0` is a false assurance. If QA commands run under `bash -lc`, PATH may differ from direct `execvp`; a `command not found` red is not conclusive until the absolute binary path or controlled PATH has been tested. MCP stdio smokes should use the server's expected framing; if `Content-Length` fails but newline-delimited JSON initialize succeeds, classify the former as probe framing error, not server failure.
20. **Phase-gated Tailscale egress tasks stop on missing exit-node proof.** If a plan requires a specific exit-node class (for example a PC residential exit-node) and the live tailnet only shows another path (for example an Android/S25 SOCKS proxy), do not substitute the available path or deploy adjacent monitoring to look productive. First prove the intended peer has `ExitNodeOption=true`, then prove the real outgoing IP from the exact per-capability context. If that precondition fails, report `blocked` with the exact activation step and stop; routing the whole VPS or reusing a different residential proxy violates the boundary.

## Verification Checklist

- [ ] Safety level classified.
- [ ] Active project boundary known.
- [ ] Backup/snapshot exists for Yellow/Red changes.
- [ ] Red action has explicit current-user approval.
- [ ] Command scope is narrow and quoted.
- [ ] Rollback command is documented.
- [ ] Post-action verification ran and produced real output.

## References

- `references/generated-artifact-cleanup-after-disk-full-2026-06-30.md` — prior concrete cleanup pattern for generated artifacts after disk pressure.
- `references/vps-disk-cleanup-audit-2026-06-30.md` — concrete pattern for VPS disk-space cleanup when the user asks for “gros ménage” without exact deletion targets: inventory first, write `CLEANUP_PLAN.md`, delete only exact rebuildable temp/cache paths, avoid Docker/project/DB pruning, then produce Markdown/HTML reports with before/after disk evidence.
- `references/disk-cleanup-option-validation-2026-06-30.md` — option-based cleanup approval pattern: present exact target lists and risk levels, accept shorthand option replies (`a`, `B`, `A+B`) as approval for those targets only, reuse a generated `targets.txt` for deletion, and smoke-test affected public services afterward.
- `references/hermes-container-vs-host-tailscale-adb-diagnostic-2026-07-01.md` — environment identity gate for host-level Tailscale/ADB diagnostics: distinguish Hermes container from real VPS host before installing or repairing system services.
- `references/read-only-docker-sprawl-audit-before-cleanup-2026-07-08.md` — read-only Docker sprawl audit pattern before cleanup: classify container count as symptom vs operational drift, collect inspect/stats/log evidence, run sandboxed Gitleaks/Trivy/OpenCodeReview smoke, and require explicit approval before stop/rm/restart/prune or port/Traefik changes.
- `references/vps-adversarial-security-audit-permission-hardening-2026-07-08.md` — second-angle VPS audit pattern after Docker/runtime cleanup: targeted sensitive-permission hardening, broad-regex chmod pitfalls, Docker host-path mapping, Claude adversarial review retry pattern, and mandatory post-fix smokes.
- `references/tailscale-userspace-exit-node-heartbeat-phase-a-2026-07-14.md` — per-capability Tailscale userspace exit-node pattern: switch only the SOCKS node, prove selected PC peer plus real egress IP, configure Uptime Kuma push heartbeat without touching existing containers, avoid host-loopback false negatives and Kuma cron flapping, and keep final status partial until a real PC cut/recovery Telegram alert is observed.
- `references/hermes-gateway-python-deps-durable-image-2026-07-16.md` — concrete pattern for making Python deps durable in `hermes-gateway`: snapshot, install via `uv`, build clean image, verify both `/usr/bin/python3.13` and `/opt/hermes/.venv/bin/python3`, and avoid leaking `.env`.
- `references/read-only-anti-drift-skill-sync-audit-2026-07-18.md` — concrete pattern for adversarially validating anti-drift audits and shared skill sync across host/runtime path boundaries: relative symlinks, actual `skill_view` proof, SSH alias remotes, fail-loud non-vacuous secret scans, and `bash -lc` PATH false reds.
