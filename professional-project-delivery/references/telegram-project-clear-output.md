# Telegram Projet Clair — mobile handoff pattern

Use this reference when the user is receiving professional/technical project updates through Telegram and has asked for mobile-readable reporting.

## Problem this solves

A professional project can generate useful evidence (logs, JSON, stack traces, QA output, manifests), but Telegram mobile becomes unreadable if those artifacts are pasted inline. The user still wants to learn and steer the project, so the agent must split **decision summary** from **technical evidence**.

## Recommended final Telegram shape

For technical projects, scraping, agents, sites, VPS work, automation, code, deployment, or long research, final Telegram replies should use short sections:

1. `📌 Verdict` — real state: terminé, partiellement terminé, échoué, en cours, or bloqué. Never say “c'est bon” if QA, commit, publish, or verification remains.
2. `🧭 Où on en est` — 2–4 lines of current project state.
3. `✅ Actions faites` — max 6 novice-readable bullets; translate important technical terms.
4. `🧠 Ce que ça veut dire simplement` — max 5 lines explaining why it matters.
5. `⚠️ Points à surveiller / limites` — only real remaining risks. Mark each as `Corrigé ✅`, `Encore ouvert ⚠️`, `À surveiller 👀`, or `Hors scope ⏸️`.
6. `👉 Prochaine action recommandée` — one priority; if needed: now / next / later.
7. `📎 Rapports et preuves` — paths/links only, no raw logs. If the user asks “les liens”, split into `Essentiels à ouvrir` and `Preuves techniques`.
8. `🔁 Reprise / rollback` — exact command if unfinished or modified system state; otherwise say `pas de rollback nécessaire`.

## Long missions

Use three levels:

- **Updates Telegram** only on real state changes, max ~800 characters:
  - `⏳ Avancement`
  - étape actuelle
  - statut
  - pourquoi c'est important
  - prochaine étape
- **Final Telegram** in the section format above.
- **Full report file** under `/opt/data/artifacts/...` with objective, initial state, actions, errors, causes, fixes, modified files, commits, tests/QA PASS/FAIL, important data, artifact paths, public URLs, resume/rollback commands, remaining limits, next action.

## What must stay out of Telegram

Never paste inline:

- raw logs;
- full stack traces;
- complete JSON;
- large tables;
- secrets/tokens/API keys or `.env` snippets;
- repeated draft/execution summaries mixed with final conclusion.

If the final would exceed roughly 2500 characters, prefer at most two Telegram messages: summary first, links/proofs/actions second. If more detail matters, write a Markdown/HTML report and link it.

## Hermes behavior rule installation pattern

When asked to make this a persistent behavior in Hermes:

1. Verify Claude Code and Codex CLI first if the user made that a hard prerequisite.
2. Consult them for risks/placement, but do not follow hypothetical paths over local evidence.
3. Discover actual Hermes rule/config files (`hermes config path`, `HERMES_HOME`, `SOUL.md`, `AGENTS.md`, profile files).
4. Back up every modified file to a timestamped artifact directory.
5. Patch the smallest real behavioral file, not secrets/config if unnecessary. In this VPS, `/opt/data/SOUL.md` was the real behavior file for response rules.
6. Write a rollback script that restores the backup and tells the user to restart/reset Hermes or gateway for the old prompt to reload.
7. Verify section presence, backup existence, rollback script executability, and absence of obvious secret patterns in the added section.

## Anti-pitfalls

- Do not store raw logs in memory; keep them in dated artifacts.
- Do not edit protected/bundled skills when the durable user-specific behavior belongs in a local behavior file or an agent-created delivery skill.
- Do not make Telegram terser by deleting proof. Move proof into files and link it.
- Do not list fixed bugs as final limitations unless there is still a real monitoring risk.
