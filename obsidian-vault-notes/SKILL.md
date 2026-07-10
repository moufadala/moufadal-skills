---
name: obsidian-vault-notes
description: "Lire, chercher, créer et éditer des notes dans un vault Obsidian (markdown) proprement : frontmatter cohérent, wikilinks, une note = un sujet, réponse État/Preuve/Action. À utiliser quand l'utilisateur veut ranger une info dans son vault, créer une fiche projet/décision/source, ou retrouver/relier des notes."
version: 1.0.0
license: MIT
platforms: [linux, macos, windows]
---
# Notes de vault (Obsidian / markdown)

## Principe
Un vault n'a de valeur que s'il **répond vite avec preuve**. On écrit du markdown lisible par un humain ET un agent, pas des dumps bruts. Une note = un sujet, reliée aux autres.

## Où vit le vault
Un dossier de fichiers markdown. **Demander le chemin** (ou utiliser le vault configuré du projet) ; ne jamais coder un chemin machine en dur.

## Avant d'écrire (orientation)
1. Lire le cockpit / l'index d'entrée du vault.
2. Chercher si une note couvre déjà le sujet → **étendre** plutôt que dupliquer (un doublon = deux vérités).
3. Repérer le bon dossier / la bonne couche (source brute vs note distillée vs décision).

## Structure d'une note structurante
- **Frontmatter** cohérent : `type`, `title`, `description`, `tags`, `timestamp`, `sensitivity`.
- Corps qui répond **État / Preuve / Action** : où on en est, la preuve (source/commande/lien), la prochaine action vérifiable.
- **Wikilinks** `[[...]]` vers les notes liées ; titre = l'insight (« X n'est utile que si… »), pas « Notes sur X ».

## Règles de qualité
- **Une note = un sujet** ; relier plutôt que gonfler.
- **Citer une source** pour tout fait ; si elle manque → `preuve manquante`.
- **Jamais de secret** (token, `.env`, cookie, mot de passe) ni de donnée personnelle sensible dans une note partagée.
- Reformuler avec ses mots ; pas de copier-coller de paragraphes bruts.

## Deux étages
Garder la **source brute** (filet cherchable, jamais modifié) séparée de la **note distillée** (propre, curée). On ne distille que ce qui a un usage — voir `distillation-interview`. Pour une base plus structurée en entités/concepts, voir `llm-wiki`.
