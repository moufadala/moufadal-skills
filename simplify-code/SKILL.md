---
name: simplify-code
description: "Nettoyer et simplifier des changements de code récents sans changer leur comportement : supprimer doublons, morts, abstractions prématurées, nommage obscur. À utiliser après avoir fait passer une fonctionnalité (phase REFACTOR), avant de commiter, ou quand du code « marche mais est moche »."
version: 1.0.0
license: MIT
platforms: [linux, macos, windows]
---
# Simplifier le code

## Principe
Du code qui marche n'est pas forcément du code fini. La complexité inutile est une dette : elle ralentit chaque lecture et chaque modif futures. On simplifie **une fois le comportement prouvé** (tests verts), pas avant.

## Quand l'utiliser
Après avoir fait passer une feature/un fix (la phase REFACTOR du TDD), avant de commiter, ou en revue quand du code « fonctionne mais est confus ». **Jamais** en même temps qu'on ajoute du comportement.

## Où chercher (cibles fréquentes)
- **Duplication** : même logique à 2+ endroits → factoriser (mais pas avant 2-3 occurrences réelles).
- **Code mort** : branches jamais atteintes, variables/imports inutilisés, commentaires périmés.
- **Abstraction prématurée** : couche/généricité pour un seul cas d'usage → aplatir.
- **Nommage** : noms qui n'expliquent pas l'intention → renommer.
- **Complexité de flux** : imbrications profondes, conditions inversables → early-return, simplifier.

## Méthode
1. Délimiter le périmètre : les changements récents, pas tout le repo.
2. Un type de simplification à la fois, **petits pas**.
3. **Relancer les tests après chaque pas** — le vert protège le comportement. S'il casse, c'est que la « simplification » changeait le comportement : annuler.

## Règle de qualité
Simplifier ne doit rien changer d'observable. Si tu ne peux pas prouver l'iso-comportement (pas de test qui couvre), écris d'abord le test, puis simplifie. Préférer « lisible et évident » à « malin et court ».
