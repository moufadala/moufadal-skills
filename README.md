# moufadal-skills

Skills **neutres** partagés entre les agents de Moufadal (Claude Code sur PC, Hermès/Codex sur VPS).

Format : standard ouvert **Agent Skills** — un dossier par skill contenant un `SKILL.md` (frontmatter `name` + `description`).

## Principe : skills NEUTRES

Ces skills décrivent **QUOI faire et QUAND**, jamais le **COMMENT** propre à un runtime :
- pas de noms d'outils spécifiques (`write_file`, `Read`… → « crée / lis la note ») ;
- pas de chemins machine codés en dur (`/opt/data/...` → « le vault ») ;
- aucune donnée personnelle.

Ainsi le même skill est lisible et exécutable par **Claude Code ET Hermès**.

## Utilisation

- **PC (Claude Code)** : ce dépôt est cloné dans `~/.claude/skills/`.
- **VPS (Hermès)** : cloné dans le dossier skills de Hermès.
- Mettre à jour : `git pull`. Ajouter un skill : nouveau dossier `<nom>/SKILL.md`, commit, push.

## Skills

- `llm-wiki/` — base de connaissance markdown compounding (pattern Karpathy).
- `distillation-interview/` — distiller une source par entretien → notes Source / Concept / Décision / Action reliées.
