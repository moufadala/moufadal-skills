# moufadal-skills

Skills **neutres** partagés entre les agents de Moufadal (Claude Code sur PC, Hermès/Codex sur VPS).

Format : standard ouvert **Agent Skills** — un dossier par skill contenant un `SKILL.md` (frontmatter `name` + `description`).

## Principe : skills NEUTRES

Ces skills décrivent **QUOI faire et QUAND**, jamais le **COMMENT** propre à un runtime :
- pas de noms d'outils spécifiques (`write_file`, `Read`… → « crée / lis la note ») ;
- pas de chemins machine codés en dur (`/opt/data/...` → « le vault ») ;
- aucune donnée personnelle.

Ainsi le même skill est lisible et exécutable par **Claude Code ET Hermès**.

## Skills à contrepartie native Hermès (modèle « projection »)

5 skills existent **en deux formes** : ici en version **neutre/courte** (27-31 lignes), et chez **Hermès** en version **native/riche** (154-453 lignes, fortement couplée à ses outils : `/opt/data`, Docker, Tailscale, Telegram, cron, Obsidian, retours terrain) :

`definition-of-done` · `careful-guard` · `web-scraping-reality` · `conversation-to-skill-review` · `professional-project-delivery`

**Ce n'est pas un doublon-bug — c'est une projection** (même pattern qu'Obsidian → Graphify) :
- **Version neutre (ici) = référence du _principe_**, portable, lue par tout runtime (PC, Codex).
- **Version native Hermès = l'opérationnel**, là où s'accumule le savoir de terrain.
- **Deux formes pour deux runtimes, par conception.** Décision actée : voir l'ADR 2026-07-10 dans le vault (« exception assumée »).

**Règles pour éviter la dérive :**
1. Quand le **principe** d'un de ces skills change, le refléter **des deux côtés** (via `conversation-to-skill-review`). Pas de pipeline de synchro.
2. **Un runtime ne charge jamais** à la fois sa version native **et** la version externe du même skill (risque de collision de chargement). PC → ce repo ; Hermès → ses skills natifs `/opt/data/skills/`. On ne mélange pas.
3. On **ne refactore pas** les versions riches de Hermès en base+couche : à l'échelle de 5 skills perso, le coût dépasse le gain.

> Ne sont PAS ici (par choix) : les *wrappers d'outils* (spotify, notion, yt-dlp, whisper, apple…) — inutiles tant que l'outil n'est pas joignable ; ils relèvent de l'**accès croisé via MCP** (voir l'ADR 2026-07-10 dans le vault). Ni les skills internes à Hermès, ni les skills personnels.

## Utilisation

- **PC (Claude Code)** : ce dépôt est cloné dans `~/.claude/skills/` (auto-pull au démarrage de session).
- **VPS (Hermès)** : à cloner dans le dossier skills de Hermès.
- Mettre à jour : `git pull`. Ajouter un skill : nouveau dossier `<nom>/SKILL.md`, commit, push (voir le skill `skill-creator`).

## Skills

### Base de connaissance / vault
- `llm-wiki/` — base de connaissance markdown compounding (pattern Karpathy).
- `obsidian-vault-notes/` — lire/chercher/créer/éditer des notes de vault proprement (État/Preuve/Action).
- `distillation-interview/` — distiller une source par entretien → Source / Concept / Décision / Action reliées.

### Méthode d'ingénierie
- `systematic-debugging/` — débogage par cause racine en 4 phases.
- `test-driven-development/` — RED-GREEN-REFACTOR.
- `writing-plans/` — plans d'implémentation exécutables.
- `specification-par-exemples/` — spec légère par l'exemple avant de coder.
- `simplify-code/` — nettoyer sans changer le comportement.
- `spike/` — expérience jetable pour lever une incertitude.
- `requesting-code-review/` — revue sécurité/qualité avant commit.
- `search-first-before-build/` — chercher l'art antérieur avant de construire.

### Recherche / veille
- `deep-research-pipeline/` — pipeline de recherche sourcée et vérifiée.
- `community-validation-before-fragile-tech/` — valider une méthode fragile avant d'agir.
- `web-scraping-reality/` — hiérarchie et pièges du scraping.

### Pilotage / qualité / collaboration
- `karpathy-project-gate/` — porte légère au démarrage d'un projet.
- `definition-of-done/` — critères de « fait » vérifiables avant de conclure.
- `professional-project-delivery/` — mode ingénierie pour un livrable sérieux.
- `dogfood-qa/` — QA exploratoire d'une app web avec preuve.
- `critical-collaboration/` — anti-complaisance, désaccord utile.
- `careful-guard/` — garde-fou avant action destructrice/irréversible.

### Outils (via guichet MCP partagé)
- `youtube-transcript/` — récupérer un transcript YouTube via l'outil MCP `youtube_transcript` (voir runbook `Guichet MCP youtube-transcript` dans le vault).

### Méta (maintenir le parc)
- `skill-creator/` — créer, améliorer, évaluer des skills.
- `subagent-driven-development/` — déléguer à des sous-agents, vérifier avant d'intégrer.
- `conversation-to-skill-review/` — décider quoi retenir : mémoire / note / skill.
