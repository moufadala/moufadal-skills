---
name: web-scraping-reality
description: "Connaissances statiques sur le web scraping : hiérarchie des solutions (du plus simple au plus lourd), coûts réels, pièges connus, réflexes. À charger AVANT toute session de scraping ou de récupération de données web, pour choisir la bonne approche et ne pas ré-apprendre les bases en se cassant les dents."
version: 1.0.0
license: MIT
platforms: [linux, macos, windows]
---

## Session references utiles

### Règle dure SearXNG + proxy résidentiel/Tailscale

Avant **toute utilisation de SearXNG** — benchmark, scraper, recherche longue, rapport, diagnostic, veille, expansion de requêtes ou simple preuve d’absence — exécuter d’abord un préflight explicite du chemin réseau mobile/résidentiel Tailscale (`socks5h://127.0.0.1:1055`) et consigner le résultat dans l’artefact : `proxy_status=PASS|FAIL`, IP observée si disponible, commande utilisée, timestamp, et impact sur la fiabilité. La règle n’est pas limitée aux benchmarks/scrapers : si SearXNG sert à prendre une décision, le proxy résidentiel doit être actif ou le résultat doit être marqué `non fiable / à rerun`. Si le proxy échoue, les résultats SearXNG ne doivent pas servir de preuve forte d’absence de résultat ou de blocage anti-bot. Pour Playwright/CDP, passer le proxy explicitement au lancement ; `ALL_PROXY` seul peut produire des faux négatifs.

- `references/source-isolation-tempfile-results.md` — éviter les faux timeouts des wrappers multi-process en écrivant les résultats scraper dans des JSON temporaires plutôt que via `multiprocessing.Queue`.
- `references/reunion-watch-pipeline-and-har-intake-2026-06-13.md` — pattern opérationnel pour avancer sur immo+vols avant HAR/NetLog utilisateur, avec pipeline registry/smoke et script intake.
- `references/proxy-photo-coverage-preflight.md` — preflight mobile/Tailscale obligatoire avant conclusions anti-bot, et gates stricts de couverture photo immo (rejeter SVG/icônes/placeholders/URLs cassées).
- `references/searxng-residential-proxy-gate-and-watch.md` — gate réutilisable avant toute utilisation SearXNG: direct-vs-SOCKS IP, `proxy_status`, blocage volontaire des benchmarks si FAIL, et watcher silencieux qui n’alerte que lorsque le proxy redevient PASS.
- `references/searxng-mobile-proxy-relay-watchdog-2026-07-01.md` — pattern validé pour SearXNG via Tailscale userspace SOCKS `127.0.0.1:1055` + relais HTTP interne `hermes-gateway:1056`, utile quand l’image SearXNG n’a pas `socksio`; vérifier Docker DNS `http://searxng:8080`, statut JSON et tick cron avant verdict.
- `references/searxng-docker-network-runtime-repair-2026-07-11.md` — incident/pattern SearXNG zéro résultat malgré proxy PASS: vérifier le réseau Docker exact de `hermes-gateway`, prouver que `searxng` ne résout pas `hermes-gateway`, puis appliquer seulement `docker network connect <réseau confirmé> searxng`; rollback `docker network disconnect`, ne pas toucher gateway, et rendre durable seulement via diff validé du compose/script.
- `references/searxng-watchdog-durable-network-attach-2026-07-11.md` — durabiliser le fix runtime SearXNG sans compose: sauvegarder le watchdog, ajouter un bloc idempotent `connect only if absent`, tester deux runs (le 2e ne reconnecte pas), vérifier proxy status + recherche >0, et tracer backup/rollback/cron sans toucher `hermes-gateway`.
- `references/searxng-tailnet-serve-exposure-2026-07-11.md` — exposer SearXNG en tailnet-only via Tailscale Serve sans Funnel/public: diagnostiquer depuis le Docker host (pas le namespace Hermes), préserver les guichets existants, ajouter un port dédié `--https=8443`, éviter `serve reset`, gérer le blocage “Serve is not enabled on your tailnet”, tolérer un premier timeout pendant la provision TLS/MagicDNS puis réessayer, et ne proposer un diff `settings.yml` qu’après preuve que l’URL tailnet atteint SearXNG mais renvoie 403/vide.
- `references/android-phone-proxy-vpn-policy-2026-07-01.md` — politique décisionnelle Android proxy/VPN: préférer le chemin Tailscale userspace déjà vérifié à Every Proxy quand le temps manque, watchdog Telegram silencieux sur succès, ne pas mélanger NordVPN téléphone avec la dépendance critique Tailscale, et isoler les besoins “sortie USA/autre pays” dans un conteneur/proxy dédié plutôt que route globale.

- `references/reunion-watch-full-run-resume-2026-06-14.md` — pattern de reprise après `Continue`: vérifier cron/artefacts, lancer un full run manuel avec French Bee si c'est la suite sûre, puis QA dashboard + cohérence Air Austral/Kiwi sans alourdir le cron quotidien.
- `references/reunion-realestate-nondestructive-ingestion-2026-06.md` — pattern réutilisable pour scrapers immobiliers productisables: DB SQLite non destructive, refresh par source, snapshot brut, scoring métier, rapport QA.
- `references/reunion-immo-source-health-before-product-polish-2026-06.md` — règle de reprise produit immo Réunion: avant carte/UX/migration DB, prouver la fraîcheur source par source; un quick gate partiel doit lister explicitement `not-tested`, et une DB/dashboard verts ne prouvent pas que SeLoger/Bien'ici/autres sources sont fraîches.
- `references/seloger-cdp-needs-hardening-registry-2026-06-15.md` — cas SeLoger Réunion: CDP peut charger une vraie page malgré 403/DataDome HTTP, mais parsing DOM non fiable = `needs-hardening`, source désactivée dans le registry avec preuves et gates de promotion; ne jamais assimiler “page chargée” à “scraper prod”.
- `references/reunion-realestate-photo-coverage-gate-2026-06-15.md` — pattern validé pour objectif “toutes les annonces affichées ont une photo” : extraction multi-stratégies `image_url`, filtres anti-placeholder/logo/DPE, SeLoger `h=800`, Domimmo listing-card, OFIM RSS détail, Zimo referer, Superimmo hCaptcha, puis gate DB réversible `active_missing_image == 0`.
- `references/realestate-app-truth-photo-gallery-gates-2026-06.md` — gates produit pour une app immo issue de scraping: audit DB→JSON→UI, mobile-first dogfood, cache local des photos, galeries multi-photos, `description_status`, patch du JSON embarqué, et piège des raws agrégés qui créent de fausses galeries.


## Quand utiliser

AVANT toute session de scraping complexe. Charger ce skill pour avoir les connaissances statiques sans avoir à les re-chercher.

### External agent prerecon reports

