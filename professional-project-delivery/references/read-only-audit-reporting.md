# Read-only deep audits with agent lanes and report artifacts

Use this reference when Moufadal asks for a serious/professional audit, especially when the scope says: no product-code modifications, use Claude/Codex lanes, produce durable HTML/MD/manifest artifacts, and prove verification.

## Durable pattern

1. **Preflight hard gates first**
   - If the user requires Claude Code and Codex CLI operational, smoke-test both before any audit work.
   - If either is KO, stop and report the exact blocker + resume command. Do not silently fall back to Hermes-only.

2. **Create an external artifact directory**
   - Use a timestamped directory outside the product repo, e.g. `/opt/data/artifacts/<project>_deep_audit_<UTC>/`.
   - Store prompts, raw model outputs, notes, reports, QA output, screenshots, and manifest there.
   - Do not write generated reports into the product repo unless explicitly requested.

3. **Limit lanes and make them independent**
   - Typical max-3 lanes: Claude Code for critical/architecture analysis, Codex CLI for concrete repo inspection, Hermes for orchestration/research/verification/report generation.
   - Preserve raw outputs (`claude-analysis.*`, `codex-analysis.*`) and then synthesize yourself. Do not let one agent be the sole source of truth.

4. **Treat “read-only” as a testable invariant**
   - Run `git status --short` before and after local QA.
   - Beware: some “audit” scripts may write JSON/MD outputs into `artifacts/` by design. If the task forbids product-repo writes, redirect outputs to `/tmp` or the audit artifact dir.
   - If side-effects happen, do not hide them: back them up under the audit artifact dir, restore tracked files, remove untracked QA files, and document the correction in `qa-report.md`.

5. **Claude Code max-turn workaround**
   - If Claude Code audit with `Read` hits `error_max_turns` / `stop_reason: tool_use`, first confirm smoke still passes.
   - Then rerun Claude with a compact no-tools prompt: `--allowedTools '' --max-turns 1 --output-format json`, feeding it the already-collected notes/evidence. Capture both the failed and recovered outputs.
   - The durable lesson is not “Claude is broken”; it is “for bounded audits, switch to a synthesis-only no-tools pass after evidence collection.”

6. **Report shape for premium audits**
   - Required minimums: `index.html`, `research-notes.md`, raw agent analyses, `action-plan.md`, `qa-report.md`, `artifact-manifest.json`.
   - For `index.html`, verify: file exists, browser opens it, console has no JS errors, and visual layout is readable. If browser QA is unavailable, say exactly what was and was not verified.
   - Keep the final user reply short: HTML path, direct verdict, proof list, remaining limits.

## Pitfalls

- Do not claim “no product files changed” from intent. Prove it with `git status --short` after QA.
- Do not leave transient audit outputs in the product repo when the user asked for reports only under `/opt/data/artifacts/...`.
- Do not over-index on agent self-reports. Verify files, parse manifests, and inspect status yourself.
- Do not turn transient credential/setup failures into durable constraints. Save the retry/recovery pattern, not the failure narrative.
