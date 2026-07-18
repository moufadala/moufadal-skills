---
name: definition-of-done
description: "À utiliser dès que l'utilisateur dit fini, terminé, prêt, done, « continue jusqu'au bout », ou demande si un projet/phase/tâche est vraiment complet. Définit des critères de « fait » vérifiables AVANT de déclarer terminé — pour code, VPS, scraping, dashboards, recherche, déploiements."
version: 1.0.0
license: MIT
platforms: [linux, macos, windows]
---

# Definition of Done — Protocole « Vraiment fini »

## Pourquoi ce skill existe

Tu as tendance à déclarer « fini » trop tôt.
L'utilisateur a un standard plus élevé : pour lui, « fini » inclut
toutes les étapes de finalisation, de vérification, et de blocages
résolus — pas seulement le cœur technique.

Ce skill t'oblige à **clarifier ce qu'est « fini » AVANT** d'exécuter
la dernière action, et à **ne pas déclarer fini tant qu'il reste**
des points ouverts non résolus avec l'utilisateur.

## Règle d'or

**Ne jamais dire « fini », « c'est bon », « terminé », « done »** tant que l'état final n'a pas été vérifié après la dernière modification.

### Final-state verification before `100%`

Si du travail sûr, réversible et inférable reste ouvert, ne pas s'arrêter sur un bilan partiel : continuer ou lancer un job borné avec notification de fin. Avant `100%`, vérifier que l'audit/gate final a tourné après le dernier changement, qu'aucun process background n'est silencieusement en cours, et que les preuves + rollback/reprise sont fournis. Détail : `references/final-state-verification.md`.
**sans avoir d'abord appliqué ce protocole.**

## Protocole en 4 étapes

### Étape 1 — Suspension

Dès que l'utilisateur dit « fini », « c'est bon », « termine »,
ou donne un signal équivalent :

→ **Ne pas exécuter la dernière action.**
→ **Ne pas envoyer le message de finalisation.**

À la place, annoncer :

> « Avant de déclarer fini, je mets au clair ce que "vraiment fini"
> veut dire ici. »

### Étape 2 — Inventaire

Lister TOUT ce qui a été fait jusqu'à présent.

### Étape 3 — Projection

Lister TOUT ce qui serait nécessaire pour un « vraiment fini »
dans ce contexte précis. Pour chaque point, indiquer :

- Si c'est déjà fait, en cours, ou à faire
- Si c'est bloquant ou optionnel
- Si toi (Hermes) peux le faire, ou si l'utilisateur doit
  intervenir (permissions, décision, action manuelle)
- Si un statut machine ou fichier QA existe, citer le champ exact plutôt qu'un résumé optimiste. Exemple : `state=completed` peut seulement vouloir dire « artefact généré », tandis que `warn_production_enabled=false` veut dire que le runtime n'est pas fini.

**Point de vigilance Moufadal :** ne pas présenter un objectif comme « atteint » quand le livrable demandé implique une intégration runtime/production mais que seul le rapport, la politique ou la preuve de concept est terminé. Séparer explicitement :

- **fini côté artefacts/preuves** ;
- **pas fini côté runtime/production** ;
- **action concrète qui transforme le POC en système branché**.

Si Moufadal exprime une frustration du type « on a toujours pas fini ? », ne pas défendre le résumé précédent : reconnaître l'écart entre le critère annoncé et le vrai critère de fin, puis lancer immédiatement la prochaine étape sûre si elle est non destructive.

**Règle “prochaine étape” Moufadal :** tant qu'une réponse contient une section ou formule du type « prochaine étape », « prochaine action », « il reste à », ou « ensuite », ne pas s'arrêter si cette action est faisable par l'agent. Exécuter d'abord l'action sûre, vérifier, puis répondre. En finalisation, éviter de créer une boucle de pilotage avec « prochaine étape recommandée » quand le travail peut continuer maintenant. Si une action restante est réellement bloquée par un garde-fou hôte ou une permission impossible à obtenir via outils, le dire comme **blocage externe vérifié**, pas comme une simple prochaine étape.