When the user brings back a ChatGPT Agent / browser-agent PDF or text report about Réunion flight or real-estate scrapers, use `references/external-agent-scraper-prerecon-triage-2026-06.md`: extract the report, classify claims as confirmed/plausible/contradicted, live-probe only high-value endpoint claims, and convert overclaimed 403/captcha endpoints into HAR/Copy-as-cURL/NetLog capture targets. Also use `references/browser-agent-real-navigation-proof.md` to gate whether the external agent actually used an interactive browser: require URL opened, real user action, result visible, URL final, screenshot/visual description, and explicit `Navigateur réel disponible: oui/non`; if absent, treat the report as research/pre-recon only and send a corrected prompt rather than accepting it as browser evidence. If the user asks whether to invest more in an external agent that found something, use `references/external-browser-agent-followup-investment-gating.md`: invest only on locally validated leads, and send a bounded deep-dive prompt that requires examples, pagination, detail pages, and observed-vs-hypothesis separation instead of another broad panorama.

For the concrete 2026-06-13 pair of PDFs (`rapport_vols_RUN.pdf` + `rapport_investigation_approfondie_immo_reunion.pdf`), use `references/external-agent-vols-immo-triage-2026-06-13.md`: French Bee remains the official flight target; Air Mauritius requires Android NetLog/API mobile; Air Austral has conflicting evidence and needs targeted rerun; immo priority expands beyond Bien’ici/SeLoger to FNAIM, 97immo, OFIM RSS, Alter, Citya, Immo974, DOMimmo, with Superimmo gated behind CDP/HAR because VPS probe returned 503.

Référence spécialisée disponible : `references/flight-amadeus-akamai.md` pour les flux compagnies aériennes CMS/Drupal → Amadeus `plnext/Override.action`, génération `ENC`, et diagnostic Akamai “Pardon Our Interruption` avant de conclure proxy/unlocker requis.

Pour les projets de monitoring de catalogues/prospectus avec reconstitution PDF, extraction produits, alertes et recherche multimodale, consulter `references/catalogue-pdf-product-recon.md` : hard reset de contexte projet, API index d'abord, preuve pages→PDF, matrice par type de viewer, et séparation stricte marketplace API vs extraction OCR catalogue.

Pour LapubRe et les catalogues volumineux, consulter `references/lapubre-large-catalogue-validation-2026-06-12.md` : pipeline API-first `sitemap.xml → /api/prospectus/{uuid} → viewer/assets`, valider 2–3 catalogues récents/gros avant extraction produit, MAGZ multi-pagination `detail.totalPages`, piège `unicode_escape` qui corrompt les URLs Unicode FLIPPING V2, retry ciblé par asset, idempotence et QA stricte pages attendues vs fichiers locaux.

Pour l'évaluation de **Scrapling** sur des scrapers existants, consulter `references/scrapling-targeted-pilots-2026-07-06.md` : ne pas migrer les APIs JSON/GraphQL/RSS stables; cibler seulement les parsers HTML fragiles à base de regex avec `adaptive`/`auto_save`, et benchmarker `StealthyFetcher` sur anti-bot sans promesse. Règle courte : `API stable -> garder`, `HTML regex fragile -> pilote`, `anti-bot -> benchmark`, `chaîne déjà validée -> ne pas réécrire`.

Pour le câblage **Scrapling en production** dans un refresh Python existant, lire aussi `references/scrapling-prod-wiring-python-cdp-playwright-2026-07-07.md` : `scrapling` seul peut manquer `curl_cffi/browserforge`, `html_content` peut casser XML/RSS, le recâblage `$PY` peut déplacer Playwright vers un cache navigateur absent, et l'extension CapSolver peut empêcher CDP 9222/9223 de démarrer sur Chrome 148.

Pour les sites de réservation aérienne avec anti-bot multi-couches, consulter aussi `references/airline-antibot-triage.md` : classer chaque site par couche bloquante, privilégier HTTP-first/curl_cffi quand Playwright échoue au protocole, et pousser une source end-to-end avant d'élargir.

## Hiérarchie des solutions de scraping (par coût décroissant)

### Niveau -1 — 0€, priorité anti-bot/mobile
**Méthode :** API mobile / NetLog Android (`chrome://net-export/`) → replay API direct
- Pour tout site protégé par Cloudflare, Imperva, DataDome, Akamai ou hCaptcha, chercher l'API mobile avant de bricoler Playwright desktop.
- Procédure terrain : Chrome Android → `chrome://net-export/` → Include raw bytes → Start logging → effectuer la recherche sur le site mobile/app web → Stop → parser le JSON NetLog pour endpoints, headers, payloads.
- Priorité obligatoire anti-bot : **API mobile NetLog → endpoint JSON DevTools desktop → CDP browser réel authentifié → Playwright + proxy résidentiel en dernier recours**.
- Cas validé comme leçon 2026-06-11 : Air Austral/Air Mauritius ont fait perdre du temps car cette piste n'a été proposée qu'après Playwright/patchright/curl_cffi/proxy.

### Niveau 0 — 0€, 60% des sites
**Méthode :** DevTools Network → identifier API → curl/requests
- Les sites SPA (React/Angular) ont presque toujours une API backend publique
- 80% du temps, l'API est directement accessible sans auth
- **Ne JAMAIS** ouvrir un browser avant d'avoir vérifié l'API

### Niveau 1 — 0€, 20% des sites
**Méthode :** Playwright pur
- Quand l'API n'est pas directement accessible
- Ou quand le site rend du HTML statique
- Playwright codegen > Playwright scripté (toujours commencer par codegen)

### Niveau 2 — 0€, 10% des sites
**Méthode :** Playwright + stealth plugins
- `playwright-stealth` (pip) ou `rebrowser-playwright` (pip/npm)
- Cache les traces headless (navigator.webdriver, chrome.runtime, etc.)
- Suffit pour contourner la détection basique

### Niveau 3 — ~0.001€/solve, 5% des sites
**Méthode :** nodriver + CapSolver
- `nodriver` (pip) — successeur d'undetected-chromedriver, CDP direct
- CapSolver pour : reCAPTCHA v2/v3, hCaptcha, Cloudflare Turnstile, DataDome
- Nécessite proxy si l'IP est rate-limitée

### Niveau 4 — 5-50€/mois, 3% des sites
**Méthode :** Proxies résidentiels + fingerprinting avancé
- BrightData, Smartproxy, Oxylabs
- Sites difficiles : Kayak, Airbnb, Amazon

### Niveau 5 — 100€+/mois, 2% des sites
**Méthode :** Services spécialisés (Kameleo, Multilogin)
- Fingerprinting browser complet
- Sites très protégés : Google Flights, certains sites bancaires

## Réflexes avant tout scraping

### Correction utilisateur — réalité terrain d'abord

Le bon ordre n'est pas de bricoler Playwright puis de découvrir les méthodes terrain après plusieurs échecs. Pour ce profil utilisateur, commencer par un **reality brief** : ce que les gens font vraiment, probabilité de succès par approche, coût, GitHub patterns, Perplexity pré-recon si disponible, puis seulement la capture technique.

Voir aussi :

