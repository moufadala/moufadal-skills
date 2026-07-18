# Overnight prod hardening — immobilier Réunion + vols RUN (2026-06-11)

Session nocturne production-like, non destructive. À utiliser comme référence pour les futures campagnes larges où l'objectif est “fiabilité max, preuves live, pas de simulation”.

## Pattern validé

1. Inventorier d'abord les scripts/configs/artefacts existants (`/opt/data/scripts`, `/opt/data/artifacts`, `morning_brief/config.yaml`) au lieu de redemander la liste des sources.
2. Faire un health check archivé avant les runs, en distinguant :
   - service local vs service via réseau Docker (`localhost:8888` peut être KO alors que `searxng:8080` marche depuis `hermes-gateway`) ;
   - CDP local `127.0.0.1:9222` vs sidecar Docker `chromium-cdp:9223` ;
   - présence de clé CapSolver vs balance réelle.
3. Exécuter une campagne bornée non destructive : stdout/stderr/meta par source, `SUMMARY.json`, rapport Markdown + HTML.
4. Classer source par source en `prod-candidate`, `needs-hardening`, `blocked-antibot`, `bug-local`, `low-value`.
5. Auditer les artefacts complets après le run : ne pas prendre `exit_code`, `winners=[]` ou un wrapper cassé au pied de la lettre.
6. Si un scraper échoue pour une raison d'environnement Python, relancer avec le venv connu avant de classer la source : `/opt/data/labs/browser-use-poc/venv/bin/python`.
7. Garder les sources anti-bot avec une prochaine action unique, mais ne pas bloquer toute la nuit dessus.

## Résultats live utiles observés

- Immobilier :
  - Bien’ici API : 24 items complets en dry-run borné, bon candidat prod.
  - SeLoger CDP : 29 annonces / 20 prix visibles, candidat prod mais à durcir avec HAR/BFF replay si CDP varie.
  - OFIM RSS/HTML : fonctionne mais valeur faible/bonus, beaucoup de champs prix incomplets.
  - multi-sources : 152 items, utile mais doit rester `needs-hardening` tant que les parseurs ne sont pas scorés source par source.
- Vols :
  - Air Austral officiel RUN↔CDG a rendu des prix live et des vols dans stdout complet, même si cette famille était historiquement fragile.
  - Kiwi browser network capture fonctionne comme fallback quand le script GraphQL direct dépend d'un template local manquant ; il a capturé des offres RUN→Paris sur plusieurs dates.
  - French Bee doit être lancé via le venv Playwright/curl_cffi/bs4 ; un lancement avec system Python peut produire un faux bug local. Même via venv, le résultat peut être `French bee - Erreur / no_cheapest_combo` : classer `needs-hardening`, pas succès.
  - Kayak HTTP brut retourne un signal anti-bot : `blocked-antibot` / `low-value` sauf HAR/API poll.
  - Air Mauritius RUN↔MRU ne doit pas absorber la campagne : si web VPS échoue, prochaine action = NetLog Android/API mobile.

## Rapport compact attendu

Final Telegram / chat : verdict d'abord, chemins rapport, top 5 actions prod, `MEDIA:/...html` si un HTML a été produit. Ne pas narrer longuement les essais ; les détails vont dans le Markdown/HTML et `SUMMARY.json`.

## Anti-pièges

- Ne pas transformer un échec de dépendance (`ModuleNotFoundError`, mauvais Python, template local manquant) en verdict site.
- Ne pas supprimer ou marquer stale des annonces quand une source échoue ; stale uniquement pour une source vue avec succès dans le run courant.
- Ne pas conclure “prod” sans stdout/stderr + données live + chemin artefact.
- Ne pas laisser un script direct cassé cacher un fallback existant : pour Kiwi, si le template GraphQL direct manque, essayer `kiwi_capture_live.py` en browser network capture.
