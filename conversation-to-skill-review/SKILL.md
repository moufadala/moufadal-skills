---
name: conversation-to-skill-review
description: "Décider quoi retenir durablement d'une interaction : mémoire, note de vault, correctif de skill, ou nouveau skill — avec preuve. À utiliser quand l'utilisateur demande ce qu'on peut apprendre d'une session, dit que l'agent a répété une erreur, veut mettre à jour la bibliothèque de skills, ou transformer un échange en comportement durable."
version: 1.0.0
license: MIT
platforms: [linux, macos, windows]
---
# De la conversation au skill

## Principe
Un enseignement tiré d'une session ne vaut que s'il est **capturé au bon endroit**. Tout ne mérite pas un skill : sur-produire des skills pollue autant que ne rien capitaliser. La question n'est pas « quoi retenir ? » mais « **où** ça doit vivre pour resservir ? ».

## Quand l'utiliser
Après une session instructive ; quand l'agent a répété une erreur ; quand l'utilisateur demande d'améliorer la bibliothèque ou de « graver » un apprentissage.

## L'arbre de décision (où ça va)
- **Fait ponctuel / préférence de l'utilisateur / contexte projet** → **mémoire** (une info = un fait).
- **Connaissance de fond, décision, preuve** → **note de vault** (source/concept/décision, voir `obsidian-vault-notes`).
- **Un skill existant a mal agi ou manque un cas** → **correctif de skill** (patcher sa description ou son corps) plutôt que d'en créer un nouveau.
- **Un comportement réutilisable manque totalement** → **nouveau skill** (voir `skill-creator`), et seulement si aucun existant ne le couvre.

## La démarche
1. **Nommer l'apprentissage** en une phrase : qu'est-ce qui a été non-évident ?
2. **Chercher l'existant** : un skill/une note couvre-t-il déjà ? → étendre, pas dupliquer.
3. **Exiger une preuve** : sur quoi s'appuie l'enseignement (un échec réel, une correction de l'utilisateur) ? Pas de skill fondé sur une intuition.
4. **Choisir UN emplacement** via l'arbre ci-dessus, écrire, relier.

## Règle de qualité
Préférer **corriger/étendre** l'existant à créer du neuf. Un nouveau skill se justifie par un manque réel + une preuve, pas par l'envie de capitaliser. Ne jamais graver une donnée personnelle sensible dans un skill partagé.
