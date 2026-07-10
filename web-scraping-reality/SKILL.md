---
name: web-scraping-reality
description: "Connaissances statiques sur le web scraping : hiérarchie des solutions (du plus simple au plus lourd), coûts réels, pièges connus, réflexes. À charger AVANT toute session de scraping ou de récupération de données web, pour choisir la bonne approche et ne pas ré-apprendre les bases en se cassant les dents."
version: 1.0.0
license: MIT
platforms: [linux, macos, windows]
---
# La réalité du web scraping

## Principe
Le scraping échoue presque toujours pour des raisons **déjà connues**. La bonne stratégie n'est pas « lancer un navigateur headless », c'est **partir du plus simple** et ne monter en lourdeur que si nécessaire. Chaque niveau coûte plus (fragilité, maintenance, détection).

## Hiérarchie des solutions (essayer dans cet ordre)
1. **API officielle / flux structuré** (RSS, JSON, endpoint documenté) → toujours préférable. Stable, légal, propre.
2. **Requête HTTP simple + parsing HTML** → pour du contenu servi côté serveur, sans JS.
3. **Rendu JS** (navigateur headless) → seulement si le contenu est injecté côté client. Coûteux, plus détectable.
4. **Contournements** (proxy résidentiel, rotation, anti-bot) → dernier recours, fragile, à valider avant (voir `community-validation-before-fragile-tech`).

## Pièges connus
- **Antibot / blocage** : souvent dû à l'IP (datacenter détecté) ou à l'absence de proxy adéquat — pas forcément à un « stack cassé ». Diagnostiquer avant de tout reconfigurer.
- **Contenu dynamique** : ce que tu vois dans le navigateur ≠ ce que renvoie la requête brute.
- **Fragilité structurelle** : un scraper basé sur la structure HTML casse au moindre changement du site.
- **Rate limiting** : trop de requêtes trop vite → bannissement temporaire.

## Réflexes
- Chercher d'abord une **API** ou un outil dédié éprouvé avant d'écrire un scraper maison (`search-first-before-build`).
- **Prouver la panne** avant de « réparer » un composant : un service peut être éteint volontairement, pas cassé.
- Respecter les conditions d'usage et la charge du site cible.

## Règle de qualité
Choisir le **niveau le plus bas** qui marche. Monter d'un cran seulement avec une raison prouvée. Un scraping fragile assumé est acceptable ; choisi par défaut, non.
