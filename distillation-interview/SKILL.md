---
name: distillation-interview
description: "Transformer une source brute (vidéo, article, transcript) en connaissance propre par un court entretien : poser ~5 questions à l'utilisateur, puis produire les notes Source → Concept → Décision → Action reliées par des relations typées, en capturant les « pépites » de passage. À utiliser quand l'utilisateur veut distiller une vidéo / source, ranger un transcript, ou éviter que son second brain devienne un cimetière de notes brutes."
version: 1.0.0
license: MIT
platforms: [linux, macos, windows]
---
# Distillation par entretien

Transformer une source brute en connaissance **utile et reliée**, en gardant l'utilisateur maître : le distillé reflète ce que **lui** veut retenir, pas un dump automatique.

## Principe
La valeur n'est pas dans la capture, elle est dans le **tri**. On garde **deux étages** : la source brute (filet cherchable, jamais supprimé) + une note distillée propre. On ne distille que ce qui a un usage ; le reste reste brut et se retrouve par recherche.

## Quand l'utiliser
- L'utilisateur envoie une vidéo / article / transcript à « mettre en base ».
- Un transcript brut (souvent auto-généré, `status: draft-auto`) attend une vraie distillation.
- Revue hebdo : vider la pile d'inbox.

## Le workflow

### 1. Entretien (les réponses de l'utilisateur SONT la distillation)
Poser ~5 questions courtes. Pour chacune, l'utilisateur peut dire « je sais pas, va voir dans la source » → aller **chercher** dans le brut (recherche ciblée, pas relecture intégrale).
1. Qu'est-ce qui t'a marqué / t'intéresse ? (l'idée forte)
2. Un outil / une astuce à essayer un jour ? (→ pépites)
3. Ça change une de nos décisions / façons de faire ? (→ décision, ou rien)
4. Un concept réutilisable à garder ? (→ concept)
5. On garde, on archive, ou poubelle ?

### 2. Pipeline : Source → Concept → Décision → Action
Règle d'or : une source qui ne produit **ni concept, ni décision, ni action** → on l'archive. Pas de note pour faire joli.
- **Source** : fiche courte — URL, résumé 10 lignes max, garder oui/non + raison.
- **Concept** (si idée réutilisable) : définition, quand l'utiliser / quand pas, sources.
- **Décision / ADR** (seulement si on change notre système) : contexte, décision, alternatives rejetées, ce qui l'invaliderait, preuve.
- **Action** (si action immédiate) : UNE prochaine action vérifiable, dans le cockpit / focus.

### 3. Pépites (ne rien perdre de ce qui traîne)
Dans la note Source, une section « **Pépites / outils mentionnés (à revoir — non distillé)** » : capturer `nom — 1 ligne — (source / minute)` pour les outils/astuces cités **en passant**, hors de l'objectif du jour. Non distillé, juste retrouvable plus tard.

### 4. Relations typées
Relier les notes par des relations **typées** dans le frontmatter (pas un simple lien qui dit juste « il y a un rapport ») :
```yaml
relations:
  - type: source_for      # une source → un concept / une décision
    target: "[[...]]"
  - type: supports        # un concept → une décision
  - type: depends_on      # une décision → un concept / une autre décision
  - type: superseded_by   # une ancienne note → la nouvelle
```
Vocabulaire minimal suffisant : `supports`, `contradicts`, `depends_on`, `superseded_by` / `replaces`, `implements`, `source_for`. C'est ça qui rend un graphe de connaissance utile (et non un joli graphe vide).

### 5. Marquer la source comme traitée
Passer le brut de `status: draft-auto` → `distilled`, avec un lien `superseded_by` vers la note canonique. La pile de brouillons diminue à chaque passe.

## Règles de qualité
- **Titres à insight** : le titre = l'idée (« Graphify n'est utile que si les relations sont typées »), pas « Notes sur X ».
- **Reformuler avec ses mots** ; ne pas coller les paragraphes bruts.
- **1 idée = 1 note** ; relier plutôt que dupliquer.
- Ne jamais écrire de secret ni de donnée personnelle sensible dans une note partagée.
