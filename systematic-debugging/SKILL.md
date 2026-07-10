---
name: systematic-debugging
description: "Débogage par cause racine en 4 phases : comprendre le bug AVANT de le corriger. À utiliser pour toute panne technique — test qui échoue, bug en prod, comportement inattendu, build cassé, lenteur — surtout sous pression quand « un petit fix rapide » est tentant."
version: 1.0.0
license: MIT
platforms: [linux, macos, windows]
---
# Débogage systématique

## Principe
Les corrections au hasard perdent du temps et créent de nouveaux bugs. **Toujours trouver la cause racine avant de corriger.** Corriger un symptôme = échec.

## La loi de fer
> **Aucune correction sans enquête de cause racine d'abord.**
Tant que la phase 1 n'est pas finie, on ne propose pas de fix.

## Quand l'utiliser
Toute panne : test qui échoue, bug prod, comportement inattendu, perf, build, intégration.
**Surtout** sous pression, quand « un seul petit fix » semble évident, ou quand un fix précédent n'a pas marché. Ne pas sauter parce que « ça a l'air simple » — un bug simple a quand même une cause.

## Les 4 phases (dans l'ordre, pas de saut)

### 1. Enquête — trouver la cause racine
- Lire le message d'erreur **en entier**, ne pas survoler.
- Reproduire le bug de façon fiable (cas minimal).
- Remonter la chaîne : où la donnée / l'état dévie-t-il pour la première fois ?
- Formuler une **hypothèse falsifiable** de cause racine (pas « ça doit être X »).

### 2. Vérifier l'hypothèse
- Un test / une mesure qui **prouve** la cause (log ciblé, breakpoint, print). 
- Si l'hypothèse tombe → retour phase 1. Ne pas corriger une cause non prouvée.

### 3. Corriger la cause, pas le symptôme
- La plus petite modification qui traite la **cause** identifiée.
- Pas de contournement qui masque le problème.

### 4. Vérifier la correction
- Le cas de repro échoue-t-il maintenant de la bonne façon → passe ?
- Aucune régression ailleurs. Nettoyer les logs/hacks de debug.

## Règle de qualité
Annoncer sa **prédiction** avant chaque test, comparer au résultat, concéder si l'hypothèse était fausse. Le systématique est *plus rapide* que le tâtonnement, pas plus lent.
