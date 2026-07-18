---
name: professional-project-delivery
description: "À utiliser quand l'utilisateur demande un livrable sérieux/professionnel — suite web, dashboard, feature produit, artefact client, ou tout projet multi-étapes où la qualité compte. Impose un mode ingénierie : découverte, contrat d'acceptation, portes de QA, et remise finale vérifiée."
version: 1.0.0
license: MIT
platforms: [linux, macos, windows]
---

# Professional Project Delivery

## Overview

Use this workflow when the user is building something professional, client-facing, sellable, reusable, or operationally important. The goal is to stop shipping plausible demos and instead deliver artifacts backed by explicit acceptance criteria, real verification, and a clear handoff.

Core principle: **no proof = not delivered**. A good final answer includes the artifact, what was tested, what failed and was fixed, and what risks remain.

## When to Use

Use this skill for:
- web suites, dashboards, landing pages, automations, client deliverables;
- work described as “pro”, “vendable”, “livrable”, “à montrer”, “à donner à quelqu’un”;
- ambiguous product ideas that need brainstorming before building;
- multi-step work where architecture, UX, testing, and maintainability matter;
- recovery after the user says something is not actually usable.

Do not use the full workflow for trivial one-off questions, tiny edits, or simple factual answers. For small tasks, apply only the lightweight parts: clarify the goal, verify the action, report honestly.

## Mandatory Mode Switch

When this skill triggers, explicitly switch into **mode ingénieur**:

1. Treat the request as a product/job-to-be-done, not just a prompt.
2. Identify whether the user needs brainstorming before execution.
3. Load relevant specialist skills before acting.
4. Define acceptance criteria before building.
5. Create a verification oracle: test script, browser QA, screenshot, build, lint, data sample, or manual evidence.
6. Do not claim completion without tool-backed verification.
7. Produce a final pedagogical HTML handoff when the work is substantial.

## Phase 0 — Triage: Ask, Research, or Act?

Ask up to 3 questions only when answers materially change the build:
- target user/client;
- must-have outcome;
- constraints: budget, deadline, platform, visual style, data source, legal/compliance.

If the user expects a professional/product deliverable but has not supplied detailed acceptance criteria, **do not jump straight from data → UI → technical QA**. First decide whether the missing criteria should be:

1. **Asked from the user** — when the answer is personal, business-specific, or cannot be inferred.
2. **Researched** — when the user is asking for best practices, benchmark UX, market standards, or “what people expect” from this class of product.
3. **Assumed explicitly** — only when the default is low-risk and reversible.

When using research instead of manual questioning, produce a short evidence-backed **product default contract** before implementation. Example for a news/watch dashboard: research card UX, filters/facets, feed-reader workflows, dashboard decision-making, and click/action patterns; then translate findings into card fields, priority rules, click behavior, actions, states, and QA gates.

If the default interpretation is obvious, act. Do not block on cosmetic questions. But for ambiguous product-shaped work, the “obvious” action is often to define/research the product contract first, not to build a plausible UI.

Use brainstorming when:
- the user is exploring a business/product idea;
- the desired outcome is vague;
- there are multiple viable approaches with meaningful trade-offs;
- the user explicitly asks “comment on devrait faire ?”.

For brainstorming, use collaborative-intelligence / creative-ideation style:
- restate goal;
- generate options;
- compare trade-offs;
- recommend one route;
- ask for a decision only if necessary.

## Phase 1 — Contract of Acceptance

Before implementation, write a short contract:

```markdown
## Contrat d’acceptation
- Livrable final: ...
- Utilisateur cible: ...
- Must-have: ...
- Must-not: ...
- Vérification obligatoire: ...
- Preuves à fournir: chemins, commandes, screenshots, logs, limites restantes.
```

For UI/web deliverables include:
- visual style constraints;
- critical interactions;
- responsive behavior if relevant;
- empty/error states;
- source links/data freshness;
- console JS = 0 blocking errors.

