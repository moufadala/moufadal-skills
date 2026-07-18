---
name: search-first-before-build
description: "À utiliser AVANT d'implémenter un module, une fonctionnalité, une architecture, un workflow, une structure de vault, un scraper ou une intégration d'outil non triviaux — pour éviter de réinventer l'existant. Force une recherche de l'art antérieur (local + externe), puis un verdict adopter / étendre / construire."
version: 1.0.0
license: MIT
platforms: [linux, macos, windows]
---
# Search First Before Build

## Quand utiliser

Charger ce skill AVANT de coder ou de concevoir quelque chose de non trivial quand la demande ressemble à :

- créer un module, une fonction, une architecture, un workflow ou un dashboard ;
- intégrer un outil, MCP, plugin, API, scraper, pipeline, Obsidian vault/template, agent skill ;
- résoudre un problème probablement déjà rencontré par d'autres ;
- Moufadal dit ou implique : “ça existe peut-être déjà”, “regarde les repos”, “ne réinvente pas”, “comment les gens font”, “cherche avant”.

Ce skill est particulièrement obligatoire pour : scraping/anti-bot, Obsidian/PKM, agents/skills, dashboards, monitoring/watchdogs, auth, proxy mobile, transcripts YouTube, santé/data personnelle, immobilier, intégrations Android/MCP.

## Principe

Ne pas partir directement en implémentation custom. Faire un mini-gate **search-first** :

```text
problème exact → inventaire local → recherche externe → comparaison → verdict adopt/extend/build → smoke test → seulement ensuite implémentation
```

L'objectif n'est pas de copier aveuglément. L'objectif est d'éviter de construire une version inférieure de quelque chose qui existe déjà, ou de rater des pièges connus.

## Workflow obligatoire

### 0. Formuler le besoin en une phrase

Avant la recherche, écrire mentalement ou dans le plan :

- composant à construire ;
- sortie attendue ;
- contraintes locales ;
- ce qui ferait dire “on peut adopter/adapter l'existant”.

Exemple : “Créer une architecture Obsidian par domaines pour Hermes, avec règles de lecture agent, templates et récupération de contexte.”

### 1. Chercher d'abord dans notre propre terrain

Vérifier si le VPS/projet contient déjà une solution ou une leçon :

- `session_search` sur les termes métier et corrections utilisateur ;
- skills existants avec `skills_list` / `skill_view` ;
- `/opt/data/scripts`, `/opt/data/artifacts`, `/opt/data/projects`, `/opt/data/vaults` ;
- runbooks et handoffs ;
- GitHub repo du projet si applicable.

Hiérarchie locale :

```text
solution déjà en prod > script local validé > artefact/rapport > skill/runbook > souvenir vague
```

### 2. Chercher l'existant externe

Faire au moins une recherche ciblée selon le domaine :

- GitHub repos/topics/issues pour code, plugins, templates, MCP, scrapers ;
- docs officielles/changelog pour outils vivants ;
- forums/Reddit/HN/communautés pour pièges et alternatives ;
- packages npm/PyPI si c'est une librairie ;
- exemples/templates publics pour Obsidian, dashboards, UX ;
- articles sérieux seulement pour arbitrage, pas comme preuve unique.

Pour GitHub, préférer quand possible `gh search repos/code/issues` ou extraction directe de README/repo plutôt que simples snippets web.

### 3. Classer les options

Pour chaque option crédible, noter brièvement :

- URL / nom ;
- maturité : stars, date récente, commits, issues, licence ;
- stack et compatibilité locale ;
- ce qu'on peut réutiliser : concept, template, code, config, tests ;
- risques : sécurité, secrets, dépendances lourdes, maintenance, surcomplexité ;
- raisons de rejet si rejetée.

### 4. Verdict obligatoire : adopt / extend / build

Avant toute implémentation, produire une ligne vérifiable :

```text
Verdict search-first: ADOPT | EXTEND | BUILD — raison principale — preuves consultées — prochain smoke test.
```

Définitions :

- **ADOPT** : utiliser un outil/template existant tel quel ou presque.
- **EXTEND** : reprendre structure/pattern/code partiel, adapter à notre contexte.
- **BUILD** : construire custom parce que l'existant est absent, incompatible, risqué, trop lourd ou non maintenu.

`BUILD` doit être justifié par preuves, pas par réflexe.

### 5. Smoke test avant intégration complète

Avant migration/implémentation large :

- cloner ou télécharger dans un sandbox/artifact, pas dans la prod ;
- tester 1 cas représentatif ;
- vérifier licence/permissions ;
- faire un rollback/backup si on touche un projet existant ;
- seulement ensuite intégrer.

