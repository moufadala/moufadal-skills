---
name: spike
description: "Expérience jetable pour valider une idée ou lever une incertitude AVANT de construire pour de vrai : tester une API, mesurer une faisabilité, comparer deux approches. À utiliser quand on ne sait pas si quelque chose est possible/adéquat et qu'on serait tenté de « voir en construisant »."
version: 1.0.0
license: MIT
platforms: [linux, macos, windows]
---
# Spike — expérience jetable

## Principe
Quand une inconnue bloque une décision (« est-ce que cette lib gère X ? », « cette approche tient-elle la charge ? »), construire la vraie solution pour le découvrir est coûteux et biaise (on s'attache au code écrit). Un **spike** répond à *une* question, vite, avec du code **explicitement jetable**.

## Quand l'utiliser
Faisabilité incertaine, choix entre deux approches, API/outil inconnu, estimation de perf. **Pas** pour du code qui doit vivre — un spike n'est jamais livré tel quel.

## Les règles
1. **Une seule question**, formulée à l'avance : « je veux savoir si… ». La réponse conclut le spike.
2. **Timebox** : se fixer une limite (temps/effort). Le but est d'apprendre, pas de finir.
3. **Jetable assumé** : pas de tests, pas de propreté, pas de cas limites. On optimise la vitesse d'apprentissage.
4. **Isolé** : branche/dossier à part, jamais mélangé au vrai code.

## À la fin (obligatoire)
- **Écrire la réponse** : ce qu'on a appris, la décision que ça permet (adopter / rejeter / creuser).
- **Jeter le code** — ou, si on le garde comme base, le réécrire proprement en TDD. Ne pas laisser du code de spike devenir de la prod par glissement (piège classique).

## Règle de qualité
Un spike sans conclusion écrite est du temps perdu : la valeur est la **décision**, pas le code. Distinguer clairement « spike » (jetable) de « prototype » (base à durcir).
