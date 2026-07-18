# Immo Réunion — source health avant polish produit

## Contexte durable

Pour une veille immobilière Réunion déjà productisée avec dashboard, alertes et historique, ne pas confondre “l'app marche” avec “les données sont fraîches”. Une DB qui contient plusieurs centaines d'annonces et un dashboard public sans erreurs peut masquer des sources importantes devenues stales.

Cas observé :
- DB principale faible volume et viable : ~1k annonces, ~800 actives, ~735 exportées.
- Historique auxiliaire SQLite viable : baseline `new`, puis événements prix/statut.
- Audits UI/data verts.
- Mais quick gate partiel : DB report + proxy + OFIM RSS, pas toutes les sources majeures.
- Sources critiques potentiellement stale : gros portails comme SeLoger/Bien'ici peuvent avoir un `seen_last_at` ancien tout en restant dans l'export.

## Règle de décision

Ne pas migrer ou réarchitecturer la DB tant que :
- le volume reste faible ;
- les requêtes/audits passent ;
- le vrai risque est la fraîcheur des sources, pas les capacités de stockage.

La prochaine étape n'est pas le polish UI ou une migration Postgres : c'est un `source_health` visible et vérifiable.

## Contrat source health recommandé

Produire un artifact `source_health.json` ou rapport équivalent avec, pour chaque source :

- `source_id`
- `enabled` / `disabled`
- `last_success_at`
- `latest_seen_last_at`
- `active_count`
- `smoke_status`: `fresh`, `stale`, `failing`, `blocked-antibot`, `not-tested`
- `classification`: `prod-candidate`, `needs-hardening`, `blocked-antibot`, `bug-local`, `low-value`
- `artifact_dir` du dernier run
- `next_action`

## Pièges

- Un quick gate qui ne teste que 2–3 composants doit dire explicitement ce qui n'est PAS testé.
- Un dashboard HTTP 200 + console 0 erreur ne prouve pas la fraîcheur métier.
- Un row count stable peut cacher une source morte ou stale.
- Ne pas marquer stale/disappeared une source dont le scraper a échoué : préserver les anciennes annonces actives jusqu'à un run source réussi.
- Ne pas activer plus d'alertes Telegram avant d'avoir des garde-fous anti-bruit par source/recherche.

## Ordre recommandé

1. Source health multi-source.
2. Freshness/failure reporting visible public/admin.
3. Seulement ensuite UX mobile, carte, alertes plus fines, performance.

## Critères d'acceptation

- Rapport couvrant toutes les sources connues, y compris `not-tested` explicite.
- Les sources majeures ne peuvent plus être implicitement “OK” parce que la DB locale existe.
- Les artefacts de smoke sont horodatés et reliés à la classification.