## Quand NE PAS chercher longtemps

Ne pas faire une recherche lourde pour :

- bug trivial avec erreur locale évidente ;
- patch de 2 lignes sur code déjà compris ;
- commande système simple et réversible ;
- urgence de réparation où le service est down et la cause locale est claire.

Même dans ces cas, si la solution devient fragile ou dépasse ~15 minutes, basculer en search-first. Exception importante : si la réparation touche une configuration durable (Docker/Traefik, auth, routing, MCP, skills, agents, cron durable, config Hermes) ou si la cause n'est pas prouvée, appliquer la règle urgence — voir `references/emergency-vs-search-first-calibration-2026-07-03.md`.

## Mode calibration visible

Pendant la période de calibration demandée par Moufadal, annoncer explicitement quand ce gate est activé afin qu'il puisse corriger le seuil de déclenchement, surtout au moment où une recherche internet/externe est envisagée.

Calibration Moufadal validée le 2026-07-03 :
- fenêtre visible : 4 jours ;
- domaines toujours sensibles : architecture, automatisation durable, sécurité, VPS/Hermes, skills, agents, scraping, Android/S25, Obsidian/LifeOS, immo, business et gros projets ;
- seuil temps : recherche externe obligatoire si le mauvais choix peut coûter environ 30 min à 1 h ou plus, à ajuster selon criticité ;
- urgence/service cassé : commencer par les checks locaux évidents et réversibles; si la cause n'est pas claire ou si la réparation dépasse environ 15 min, basculer en search-first et expliquer avec exemples ;
- pendant la calibration, donner brièvement les requêtes de recherche externes utilisées, pas seulement le verdict.

Formules courtes recommandées :

```text
Gate search-first activé : je vérifie d'abord localement avant de construire.
```

```text
Recherche externe justifiée selon moi : [raison courte]. Je vérifie repos/docs/community avant de coder; tu pourras me dire si c'était trop tôt ou utile.
Requêtes utilisées : [2–4 requêtes courtes, pas les logs bruts].
```

Si Moufadal répond que la recherche internet n'était pas justifiée, noter la frontière et transformer l'exemple en cas négatif SkillOps si récurrent. Si Moufadal confirme que c'était justifié, transformer l'exemple en cas positif si utile.

Pendant la période de mini-monitoring, consigner chaque décision de recherche externe dans `/opt/data/logs/search_first_calibration.jsonl` en JSONL compact :

```json
{"ts":"<UTC ISO>","task":"<résumé court>","external_search":true,"reason":"<necessity/utility/affordability>","level3_signal":false,"user_feedback":"pending"}
```

Si Moufadal donne un feedback après coup, ajouter une nouvelle ligne `feedback_update` plutôt que réécrire l'historique.

Détail de calibration et exemples à maintenir : `references/visible-external-search-calibration-2026-07.md`.

Mini-monitoring humain pendant une fenêtre de calibration : `references/human-feedback-mini-monitoring-2026-07.md`. À utiliser quand Moufadal veut voir les décisions de recherche externe et corriger le seuil.

Calibration Moufadal validée avec seuils, niveau 3 et affichage bref des requêtes : `references/moufadal-visible-search-calibration-2026-07-03.md`. À lire quand une décision durable touche Hermes/skills/VPS/agents/scraping/automation/sécurité et que l'utilisateur veut voir pourquoi une recherche externe a été lancée.

Urgence/service cassé vs recherche externe : `references/emergency-vs-search-first-calibration-2026-07-03.md`. À lire quand il faut décider entre réparer localement d'abord, chercher après préflight, chercher immédiatement, ou proposer Niveau 3.

Recherche/sources sur la calibration des recherches externes : `references/tool-search-calibration-research-2026-07.md`. À lire quand la question porte sur “quand lancer internet ?” plutôt que seulement “chercher avant de construire”.

Calibration à partir de l’historique réel de Moufadal : `references/session-history-trigger-calibration-2026-07-03.md`. À lire quand il faut distinguer T0 action simple, T1 récupération locale de contexte connu, T2 recherche externe sourcée, et T3 DeepResearch/premium avec Claude + artefact. Pour ce type d’audit, ne pas se limiter à `session_search` ou `/opt/data/state.db` : inspecter aussi l’archive Obsidian des conversations, notamment `/opt/data/vaults/moufadal-second-brain/30-Conversations` (`Journal Hermes/`, `Distillations/`, `Sources/`, notes de patterns/corrections), puis préciser la couverture temporelle de chaque source.

## Escalade vers niveau 3

