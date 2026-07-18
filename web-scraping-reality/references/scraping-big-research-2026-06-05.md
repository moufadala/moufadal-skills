# Grosse recherche — accélérateurs scraping terrain (2026-06-05)

## Verdict opérationnel

Les plus gros gains de temps viennent de cette séquence :

1. **HTML/hydration avant navigateur** : JSON-LD, `#__NEXT_DATA__`, `window.__NUXT__`, state Redux/Apollo.
2. **JS bundle mining** : chercher endpoints/API/GraphQL/Algolia/Meilisearch dans les bundles.
3. **HAR/Copy as cURL** : capturer le vrai navigateur humain puis rejouer.
4. **HTTP replay avancé** : `curl_cffi` si `requests/httpx` bloquent par fingerprint TLS/HTTP2.
5. **Browser debug instrumenté** : Playwright codegen + trace viewer + storage state.
6. **Anti-détection seulement après preuve** : Patchright/rebrowser/nodriver/Camoufox/proxy/CapSolver.
7. **Industrialisation** : Crawlee/Scrapy selon browser-vs-HTTP.

## Outils à tester en priorité sur VPS

### 1. `har2requests`
- Transforme un HAR en code Python `requests`.
- Utile après capture humaine.
- Commande smoke : `pip install har2requests && har2requests input.har > replay.py`.
- Piège : nettoyer cookies/secrets et refactorer le code généré.

### 2. `curl_cffi`
- HTTP client Python avec impersonation TLS/JA3/HTTP2/HTTP3.
- Commande smoke : `requests.get(url, impersonate="chrome")`.
- À utiliser quand `requests/httpx` renvoient 403 mais la page fonctionne dans Chrome.
- Ne résout pas JS challenge/CAPTCHA/DataDome fort.

### 3. Playwright trace viewer
- Activer sur scripts instables.
- Donne screenshots, snapshots DOM, actions, console, réseau.
- Commande : `npx playwright show-trace trace.zip`.

### 4. JS bundle/API scanner maison
- Script à créer : télécharge HTML + JS, cherche `api`, `graphql`, `algolia`, `meilisearch`, `search`, `offset`, `cursor`, `listing`, `realEstate`.
- Gain : trouve souvent endpoints sans browser.

### 5. Crawlee
- Pour transformer scraper ponctuel en crawler robuste : queue, retries, sessions, proxy, storage, Playwright.
- À installer en venv projet; pas global.

### 6. Patchright
- Drop-in Playwright Chromium patché anti-détection.
- À tester si vanilla Playwright est détecté.
- Pièges : console API affectée; pas miracle sur DataDome fort.

### 7. mitmproxy
- À utiliser si HAR/Copy cURL insuffisant.
- Atouts : replay, sticky cookies/auth, modify headers/body, anticache.
- Plus lourd à configurer avec certificat HTTPS.

## Méthodes par symptôme

- **Données dans HTML** → parse direct / JSON-LD / hydration.
- **SPA vide** → bundle mining + HAR.
- **XHR/fetch visible** → Copy as cURL → replay → har2requests/curlconverter.
- **Replay HTTP 403** → curl_cffi.
- **Formulaire complexe** → Playwright codegen + trace viewer.
- **Script casse sans raison** → trace viewer + screenshots + network logs.
- **Vanilla Playwright détecté** → Patchright smoke test.
- **CAPTCHA visible** → CapSolver ciblé; vérifier token accepté, pas seulement reçu.
- **IP datacenter bloquée** → proxy résidentiel sticky seulement après preuve.
- **Crawl long/multi-pages** → Crawlee si browser, Scrapy si HTTP stable.

## Signaux/outils validés

- Next.js SSR expose les props côté client : utile pour `__NEXT_DATA__`.
- Algolia Search API : `x-algolia-application-id`, `x-algolia-api-key`, endpoint `/1/indexes/...`.
- Meilisearch : `POST /indexes/{index_uid}/search`, pagination `offset/limit/page/hitsPerPage`.
- GraphQL : `query`, `variables`, `operationName`, fragments, persisted query hashes.
- Playwright docs : codegen, network interception, trace viewer, storage state.
- mitmproxy docs : client/server replay, sticky cookies/auth, modify headers/body.
- Crawlee docs : queues, retries, sessions, proxy rotation, Playwright.
- Scrapy docs : spiders, pipelines, AutoThrottle, jobs, stats, shell, broad crawls.
- Camoufox docs : fingerprint Firefox niveau C++ mais releases 2026 expérimentales; labo, pas premier choix prod.

## Scripts utilitaires à créer

1. `probe_hydration.py URL`
2. `probe_js_endpoints.py URL`
3. `har_summary.py file.har`
4. `replay_curl_cffi.py URL`
5. `playwright_trace_probe.py URL`
6. `patchright_smoke.py URL`

Rapport complet local : `/opt/data/artifacts/research/scraping-big-research-2026-06-05.md`.
