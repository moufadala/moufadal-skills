---
name: search-first-before-build
description: "À utiliser AVANT d'implémenter un module, une fonctionnalité, une architecture, un workflow, une structure de vault, un scraper ou une intégration d'outil non triviaux — pour éviter de réinventer l'existant. Force une recherche de l'art antérieur (local + externe), puis un verdict adopter / étendre / construire."
version: 1.0.0
license: MIT
platforms: [linux, macos, windows]
---
# Chercher avant de construire

## Principe
La plupart des problèmes ont déjà une solution : dans ton propre système, dans une lib, dans un pattern communautaire. Coder d'abord, c'est risquer de réinventer (moins bien) quelque chose qui existe — et de le maintenir seul. **Chercher coûte quelques minutes ; réinventer coûte des semaines.**

## Quand l'utiliser
Avant tout module / feature / architecture / workflow / structure de vault / scraper / intégration non trivial. Pour un one-liner évident, inutile.

## La recherche (deux directions, toujours les deux)
1. **Interne** : ai-je déjà ça ? — chercher dans le code, les notes/runbooks, les skills existants, l'historique. Un doublon interne est le pire (deux sources de vérité).
2. **Externe** : quelqu'un a-t-il déjà résolu ça ? — lib maintenue, outil standard, pattern documenté, discussion communautaire. Noter maturité, maintenance, adéquation.

## Le verdict (obligatoire avant de coder)
Conclure par UN des trois :
- **Adopter** : une solution existante convient → l'utiliser telle quelle.
- **Étendre** : une base existe mais incomplète → la compléter plutôt que repartir de zéro.
- **Construire** : rien d'adéquat (ou dépendance trop fragile/risquée) → construire, en justifiant *pourquoi* l'existant ne suffit pas.

## Règle de qualité
Le verdict « construire » doit **citer ce qu'on a écarté et pourquoi**. Sans cette trace, c'est un réflexe « pas inventé ici », pas une décision. Voir aussi `community-validation-before-fragile-tech` pour estimer la fiabilité d'une méthode avant de s'y engager.