- `references/research-first-prerecon-protocol.md`
- `references/evidence-hierarchy.md` — quand un rapport de recherche contredit un artefact local, le local prime toujours
- `references/perplexity-comet-browser-agent-prerecon.md`
- `references/external-agent-prerecon-triage.md` — quand l'utilisateur fournit un rapport PDF/ChatGPT/Comet sur un site à scraper : traiter comme pré-recon, extraire les claims, vérifier localement les endpoints/protections/pagination, puis réécrire un brief capteurs avec faits vs hypothèses.
- `references/chatgpt-agent-immo-prerecon-triage-2026-06-13.md` — cas concret immobilier Réunion : ChatGPT Agent PDF utile mais à corriger par probes VPS; FNAIM URL corrigée, Logic-Immo/PAP 403, priorité socle lifecycle non destructif + HTML P1 avant Bien’ici/SeLoger HAR/NetLog.
- `references/flight-run-source-prioritization-2026-06-04.md` — notes terrain RUN : Air Mauritius formulaire OK mais blocage Imperva/hCaptcha, réalité Google Flights/SerpApi, Skyscanner API officielle vs HAR/replay, et priorité compagnies.
- `references/reunion-flights-realestate-prerecon-2026-06.md` — exemple concret Perplexity → OCR → probes HTTP pour vols RUN + immobilier 974
- `references/feasibility-first-multisite-scraping.md` — quand le goal utilisateur est “que ça marche”, classer les sources par faisabilité et obtenir une preuve live avant d'attaquer les sites durs
- `references/anti-bot-proxy-unblocker-pricing-2026.md` — prix proxies résidentiels, unblockers managés, CapSolver et taux de succès réels par cible (2026)
- `references/flight-antibot-cdp-capsolver-2026-06.md` — détails terrain sur Corsair/Air Mauritius/French Bee : CDP/Xvfb, CapSolver, Imperva/hCaptcha, sélecteurs utiles
- `references/mobile-netlog-antibot-priority-2026-06-11.md` — règle postmortem : pour anti-bot Cloudflare/Imperva/DataDome/Akamai, proposer API mobile via `chrome://net-export` Android avant les variantes Playwright desktop.
- `references/flight-antibot-amadeus-http-first-2026-06.md` — pattern HTTP-first pour sites de vols Amadeus : `curl_cffi`, POST front-end → `ENC` dynamique, blocage final Akamai/Amadeus
- `references/flight-aggregators-kayak-kiwi-graphql-2026-06.md` — pattern agrégateurs vols RUN : Kayak `/i/api/search/dynamic/flights/poll`, Kiwi/Skypicker GraphQL direct, forçage EUR/FR, parsing itinéraires, et discipline de points d'étape courts pendant runs longs.
- `references/kiwi-family-roundtrip-graphql-2026-06.md` — pattern Kiwi A/R famille : capturer `SearchReturnItinerariesQuery`, patcher dates/passagers 2 adultes + enfants, scanner une fenêtre de dates, trier sur `priceEur.amount`, puis valider le booking URL en navigateur avec `passengers=A-C-I` et prix affiché.
- `references/airline-official-family-fares-2026-06.md` — pattern compagnie officielle pour familles/groupes RUN⇄Paris : utiliser Kiwi comme découverte de fenêtres, puis vérifier French Bee/Air Austral officiels; French Bee famille en séquentiel; Air Austral `np` + `tp_i=ADT/CHD`; classer l'officiel direct avant OTA quand il est moins cher/propre.
- `references/flight-coherence-comparison-2026-06.md` — comparaisons terrain agrégateurs vs officiels pour RUN : Air Austral DZA/TNR, Kayak, Trip.com, règles d’écart prix, format compact, et exclusion Corsair.
- `references/flight-aggregator-coherence-checks-2026-06.md` — contrôle de cohérence agrégateurs vs sources officielles RUN : Air Austral DZA/TNR, French Bee Paris, exclusion des sources officielles non validées (ex. Corsair), et distinction blocage site vs bug local screenshot/Chromium.
- `references/flight-aggregator-official-coherence-campaigns.md` — méthode de campagne comparative complète : plusieurs routes/dates, offres détaillées, écarts EUR/% officiels vs agrégateurs, et format compact adapté à l'utilisateur.
- `references/flight-functional-coverage-matrix-2026-06.md` — correction métier vols: ne pas conclure robustesse sur quelques routes adultes; exiger une matrice OD pairs, directions, trip types, enfants/infants, cabines/fare families, escales, filtres métier, et rapports pass/fail avec artefacts.
- `references/flight-source-scope-correction-2026-06-21.md` — correction de scope utilisateur: pour consolider des scrapers vols, ne pas réduire aux deux sources officielles récemment vertes; inventorier aussi agrégateurs et pistes précédentes (Kiwi, Kayak, Skyscanner, Air Mauritius, Corsair, mobile probes), classer les absents explicitement, et corriger les faux positifs prix comme `Erreur 500` → `eur 500`.
- `references/flight-multisource-consolidation-final-verdict-2026-06-21.md` — pattern de verdict final multi-source vols: séparer `solid now`, gaps non solides, faux négatifs réseau corrigés, taxonomie commune, et contrat compact Telegram + artefacts Markdown/JSON.
- `references/flight-solid-evidence-hardening-2026-06-21.md` — correction qualité utilisateur: un inventaire large n’est pas un résultat solide; produire un rapport `solid-only`, réparer les `bug-local` avant verdict, exiger JSON structuré prix+segments+booking URL ou matrice fonctionnelle, et séparer clairement “solide”, “non solide”, “en cours”.
- `references/flight-proxy-watchers-and-solid-kiwi-2026-06-21.md` — RUN vols: ne pas interpréter les logs Tailscale `magicsock` comme panne; vérifier direct vs SOCKS, corriger les faux positifs prix (`Erreur 500`→`eur 500`), réparer Kiwi direct stale-template, et livrer un rapport `solid-only` avec prix+segments+booking URL.
- `references/tailscale-socks-exit-node-connect-failure-2026-06-21.md` — diagnostic proxy mobile: `magicsock`/`wgengine`, exit node sélectionné et handshake SOCKS OK ne prouvent pas l'egress Internet; si `curl --socks5-hostname` échoue en `(97)` ou SOCKS CONNECT renvoie `0x05 0x01`, classer `network-preflight-failed` et faire corriger Android avant de relancer les scrapers.
- `references/flight-frenchbee-rerun-hardened-after-proxy-2026-06-21.md` — quand le téléphone/Tailscale revient, relancer seulement les cas French Bee faussement échoués par proxy + une matrice de durcissement bornée; préflight direct-vs-SOCKS par cas, exécution séquentielle Playwright, artefacts par cas et reporting compact `completed/total` avant tout verdict “solide”.
- `references/residential-proxy-centralization-2026-06-11.md` — centraliser `SOCKS_PROXY`/`HERMES_SOCKS_PROXY`, gérer host vs container, vérifier le handshake SOCKS5 avant d'accuser les scrapers, et persister le pont Android/VPS via service host.
- `references/tailscale-android-exit-node-vps-mobile-ip-2026-06.md` — alternative plus simple au bricolage Termux/SSH pour sortir un VPS par l'IP téléphone: Tailscale Android exit node, avec validation communauté/docs, risques Android/VPN/batterie, preuve IP avant/après, rollback, et interdiction de router naïvement tout le VPS en permanence.
- `references/tailscale-userspace-playwright-socks-proxy-2026-06.md` — pattern validé sans sudo: Tailscale userspace + SOCKS local `127.0.0.1:1055` + exit node Android; preuve IP directe vs IP téléphone; surtout, Playwright/Chromium doit recevoir `launch(proxy={...})` ou `--proxy`, car `ALL_PROXY` seul peut créer des faux négatifs/reset.
- `references/tailscale-exit-node-vps-preflight.md` — correction post-incident: l'UI Android “Exit Node — Running on this device” ne prouve pas que le VPS peut utiliser le téléphone; exiger `exit-node list`/`ExitNodeOption=true` + IP direct vs SOCKS avant tout verdict scraper.
- `references/tailscale-exit-node-timeboxed-flight-rerun-2026-06-21.md` — quand le proxy téléphone est actif mais gêne l'utilisateur, traiter la fenêtre comme rare: préflight IP immédiat, retirer les flags `--no-proxy`, lancer d'abord les cibles qui dépendent vraiment du proxy, puis seulement les bonus.
- `references/tailscale-consequence-audit-and-scraper-registry-2026-06.md` — audit des conséquences Tailscale après installation: listener loopback, routes/DNS, direct vs proxy, conflits d'anciens bridges `1080`, centralisation proxy_config, watchdog silencieux, et réponse structurée quand l'utilisateur signale que les scrapers partent dans des tests dispersés: créer registry + smoke runner avant de coder encore.
- `references/scraper-confidence-audit-after-network-changes-2026-06.md` — pattern quand l'utilisateur demande si “tout marche” après modifs réseau/proxy/Traefik: ne pas rassurer sans preuve; run infra + registry + quick/full smoke non destructif; distinguer sources actives prouvées, sources désactivées non couvertes, site blocks et bugs locaux; citer artefacts et comptes.
- `references/daily-scraper-gate-proxy-propagation.md` — pattern post-registry: propager explicitement le proxy à travers daily shell → pipeline → orchestrateur → scraper Playwright, ajouter un quick gate cron silencieux avant le daily, corriger les wrappers scheduler, prouver de bout en bout via manifest/tasks.json, et éviter les faux négatifs Python `__pycache__` via `PYTHONDONTWRITEBYTECODE`/`PYTHONPYCACHEPREFIX`.
- `references/scraper-source-registry-smoke-runner.md` — checklist réutilisable pour transformer un ensemble de scrapers fragiles en registry + smoke runner non destructif, avec classifications `prod-candidate` / `needs-hardening` / `blocked-antibot` / `bug-local` / `low-value`.
- `references/graphql-replay-best-effort-and-smoke-runner-hardening-2026-06.md` — pattern pour remplacer un lancement navigateur fragile par un wrapper `direct replay → browser fallback → refresh template`, plus mitigation `PYTHONDONTWRITEBYTECODE=1` dans les smoke runners pour éviter les faux négatifs `__pycache__`.
- `references/proxy-fallback-and-flight-probe-false-negatives-2026-06.md` — pattern proxy mobile/Tailscale pour éviter les faux négatifs: ne pas fallback automatiquement vers l'ancien `1080`, preflight `1055`, fallback direct explicite avec `proxy_status`, FrenchBee one-way `travel_type=O`, et preuve manuelle des sources désactivées sans les activer en prod.
- `references/proxy-policy-official-validation-and-strict-mode-2026-06.md` — politique proxy validée docs/communauté: Tailscale userspace `1055`, Playwright proxy explicite, `socks5h` côté HTTP, `HERMES_REQUIRE_PROXY=1`/strict-mode pour éviter les fallbacks VPS non assumés, et champs registry `require_proxy`/`allow_direct_fallback`/`manual_only`.
- `references/proxy-preflight-and-priority-flight-campaign-2026-06.md` — correction post-incident: quand l'utilisateur active l'exit node Android pour une fenêtre courte, vérifier `exit-node list`/`ExitNodeOption`/IP direct-vs-SOCKS avant tout verdict, prioriser les scrapers réellement dépendants du proxy (ex. French Bee), retirer les flags `--no-proxy`, puis enchaîner via superviseur auto-goal si le proxy peut rester actif.
- `templates/scraper_source_registry.min.json` — squelette JSON/YAML de registry à copier puis adapter pour un nouveau projet multi-sources.

