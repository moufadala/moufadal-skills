---
name: llm-wiki
description: "Construire et maintenir une base de connaissance markdown interconnectée (pattern « LLM Wiki » de Karpathy) : ingérer des sources, créer des pages entité/concept/comparaison reliées par des wikilinks, garder un index et un journal. À utiliser quand l'utilisateur veut créer / alimenter / interroger un wiki ou un second brain markdown, ingérer une source, ou auditer la cohérence de ses notes."
version: 1.0.0
license: MIT
platforms: [linux, macos, windows]
---
# LLM Wiki — base de connaissance markdown « compounding »

Construire une base de connaissance **durable et cumulative** en fichiers markdown reliés. Contrairement au RAG (qui redécouvre le savoir à chaque requête), le wiki **compile le savoir une fois** et le garde à jour : les liens croisés sont déjà là, les contradictions déjà signalées.

**Répartition des rôles** : l'humain choisit les sources et dirige l'analyse ; l'agent résume, relie, classe et maintient la cohérence.

## Quand l'utiliser
- Créer / démarrer un wiki ou un second brain markdown.
- Ingérer une source (article, transcript, papier) dans le wiki.
- Répondre à une question quand un wiki existe déjà.
- Auditer / linter la cohérence du wiki.

## Où vit le wiki
Un simple dossier de fichiers markdown — ouvrable dans Obsidian, VS Code, n'importe quel éditeur. Aucune base de données. **Demander le chemin à l'utilisateur** (ou utiliser le dossier de vault configuré du projet) ; ne jamais coder un chemin machine en dur.

## Architecture — 3 couches
```
wiki/
├── SCHEMA.md      # conventions, structure, taxonomie de tags
├── index.md       # catalogue des pages, 1 ligne de résumé chacune
├── log.md         # journal chronologique, append-only
├── raw/           # Couche 1 : sources brutes, IMMUABLES (jamais modifiées)
├── entities/      # Couche 2 : pages entité (personnes, orgs, produits)
├── concepts/      # Couche 2 : pages concept / sujet
└── comparisons/   # Couche 2 : analyses comparées
```
- **Couche 1 — sources brutes** : immuables ; l'agent lit, ne modifie jamais.
- **Couche 2 — le wiki** : pages markdown créées et reliées par l'agent.
- **Couche 3 — le schéma** (`SCHEMA.md`) : structure, conventions, tags.

## Rituel d'orientation (À CHAQUE session sur un wiki existant)
Avant toute action :
1. Lire `SCHEMA.md` (domaine, conventions, taxonomie).
2. Lire `index.md` (pages existantes + résumés).
3. Parcourir la fin de `log.md` (20-30 dernières entrées).

Puis, pour un gros wiki, chercher le sujet courant avant de créer quoi que ce soit. Ça évite : doublons, liens manqués, contradictions avec le schéma, travail refait.

## Frontmatter d'une page
```yaml
---
title: Titre de la page
created: AAAA-MM-JJ
updated: AAAA-MM-JJ
type: entity | concept | comparison | query | summary
tags: [issus de la taxonomie]
sources: [raw/articles/source.md]
confidence: high | medium | low   # optionnel
contested: true                   # si contradictions non résolues
---
```
Les sources brutes reçoivent aussi un petit frontmatter (`source_url`, `ingested`, `sha256` du corps) pour détecter les ré-ingestions et les dérives.

## Seuils (éviter le fouillis)
- **Créer une page** quand une entité/concept apparaît dans 2+ sources OU est centrale à une source.
- **Compléter une page existante** quand la source recoupe l'existant.
- **NE PAS créer** de page pour une mention en passant.
- **Scinder** une page > ~200 lignes en sous-sujets reliés.
- **Archiver** une page entièrement remplacée.

## Politique de mise à jour (contradictions)
1. Comparer les dates (le plus récent prime en général).
2. Si vraiment contradictoire : noter les deux positions avec dates + sources.
3. Marquer `contradictions: [autre-page]` dans le frontmatter.
4. Signaler pour revue humaine.

## Règles de cohérence
- Fichiers : minuscules, tirets, pas d'espaces (`transformer-architecture.md`).
- Chaque page : ≥ 2 wikilinks sortants `[[...]]`, ajoutée à `index.md`, action loggée dans `log.md`.
- Chaque tag utilisé doit exister dans la taxonomie du `SCHEMA.md` (l'ajouter **avant** usage) → évite la prolifération de tags.

## Principe directeur
Le but n'est pas d'accumuler des notes, mais de **répondre vite avec preuve** : où on en est, pourquoi, quelle source, ce qui a changé, prochaine action. Markdown-first ; pas de RAG / vector lourd tant que le volume ne le justifie pas.
