# Deep code review orchestration lessons

Use this reference for serious project-wide reviews where Claude Code is the primary reviewer but Hermes remains responsible for orchestration and final truth.

## Pre-review questions

Ask only questions that materially change scope or side effects:

- Desired output: audit-only, fix branch, PR-ready branch, public release, or pedagogical report?
- Scope boundaries: product UX, security/privacy, tests/CI, deployment, data pipeline, performance, docs?
- Change permission: can the agent edit files, create commits, push/open PR, or only report?
- Risk tolerance: conservative no-deploy review vs aggressive fix-and-verify.
- Required audience: technical report, beginner-friendly explanation, or both.

## Review execution pattern

1. Establish baseline: branch, git status, test state, public/runtime state if relevant.
2. Ask Claude Code for deep critique with explicit categories and evidence requirements.
3. Treat Claude output as a hypothesis until verified by diffs/tests/logs.
4. If Claude hits `max_turns` or gives partial output, use a second pass: Codex, Hermes-local tests, or a narrower Claude follow-up.
5. Convert findings into acceptance gates before implementing fixes.
6. Run QA after implementation and again after any commit/regeneration/publish step that can change provenance.
7. Produce final artifacts: dated report, logs, test outputs, rollback command.

## Release-quality no-go examples

- Dirty working tree used to build an artifact that is being promoted.
- Privacy/public-safety findings untested at runtime.
- Public dashboard QA not rerun after deploy.
- Claude summary with no matching artifact, diff, or command output.

## Reporting discipline

For Telegram or other chat channels, keep the final message short: verdict, state, max six actions, plain-language meaning, limits, next step, report paths, rollback. Put logs and detailed matrices in files, not in chat.
