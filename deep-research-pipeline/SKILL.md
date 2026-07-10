---
name: deep-research-pipeline
description: "À utiliser quand l'utilisateur veut une recherche de qualité, actuelle et sourcée — un rapport « comme les meilleurs », des réponses sémantiques solides, ou quand une recherche web simple ne suffit pas. Impose un pipeline type Deep Research : cadrage, recherche décomposée, multi-sources, dédoublonnage, scoring de confiance des sources, vérification/critique des citations, synthèse finale."
version: 1.0.0
license: MIT
platforms: [linux, macos, windows]
---
# Pipeline de recherche approfondie

## Principe
Une recherche fiable ne se résume pas à « une requête → un résumé ». La qualité vient de la **décomposition** (plusieurs angles), de la **triangulation** (plusieurs sources par affirmation) et de la **vérification adverse** (chercher à réfuter avant de conclure). Une affirmation non sourcée n'est pas un résultat.

## Quand l'utiliser
Question qui mérite un vrai rapport : décision d'architecture, veille, comparatif, sujet où se tromper coûte cher. Pour une question factuelle simple, une recherche directe suffit.

## Le pipeline
1. **Cadrer** : reformuler la question, découper en 4-6 **angles** distincts (sinon on creuse un seul).
2. **Rechercher en largeur** : un lot de requêtes par angle ; collecter les sources sans filtrer trop tôt.
3. **Récupérer et extraire** : lire les meilleures sources, en tirer des **affirmations falsifiables** (pas des impressions).
4. **Dédoublonner** les affirmations équivalentes issues de sources différentes.
5. **Scorer la confiance** : source primaire (doc officielle, spec, papier) > blog > forum. Noter la qualité par affirmation.
6. **Vérifier / critiquer** : pour chaque affirmation importante, chercher à la **réfuter** (contre-source, cas limite). Ne garder que ce qui survit.
7. **Synthétiser** : rapport structuré, chaque affirmation **citée**, avec les incertitudes et questions ouvertes explicites.

## Règles de qualité
- **Citer au moins une source** par fait affirmé ; sinon `preuve manquante`.
- Distinguer *confirmé* / *contesté* / *non vérifié*.
- Signaler les **angles non couverts** au lieu de laisser croire à l'exhaustivité.

## Lien
Pour un gros volume, ce pipeline se parallélise (plusieurs chercheurs en parallèle, un vérificateur adverse par affirmation) — voir `subagent-driven-development`.
