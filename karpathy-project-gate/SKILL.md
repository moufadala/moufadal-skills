---
name: karpathy-project-gate
description: "Porte légère à passer au démarrage/reprise d'un projet sérieux : simplifier, quantifier, cadrer l'exécution, router vers les bons skills, exiger des artefacts vérifiés — sans imposer un processus lourd à une tâche triviale. À utiliser quand l'utilisateur lance ou reprend un projet et se demande s'il est bien cadré ou si c'est du bricolage."
version: 1.0.0
license: MIT
platforms: [linux, macos, windows]
---
# Porte de projet (légère)

## Principe
Avant d'investir dans un projet, un petit sas évite deux échecs : (1) partir dans tous les sens sans cadrage, (2) sur-processer une tâche qui ne le mérite pas. La porte est **proportionnée** : plus le projet est sérieux/coûteux, plus elle est stricte.

## Quand l'utiliser
Au démarrage ou à la reprise d'un projet non trivial, ou quand l'utilisateur demande « est-ce robuste ? est-ce que c'est du bricolage ? ».

## La porte (5 checks)
1. **Simplifier** : quelle est la version la plus simple qui délivre la valeur ? Retirer tout ce qui n'est pas nécessaire au premier résultat utile.
2. **Quantifier** : c'est quoi « réussi », mesurablement ? (voir `definition-of-done`). Sans métrique, on ne saura pas si on avance.
3. **Cadrer l'exécution** : découper en pas vérifiables (voir `writing-plans`) ; identifier la première tranche livrable.
4. **Router vers les bons skills** : quel(s) skill(s) existant(s) s'appliquent ? A-t-on cherché l'art antérieur (`search-first-before-build`) ?
5. **Exiger des artefacts vérifiés** : chaque étape produit une preuve (test, sortie, capture), pas une affirmation.

## Dosage (ne pas sur-appliquer)
- Tâche triviale / one-shot → sauter la porte, juste faire.
- Projet moyen → checks 1-3.
- Projet sérieux / à enjeu → les 5, sérieusement.

## Règle de qualité
La porte sert à **accélérer** en évitant le travail refait, pas à ajouter de la cérémonie. Si un check ralentit sans réduire un risque réel, l'alléger.
