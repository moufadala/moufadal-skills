---
name: definition-of-done
description: "À utiliser dès que l'utilisateur dit fini, terminé, prêt, done, « continue jusqu'au bout », ou demande si un projet/phase/tâche est vraiment complet. Définit des critères de « fait » vérifiables AVANT de déclarer terminé — pour code, VPS, scraping, dashboards, recherche, déploiements."
version: 1.0.0
license: MIT
platforms: [linux, macos, windows]
---
# Définition de « fait »

## Principe
« C'est fini » sans critère vérifiable, c'est une opinion. Le travail est fini quand il **passe des vérifications objectives** définies à l'avance — pas quand il « a l'air » fini ou qu'on est fatigué. Déclarer terminé trop tôt reporte le vrai coût plus loin (et plus cher).

## Quand l'utiliser
Aux mots « fini / terminé / prêt / done / jusqu'au bout », et avant toute livraison, clôture de phase, ou annonce « ça marche ».

## Définir le « fait » AVANT de commencer (ou au plus tôt)
Une tâche a une **Definition of Done** = une liste de critères vérifiables, ex. :
- **Code** : compile, tests passent, pas de régression, lint OK.
- **Comportement** : le cas réel visé fonctionne, prouvé par une exécution (pas une supposition).
- **Cas limites** : vide / invalide / gros volume gérés.
- **Trace** : preuve attachée (commande + sortie, capture, log, URL testée).
- **Propreté** : hacks de debug retirés, doc/notes à jour.

## Le rituel de clôture
1. Ressortir la liste de critères.
2. **Prouver chacun** — exécuter, ne pas affirmer. « Les tests passent » → montrer la sortie.
3. Si un critère échoue ou n'est pas prouvé → **pas fini**. Le dire clairement, avec ce qui manque.
4. Rapporter honnêtement : ce qui est fait+prouvé, ce qui est sauté, ce qui a échoué.

## Règle de qualité (anti-complaisance)
Ne jamais dire « c'est fait » sans preuve. Si un test échoue, le dire avec la sortie. « Fait » = vérifié, pas espéré.
