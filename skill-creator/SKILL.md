---
name: skill-creator
description: "Créer, améliorer et évaluer des skills au format Agent Skills. À utiliser pour écrire un nouveau skill depuis zéro, corriger/optimiser un skill existant, améliorer sa description pour un meilleur déclenchement, ou auditer une bibliothèque de skills. C'est le méta-skill qui sert à maintenir tous les autres."
version: 1.0.0
license: MIT
platforms: [linux, macos, windows]
---
# Créer et maintenir des skills

## Ce qu'est un skill (rappel)
Un dossier avec un `SKILL.md` : frontmatter YAML (`name` + `description` requis) + un corps markdown. Chargé dynamiquement, découvert par sa **description**. C'est un format ouvert, portable et git-partageable.

## La description est le levier n°1
Un skill n'est utile que s'il se **déclenche** au bon moment. La `description` doit dire **CE QUE** fait le skill **ET QUAND** l'utiliser, avec les mots que l'utilisateur emploierait.
- ✅ « Débogage par cause racine en 4 phases… à utiliser pour tout test qui échoue, bug prod, build cassé. »
- ❌ « Use whenever the user asks about X, related setup, troubleshooting, automation, workflows… » (texte auto-généré, ne discrimine rien → mauvais déclenchement).

## Règle d'or : skills NEUTRES (pour un parc multi-agents)
Décrire **quoi / quand**, jamais le **comment** propre à un runtime :
- pas de nom d'outil spécifique (traduire en action : « crée la note », « lis le fichier ») ;
- pas de chemin machine codé en dur (parler du « vault », du « projet ») ;
- aucune donnée personnelle.
→ Ainsi le même skill tourne sur plusieurs agents. *(Le format est portable ; les OUTILS qu'un skill invoque doivent exister sur chaque machine — c'est la vraie limite.)*

## Structure d'un bon skill
- **Principe** : pourquoi, en 2-3 lignes.
- **Quand l'utiliser** (et quand alléger).
- **Le workflow** : étapes concrètes, vérifiables.
- **Règles de qualité / anti-patterns**.
Garder court : un skill est un aide-mémoire déclenchable, pas un cours.

## Créer / améliorer
1. **Un skill = un sujet.** Si ça couvre deux choses, scinder.
2. **Chercher d'abord** un skill existant qui recouvre (voir `search-first-before-build`) → étendre plutôt que dupliquer.
3. **Tester le déclenchement** : la description matche-t-elle les formulations réelles de l'utilisateur ? Ajuster les mots-clés.
4. **Auditer un parc** : repérer descriptions auto-générées, doublons, skills jamais déclenchés, skills couplés à un outil absent → réécrire, fusionner ou archiver.

## Anti-patterns
Description fourre-tout ; skill géant multi-sujets ; comment codé en dur ; recopier un skill d'un autre runtime sans le neutraliser.
