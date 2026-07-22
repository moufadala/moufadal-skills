---
name: notebooklm
description: "Piloter Google NotebookLM via les outils MCP partagés (mcp_notebooklm_*) exposés par le serveur du tailnet : créer des notebooks, ajouter des sources, chatter, générer des artefacts (podcast, vidéo, slides, infographie, rapport, mind map, quiz, flashcards). À utiliser quand l'utilisateur veut créer un notebook, un podcast/audio à partir de sources, une revue de littérature, ou interroger un corpus. NE PAS installer notebooklm-py en local ni se connecter au compte : compte single-consumer, seul le serveur VPS y touche."
version: 1.0.0
license: MIT
platforms: [linux, macos, windows]
---
# NotebookLM (via outils MCP partagés)

## Principe
NotebookLM se pilote par les **outils MCP `mcp_notebooklm_*`** exposés par le serveur partagé du
tailnet (VPS). L'agent **appelle les outils** ; toute la plomberie (paquet `notebooklm-py`, auth
master-token, re-mint des cookies) vit **côté serveur**. Runbook serveur :
`[[NotebookLM MCP - serveur partage sur le VPS (tailnet)]]` dans le vault.

## ⛔ Règles dures (ne pas violer)
- **NE PAS** `pip install notebooklm-py`, `notebooklm login`, ni lancer la CLI/API en local.
  Le compte NotebookLM est **single-consumer** : deux consommateurs se déconnectent mutuellement.
  Seul le serveur VPS a le droit de toucher le compte. Toi, tu passes **uniquement** par les outils MCP.
- Si les outils `notebooklm` **ne sont pas dans la session** → dire que le guichet MCP n'est pas
  branché/chargé (il se charge au démarrage de session), **ne pas bricoler** un fetch local.
- **Jamais de secret** (bearer token du serveur) dans une note, un log, le vault.

## Prérequis
- Les outils `notebooklm` doivent être **disponibles dans la session** (serveur MCP enregistré +
  session redémarrée). Vérif rapide : lister les outils, chercher le préfixe `notebooklm`.

## Ce qu'on peut générer (artefacts)
`generate` prend `--wait` (attendre la fin), `--language`, souvent un `--format`/`--length`/`--style`.
La génération est **asynchrone** : lancer → récupérer un `task_id`/artifact id → attendre/poller.

| Artefact | Formats / options notables | Sortie |
|---|---|---|
| Podcast (audio) | `deep-dive / brief / critique / debate`, longueur `short/default/long` | .mp3 |
| Vidéo | `explainer/brief/cinematic/short` ; styles (`whiteboard, anime, watercolor…`) ; `cinematic`=Veo3, ~30-40 min, abo Ultra | .mp4 |
| Slide deck | `detailed/presenter` ; portrait 9:16 = **le demander dans le prompt** (pas de flag orientation) | .pdf / .pptx |
| Infographie | orientation `landscape/portrait/square`, styles (`bento-grid, editorial…`) | .png |
| Rapport | `briefing-doc / study-guide / blog-post / custom` | .md |
| Mind map | `interactive` (défaut) ou `note-backed` | .json |
| Data table | description requise | .csv |
| Quiz / Flashcards | `difficulty easy/medium/hard`, quantité | .json/.md/.html |

**Au-delà de l'UI web** : export quiz/flashcards en JSON, slide deck en **.pptx** éditable,
mind map en JSON, `source fulltext <id>`, sauver un Q&A en note, deep research web/Drive.

## Workflows types
- **Piège n°1 (toujours) : une source doit être INDEXÉE/READY avant tout `ask` ou `generate`.**
  Après `source add`, poller le statut (`source list` / `source wait`) jusqu'à READY (~30 s à
  quelques min/source). Chatter/générer trop tôt échoue.
- **Recherche → podcast** : créer notebook → `source add` (URLs/PDF/YouTube) → attendre READY →
  `generate audio "angle voulu"` → attendre la fin → `download`.
- **Analyse de doc** : créer → `source add` doc → `ask "résume / quels arguments"`.
- **Import en masse** : créer → plusieurs `source add` → `source list` pour vérifier.
- **Deep research web** (15-30 min en `deep`) : `source add-research "requête" --mode deep` puis
  attendre l'import. Pour une génération/recherche longue, **déléguer l'attente à un sous-agent**
  (Task `general-purpose` qui `wait` puis `download`) et continuer la conversation principale.

## Limites connues
- **Sources/notebook** selon le plan (Standard 50 / Plus 100 / Pro 300 / Ultra 600) — appliqué par
  le compte, pas par l'outil.
- Types de sources : PDF, URL web, YouTube, Google Docs, texte/Markdown/Word, EPUB, audio, vidéo, images.
- Langue : réglable (`--language` / config) ; défaut `en`. Préciser `fr` pour des artefacts en français.
- API Google **non officielle** → peut casser sans préavis (filtre `essayer`, pas `adopter`).

## Après usage
- Ne pas coller un artefact/transcript brut tel quel dans le vault : garder la **source brute**
  séparée, puis **distiller** (Source → Concept → Décision → Action) — voir `distillation-interview`.

## Liens
Runbook serveur + exploitation : `[[NotebookLM MCP - serveur partage sur le VPS (tailnet)]]`.
Décision d'archi (un seul déploiement, single-consumer) :
`[[ADR 2026-07-22 - NotebookLM via notebooklm-py - un seul deploiement VPS, jamais deux]]`.
Convention de branchement MCP partagé : voir mémoire `guichet-mcp-convention`.