1. **Reality brief** : odds terrain, méthodes communautaires, coûts, pièges connus
2. **GitHub search** : chercher code/issues existants avant de coder
3. **Perplexity Pro pré-recon** si l'utilisateur a des crédits : hypothèses, keywords, endpoints probables, screenshots, checklist — jamais source de vérité finale. Si le rapport arrive en PDF/email/screenshot, extraire le texte puis vérifier qu'il n'est pas tronqué; compléter par OCR d'images si nécessaire.
4. **Validation locale immédiate** : probes `curl`/`requests` sur les endpoints/pages proposés, avec HTML/JSON brut archivé. Libeller clairement `Perplexity affirme` vs `curl local confirme/infirme` vs `HAR nécessaire`.
5. **Human-in-the-loop capture tôt** : Playwright codegen / HAR / mitmproxy pendant que l'humain fait l'action réelle. Si le VPS/headless est bloqué par DataDome/Cloudflare/403 mais que l'utilisateur accède au site dans son navigateur normal, demander rapidement un HAR Chrome `Save all as HAR with content` sur 1-3 pages représentatives au lieu de bricoler longtemps côté serveur. Le HAR sert à découvrir les endpoints, payloads, pagination, IDs et dépendance cookies; il ne prouve la reproductibilité qu'après replay local.
   - Méthode la plus rapide quand une requête précise est repérée : DevTools Network → clic droit sur XHR/fetch gagnant → `Copy as cURL` → rejouer localement → convertir en Python/JS avec curlconverter si besoin. Attention : cookies/tokens dans le cURL/HAR = secrets, utiliser profil dédié.
   - Méthode plus profonde : mitmproxy/Charles/Proxyman si le site masque ou multiplie les requêtes; capture toutes les requêtes d'un vrai navigateur, permet replay client-side et inspection WebSocket/SSE.
   - Si replay échoue avec 403/DataDome malgré le bon endpoint : le blocage est probablement lié aux cookies courts, au fingerprint, à l'IP ou au challenge; prochaine hypothèse = profil Chrome humain persistant, proxy résidentiel/mobile, ou extraction semi-manuelle assistée.
5. **DevTools Network → identifier l'API** (80% du travail)
6. **Si API trouvée** → curl/requests direct
7. **Si pas d'API** → Playwright codegen puis script robuste
8. **Si codegen échoue** → Playwright scripté avec interception réseau
9. **Si bloqué par anti-bot** → stealth plugin
10. **Si CAPTCHA / hCaptcha / Imperva / Incapsula détecté** → **CapSolver immédiatement, pas “plus tard”**
    - Vérifier tout de suite `CAPSOLVER_API_KEY`, `/opt/data/capsolver-ext`, Chrome CDP `:9222`.
    - Produire un artefact CapSolver/CDP : screenshot du challenge, logs réseau, verdict “résolu / non résolu”.
    - Ne pas classer une cible comme bloquée tant qu’un test CapSolver réel n’a pas été tenté ou explicitement impossible.
