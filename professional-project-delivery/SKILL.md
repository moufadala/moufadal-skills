---
name: professional-project-delivery
description: "À utiliser quand l'utilisateur demande un livrable sérieux/professionnel — suite web, dashboard, feature produit, artefact client, ou tout projet multi-étapes où la qualité compte. Impose un mode ingénierie : découverte, contrat d'acceptation, portes de QA, et remise finale vérifiée."
version: 1.0.0
license: MIT
platforms: [linux, macos, windows]
---
# Livraison de projet professionnelle

## Principe
Un livrable sérieux n'est pas « du code qui tourne sur ma machine » : c'est un résultat **cadré, vérifié et remis proprement**. Le mode ingénierie évite le piège du « ça marche chez moi » et des allers-retours interminables.

## Quand l'utiliser
Livrable client-facing, suite web, dashboard, feature produit, tout projet multi-étapes à enjeu. Pas pour un script jetable.

## Les 4 phases
1. **Découverte** : clarifier le besoin réel et le « fait » attendu. Reformuler par l'exemple (voir `specification-par-exemples`). Lever les ambiguïtés métier **avant** de coder.
2. **Contrat d'acceptation** : lister les critères vérifiables que le livrable doit satisfaire (voir `definition-of-done`). C'est l'engagement partagé.
3. **Exécution cadrée** : plan en tranches livrables (`writing-plans`), chaque tranche produisant une preuve. Chercher l'existant avant de construire (`search-first-before-build`).
4. **QA + remise** : exercer réellement le livrable (`dogfood-qa`), passer les portes de qualité/sécurité (`requesting-code-review`), puis remettre — avec les preuves et le mode d'emploi.

## La remise finale
- Le livrable **fait ce que dit le contrat**, prouvé, pas supposé.
- Preuves attachées (tests, captures, URL testée).
- Points en suspens **listés honnêtement**, pas cachés.

## Règle de qualité
Ne jamais annoncer « livré » sans avoir passé le contrat d'acceptation. Un livrable pro se juge sur la preuve, pas sur l'effort. Qualité proportionnée à l'enjeu — ne pas sur-processer un petit besoin.
