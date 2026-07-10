---
name: specification-par-exemples
description: "À utiliser quand une demande de fonctionnalité est floue : intention métier vague, entrées en langage naturel, cas limites cachés, ou « ça doit marcher comme tel autre produit ». Transforme la demande en spécification légère par l'exemple — critères d'acceptation, questions de clarification là où l'ambiguïté demeure, puis portes de QA exécutables avant de coder."
version: 1.0.0
license: MIT
platforms: [linux, macos, windows]
---
# Spécification par l'exemple

## Principe
Un cahier des charges abstrait (« le système doit gérer les utilisateurs ») laisse place à l'interprétation → on code la mauvaise chose. Des **exemples concrets** (entrée → sortie attendue) lèvent l'ambiguïté mieux que n'importe quelle prose, et deviennent directement des **tests d'acceptation**.

## Quand l'utiliser
Demande à intention métier floue, entrées en langage naturel, « comme [autre produit] », cas limites pressentis mais non dits. Avant de coder une feature dont le comportement n'est pas 100 % clair.

## La démarche
1. **Recueillir des exemples**, pas des règles : « pour cette entrée, voilà la sortie attendue ». Couvrir le cas nominal + 2-3 cas limites (vide, invalide, extrême).
2. **Dériver les critères d'acceptation** de ces exemples : une liste de « étant donné… quand… alors… » vérifiables.
3. **Ne poser des questions QUE là où l'ambiguïté métier subsiste** — pas de questionnaire inutile sur ce qui est déjà clair. Une question ciblée > dix questions génériques.
4. **Portes de QA exécutables** : transformer les critères en vérifications (tests, checks manuels reproductibles) **avant** d'écrire l'implémentation.

## Règle de qualité
Si l'utilisateur dit « comme le produit X », capturer le comportement précis de X en exemples — ne pas supposer qu'on partage la même image mentale. Un exemple ambigu qui reste ambigu après clarification = un trou à signaler, pas à combler par hypothèse.

## Lien
Les exemples/critères alimentent directement `test-driven-development` (chaque critère → un test rouge) et `definition-of-done`.
