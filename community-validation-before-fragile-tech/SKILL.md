---
name: community-validation-before-fragile-tech
description: "Valider une méthode technique contre la communauté et la doc AVANT d'agir, et estimer sa probabilité de succès. À utiliser avant de s'engager sur une technique fragile, contournante ou incertaine (scraping, contournement, API non officielle, hack de config) — pour éviter de « réparer » un stack qui n'a pas de vrai problème ou de partir sur une voie sans issue."
version: 1.0.0
license: MIT
platforms: [linux, macos, windows]
---
# Valider avant de s'engager sur du fragile

## Principe
Une technique fragile (scraping, API non officielle, contournement, config exotique) échoue souvent pour des raisons **déjà connues** de la communauté. Vérifier la doc et les retours d'expérience **avant** d'agir évite deux pièges symétriques : (1) s'acharner sur une voie sans issue, (2) « réparer » un composant qui n'était pas cassé.

## Quand l'utiliser
Avant toute méthode incertaine ou contournante ; dès qu'on est tenté de « bricoler » un stack ; quand un composant semble défaillant → d'abord vérifier que le problème est réel.

## La démarche
1. **Formuler la méthode envisagée** en une phrase testable.
2. **Confronter aux sources** : doc officielle, issues/discussions récentes, retours d'usage. La méthode est-elle supportée, dépréciée, connue pour casser ?
3. **Estimer une probabilité de succès** explicite (haute / moyenne / faible) + la principale cause d'échec connue.
4. **Diagnostiquer avant de réparer** : si un composant paraît cassé, prouver la panne (log, test) avant de le reconfigurer. Un état « intermittent » peut être **voulu** (service éteint volontairement), pas une dérive.

## Règle de qualité
Si la probabilité est faible ou la preuve manque → répondre **`preuve manquante`** et proposer comment l'obtenir, plutôt que de foncer. Une voie fragile choisie en connaissance de cause est acceptable ; choisie par défaut, non.

## Leçon type
Avant de conclure « le stack a dérivé », vérifier : (a) le composant est-il censé tourner là, maintenant ? (b) le chemin/hôte est-il le bon (piège conteneur vs hôte) ? (c) quelqu'un a-t-il documenté ce symptôme ?
