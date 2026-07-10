---
name: writing-plans
description: "Écrire un plan d'implémentation exécutable : tâches petites et vérifiables, chemins de fichiers, extraits de code, critères de « fait ». À utiliser avant d'attaquer une fonctionnalité ou un chantier non trivial, pour transformer une intention floue en étapes concrètes qu'un agent ou un humain peut exécuter sans deviner."
version: 1.0.0
license: MIT
platforms: [linux, macos, windows]
---
# Écrire un plan d'implémentation

## Principe
Un bon plan sépare la **réflexion** (quoi/pourquoi/dans quel ordre) de l'**exécution** (taper le code). Écrit d'abord, il révèle les trous et les dépendances avant qu'ils ne coûtent cher, et il permet de déléguer sans re-expliquer.

## Ce qu'un plan doit contenir
- **Objectif** : le résultat visé en 1-2 lignes + comment on saura que c'est atteint.
- **Contexte / contraintes** : fichiers concernés, ce qu'il ne faut pas casser.
- **Tâches** : découpées en pas **petits et vérifiables**, dans l'ordre de dépendance. Chaque tâche cite les **chemins de fichiers** exacts et, si utile, un extrait de code.
- **Critères de fin** par tâche (test qui passe, commande qui répond, fichier créé).
- **Risques / inconnues** : ce qui pourrait invalider le plan, et comment lever le doute.

## Règle du grain
Une tâche = quelque chose qu'on peut faire **et prouver** en un pas. Si une tâche est vague (« améliorer la perf »), la découper jusqu'à ce que chaque sous-tâche ait un critère de fin objectif.

## Quand l'utiliser
Avant toute fonctionnalité ou refonte non triviale, migration, ou dès que le travail dépasse quelques fichiers. Pour un one-liner évident, pas besoin.

## Anti-patterns
- Plan qui décrit un but sans étapes vérifiables → intention, pas plan.
- Mélanger plan et exécution : écrire le plan d'abord, l'exécuter ensuite.
- Sauter les critères de fin → on ne sait jamais si c'est « fini » (voir `definition-of-done`).
