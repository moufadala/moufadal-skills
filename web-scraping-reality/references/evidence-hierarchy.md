# Hiérarchie des preuves — scraping & recherche (correction 2026-06-06)

## Quand ce document s'applique

Quand tu as à la fois des résultats locaux (artefacts, scripts, screenshots) ET des rapports de recherche externes (PDF, web_search, analyses AI research). L'erreur classique : citer le rapport externe et ignorer l'artefact local.

## Hiérarchie (du plus haut au plus bas)

1. **Artéfacts locaux** — scripts qui tournent, JSON produits, screenshots, HAR captures, sessions de debug réussies. Ce sont des faits, pas des prédictions.
2. **Patterns communautaires validés localement** — GitHub stars, issues fermées, code qu'on peut exécuter ici. Vérifiable en 2 min.
3. **Rapports de recherche / analyses AI génériques** (PDF, blog posts, web_search résumés). Ces sources ne connaissent PAS :
   - Ta stack exacte (versions, configs, workarounds)
   - L'état précis de tes services (CDP sidecar, Chromium flags, swap)
   - Les solutions que tu as déjà trouvées et qui sont documentées dans tes skills/AGENTS.md

## Piège validé

Le 2026-06-06, un rapport de recherche disait « French Bee infaisable même en payant » alors que :
- Le script `/opt/data/scripts/frenchbee_solver.py` tournait et produisait des prix
- Des artefacts `official_frenchbee_RUN_ORY_*.raw.json` existaient avec 3 dates confirmées
- La technique (curl_cffi form → headful Xvfb → Amadeus Override.action) était documentée dans `browser-js-scraping/references/frenchbee-amadeus-imperva-headful-2026-06-04.md`

Le rapport avait raison dans son contexte général (Imperva reese84 + Amadeus est dur), mais il ne connaissait pas la solution spécifique trouvée sur ce VPS.

## Réflexe

Avant de citer une source externe qui dit « impossible » ou « abandonner », vérifier :
- Y a-t-il un script/skill qui dit le contraire ?
- Y a-t-il des artefacts dans `/opt/data/artifacts/` ?
- La session actuelle ou des sessions récentes ont-elles déjà résolu le problème ?
- Le `web-scraping-reality` ou `browser-js-scraping` skill ont-ils une référence qui contredit ?

Si oui, le local prime toujours.