# Max-effort background audits without blocking Telegram

Use this reference when Moufadal asks for a deep/max-effort review or audit, wants Claude Code + Codex involved, and explicitly says he must be able to keep using the current chat for other work.

## Pattern

1. **Ask only the scope questions that change the audit contract**
   - Périmètre: repo only vs repo + scripts + public runtime + GitHub privacy.
   - Axes: prod reliability, product/UX, data/scraping, security/privacy, architecture/code.
   - Mode: audit-only, audit+plan, audit+P0 fixes, or full chantier decisions.
   - Allowed commands: non-destructive tests, public QA, dry-runs only.
   - Workers: Claude, Codex, or both.
   - Deliverable: Markdown, HTML, or both.
   - Timebox: quick, deep, or max-effort.

2. **Convert answers into a written audit contract**
   - Store it under a dated artifact dir, not inside the product repo.
   - Make destructive boundaries explicit: no DB mutation, no live Telegram alerts, no prod publish, no git push unless separately approved.

3. **Create a read-only working mirror**
   - Copy the target repo into `/opt/data/artifacts/<project>_deep_review_<UTC>/repo_mirror/`.
   - Initialize a local git snapshot inside the mirror if helpful.
   - Run Claude/Codex against the mirror so their reads/tests cannot dirty production files.
   - Still record `git status --short` in the original repo before and after to prove the invariant.

4. **Launch the orchestrator in background**
   - Use `terminal(background=true, notify_on_complete=true)` for the long audit script/process.
   - Return immediately with the `session_id`, artifact paths, and a compact Telegram steering update.
   - Do not keep the chat hostage while the audit runs.

5. **Worker split**
   - Claude Code: primary architectural/deep product/quality review.
   - Codex CLI: independent counter-review focused on missed concrete bugs, privacy, false PASS tests, and operational fragility.
   - Hermes: evidence collection, public probes, QA checks, synthesis, and final verification.

6. **Evidence to collect before/alongside agents**
   - Public endpoint probes and JSON parse/count checks.
   - Local app stats: listing count, generated_at, source counts, photo/gallery coverage, description completeness.
   - Targeted gates/tests, with logs saved under `qa/`.
   - Codebase metrics if available.
   - Raw agent outputs under `raw/`.

7. **Final artifact shape**
   - `index.html`: pedagogical, mobile-readable, with sections for verdict, proof, Claude audit, Codex counter-review, QA, read-only invariant, and reprise.
   - `FINAL_REPORT.md`: complete text version.
   - `artifact-manifest.json`: paths to reports, raw outputs, QA logs, git status before/after.
   - `qa/final_artifact_check.json`: existence/size/section checks.

## Telegram response while audit is running

Keep it short and status-oriented:

- `📌 Verdict`: launched/running, not complete.
- `🧭 Où on en est`: background process + artifact dir.
- `✅ Actions faites`: contract, script, background session id, read-only mirror.
- `⚠️ Limites`: report not ready yet; worker auth/quota may fail and logs will show it.
- `📎 Preuves`: artifact dir, expected HTML/MD, log path.
- `🔁 Reprise`: exact `process poll <session_id>` or script path.

## Pitfalls

- Do not promise “rapport final” before the background process has completed and the final artifact check passed.
- Do not let Claude/Codex run against the production repo when the user asked for audit/read-only or wants to keep working in chat.
- Do not report an agent self-summary as truth; synthesize only after reading raw outputs and QA evidence.
- Do not hide partial worker failure. If Claude or Codex smoke/auth fails, the report should say which lane was missing and what evidence Hermes still collected.