11. **Si IP bannie après CapSolver** → proxy résidentiel ou profil Chrome humain persistant

Règle de sortie : aucune conclusion de faisabilité sans artifact reproductible (HAR, curl, raw JSON, screenshot, replay script, ADR). Pour une page CAPTCHA, l’ADR doit dire explicitement : `CapSolver testé: oui/non`, méthode utilisée (`extension`, `API token`, `CDP`), résultat, et prochaine hypothèse.

### Pré-recon multi-verticale et screenshots

Quand l'utilisateur prépare un gros prompt Perplexity/browser/ChatGPT Agent pour du scraping, intégrer tous les verticals signalés avant envoi (ex. vols + immobilier), et pas seulement le sujet initial. Pour les sites à interface visuelle, demander explicitement des screenshots comme preuves opérationnelles : formulaire ouvert, filtres, résultats, erreurs, pagination, consent banners, et page détail. Si l'outil ne peut pas joindre les images, demander une description structurée équivalente.

Si l'utilisateur veut exploiter ChatGPT Agent comme levier externe pour plusieurs familles de scrapers, préférer des prompts séparés par vertical plutôt qu'un prompt global : par exemple un prompt vols RUN et un prompt immobilier Réunion. **Signal utilisateur fort 2026-06-13 : demander le maximum dans chaque prompt**, pas juste une recherche générale — navigateur réel, code source, JS bundles, DevTools/Network/HAR si disponible, Copy-as-cURL, screenshots/descriptions, endpoints XHR/fetch, anti-bot, pagination/complétude, et artefacts exacts à fournir à Hermes. Livrer des fichiers prêts à coller et, si demandé, des PDF téléchargeables. Voir `references/chatgpt-agent-prompt-pack-vols-immo-2026-06-13.md` pour le modèle de pack, le contrat de sortie et la conversion PDF via Chromium CDP.

Pour l'immobilier, prioriser les méthodes sobres avant Playwright : robots.txt/sitemap/RSS/alertes officielles → HTML paginé → JSON-LD → HAR/XHR → Playwright. Prévoir dès la pré-recon les champs de notification et de déduplication (ID annonce, URL canonique, loyer, ville, surface, date, agence, content_hash).

- `references/reunion-flights-real-estate-prerecon.md` pour le périmètre Réunion vols + locations.
- `references/reunion-realestate-seloger-comparison-2026-06.md` pour décider si une source immobilière difficile (ex. SeLoger) mérite un vrai scraper : échantillon manuel/PDF → normalisation → matching contre la DB existante → taux d'unique probable avant anti-bot.
- `references/seloger-dom-card-pagination-2026-06-15.md` pour productiser SeLoger quand CDP charge la SERP : utiliser les cards DOM `[id^="classified-card-"]`, pagination `aria-label`, parse prix ligne-par-ligne avec NBSP/narrow NBSP, et imprimer un JSON final parsable par le smoke runner.
- `references/business-scraper-stabilization-2026-06.md` pour transformer des scrapers existants en module métier robuste : dry-runs par source, backup SQLite, lifecycle `is_active`, rapports scorés/dédupliqués, et retry overnight non destructif.
- `references/lapubre-product-extraction-magz-v2-2026-06-13.md` pour les catalogues retail/brochures : ne pas confondre téléchargement complet du catalogue et extraction produits/prix; expliquer options/risques, générer 20 `product_candidates` validables avec preuve visuelle/source, puis promouvoir uniquement les lignes `validated`/`corrected` dans `products`.

### Stabilisation métier de scrapers existants

Quand l'utilisateur demande de “tester, optimiser, nettoyer, retenter” des scrapers ou d'obtenir des “modules métier qui fonctionnent”, ne pas seulement améliorer les sélecteurs. Construire une couche d'orchestration non destructive au-dessus des scrapers : inventaire, compilation, dry-run par source, parsing JSON des résultats, backup DB avant refresh, rapports JSON/Markdown, filtres métier et scoring.

Règles durables :
- pour l'immo Réunion résidentiel, utiliser aussi `references/reunion-immo-residential-quality-gate-2026-06-23.md` : fraîcheur DB ≠ qualité résidentielle, exporter un sous-ensemble `residential_candidate`, et éviter les filtres texte trop agressifs ;
- marquer les anciennes annonces `inactive`, jamais les supprimer pendant la stabilisation ;
- ne marquer stale que les sources réellement vues dans le run courant ; si une sous-source échoue en `429/403/CAPTCHA` dans un wrapper global, conserver ses anciennes annonces actives jusqu'à un retry réussi ;
- attention aux faux timeouts dans les runners `multiprocessing`: envoyer de gros payloads de listings via `Queue` peut remplir le pipe et bloquer le child avant `join()`. Pour les sources volumineuses, faire écrire le child dans un fichier temporaire puis lire ce fichier côté parent ;
- filtrer par défaut les catégories qui polluent un objectif résidentiel (`bureau`, `local commercial`, `box`, `garde-meuble`, `parking`, `terrain`, `chambre/colocation`) ;
- ajouter des garde-fous métier contre les prix parsés impossibles avant de présenter un “top” ;
- dédupliquer au niveau métier (ville + loyer + surface + pièces), pas seulement par ID source ;
- pour les runs longs, lancer un runner overnight avec artefacts horodatés, symlink `latest`, retry différé des sources transitoires, et rapports de variantes métier.

### Discipline d'exploration — ne pas effleurer 5 pistes

Signal utilisateur fort : sur les tâches de scraping, éviter de tester superficiellement plusieurs options puis de conclure trop tôt. Pour chaque cible prioritaire, tenir un inventaire explicite :

- ✅ réellement testé : URL, action, résultat, artefact produit
- ❌ pas encore testé : hypothèses restantes concrètes
- prochain test unique : celui qui réduit le plus l'incertitude

Si l'utilisateur dit qu'on “galère”, qu'on teste trop de choses sans ordre, ou demande le consensus communautaire, ne pas lancer immédiatement un nouveau scraper. La bonne prochaine étape est de stabiliser le système d'exploration: `scraper_source_registry.yaml` ou table équivalente + runner de smoke par source + classification `prod-candidate` / `needs-hardening` / `blocked-antibot` / `bug-local` / `low-value`. Voir `references/tailscale-consequence-audit-and-scraper-registry-2026-06.md`.

**Campagne bornée “continue 20 min / sans relâche” :** ne pas répondre par une promesse ou un plan seul. Démarrer immédiatement un run non destructif borné et archivé, tout en menant la pré-recon utile en parallèle : discovery/docs/communauté, vérification proxy/fingerprint, smoke par source, classification registry, puis patchs sûrs uniquement. Le rapport final doit distinguer recherche vérifiée, hypothèses, bugs locaux, blocages anti-bot et prochains tests uniques. Si un run dépasse Telegram, le lancer en background avec notification et livrer le chemin d'artefact.