**Correction “donc t'as pas fini” :** si Moufadal conteste une finalisation, ne défends pas le rapport précédent. Repars immédiatement des critères de fin vérifiables, relance les checks machine pertinents, et distingue explicitement : `fait`, `pas fait`, `bloqué par permission/destructif`, `accepté seulement si Moufadal renonce à ce critère`. Si le point restant est destructif mais nécessaire au vrai 100%, le statut doit rester **pas fini / validation requise**, pas “terminé avec prochaine action recommandée”.

**Correction “pourquoi tu t'es arrêté ?” :** répondre d'abord franchement à la question de gouvernance (`besoin de toi ?`, `prompt insuffisant ?`, `skill/procédure insuffisante ?`, `% réel`). Puis lancer immédiatement les actions sûres restantes, idéalement en background avec notifier si elles sont longues. Ne pas utiliser la demande d'explication comme prétexte pour suspendre le travail : expliquer brièvement, corriger le protocole, continuer, puis vérifier les artefacts.

**Correction “ne t'arrête pas au petit problème” :** quand un audit ou une finalisation révèle un petit blocage externe, ne l'utilise pas comme excuse pour arrêter la classe de travail. Continuer toutes les corrections sûres et réversibles encore faisables, puis isoler le blocage résiduel dans la section limites avec preuve précise. Le statut peut devenir “tout le fixable est fait, reste blocage externe”, mais seulement après avoir vraiment traité le reste.

**Correction “règle-le en autonome, pas étape par étape” :** si Moufadal demande de ne pas se perdre dans un audit ou dans des micro-étapes, le critère de fin n'est pas “rapport produit”. Pour les sujets VPS/Docker/sécurité/architecture, faire en autonomie toutes les remédiations sûres et réversibles : snapshot/rollback, correction des P0, nettoyage des artefacts évidents, durcissement des images/services, re-scan après mutation, puis watchdog ou gate durable si la dérive peut revenir. Si Moufadal demande ensuite “audit sous un autre angle”, ne répète pas le même gate : change explicitement de threat model (ex. permissions/secrets/cron/logs/backups/namespace/résilience après un audit Docker) et continue les corrections sûres jusqu'à un audit final post-mutation. Ne demander validation que pour une destruction de données, une rotation de secret/token susceptible de casser le runtime, une coupure de service non réversible, ou un choix business. Le bilan final doit distinguer `corrigé sur le périmètre actionnable` de `parfait absolu` quand des CVE non-fixables/vendor-only restent.

**Background jobs are not “done” until they finish.** If a benchmark, crawl, audit, or batch job is launched in background, the task status is `en cours` unless you have checked completion and final outputs. In final Telegram-style updates, include the process/job ID, run directory, notifier/cron if any, and the exact remaining condition for completion. Do not convert “launched successfully” into “completed”.

**When a background-completion notification arrives, immediately close the loop.** Do not just report the notification. Inspect the run log, QA file, generated artifacts, and any public URLs; check process exit code; verify sizes/hashes when files are delivered; then update the task ledger from `running` to `completed`, `completed_with_note`, or `blocked` with the exact residual limitation. If an optional critique lane failed (e.g. auth/quota), mark that lane as a limitation without downgrading verified core artifacts. If the user explicitly says they are going to sleep / do not want to resume tomorrow / all tests must pass, treat feasible reviewer gaps as blocking until you run a final acceptance addendum: missing test suites, helper compilation, CLI contracts, smoke/dry-run paths, rollback readability, and a compact review artifact. A process `exit 0` plus a report is not enough if the run itself shows `error_max_turns`, missing review files, or misleading QA counters.

**Runtime / gateway / production personnelle :** ne jamais marquer fini parce que le code source est patché si le service long-running n'a pas chargé le patch. Pour Hermes/gateway, « vraiment fini » inclut : patch appliqué, syntaxe/tests ciblés PASS, redémarrage ou rechargement du process réellement effectué, statut service vérifié, scénario utilisateur réel post-restart, et rollback documenté. Pour un conteneur Docker patché en runtime, « vraiment fini » inclut aussi la reproductibilité : image/tag immutable créé si nécessaire, conteneur actif recréé depuis cette image, `docker inspect` montrant `Config.Image=<image patchée>`, absence de restart loop, smoke public après la recréation, et rollback/recreate command sauvegardés. Si seul le runtime est corrigé mais que `Config.Image` pointe encore vers l'ancien tag, le statut est `partiellement terminé / dette de reproductibilité`, pas terminé. Si le restart est bloqué par approbation de sécurité, le statut doit rester `partiellement terminé / restart bloqué`, même si le code est prêt.

