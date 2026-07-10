---
name: test-driven-development
description: "Développement piloté par les tests avec la discipline RED-GREEN-REFACTOR : écrire un test qui échoue AVANT le code, faire le plus petit changement qui le fait passer, puis refactoriser une fois la preuve obtenue. À utiliser pour le vrai travail de fonctionnalité et les corrections de bug."
version: 1.0.0
license: MIT
platforms: [linux, macos, windows]
---
# TDD — développement piloté par les tests

## Principe
Le test écrit **avant** le code décrit le comportement voulu et prouve, à la fin, qu'il est atteint. Écrire le code d'abord et le test après, c'est décrire ce que le code fait déjà (biais de confirmation), pas ce qu'il devrait faire.

## Le cycle RED → GREEN → REFACTOR

### 🔴 RED — écrire un test qui échoue
- UN test qui décrit le prochain petit comportement attendu.
- **Le lancer et vérifier qu'il échoue** — et qu'il échoue pour la bonne raison (pas une faute de frappe). Un test qui passe tout de suite ne prouve rien.

### 🟢 GREEN — le plus petit code qui fait passer
- Écrire le **minimum** pour passer le test. Pas d'anticipation, pas de généralisation prématurée.
- Relancer : vert.

### 🔵 REFACTOR — nettoyer sous protection du vert
- Améliorer nommage, doublons, structure — **sans** changer le comportement.
- Relancer après chaque pas : toujours vert. Si ça casse, on sait exactement quoi.

## Quand l'utiliser
Vrai travail de fonctionnalité et correction de bug. Pour un bug : écrire d'abord le test qui **reproduit** le bug (rouge), puis corriger (vert) — ça garantit qu'il ne reviendra pas.

## Quand alléger
Spike/exploration jetable (voir `spike`), script one-shot trivial. Mais dès que le code doit vivre, revenir au cycle.

## Règles de qualité
- 1 test = 1 comportement, nom explicite (« retourne 0 pour une liste vide »).
- Ne jamais avancer sur un rouge non compris.
- Ne pas refactoriser et ajouter du comportement dans le même pas.
