# Test prompts for conversation-to-skill-review

Use these as lightweight eval prompts before changing the skill materially.

## Should trigger

1. "À partir de nos interactions, quels skills on peut créer et lesquels il vaut mieux juste patcher ?"
   - Expected: inspect Obsidian/session history, propose patch-vs-create decisions, avoid creating too many narrow skills.

2. "Tu as encore dit fini alors qu’il restait la QA, transforme ça en amélioration durable."
   - Expected: inspect `definition-of-done`, patch if needed, do not just apologize.

3. "Mets à jour la skill library avec ce qu’on a appris dans cette session."
   - Expected: identify governing skills, patch existing umbrella first, create new skill only if no owner exists.

## Should not trigger

1. "Résume-moi cette vidéo YouTube dans Obsidian."
   - Expected owner: `obsidian` / `youtube-content`, not this skill unless the user asks about behavior improvements.

2. "Quel est l’état du cron de cette nuit ?"
   - Expected owner: `session-continuity-recovery` / `long-task-ledger`.

3. "Crée une nouvelle landing page HTML."
   - Expected owner: design/project delivery skills.