### Correction utilisateur — zéro simulation quand l'objectif est le scraping réel

Si l'utilisateur demande de “re-scraper”, “relancer le processus”, “exécuter vraiment”, ou corrige explicitement “je ne veux pas de simulation”, alors toute réponse théorique ou rapport estimé est une erreur. Le bon comportement est :

1. Retrouver les cibles depuis les artefacts, scripts, skills et sessions disponibles avant de demander une liste.
2. Vérifier l'outillage réel (`scraping-health`) : Playwright, CDP, `curl_cffi`, `har2requests`, scripts existants.
3. Lancer des scrapers/probes réels, même en dry-run non destructif si l'écriture DB est risquée.
4. Mesurer pendant l'exécution : temps, statut HTTP, nombre d'items/URLs, artefacts produits, blocage exact.
5. Comparer les méthodes seulement à partir d'observations live ou d'anciens artefacts clairement cités — jamais inventer des gains “typiques”.
6. Produire un rapport final uniquement après les runs, avec matrice `site → méthode → résultat → temps → données collectées → gain constaté → artefact`.

Si le contexte est compressé et que la liste de sites semble absente, commencer par relire `/opt/data/AGENTS.md`, mémoires, `PRESERVE_*`, `/opt/data/scripts`, `/opt/data/artifacts`, puis reprendre les cibles trouvées. Ne pas dire “donnez-moi les URL” tant que cette récupération locale n'a pas été tentée.