Proposer proactivement le niveau 3 — revue Claude Code + deuxième boucle de recherche externe + rapport complet — quand au moins un de ces signaux apparaît :

- 3 corrections de Moufadal sur le seuil search-first en quelques jours, surtout faux positifs/faux négatifs répétés ;
- une décision structurante dépend du gate : architecture durable, gros projet, automatisation récurrente, agent/routing, sécurité, scraping fragile ;
- le verdict `BUILD` est envisagé mais les preuves externes/locales sont faibles ou contradictoires ;
- un incident montre que Hermes a quand même réinventé, oublié un repo/template, ou cherché trop tard ;
- le coût d'une erreur est élevé : plusieurs heures de dev, dette technique, exposition de données, panne VPS, ou mauvais choix d'outil.

Formule recommandée :

```text
Je pense que le niveau 3 est justifié ici : [signal concret]. Le niveau 2 suffit pour exécuter, mais une revue Claude + seconde recherche réduira le risque de construire la mauvaise chose.
```

Ne pas attendre que Moufadal demande explicitement si ces signaux sont présents. Proposer, puis laisser Moufadal valider ou refuser.

## Sortie attendue compacte

Pour Moufadal, ne pas noyer Telegram. Adapter la sortie au niveau détecté :

- **T0/T1** : réponse courte, récupération locale et point utile; pas de rapport Projet Clair si la demande est juste une petite question ou une continuité.
- **T2** : verdict search-first compact avec sources/requêtes principales et prochain smoke test.
- **T3** : rapport complet dans `/opt/data/artifacts/...`, Claude/revue si disponible, Telegram seulement pour le verdict, preuves et prochaine action.

Exemple T2 :

```text
Gate search-first activé.
Trouvé : A, B, C.
Verdict : EXTEND — on reprend X/Y, mais on garde notre stack pour Z.
Requêtes utilisées : ...
Prochaine action : smoke test sur ...
```

Pour une mission longue, écrire le comparatif complet dans `/opt/data/artifacts/.../SEARCH_FIRST_REPORT.md`.

## Clarifier le périmètre quand Moufadal demande “qu'est-ce qui a été implémenté ?”

Ne pas laisser croire qu'une recherche, un rapport ou une règle de prompt équivaut à une intégration runtime. Quand une correction porte sur `search-first` ou `when to use tools`, distinguer explicitement :

- **Search-first avant build** : gate de conception pour éviter de réinventer avant de coder.
- **Calibration d'appel web/outils** : décision épistémique `necessity / utility / affordability` pour savoir si une recherche externe est vraiment nécessaire.
- **Implémenté dans le skill** : texte, workflow, références, logs déclaratifs, critères d'escalade.
- **Implémenté dans le runtime** : hook/intercepteur qui force ou journalise automatiquement chaque appel outil. Ne l'affirmer que si un patch code/config a été appliqué et vérifié.

Formule sûre quand l'état est hybride :

```text
Oui, ça concerne le sujet du message précédent, mais seulement au niveau garde-fou agentique/skill et monitoring déclaratif. Ce n'est pas encore une interception runtime automatique de tous les appels web/outils.
```

Si Moufadal demande confirmation, répondre d'abord par cette séparation avant de livrer le bilan ou les chemins d'artefacts.

## Pièges connus issus des sessions Moufadal

- Obsidian : beaucoup de vaults/templates existent déjà ; ne pas inventer une architecture complète sans benchmarker Vault Hub/GitHub/forum.
- Portail immo : des morceaux existaient (`fredy`, `flathunter`, `property-pulse`, scrapers), mais aucun clone exact ; bonne décision = EXTEND patterns + build local.
- Proxy/SearXNG/Android : les chemins communautaires doivent être validés contre notre topologie réelle Tailscale/SOCKS/HTTP relay avant modification.
- Skills/agents : chercher des skills existants et pratiques d'évaluation avant de créer un nouveau protocole local.
- Scraping : toujours comparer avec scripts locaux validés avant de croire une source externe disant que c'est impossible.
- Calibration web/outils : ne pas mélanger “chercher avant de construire” avec “savoir quand lancer une recherche internet”. Ce sont deux problèmes liés mais différents ; les rapports et bilans doivent les séparer.

## À combiner avec

- `community-validation-before-fragile-tech` pour les méthodes fragiles/mouvantes.
- `advanced-web-search` pour stratégie de recherche et extraction.
- `github-repo-management` pour analyse de repos.
- `obsidian` pour architectures PKM/vaults/templates.
- `agent-self-improvement` pour convertir les corrections utilisateur en golden cases/skills.
