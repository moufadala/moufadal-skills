---
name: subagent-driven-development
description: "Exécuter un plan en déléguant des tâches à des sous-agents, avec revue avant d'intégrer. À utiliser pour un travail décomposable en morceaux parallélisables (recherche multi-angles, revue multi-dimensions, migration sur N fichiers) ou quand un problème dépasse ce qu'un seul contexte peut tenir."
version: 1.0.0
license: MIT
platforms: [linux, macos, windows]
---
# Développement piloté par sous-agents

## Principe
Certains travaux gagnent à être **décomposés et confiés à plusieurs agents** : soit pour la largeur (couvrir plusieurs angles en parallèle), soit pour la confiance (perspectives indépendantes + vérification adverse), soit pour l'échelle (plus que ce qu'un seul contexte tient). Le coordinateur garde la **conclusion**, pas le détail brut de chaque agent.

## Quand l'utiliser
Recherche multi-angles, revue multi-dimensions, migration/audit sur beaucoup de fichiers, génération de N alternatives à comparer. **Pas** pour une tâche courte et séquentielle — l'orchestration coûte plus qu'elle ne rapporte.

## Comment bien déléguer
Chaque sous-agent doit recevoir (sinon il duplique, dévie ou laisse des trous) :
1. **Objectif** clair et borné.
2. **Format de sortie** attendu (structuré si le résultat doit être recomposé).
3. **Indications d'outils / de sources** à utiliser.
4. **Limites** de la tâche (ce qu'il ne doit pas faire).

## Patterns utiles
- **Fan-out / synthèse** : N agents couvrent chacun une part → un agent synthétise.
- **Vérification adverse** : pour chaque résultat, un ou plusieurs agents *indépendants* tentent de le réfuter ; on ne garde que ce qui survit.
- **Pipeline** : chaque élément traverse plusieurs étapes sans barrière globale.
- **Revue en 2 temps** : produire, puis faire relire par un agent frais avant d'intégrer.

## Règles de qualité
- Topologie **orchestrateur → workers** (un coordinateur délègue), pas un maillage flou.
- Ne pas cacher les limites : si on a plafonné la couverture (top-N, échantillon), le **dire**.
- Intégrer seulement ce qui est vérifié.