For dashboards/feeds/monitoring products, the contract must include **product semantics**, not just interface mechanics. Use this quick contract explicitly enough that the final UI can help the user decide:
- **priority rules**: why this card/item is above another and whether the score is explainable;
- **source links / provenance**: where the item came from, whether the source is official/scraped/manual, and how to open the original;
- **actions / next action**: what the user can do now — open, save, hide, compare, contact, copy/share, mark seen;
- **freshness / trust signals**: last checked, stale data, blocked source, unverified item, missing fields;
- required card fields and which fields may be missing;
- click model: card selection vs external source link vs secondary actions;
- user state persistence: seen, saved, hidden, copied/shared, duplicate;
- QA that validates user value, e.g. “top priorities are visible in 5 seconds”, not only DOM presence.

## Phase 2 — Planning

For non-trivial implementation, load/use `writing-plans`.

Plan should include:
- exact files/artifacts;
- task breakdown;
- verification command per task;
- QA gate before final answer.

If the user corrects the scope after delivery (e.g. “there were lots of other things”, “I meant the audios I sent”, “ce n'est pas utilisable”), do not defend the prior artifact or overclaim success. Re-enter discovery/product-semantics mode: recover the missing inputs, summarize the recovered asks, identify the missing **decision value** fields/actions (`why it matters`, source/provenance, freshness, priority, next action), revise the acceptance contract, and produce a corrected V2 with a manifest of inputs/outputs/verification. Preserve or archive the prior artifact first, ship the V2 separately when possible, and keep rollback/reversible changes available instead of overwriting blindly. This is especially important after context compaction or long-running tasks.

If the user says there are still “plein de bugs”, “du laisser-aller”, or that progress is too slow, treat it as a methodology failure signal, not just another bug ticket. Reproduce representative failures, convert them into **bug families**, add/update behavioral acceptance tests before fixing, and run a red→green loop. Do not ask the user to enumerate every case when the class can be generated from data/domain grammar/metamorphic variants. See `references/ai-assisted-product-completion-loop.md`.

If the user says the currently served artifact is an **older/lost version** (“ce n'est pas la dernière version”, “on avait repris depuis zéro”, “tu as lancé l'ancienne version”), stop feature work on the current artifact and run a forensic version-recovery loop before publishing anything else: inventory candidate workspaces/backups, search handoffs/screenshots/session notes for product markers, compare candidates against the user's described UX and counts, build/serve the candidate, QA it publicly, snapshot rollback, then patch the pipeline that could overwrite it. See `references/forensic-version-recovery-after-regression.md`.

If the user says the current work is **not the same project** or “on part de zéro”, immediately stop carrying over assumptions from prior artifacts, courses, dashboards, repositories, or compaction summaries. Create or switch to a clean project workspace, write a short context boundary (`this project is independent of X/Y/Z`), and ask only for the product direction that cannot be inferred. Do not keep adapting the old deliverable under a new name.

For serious ongoing projects, prefer a durable workspace instead of scattering one-off artifacts:

```text
/opt/data/projects/<project-slug>/
  README.md
  project.yaml
  data/
  src/
  tests/
  artifacts/<timestamp-task>/
    contract.md
    plan.md
    final artifact(s)
    qa-report.md
    screenshots/
    handoff.html
```

Do not move or delete legacy artifacts unless explicitly asked; copy useful inputs into the clean project and preserve old paths.

For code-heavy projects, use TDD where possible. For UI prototypes, use acceptance tests and browser QA instead of pretending unit tests cover UX.

## Phase 3 — Execution

Choose the execution lane:

- Hermes tools directly: small edits, simple artifact generation, direct verification.
- Claude Code via `claude_runner.py` or `claude -p`: architecture/debugging/implementation deeper than a few turns.
- `delegate_task`: bounded parallel research/review subtasks.
- Kanban/background/cron: durable multi-workstream or recurring operations.

For each lane, preserve ownership in Hermes: verify outputs yourself before telling the user it worked.

### Phase-gated infrastructure/capability rollouts

When Moufadal explicitly requests “phase par phase”, “une seule phase”, or “stop après QA”, treat the phase boundary as a hard acceptance gate. Execute only the current phase, produce the requested proof, and stop even if the next phase is obvious. If the phase involves routing, monitoring, cron, Docker, credentials, scraping egress, or agent infrastructure, validate the actual capability end-to-end rather than the presence of a running service. For example, a PC-egress heartbeat should prove `curl ifconfig.co` through the exact proxy/exit-node and should test failure plus recovery, not merely that the PC answers. If the final alert destination is outside Hermes visibility, require user confirmation before calling the alert proof complete. See `references/phase-gated-infra-capability-qa.md`.

### User signal: “travaille sans relâche / fais le max en parallèle”

When the user explicitly asks for maximum throughput, switch from sequential artisan mode to **bounded parallel engineering mode**. If the request concerns Moufadal's VPS portfolio or multiple ongoing projects, first load/use `project-skill-router` and route to `__portfolio__`; then advance every safe/reversible lane instead of giving only a status report. Detailed portfolio pattern: `project-skill-router/references/maximum-portfolio-advance-2026-06-23.md`.

1. Split the work into independent axes with separate artifacts (e.g. data render, OCR/layout spike, DB/import guard, QA report).
2. Launch parallel/background jobs for long bounded tasks with `notify_on_complete=true` and keep their `session_id`s visible.
3. If `delegate_task` or an external model fails due to quota/auth/setup, do not stop; fall back to local scripts/background processes and record the blocker only as context.
4. Poll/wait in batches, then integrate results into one final status report.
5. Mark non-perfect outcomes as QA signals rather than hiding them; e.g. matched vs unmatched counts, fallback artifacts, next blocker.
6. Finish by verifying files/tests/process list so “maximum parallel” still ends in a coherent, checked handoff.

## Phase 4 — QA Gates

### Avoid false PASS on product work

For user-facing projects, a passing pipeline is not enough if it only validates intermediate files. Add a gate that verifies the exact delivered artifact (public URL, generated HTML/PDF, app bundle, dashboard, etc.) after the final build/publish step. If the user reports obvious UX bugs after a PASS, treat it as a methodology failure first: missing acceptance contract, stale artifact, weak oracle, or tests checking implementation tokens instead of user behavior.

At least one gate must exist for every serious deliverable.

Common gates:
- build/lint/test command;
- Playwright/browser interaction test;
- console error check;
- screenshot/visual inspection;
- source/data validity check;
- security scan for secrets or unsafe operations;
- reviewer subagent for spec compliance and code quality.

For web UI, apply `dogfood` principles:
- navigate to the exact artifact URL the user will open, not only a local file path;
- for VPS/reverse-proxy publication, verify DNS and network families too: A/AAAA records, `curl -4`/`curl -6` when dual-stack exists, and whether the canonical URL is truly reachable without forcing a family; stale AAAA records can make a valid IPv4 service fail for some clients;
- if the artifact is meant for Telegram/mobile use, provide and verify a public/reachable URL before calling it delivered;
- test localhost as a backend check only; if localhost works but the public IP/port times out, diagnose exposure/routing separately instead of claiming the app is usable;
- when using an existing public dashboard route, verify it serves the current build, not an older root-owned artifact;
- test search/filter/click/key flows;
- for dashboards with persisted UI state, run both fresh-state QA (`localStorage.clear()`/cache-bust) and dirty-state QA with existing filters/search;
- verify reset/clear buttons by asserting DOM state and localStorage, not just by clicking visually;
- verify data counts and category/search results against the acceptance contract;
- inspect console after interactions;
- save screenshot when possible;
- write a `qa-report.md` with exact pass/fail counts;
- report exact failures and fixes.

### Post-deploy production verification

Use this GStack `/land-and-deploy` inspired loop after a PR merge, VPS publish, cron rollout, dashboard publication, or user claim that “it is in prod”. Do not stop at “CI green” or “container restarted”. Verify the exact runtime the user will touch.

Required checks, adapted to the project:

1. **CI / build source:** head commit or deployed artifact matches the intended change.
2. **Runtime reachability:** public URL if one exists; otherwise documented local/container health endpoint.
3. **Real user smoke:** browser/curl/API path that exercises the changed feature, not just `/`.
4. **Console/log health:** no blocking browser console errors for web UI; no fresh service errors in logs for backend/cron.
5. **Rollback:** exact branch, artifact backup, service command, or DB backup path.
6. **Evidence:** save check output, screenshot, or log path under the task artifact directory.

If production verification is blocked by branch protection, required review, DNS, credentials, or approval, report status as **partially complete / blocked**, not “done”.

### Verify delegated/background research artifacts before reporting

When a serious deliverable is produced through a background script or delegated model, do not trust process exit code or the mere existence of files. Open the main artifact and verify that it contains the promised substance. Some model CLIs can return JSON with `is_error: true` or an auth/API error while the wrapper exits `0`, leaving behind a minimal placeholder report. If that happens, continue with Hermes/local tools and authoritative docs until the report is actually complete, then overwrite the placeholder with a real deliverable and rerun a file/substance QA gate.

## Phase 5 — Final Handoff

Final user response must be compact but grounded:

- artifact path/link;
- what changed;
- proof of verification;
- remaining risks/limits;
- next recommended step.

### Telegram mobile: adaptive Projet Clair format

When the source is Telegram, **classify the user's request before choosing the shape of the reply**. Moufadal explicitly corrected that the full Projet Clair template is useful for technical/project delivery, but becomes annoying when applied to every simple question or live-guidance turn.

Use this adaptive ladder:

- **T0 — Flash**: presence checks, yes/no, short status, version/path, “T’es là ?”, “ça tourne ?”. Reply in 1–3 direct lines. No section scaffold.
- **T1 — Compact**: small action, small clarification, live SSH/debug guidance, minor cron/reminder change. Use a direct verdict plus at most 2–5 bullets or one next command.
- **T2 — Standard technical**: bounded diagnosis or tool-backed check with a real conclusion but no large deliverable. Use only the needed sections, usually `📌 Verdict`, `✅ Fait`, `⚠️ Limites`, `👉 Suite`.
- **T3 — Projet Clair complet**: serious technical/professional work (scraping, agent, site, VPS, automation, code, deployment, long research), risky system changes, incidents, rollback/reprise needs, or when Moufadal explicitly asks for a report/HTML/proofs. Split outputs into: (1) a readable Telegram steering summary, (2) a complete Markdown/HTML report file, and (3) raw logs in artifact files. Follow `references/telegram-project-clear-output.md`.

In case of doubt between T2 and T3, prefer **T2** unless there is a production/system risk, a rollback path, a long-running task, or a user-requested report. Avoid fake sections: no `🔁 Reprise / rollback` when nothing changed, no `📎 Rapports` when no artifact exists, no `✅ Actions faites` for a pure explanation, and no `🧠 Ce que ça veut dire simplement` when the answer is already simple.

For long missions, send only short progress updates when the state truly changes, then a concise final Telegram message plus a complete report under `/opt/data/artifacts/...`. Do not list already-fixed problems as final limits unless there is still a real monitoring risk.

For substantial professional work, also create a small HTML handoff or interactive report in `/opt/data/artifacts/...`.

When Moufadal explicitly asks for a report “sous forme d’un cours”, says he is lost, or requests pedagogy/diagrams/no opaque code blocks, switch the HTML handoff into **pedagogical course mode**: teach the mental model first, use simple process diagrams, include glossary/status cards, hide raw logs behind artifact links, and verify the HTML contains the promised learning sections. See `references/pedagogical-course-report-for-novices.md`.

### HTML Handoff / Interactive Report Requirements

Choose the report shape by job-to-be-done. The HTML should be client-readable and explain:

1. What was built or changed.
2. Why this approach is better.
3. How it works now.
4. What was tested.
5. What could still break / risks.
6. What should happen next.

For reports, research syntheses, eval viewers, QA handoffs, or dashboards, prefer an **evidence-rich interactive static HTML** rather than a flat Markdown dump. Default useful tabs: `Résumé`, `Evidence`, `Output`, `Benchmark`, `Sources`, `Failures`, `QA / limites`, and `Next`. Include adjacent `source-map.json`, `research-notes.md`, `qa-report.md`, or an artifact manifest when the work is non-trivial. See `references/report-quality-playbook.md`.

Avoid adding a frontend stack just to make tabs/cards. Static HTML/CSS/JS is the default for Hermes reports because it is portable, Telegram/mobile-friendly, archivable, and low-maintenance. Use React/Vite only when the report becomes a durable app with complex state, reusable components, large data volume, routing, or recurring publication.

It must not be a dark generic developer dashboard. Prefer clean editorial layout, readable sections, and source/proof links. If creating UI/design, load `claude-design` and `popular-web-designs` first.

Suggested filename:

```text
/opt/data/artifacts/<project>/<timestamp>_handoff.html
# or, for eval/research/report viewers:
/opt/data/artifacts/<project>/<timestamp>_report.html
```

## Default Prompt Pattern

When launching a serious project, internally follow:

```text
Mode ingénieur. Build as a professional deliverable.
First define acceptance criteria. If ambiguity changes the product, ask concise questions; otherwise proceed.
Use relevant skills. Create a verification gate. Run it. Fix failures. Produce artifact + proof + HTML handoff.
Do not claim completion without verified evidence.
```

## Support References

- `references/decision-dashboard-recovery.md` — acceptance contract for decision dashboards: priority, provenance, freshness, action, reason, risk; and the recovery pattern when Moufadal says a polished UI is not usable.
- `references/scoped-agent-prompts-and-report-audits.md` — when producing GPT/agent prompts or auditing PDF reports for an existing watch/pipeline project: restrict scope to verified/in-progress sources, do not name out-of-scope sites, and compare report claims against current scripts/config/dry-runs before accepting them.
- `references/finished-deliverable-loop.md` — concrete pattern for turning plausible UI/artifact work into a verified durable project workspace with run artifacts, QA report, screenshots, and concise accountability replies.
- `references/forensic-version-recovery-after-regression.md` — when the live/public artifact is an older/lost version: freeze feature work, recover the true source of truth via handoffs/screenshots/candidates, QA before publish, snapshot rollback, patch refresh jobs, and protect source with targeted Git/snapshots.
- `references/data-driven-real-estate-dashboard-qa.md` — checklist pour dashboards HTML/JS construits depuis une DB immo: contrat d’acceptation, export JSON, filtres facettés avec compteurs, variantes, modal photo, QA navigateur et pièges JSON/images.
- `references/static-real-estate-photo-cache.md` — procédure V5 pour aspirer/cache localement les photos principales d’annonces immo, patcher `listings.json` + JSON embarqué, et prouver le chargement navigateur avec `naturalWidth`.
- `references/static-real-estate-gallery-description-qa.md` — extension V6 pour apps immo statiques: audit descriptions source vs synthèses, extraction exacte des galeries, cache `local_image_urls[]`, UI `+N photos`/compteur `1/N`, QA navigateur et piège des raws SERP agrégés.
- `references/static-dashboard-publication-and-state-qa.md` — publication et QA des dashboards statiques: ne pas livrer un simple chemin local, vérifier l’URL publique exacte, distinguer localhost/port public/tunnel, éviter les anciens artefacts publics, tester localStorage/reset/cache et JSON embarqué.
- `references/static-real-estate-dashboard-clean-default-suspects-export.md` — decision guide pour publier durablement des dashboards sur VPS: distinguer egress Tailscale vs ingress web, auditer Traefik/Docker/DNS/permissions, préférer Traefik + conteneurs statiques, utiliser Cloudflare Tunnel nommé en fallback, éviter `trycloudflare`, ports random et dossiers root-owned.
- `references/sqlite-product-layer-real-estate-dashboard.md` — pattern pour décider SQLite vs migration sur dashboards immo: garder la table scraper brute, ajouter une couche d’enrichissement produit non destructive, canonicaliser les doublons, exporter depuis la vue produit, et vérifier DB → export → public → navigateur.
- `references/vite-subpath-static-publication.md` — runbook pour publier un build Vite compilé avec `base: '/subpath/'` sur un hôte HTTPS propre: monter le parent, servir `/subpath/index.html` à `/`, vérifier `/subpath/assets/*` et faire QA navigateur.
- `references/news-watch-dashboard-product-contract.md` — research-backed default product contract for news/watch dashboards: priority semantics, card fields, click/actions, filters, states, and QA gates.
- `references/ai-assisted-product-completion-loop.md` — when AI-built product work still has obvious user-visible bugs or the user complains progress is too slow: reproduce complaints, generalize into bug families, write acceptance/eval cases, run red→green QA, and answer with accountability rather than defending prior audits.
- `references/real-estate-portal-clean-ux-reboot.md` — recovery pattern when an immo dashboard becomes cluttered or over-personalized: benchmark standard property portals, reboot in a clean React/Vite workspace if justified, keep only 4 first-level filters, and QA public/mobile UX plus rollback.
- `references/static-real-estate-clean-portal-reboot-v1.md` — concrete runbook for replacing a cluttered scraper-backed immo dashboard with a reversible static V1 property portal over the existing export: field/photo audit, clean parallel workspace, `T2` query expansion, public/mobile QA, and honest photo/gallery limits.
- `references/static-real-estate-clean-search-optimization.md` — after the clean V1 works, optimize search without adding clutter: research Citya/SeLoger/filter UX, add only high-value filters like `Pièces min.`, parse natural phrases such as `Saint-Denis T2 moins de 800`, and QA public results against the parsed constraints.
- `references/real-estate-existing-solutions-research-before-reboot.md` — when Moufadal asks to check GitHub/communities before rebuilding an immo portal: research existing UI portals, scraper/aggregator/notifier projects, extraction tools, licenses, and translate findings into a simple V1 over the scraped DB instead of cloning a repo wholesale.
- `references/static-real-estate-shareable-search-url-state.md` — P1 pattern for static immo dashboards: implement bookmarkable/shareable saved searches via URL state before maps or true alerts; includes implementation and QA gates.
- `references/static-real-estate-clean-portal-iteration-qa.md` — repeat optimization loop for an already-published clean immo portal: research → plan → low-clutter change → public QA; covers URL-state/copy search, debounce/performance, mobile overflow, schema fallback, and concise evidence replies.
- `references/static-real-estate-saved-search-alert-engine.md` — next-step pattern after URL state: server-side saved-search matching over the generated JSON export, silent first-run `seen` bootstrap, Telegram-ready digest only for new canonical matches, and cron `no_agent=True` gating after user approval.
- `references/static-real-estate-listing-history.md` — next-step pattern after saved-search alerts: auxiliary history SQLite, non-spammy price/status events, digest enrichment, and a public/admin `changes.json` that excludes baseline `new` events while keeping audit counts.
- `references/static-real-estate-source-health-mobile-cockpit.md` — P0/P1/P2 pattern for mature static immo dashboards: add source freshness JSON/HTML before DB migration, mobile region-map filters that reset conflicting local state, safe saved-search cockpit, and anti-spam alert QA.
- `references/static-real-estate-active-watch-intelligence-layer.md` — next layer after a clean static immo portal: active watch/history, source-break Telegram alerts, non-destructive dedup, premium-photo limits, Réunion localization ontology, and opportunity scoring on separate pages/modal without cluttering the main search UX.
- `references/recovering-multi-deliverable-course-dashboard.md` — recovery pattern for course/report + dashboard sessions after compaction/freezing: verify generated artifacts, reconstruct the full work ledger, then continue the remaining deliverables with product-semantic QA.
- `references/course-to-build-spec-recovery.md` — after a course/report handoff or terse “continue/travail”, distill the course into a project spec, inspect existing artifacts before rebuilding, rerun QA, and add complementary product QA for gaps such as mobile and priority visibility.

- `references/project-canon-snapshots-artifacts-policy-2026-06-22.md` — decision pattern after overnight/prototype work: separate dev canon from public switch, require snapshots before broad edits, use targeted ownership repair, archive-first artifact policy, and define a narrow V1 before building everything.
- `references/report-quality-playbook.md` — standard for evidence-rich interactive reports/viewers: static HTML by default, tabs for Résumé/Evidence/Output/Benchmark/Sources/QA, source maps, artifact manifests, report relevance score, and anti-tool-sprawl guidance for when React/Vite/Quarto/Observable are actually justified.
- `references/research-pipeline-traceability-report.md` — when Moufadal asks why a research item was omitted or wants a complete benchmark/research HTML report, include the full pipeline: queries, engines, raw counts, filters, scoring, exclusions, synthesis path, Telegram condensation, and QA.
- `references/read-only-audit-reporting.md` — workflow for read-only deep audits with Claude/Codex/Hermes lanes, artifact-only reporting, git-status side-effect checks, and Claude max-turn synthesis fallback.
- `references/max-effort-background-audit.md` — when Moufadal asks for a deep/max-effort audit while continuing to use the same Telegram chat: ask only contract-changing questions, create a read-only mirror, launch Claude+Codex audit in background with `notify_on_complete`, and deliver a pedagogical HTML/MD report with raw evidence and read-only proof.
- `references/telegram-project-clear-output.md` — Telegram mobile handoff format for technical/professional work: concise steering summary in chat, full reports/logs in artifacts, novice explanations, status labels, and rollback/resume commands.
- `references/adaptive-telegram-response-formats.md` — session-derived T0/T1/T2/T3 classifier for deciding when **not** to use full Projet Clair; captures Moufadal's correction that simple questions/live guidance need flash or compact answers.
- `references/phase-gated-infra-capability-qa.md` — phase-by-phase infra/capability rollout pattern: one phase only, end-to-end heartbeat, failure/recovery proof, user-confirmed external alert, and rollback artifacts.

## Common Pitfalls

0. **Generating Markdown reports with an unquoted shell heredoc.** If a report contains backticks, shell snippets, or rollback commands, do not write it with `cat <<EOF` unless the delimiter is quoted (`<<'EOF'`). Otherwise command substitution can corrupt the report and even execute example rollback commands. Prefer `write_file` for final reports, then read the artifact back and re-check any config values mentioned in rollback snippets. See `references/shell-generated-report-quoting-and-runtime-reload.md`.
1. **Skipping brainstorming when the request is product-shaped.** If the user is deciding what to sell/build, brainstorm first.
2. **Promoting a workbench directly to production canon.** For React/Vite or similar UI workbenches, distinguish `canonique dev` from `canonique public/prod`: a workbench may become the source of development after build/lint evidence, but public replacement should wait for snapshot/git, browser QA desktop/mobile, console check, screenshot, and a reversible deploy path. Keep the legacy version as archive/rollback until that gate passes.
3. **Treating DOM checks as UX QA.** DOM presence is not enough; test real interactions.
4. **Treating public reachability as product success.** A dashboard can load correctly and still be “not terrible” because cards lack decision value. When the user complains after technical QA, re-audit the product semantics: required fields, descriptions, geography/sector grouping, why-this-item explanations, and whether missing source data is clearly labeled.
5. **Stacking features onto a cluttered product.** If the user calls the UI a “fouillis” or says to forget a personalized search, do not add another tab/filter/button. Stop, benchmark the product category, write a clean default contract, and consider a clean workspace/reboot. For real-estate portals, use `references/real-estate-portal-clean-ux-reboot.md`: search-first, photo-first cards, four first-level filters max, standard save/hide/source/detail flows, technical/suspect/debug info secondary.
6. **Fixing the old dashboard when the user asked to restart clean.** For scraper-backed immo dashboards, a better V1 may be a separate static portal over the existing export, not another patch to the legacy app. Build in a parallel output directory, back up before publication, keep internals/admin/debug out of the first screen, and QA real public search examples like `Saint-Denis T2` with shorthand expansion. See `references/static-real-estate-clean-portal-reboot-v1.md`.
7. **Optimizing the clean immo portal by adding visible complexity.** Once the clean V1 works, do not immediately add maps, alerts, source-health, scoring, or admin panels. First improve the existing search contract: parse natural phrases (`T2`, `moins de 800`, `40m2`, `st denis`), add at most one high-value classic filter such as `Pièces min.`, and verify public results obey the parsed constraints. See `references/static-real-estate-clean-search-optimization.md`.
7. **Confusing local principal photos with complete photo UX.** For immo dashboards, `photo principale locale: 495/495` is not enough if some listings have multiple source photos. Add `image_urls[]`/`local_image_urls[]`, card `+N photos`, modal navigation, and QA that proves the image changes and loads. Also distinguish `Description source` from synthetic summaries instead of implying all descriptions are equally complete.
7. **Migrating the database engine when the problem is product semantics.** For small scraper-backed dashboards, do not jump from messy listings to Postgres/backend migration. First audit row counts, field coverage, duplicate groups, source freshness, public artifact size, and concurrency needs. If the engine is not the bottleneck, keep the raw table stable and add non-destructive product/admin layers: product-enrichment views, history SQLite, `source_health.json/html`, saved-search cockpit JSON/HTML, and public QA. See `references/sqlite-product-layer-real-estate-dashboard.md` and `references/static-real-estate-source-health-mobile-cockpit.md`.
8. **Jumping from shareable searches to fake alerts.** Once a static immo dashboard has URL-state searches, the next useful product step is often saved-search matching — but not a pretend email/backend feature. Build a small non-destructive alert engine over the generated JSON, bootstrap `seen` silently, emit only new canonical matches, QA the anti-spam behavior, and schedule cron only after user approval. See `references/static-real-estate-saved-search-alert-engine.md`.
9. **Delivering active immo intelligence by re-cluttering the clean portal.** When adding watch reports, source health, dedup, localization, photo quality, alerts, or scoring to a clean static real-estate portal, keep the first screen search-first. Put operational/intelligence layers on separate pages or behind a small modal action such as `Analyse`; use non-destructive data layers and suppress first-run alert spam. See `references/static-real-estate-active-watch-intelligence-layer.md`.
10. **Delivering “a little HTML” without handoff.** For professional work, produce both the artifact and a pedagogical explanation HTML.
11. **Asking too many questions.** Ask only questions that change the build. Otherwise choose a sensible default and proceed.
9. **Letting subagents self-certify.** Verify their outputs with direct tools.
10. **Overusing the heavy workflow.** Keep simple tasks simple.

## Verification

### HTML/dashboard first-paint check

For self-contained HTML dashboards, QA must cover the **raw initial HTML before JavaScript runs**, not only Playwright after-load state. Mobile previews and Telegram file viewers can capture the page before JS populates placeholders; a dashboard can therefore show `0 item` while stats claim data exists. Render useful fallback content directly into the HTML (cards, source rows, counter, initial reader) and add regression checks for non-empty `#items`, non-stale `#count`, non-empty `#sources`, and a useful reader before JS enhancement. See `references/html-dashboard-first-paint-qa.md`.

## Verification Checklist

Before final answer:

- [ ] Relevant skills loaded.
- [ ] Acceptance contract defined or implicit because task is tiny.
- [ ] Artifact exists at a durable path.
- [ ] QA gate executed with real output.
- [ ] UI interactions tested if applicable.
- [ ] Screenshot/visual check done when applicable.
- [ ] HTML handoff created for substantial professional work.
- [ ] Final answer includes proof, limits, and next step.