Pendant les runs longs, surtout via Playwright/Chrome, **ne pas bloquer Telegram** : lancer en background avec `notify_on_complete=true` ou via un runner parallèle borné, annoncer le `session_id`, puis rester disponible pour les messages utilisateur. Donner des points d'étape courts : site/route en cours, PID/session si disponible, artefacts attendus, et distinction claire entre blocage du site (CAPTCHA/403/robot) et bug local d'outillage (crash screenshot, bug Playwright, surcharge Chromium, permissions d'artefacts, proxy non transmis à Chromium). Ne pas répéter des intentions sans action ni résultat.

### Proxy mobile/résidentiel : Playwright doit recevoir le proxy explicitement

Quand le VPS sort via un téléphone Android/Tailscale userspace ou un SOCKS local, ne pas supposer que `ALL_PROXY` suffit. Pour Chromium/Playwright, utiliser `chromium.launch(proxy={"server": "socks5://127.0.0.1:1055"})`, ou ajouter une option CLI `--proxy` au scraper qui remplit ce champ. Toujours archiver deux preuves : IP directe VPS et IP via SOCKS. Si `ALL_PROXY` donne `ERR_CONNECTION_RESET` mais que `launch(proxy=...)` charge la page, classer l'échec précédent comme bug local de routage, pas comme blocage site. Voir `references/tailscale-userspace-playwright-socks-proxy-2026-06.md`.

**Préflight Tailscale obligatoire avant verdict scraper :** ne pas prendre l'UI Android, le badge admin “Exit Node”, ni les logs `wgengine`/`magicsock` comme preuve suffisante. Ils peuvent seulement prouver que le téléphone est connecté au tailnet. Côté VPS, vérifier que le téléphone est réellement utilisable comme exit node (`tailscale exit-node list` ou JSON avec état exit-node utilisable), puis comparer IP directe vs IP via `--socks5-hostname 127.0.0.1:1055`. Pièges observés: `EXIT NODE = None` sur Android signifie que l'état nécessaire n'est pas actif; un vieux `ExitNodeID` côté VPS peut rester alors que `RouteAll=false`; `AllowedIPs` limité à `100.x/32` signifie pas de route Internet. Si le SOCKS retourne encore l'IP VPS, classer l'échec comme `network-preflight-failed`, pas comme scraper/site cassé. Détail + commandes: `references/tailscale-exit-node-vps-preflight.md`.

- `references/flight-campaign-runner-false-negatives-2026-06-11.md` — faux négatifs `winners=[]`, parsing du stdout complet, `ok:true`/`price_eur`/`EUR301,70`, succès partiels officiels et bugs locaux de runner.
- `references/overnight-prod-hardening-2026-06-11.md` — campagne nocturne production-like immo Réunion + vols RUN : inventaire → health archivé → dry-runs non destructifs → classification `prod-candidate`/`needs-hardening`/`blocked-antibot`/`bug-local`/`low-value`, fallback Kiwi browser capture, et séparation bug local vs blocage site.

### Campagnes larges sur scrapers fragiles

Signal utilisateur validé : quand les scrapers “marchent mais sont fragiles”, ne pas se limiter à un seul trajet/date ni lancer un gros paquet incontrôlé. Créer une **campagne bornée** : matrice large de dates/destinations/origines utiles, mais quotas par famille de scraper (`French Bee max 1` si profil Chromium persistant/headed, `Air Mauritius/Air Austral max 1`, probes HTTP légers plus parallèles), timeouts courts, artefacts par tâche (`stdout`, `stderr`, `status`) et `SUMMARY.json` final. Lancer en background avec notification pour préserver Telegram. Voir `references/fragile-flight-scraper-campaigns-2026-06-11.md` pour le pattern campagne vols RUN.

Correction métier vols : une campagne “large” ne doit pas seulement multiplier les dates sur le même cas adulte. Avant de dire qu'un scraper vols est robuste, couvrir explicitement les axes fonctionnels : OD pairs/aéroports, sens aller-retour, one-way vs A/R 7/14 nuits, compositions passagers avec enfants/infants, cabines/familles tarifaires, direct/max-1-escale/any-stops, durée max et prix total vs prix par passager. Produire un rapport `tested / not-tested / blocked / bug-local` par axe. Voir `references/flight-functional-coverage-matrix-2026-06.md`.

Après une campagne, ne jamais prendre `winners=[]` au pied de la lettre sans audit rapide des artefacts : parser le stdout complet, pas seulement la tail, compter `ok:true`, `price_eur`, `EUR...`, et les pages officielles rendues avec prix comme succès partiels. Séparer explicitement `blocage site` (Cloudflare/403/CAPTCHA/Pardon) de `bug local runner` (profil Chrome déjà utilisé, TargetClosed, Xvfb absent, mauvais interpréteur Python/venv, dépendance manquante, template local absent, parseur qui ignore un prix). Si le bug est local et qu'un venv validé existe, relancer une fois avec le venv avant de classer la source. Voir aussi `references/flight-campaign-result-classification-2026-06-11.md` et `references/overnight-prod-hardening-2026-06-11.md` pour classer les résultats métier quand `exit_code`/`ok_hint` mentent, relire les `stdout_file` complets, sérialiser les scrapers à profil navigateur persistant, et produire un bilan compact.

Pour cet utilisateur, les bilans de scraping/comparaison doivent être compacts par défaut : bullets courts, chiffres clés, écarts en EUR/% et verdict explicite. Éviter les longs pavés narratifs; si beaucoup d'informations existent, grouper par route/source et renvoyer les détails en artefact ou référence. Signal fort validé : si l'utilisateur dit que c'est trop long, refaire immédiatement une version plus courte mais complète, avec verdict d'abord puis détails en annexe/fichier — ne pas défendre le format précédent.

Pour un site SPA/formulaire, pousser au moins ces pistes avant d'abandonner:

1. URL directe ou deep-link du moteur (`/search`, paramètres comme `?fsopen=true`)
2. Screenshot de ce que Playwright voit réellement
3. Remplissage Playwright pur, sans LLM, avec locators stables
4. Interception réseau XHR/fetch pendant le clic Search
5. Replay `curl`/`requests` d'un appel gagnant si trouvé

### Correction utilisateur — arbitrer entre “sites cassés” et “ça doit marcher”

Sur une mission multi-sites, ne pas revenir trop vite polir la cible déjà gagnante quand l'objectif est de diagnostiquer les blocages : si un site fonctionne end-to-end et d'autres restent cassés, mettre le site gagnant en pause après preuve minimale, puis pousser les cibles non fonctionnelles jusqu'à un verdict documenté.

Mais si l'utilisateur corrige la trajectoire avec un signal du type **“le goal c'est que ça marche”, “attaque les plus faisables d'abord”, “pas les plus gros”**, inverser immédiatement la priorité : classer les cibles par faisabilité réelle, tester d'abord la source la plus probable, obtenir une preuve live, puis stabiliser ce chemin avant de revenir aux sites durs. Ne pas confondre difficulté technique intéressante avec valeur utilisateur.

Dans les deux cas, chaque cible non gagnante garde une fiche courte : capture visuelle, URL finale, erreur exacte, réseau, et prochaine hypothèse concrète.

Pour chaque cible cassée, produire une ligne de matrice qui sépare clairement **site anti-bot/protection**, **bug local/outillage**, et **filtrage métier/valeur** :
- état : formulaire chargé / page blanche / challenge / résultats / API rejouable ;
- protection site : Cookie banner, Imperva, hCaptcha, Cloudflare, HTTP/2, DataDome, etc. ;
- bug local possible : venv, mauvais interpréteur, proxy non transmis à Playwright, profil Chrome déjà utilisé, parser qui ignore un prix, screenshot/Chromium crash ;
- valeur métier : source hors scope, doublon, champ clé absent, qualité business trop faible ;
- preuve : screenshot + chemin artefact + script de reproduction ;
- prochaine approche : CDP/Xvfb, profil humain, token CAPTCHA, HAR manuel, API replay, proxy.

Pour les comparatifs vols agrégateur vs officiel, ne pas utiliser le mot “cohérent” seul : toujours chiffrer l’écart (EUR et %, quand possible), préciser si c’est le même vol/horaire/compagnie, et classer la source comme `live exact`, `probablement live`, `indicatif/à partir de`, ou `non concluant`. Ne pas comparer un aller simple agrégateur à un aller-retour officiel sans le signaler clairement.
6. Si screenshot/réseau montre CAPTCHA, hCaptcha, Imperva, Incapsula ou “Pardon our interruption” : basculer immédiatement en test CapSolver/CDP avant d’élargir à une autre compagnie/source.

### Gate anti-bot obligatoire

Quand une cible échoue avec `captcha`, `hcaptcha`, `Imperva`, `Incapsula`, `Pardon Our Interruption`, `Access denied`, ou page blanche suspecte :

```bash
# disponibilité locale
printenv CAPSOLVER_API_KEY >/dev/null && echo CAPSOLVER_API_KEY_OK || echo CAPSOLVER_API_KEY_MISSING
test -d /opt/data/capsolver-ext && echo CAPSOLVER_EXT_OK || echo CAPSOLVER_EXT_MISSING
curl -s http://127.0.0.1:9222/json/version || true
```

Ensuite créer un test dédié avant de conclure :
- Chrome CDP headed/Xvfb avec extension CapSolver si disponible.
- Screenshot avant/après 30-90s.
- Logs réseau et URL finale.
- Si extension échoue, noter explicitement l’hypothèse suivante : API token + injection callback, profil humain persistant, ou proxy résidentiel.

Ne pas repousser CapSolver à “plus tard” : si le problème visible est un CAPTCHA, c’est le prochain test, pas une option secondaire.

### CapSolver : ne pas confondre disponibilité et résolution effective

Pour chaque cible, distinguer explicitement :
- `CAPSOLVER_API_KEY` présent / balance OK ;
- extension chargée dans Chrome/CDP ;
- challenge détecté ;
- tâche API ou classification réellement créée ;
- solution reçue ;
- token/clic accepté par le site.

Piège validé 2026-06-03 sur Corsair/Imperva+hCaptcha : `HCaptchaTaskProxyLess` peut retourner `ERROR_INVALID_TASK_DATA: We don't support this service` même si l'extension contient ce type. Dans ce cas, ne pas conclure trop vite “solveur impossible” : capturer d'abord le vrai payload hCaptcha (`/getcaptcha`, `rqdata`, enterprise data, n-data si présent), puis tester un provider qui accepte ces champs (2Captcha / Anti-Captcha / CapMonster selon docs actuelles). Si le payload complet reste indisponible ou refusé, classer alors en besoin proxy résidentiel/mobile + profil navigateur persistant. Une extension chargée + clé OK n'est jamais une preuve de solveur effectif, et un token retourné n'est pas une preuve tant qu'il n'est pas accepté par le site.

### Airlines Amadeus — HTTP-first avant navigateur lourd

Sur les sites de vols adossés à Amadeus, différencier le front site du moteur `plnext` :

- Si Playwright/Chromium échoue avec une erreur protocolaire (`ERR_HTTP2_PROTOCOL_ERROR`, timeout) mais que le HTML est accessible, tester `curl_cffi` avec impersonation Chrome avant de complexifier le navigateur.
- Chercher les formulaires front (`Drupal`, `amadeus-form-*`) et les champs cachés frais (`form_build_id`, `form_id`, langue, passagers).
- Rejouer le POST front-end pour générer un `ENC` dynamique vers `Preload.action`/`Override.action`.
- Si le follow Amadeus renvoie `Pardon Our Interruption`, le payload front est probablement correct : le blocage restant est fingerprint/réputation Akamai/Amadeus. Tester cookies/referrer exacts + CDP/nodriver sur l'URL générée, puis proxy résidentiel/mobile si nécessaire.

Voir `references/flight-antibot-amadeus-http-first-2026-06.md` pour le cas French Bee RUN→ORY validé.

## GitHub comme source de recherche (alternative à SearXNG)

Quand SearXNG est en panne ou donne des résultats inutilisables, utiliser GitHub CLI :

```bash
# Rechercher du code réel qui résout le problème
gh search code "playwright readonly datepicker" --limit 10

# Rechercher des issues contenant la solution
gh search issues "angular formControlName value not setting" --limit 10

# Rechercher des repos d'outils de scraping
gh search repos "nodriver" --sort stars --limit 5
```

**Pourquoi GitHub est meilleur :**
- Code réel et fonctionnel (pas d'articles Medium SEO)
- Issues avec solutions validées par la communauté
- Classement par ⭐=pertinence
- Accès aux workarounds officiels (issue Playwright #14281 pour le datepicker readonly)

## Outils de découverte alternatifs

### Perplexity Comet / Perplexity Pro (browser agent)
Si l'utilisateur parle de **Perplexity Comet**, ne pas le traiter comme un simple moteur de recherche : c'est un navigateur agentique capable d'interagir avec les pages (clics, formulaires, onglets, observations visuelles) via l'utilisateur. Voir `references/perplexity-comet-browser-agent-prerecon.md` pour le prompt type et le protocole.

À utiliser pour accélérer la pré-recon quand le VPS/headless bloque :
- Explorer manuellement une SPA ou un widget complexe
- Pousser un parcours utilisateur réel jusqu'aux résultats
- Obtenir URL finale, screenshots/observations, messages d'erreur, champs visibles
- Demander explicitement les requêtes XHR/fetch/HAR si Comet peut les exposer
- Repérer des indices de routes/API dans le code ou l'interface
- Produire une analyse structurée à challenger

**Limite importante :** Comet/Perplexity ne remplace PAS DevTools/mitmproxy/HAR. Il n'est pas un composant de production, ne donne pas toujours les headers/payloads exacts, et peut halluciner des endpoints. Toute conclusion doit être validée par un artefact local : HAR, capture réseau, réponse brute, puis replay `curl`/`requests`.

**À utiliser :** outil humain d'appoint pour accélérer la découverte, jamais preuve finale. La bonne boucle est : prompt structuré à Comet → l'utilisateur transmet rapport/screenshots/URLs/payloads → validation locale → scraper reproductible.

### Playwright codegen
```bash
playwright codegen https://site.com
```
Ouvre un navigateur visible + enregistreur. L'humain clique, codegen génère le script Playwright. **Toujours essayer AVANT d'écrire du code à la main.**

### Playwright MCP pour exploration agentique

Playwright MCP n'est pas un moteur plus puissant que Playwright : il expose Playwright à un agent via snapshots d'accessibilité, refs d'éléments, console/réseau/artefacts. À utiliser comme outil de découverte/debug quand Playwright brut fait perdre du temps sur les sélecteurs, dropdowns, formulaires dynamiques ou états de page. Ne pas le confondre avec une solution anti-bot : IP datacenter, CAPTCHA, Imperva/Akamai restent des problèmes séparés.

Pattern VPS validé 2026-06-04 avec Claude Code + `@playwright/mcp@0.0.75` :

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": [
        "-y", "@playwright/mcp@latest",
        "--headless", "--no-sandbox",
        "--executable-path", "/opt/data/home/.cache/ms-playwright/chromium-1223/chrome-linux64/chrome",
        "--user-data-dir", "/tmp/playwright-mcp-userdata",
        "--output-dir", "/opt/data/artifacts/playwright-mcp-analysis/output",
        "--timeout-action", "10000",
        "--timeout-navigation", "90000"
      ]
    }
  }
}
```

Deux pièges locaux validés :
- sans `--user-data-dir`, MCP tente `/opt/hermes/.playwright/...` et échoue `EACCES` ;
- sans `--executable-path`, MCP cherche `/opt/google/chrome/chrome` alors que Chrome système n'est pas installé.

Usage recommandé : MCP découvre et produit snapshots/refs → écrire ensuite un script Playwright déterministe. Exemple Air Mauritius : MCP a sélectionné RUN→MRU avec succès, mais la tentative full dates+search a dépassé les tours; le prochain bon test est un script Playwright borné utilisant les artefacts MCP.

### mitmproxy
```bash
mitmweb --listen-port 8080  # Interface web pour voir les requêtes en direct
```
Proxy intercepteur. Lance le navigateur avec `--proxy-server=localhost:8080`, fais les clics manuellement, mitmproxy capture TOUS les appels API (URL, payload, réponse). Ensuite, reproduis avec curl.

### Human-in-the-loop Network Capture
1. Start Playwright with `page.on("request")` interception
2. Human does the interaction (fill fields, click search)
3. Capture ALL API calls
4. Reproduce the winning call with curl — no browser needed

## Pièges connus

### CookieYes / Cookie Consent (pas un CAPTCHA)
- Ce n'est PAS un CAPTCHA — CapSolver ne sert à rien
- Solution : **supprimer du DOM** avec `.remove()`, pas seulement cliquer "Accepter"
- Le bouton "Accepter" fait disparaître la bannière visuellement mais le DOM reste et intercepte les clics
- La méthode fiable :
  ```javascript
  document.querySelectorAll('.cky-consent-container, .cky-modal, .cky-overlay')
    .forEach(e => e.remove());
  ```

### Bouton Search disabled (form validation)
- Si le bouton "Rechercher" est `disabled`, la validation du formulaire bloque
- Forcer `btn.disabled = false` puis `btn.click()` ne déclenche PAS la recherche
- Il faut résoudre la cause (champ obligatoire manquant), pas le symptôme
- Vérifier `document.querySelector('button').disabled` + `form.checkValidity()`

### Widget hors formulaire standard
- Parfois les champs (Origin1, Destination1, Date1) ne sont PAS dans le `<form>` HTML
- Le formulaire ne contient que des champs cachés (region, language)
- Le widget JS lit les champs directement et fait son propre appel API
- La recherche ne peut PAS être déclenchée par un submit HTML standard

### Angular Material Datepicker
- L'input a `readonly=""` — le valeur ne peut pas être changée via DOM
- Solution : cliquer sur l'input pour ouvrir le calendrier, puis cliquer une date
- Alternative : `inp.removeAttribute('readonly')` PUIS nativeSetter

### Formulaires Angular avec formControlName
- `page.fill()` et `page.type()` ne déclenchent pas toujours Angular
- Solution : `page.evaluate()` avec nativeSetter + dispatchEvent('input') + dispatchEvent('change')
- Ou utiliser `page.locator().pressSequentially()` qui simule des frappes

### Cloudflare Bot Management
- Si `/_cf` ou `/cdn-cgi/` dans les logs → Cloudflare
- Playwright + stealth passe ~70% du temps
- Le reste nécessite proxies résidentiels ou rebrowser-playwright

### SPA qui se re-render (Angular/React)
- Les references DOM deviennent obsolètes après un re-render
- Solution : utiliser les locators Playwright (auto-re-query) pas les element handles
- `page.locator()` > `page.query_selector()`

## Anti-patrons à éviter

- ❌ Coder le scraping à la main avant d'avoir donné à l'utilisateur la réalité terrain et les odds de succès
- ❌ Oublier GitHub/perplexity pré-recon et passer directement aux essais isolés
- ❌ Attendre plusieurs échecs avant de proposer Playwright codegen, HAR ou capture humaine
- ❌ Coder le scraping à la main avant d'avoir essayé codegen
- ❌ Utiliser `page.query_selector()` pour les éléments qui changent → utiliser `page.locator()`
- ❌ Insister plus de 30 min sur un site niveau 3-4 sans passer à une autre approche
- ❌ Scrapper le DOM si l'API est accessible
- ❌ Payer pour un service scraping sans avoir vérifié que le site est niveau 4-5