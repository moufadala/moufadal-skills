# Adaptive Telegram Response Formats — Session Learning

## Trigger

Moufadal explicitly corrected the assistant's response style: the full `Projet Clair` Telegram format (`📌 Verdict`, `🧭 Où on en est`, `✅ Actions faites`, `🧠`, `⚠️`, `👉`, `📎`, `🔁`) was being applied too uniformly across very different requests.

This is a first-class skill signal, not just memory: it changes how professional/project delivery should be reported on Telegram.

## Observed mismatch

The same heavy structure appeared across tasks such as:

- presence checks: “T la ?”, “Tj la ?”;
- small actions: stopping a reminder;
- simple status checks: conversation autosave;
- live guidance: SSH/Tailscale/ADB debugging;
- real project/research deliverables.

The format remains useful for substantial technical/project work, but it creates cognitive load and feels artificial for small or live conversational turns.

## Durable rule

Before every Telegram reply, classify the user request into one of four tiers:

### T0 — Flash

Use for: presence, yes/no, direct status, version/path, “ça tourne ?”.

Shape:

- 1–3 direct lines;
- no section scaffold;
- no rollback/report sections.

Example:

```text
Oui, je suis là ✅
Envoie-moi la sortie SSH et je te guide.
```

### T1 — Compact

Use for: small action, live guidance, minor cron/reminder change, clarification.

Shape:

- direct verdict;
- 2–5 bullets max or one next command;
- proof only if needed.

Example:

```text
✅ Rappel supprimé.
Job retiré: `68327f165fe7`. Il ne renverra plus de messages.
```

### T2 — Standard technical

Use for: bounded diagnosis/tool-backed check with a conclusion but no large deliverable.

Shape usually:

- `📌 Verdict`
- `✅ Fait`
- `⚠️ Limites`
- `👉 Suite`

Omit sections that do not carry information.

### T3 — Projet Clair complet

Use for: serious technical/professional work, VPS/deploy/scraping/code/automation, long research, risky changes, rollback/reprise needs, or explicit report/HTML/proof requests.

Shape: full Projet Clair plus artifact files and raw logs outside Telegram.

## Selection rule

If unsure between T2 and T3, choose T2 unless there is:

- production/system risk;
- rollback/reprise path;
- long-running task;
- user-requested report/HTML/proofs;
- serious professional delivery.

## Anti-patterns

- `🔁 Reprise / rollback` when nothing was changed.
- `📎 Rapports et preuves` when no artifact exists.
- `✅ Actions faites` for a pure explanation.
- `🧠 Ce que ça veut dire simplement` when the answer is already simple.
- Treating every Telegram technical mention as a full T3 report.

## Implementation note

This reference complements `references/telegram-project-clear-output.md`: that file defines full T3 reporting for serious work; this file defines when **not** to use T3.
