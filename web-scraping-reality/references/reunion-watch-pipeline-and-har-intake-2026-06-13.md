# Réunion immo + vols: pipeline opérationnel avant HAR/NetLog

Session: 2026-06-13

## Classe de problème

L'utilisateur n'a pas encore fourni les HAR/NetLog nécessaires pour débloquer certains sites anti-bot, mais il veut quand même avancer utilement. La bonne réponse n'est pas d'attendre passivement: construire des briques robustes autour des sources déjà exploitables, puis préparer l'ingestion des captures réseau.

## Pattern recommandé

1. **Séparer les statuts** au lieu de mélanger les sources:
   - `prod-candidate`: source testée, prix/annonces extraits en run réel.
   - `bug-local-or-blocked`: HTTP/rendu OK partiel mais pas de signal métier fiable.
   - `blocked-antibot`: CAPTCHA/Cloudflare/Imperva confirmé.
   - `fallback-indicatif`: agrégateur marché, utile mais non officiel.

2. **Créer un runner unifié** plutôt qu'un script monolithique fragile:
   - appeler les watchers existants en subprocess bornés;
   - écrire stdout/stderr séparés;
   - produire un `manifest.json` unique;
   - produire un `telegram_summary.txt` court;
   - maintenir un pointeur stable `artifacts/<class>/latest`.

3. **Dashboard HTML local** pour décision rapide:
   - résumé 1 minute;
   - cartes vols avec source/statut/prix min/raw JSON;
   - top annonces immo filtrées avec liens source;
   - pas de faux KPI ni de décoration qui masque la preuve.

4. **Mode rapide vs mode complet**:
   - rapide: Kiwi + Air Austral + immo, utile pour QA quotidienne;
   - complet: ajoute French Bee avec attentes longues, car Amadeus/Akamai peut rendre tardivement.

5. **Vérifier la cohérence officiel ↔ agrégateur avant automatisation**:
   - comparer uniquement des vols identiques quand possible (`flight_number`, horaires, route);
   - utiliser `price_eur` côté Kiwi, jamais `price_amount` seul car il peut refléter une devise/locale non-EUR;
   - calculer delta EUR et %, puis classer `exact/live` ≤5%, `probably live` ≤15%, `indicative` ≤30%, `aberrant` au-delà;
   - Air Austral officiel reste source de vérité, Kiwi sert de contrôle de cohérence/veille marché;
   - script produit: `/opt/data/scripts/flight_coherence_check.py`, rapports `coherence_air_austral_vs_kiwi.{json,md}`.

6. **Automatisation quotidienne no-agent**:
   - script shell source: `/opt/data/scripts/reunion_watch_daily.sh` et wrapper réellement exécuté par cron sous `~/.hermes/scripts/reunion_watch_daily.sh`;
   - après toute modification du script source, synchroniser explicitement le wrapper cron: `install -m 755 /opt/data/scripts/reunion_watch_daily.sh /opt/data/.hermes/scripts/reunion_watch_daily.sh`, puis `bash -n` sur les deux;
   - lancer pipeline rapide, puis cohérence Air Austral vs Kiwi, puis imprimer un résumé court Telegram avec lignes source/prix/offres;
   - durcir le script quotidien avec `flock` anti-double-run, `PYTHONPYCACHEPREFIX=/tmp/pycache-hermes`, stdout JSON dans le run dir (`pipeline_result.json`, `coherence_result.json`) et logs durables sous `/opt/data/logs/`;
   - ne promouvoir `artifacts/reunion-watch/latest` qu'après un `manifest.ok == true`; un run échoué doit laisser un marqueur explicite (`NOT_LATEST_FAILED_RUN.txt`) et ne pas casser le dernier dashboard valide;
   - utiliser cron Hermes `no_agent=true` pour éviter de consommer du modèle et envoyer stdout seulement.

7. **Préparer l'arrivée des HAR/NetLog**:
   - écrire un intake qui lit HAR Chrome et Chrome NetLog JSON;
   - extraire et classer les endpoints high-value (`api`, `ajax`, `graphql`, `availability`, `fare`, `price`, `booking`, `Override.action`, `plnext`, `amadeus`);
   - redacter cookies, Authorization, tokens, sessions, CAPTCHA, Cloudflare, Incapsula/Akamai;
   - produire `sanitized_requests.json` + `endpoint_report.md`;
   - ne jamais rejouer automatiquement des requêtes avec secrets bruts.

## Piège French Bee confirmé

Un HTTP 200 + HTML volumineux + screenshot blanc n'est pas une preuve de blocage définitif. French Bee/Amadeus peut nécessiter:

- capture console/pageerror;
- `body_text` comme preuve métier;
- attente `networkidle`;
- timeout rendu autour de 180s;
- extra wait autour de 45s.

Le faux négatif `no_cheapest_combo` peut être corrigé par attente plus longue si le bootstrap Akamai/Incapsula a réussi.

## Artefacts/scripts produits dans cette session

Ces chemins sont session-spécifiques mais décrivent le modèle réutilisable:

- `/opt/data/scripts/reunion_watch_pipeline.py`: orchestration immo+vols, manifest, dashboard, résumé Telegram.
- `/opt/data/scripts/har_netlog_intake.py`: intake HAR/NetLog avec redaction secrets et rapport endpoints.
- `/opt/data/artifacts/reunion-watch/latest`: pointeur stable du dernier dashboard unifié.

## Vérification minimale avant livraison

- `python3 -m py_compile` sur les scripts modifiés avec `PYTHONPYCACHEPREFIX=/tmp/pycache-hermes` si `/opt/data/scripts/__pycache__` est non inscriptible.
- Run quick réel du pipeline.
- Vérifier `manifest.ok == true`, `prod_flights` présent et cohérent avec les cartes vols.
- Vérifier que le dashboard contient résumé, cartes vols et >=10 annonces immo, avec contenu rendu côté HTML initial (`data-testid="summary-panel"`, `flight-card`, `immo-listing`) pour éviter un faux dashboard vide au premier affichage.
- Ouvrir le HTML au navigateur et vérifier console JS vide si possible.
- Vérifier que `/opt/data/scripts/reunion_watch_daily.sh` et `/opt/data/.hermes/scripts/reunion_watch_daily.sh` sont strictement identiques (`cmp -s`) et que le lock `flock` empêche deux runs simultanés.
- Tester l'intake HAR/NetLog avec un HAR factice contenant token/cookie/auth pour confirmer `[REDACTED]`.
- Lancer la batterie métier non destructive: `python3 /opt/data/scripts/reunion_watch_business_qa.py`; elle couvre vols, cohérence Air Austral/Kiwi, filtres immo, OFIM, HAR/NetLog, dashboard, résumé Telegram, artefacts live et garde-fous opérationnels; rapport sous `/opt/data/artifacts/reunion-watch-business-qa/<timestamp>/BUSINESS_QA_REPORT.md`. Dernier jalon attendu après durcissement: 31/31 tests OK.