**Catégories à vérifier systématiquement** (adapter au contexte) :

| Catégorie | Exemples |
|-----------|----------|
| Déploiement | Site en ligne ? HTTPS ? DNS ? |
| CI / tests | Automatisé ? Vert ? |
| Sécurité / confidentialité | Secrets dans le diff ? Données privées exposées ? |
| Documentation | README ? Instructions de reprise ? |
| Rollback | Commande de rollback documentée ? |
| Garde-fous | Protection de branche ? Limites de ressources ? Alertes ? |
| Vérification finale | Smoke test après la dernière mutation ? QA ? Portail accessible ? Si le livrable affirme GitHub/public web/dashboard, vérification externe/net réelle (`gh api`, `curl -L` URL canonique) après mutation ? |
| Fichier téléchargeable | URL publique testée depuis l'extérieur ? HTTP 200 ? taille + hash identiques ? process/conteneur nommé ? rollback exact ? Voir `references/ad-hoc-downloadable-file-delivery.md`. |
| Background/cron long | Process/job ID ? Notifier ? état `running` vs `completed` ? chemin logs/run dir ? |
| Blocages connus | Permissions manquantes ? API rate limit ? Dette technique ? |

### Étape 4 — Demande de clarification

Demander explicitement à l'utilisateur :

> « Voici ce qui reste avant que ce soit "vraiment fini" :
>
> 1. [Point A] — faisable par moi ✅
> 2. [Point B] — nécessite ton action 👉 [lien/clics exacts]
> 3. [Point C] — à ta décision : est-ce nécessaire pour toi ?
>
> Est-ce que je fais tout ça, ou considères-tu que c'est fini
> malgré les points restants ? »

## Après validation

Quand l'utilisateur répond :

- Si « oui, fais tout » → tout exécuter, puis vérifier, puis « fini ».
- Si « non, c'est bon comme ça » → marquer comme fini avec la note
  « Accepté par l'utilisateur sans [points restants] ».
- Si « je fais X manuellement » → attendre confirmation que c'est fait,
  puis **relancer immédiatement la vérification qui bloquait** et le test/audit parent avant de marquer fini. La confirmation utilisateur seule n'est pas une preuve de fin.

### Confirmation manuelle / permissions hôte

Quand un blocage externe est levé par Moufadal hors de l'agent — chmod/chown côté host, clic console, réglage DNS, token, firewall, redémarrage manuel — appliquer ce mini-protocole :

1. Vérifier depuis l'environnement agent que le changement est visible.
2. Relancer exactement le check qui échouait.
3. Relancer le test/audit parent qui dépendait de ce check.
4. Écrire ou attacher une preuve courte si le travail est une livraison projet.
5. Seulement ensuite passer le statut de `bloqué externe` à `corrigé` ou `fini`.

Détail et exemple : `references/manual-permission-unblock-verification.md`.

## Exemples concrets

Voir `references/worked-examples.md` pour des applications du protocole
dans 5 contextes différents : GitHub PR, scraping, déploiement,
recherche/analyse, installation VPS.

## Skills liés à charger selon le cas

- `long-task-ledger` quand la finalisation dépend d'un process background, cron, benchmark, crawl, ingestion, audit nocturne ou plusieurs workstreams ouverts. Le statut reste `en cours` tant que le ledger n'indique pas la condition de fin vérifiée.
- `conversation-to-skill-review` quand une contestation utilisateur révèle une erreur récurrente à transformer en patch de skill, note Obsidian ou mémoire durable plutôt qu'en simple excuse.

## Ce que ce skill change concrètement

**Avant** (sans skill) :
> ✅ PR mergée, CI verte, c'est fini.

**Après** (avec skill) :
> « Avant de dire fini, voici ce que je vois :
> ✅ PR mergée, CI verte, smoke OK.
> ⚠️ Il reste : protection de `main` pas activée (action manuelle).
> Tu veux qu'on le fasse, ou c'est bon pour toi comme ça ? »
