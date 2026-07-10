---
name: youtube-transcript
description: "Récupérer le transcript (sous-titres) d'une vidéo YouTube via l'outil MCP youtube_transcript, quand un agent a accès au guichet MCP partagé. À utiliser quand l'utilisateur envoie un lien YouTube à distiller/analyser et qu'il faut d'abord en obtenir le texte. Gère proxy éteint et absence de sous-titres."
version: 1.0.0
license: MIT
platforms: [linux, macos, windows]
---
# Récupérer un transcript YouTube (via outil MCP)

## Principe
Le transcript se récupère par un **outil MCP partagé** (`youtube_transcript`) exposé par le guichet du tailnet — pas en réinstallant yt-dlp/proxy sur chaque machine. L'agent appelle l'outil ; la plomberie (proxy résidentiel, yt-dlp) vit côté serveur.

## Prérequis
- L'outil `youtube_transcript(url, lang)` doit être **disponible dans la session** (serveur MCP enregistré et chargé au démarrage). Sinon → dire que le guichet n'est pas branché, ne pas bricoler un fetch local.
- Le **proxy résidentiel doit être allumé** (sinon YouTube bloque). L'outil renvoie un message clair si c'est éteint.

## Workflow
1. **Appeler l'outil** : `youtube_transcript(url)` (langue par défaut `fr,en` ; préciser `lang` si besoin).
2. **Lire le retour** :
   - Texte des sous-titres → OK, passer à l'étape suivante.
   - `[PROXY OFF]` → demander à l'utilisateur de **rallumer le proxy**, puis réessayer.
   - `[AUCUN SOUS-TITRE]` → la vidéo n'a pas de sous-titres (le fallback whisper n'est pas garanti en v1) ; proposer une alternative (autre source, ou activer whisper côté serveur).
3. **Ne pas coller le transcript brut** dans le vault tel quel : l'enregistrer comme **source brute** (filet cherchable) puis enchaîner sur la **distillation** — voir `distillation-interview`.

## Règles de qualité
- Le transcript brut est un **moyen**, pas la fin : la valeur vient de la distillation (Source → Concept → Décision → Action).
- Garder la source brute séparée de la note distillée (deux étages).
- Ne jamais écrire de secret (token du guichet MCP) dans une note.

## Lien
Une fois le transcript obtenu → `distillation-interview` pour le transformer en connaissance reliée.
