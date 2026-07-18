# Accélérateurs scraping validés terrain — 2026-06

Objectif : réduire le temps perdu avant de coder un scraper fragile.

## 1. Capture humaine HAR / Copy as cURL
- Usage : sites visibles chez l'utilisateur mais bloqués sur VPS/headless.
- Workflow : DevTools Network → Fetch/XHR → Copy as cURL ou Save all as HAR with content → replay local.
- Gain : identifie endpoints, payloads, pagination, IDs, cookies requis.
- Piège : le HAR contient secrets/cookies; le replay peut échouer si tokens/fingerprint/IP liés.

## 2. curl_cffi / curl-impersonate
- Usage : remplacer `requests/httpx` quand HTTP direct renvoie 403 sans raison visible.
- Atout : imitation TLS/JA3/HTTP2/HTTP3 de vrais navigateurs, API proche de requests.
- Smoke test : `pip install curl_cffi` dans venv puis `requests.get(url, impersonate="chrome")`.
- Limite : ne résout pas JS challenge fort, CAPTCHA, DataDome dur, réputation IP.

## 3. Pattern source maps / JS bundle mining
- Usage : SPA React/Next/Nuxt/Angular où l'API est cachée dans bundles JS.
- Workflow : récupérer JS → chercher `api`, `graphql`, `algolia`, `search`, endpoints, fragments GraphQL, noms de variables.
- Gain : trouve endpoints sans cliquer longtemps.
- Piège : endpoints peuvent nécessiter cookies/tokens runtime.

## 4. Next.js / Nuxt / hydration data
- Usage : sites qui hydratent la page avec JSON intégré.
- Chercher : `#__NEXT_DATA__`, `window.__NUXT__`, `application/ld+json`, state Redux/Apollo.
- Gain : extraction directe depuis HTML, sans browser.
- Piège : parfois seulement données partielles ou SEO.

## 5. Algolia / Meilisearch / Elastic public keys
- Usage : marketplaces, annuaires, e-commerce, annonces.
- Workflow : chercher `X-Algolia-Application-Id`, `X-Algolia-API-Key`, index names, `queries`.
- Gain : API de recherche complète avec pagination/filtres.
- Piège : clés search-only publiques mais rate-limitées; respecter filtres et coûts.

## 6. GraphQL mining
- Usage : SPA avec endpoint `/graphql` ou Apollo/Relay.
- Workflow : récupérer payloads HAR, fragments dans JS, persisted query hashes, variables pagination.
- Gain : requêtes structurées faciles à rejouer.
- Piège : introspection souvent désactivée; persisted queries nécessitent hash exact.

## 7. Playwright MCP / codegen / trace viewer
- Usage : comprendre vite un formulaire complexe ou des sélecteurs instables.
- Workflow : codegen humain → locators; trace viewer/screenshots pour debug; MCP pour exploration agentique.
- Gain : évite 1h de sélecteurs manuels.
- Piège : ne contourne pas anti-bot, seulement ergonomie/debug.

## 8. Crawlee
- Usage : passer d'un script ponctuel à un crawler robuste.
- Atout : queue persistante, retries, sessions, proxy rotation, stockage, Playwright intégré.
- Gain : moins de plomberie maison pour runs longs/multi-pages.
- Piège : outil à installer/tester; pas miracle anti-bot dur.

## 9. Browsertrix Crawler
- Usage : archiver/capturer massivement un site JS avec vrai navigateur et CDP.
- Atout : Docker, Brave/Puppeteer, WARC/WACZ, comportements personnalisés.
- Gain : bon pour exploration exhaustive/offline, pas seulement extraction.
- Piège : orienté web-archiving, parsing métier à faire ensuite; licence AGPL.

## 10. Patchright / rebrowser-playwright / nodriver
- Usage : quand vanilla Playwright est détecté par webdriver/CDP leaks.
- Atout : drop-in Playwright patché ou CDP direct plus discret.
- Gain : peut passer des bot checks basiques/intermédiaires.
- Piège : pas garanti sur DataDome/Cloudflare fort; consoles/CDP peuvent être limités; vérifier activité/version.

## 11. Sources sobres avant navigateur
- robots.txt, sitemap.xml, RSS/Atom, alertes email, JSON-LD, OpenGraph, pages AMP/mobile.
- Gain : parfois 80% des données sans anti-bot.
- Piège : couverture partielle; valider doublons et fraîcheur.

## 12. Mobile/API/app reconnaissance
- Usage : sites web très protégés mais app mobile/API plus simple.
- Workflow : chercher endpoints publics, docs, APK/network seulement dans un cadre légal/autorisé.
- Gain : API plus propre que DOM web.
- Piège : auth/ToS; ne pas contourner illégalement.

## Matrice de décision rapide
1. HTML contient données ? → parse direct / JSON-LD / hydration.
2. SPA sans données HTML ? → DevTools/HAR/Copy cURL.
3. HTTP 403 direct ? → curl_cffi impersonation.
4. Formulaire complexe ? → Playwright codegen/MCP/trace.
5. Pagination/crawl long ? → Crawlee queue/retries/sessions.
6. Browser détecté ? → Patchright/rebrowser/nodriver smoke test.
7. CAPTCHA/DataDome fort ? → CapSolver + profil humain/proxy résidentiel; ne pas insister en vanilla.

## État VPS observé 2026-06-05
- Playwright : disponible dans Python global.
- Node/npm/npx : disponibles.
- curl_cffi, nodriver, crawlee, scrapy, mitmproxy : non installés globalement; installer en venv projet si besoin.
