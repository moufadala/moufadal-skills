---
name: requesting-code-review
description: "Passer une revue avant de commiter/livrer : scan de sécurité, portes de qualité, correction des problèmes trouvés. À utiliser avant un commit important, une PR, ou une livraison — pour attraper secrets, régressions, bugs et manques de tests avant qu'ils partent."
version: 1.0.0
license: MIT
platforms: [linux, macos, windows]
---
# Revue avant commit / livraison

## Principe
Une relecture délibérée juste avant de figer attrape ce que l'élan de l'implémentation masque : un secret oublié, une régression, un cas limite non géré. Cinq minutes de revue valent des heures de correction en aval.

## Quand l'utiliser
Avant un commit conséquent, une PR, une livraison, un push sur un dépôt partagé.

## Les portes (dans l'ordre)
1. **Sécurité** : aucun secret / token / `.env` / credential dans le diff. Aucune donnée personnelle qui ne devrait pas fuir. C'est bloquant.
2. **Correctness** : le changement fait ce qu'il prétend ; les cas limites (vide, invalide, gros volume) tiennent ; pas de régression évidente sur le code voisin.
3. **Tests** : le comportement nouveau/corrigé est couvert par un test qui échouerait sans le changement.
4. **Qualité** : nommage clair, pas de code mort ni de hack de debug oublié (voir `simplify-code`).
5. **Portée** : le diff ne touche que ce qu'il doit ; rien hors sujet ne s'est glissé dedans.

## Méthode
- **Lire le diff en entier**, ligne à ligne — pas seulement les fichiers qu'on croit avoir touchés.
- Pour chaque problème : le **prouver** (scénario concret) avant de le corriger, et le corriger avant de figer.
- Sur un gros diff, déléguer plusieurs relecteurs par dimension puis vérifier (voir `subagent-driven-development`).

## Règle de qualité
Un problème de sécurité non résolu **bloque** le commit. Pour le reste, classer par gravité et corriger le sérieux avant de livrer. Rapporter honnêtement ce qui reste en suspens.
