# Anti-bot : prix proxies, unblockers et taux de succès (2026)

## Proxies résidentiels

| Provider | Prix/Go | Particularité |
|----------|---------|---------------|
| **Webshare** | 0,99 $/Go | Free tier 1Go + 10 IP datacenter, pool 80M+ IP. Faiblesse : ASN datacenter détecté |
| **IPRoyal** | 1,75 $/Go | **Trafic non-expirant** — idéal pour usage irrégulier |
| **Decodo (ex-Smartproxy)** | ~2 $/Go abo, 3,50 $/Go PAYG | 115M+ IP, 195+ pays, 99,86% success rate annoncé |
| **Bright Data** | 3,50-8,40 $/Go | Plus gros pool (150M+), plus cher |

**Budget typique usage individuel :** 10-25 $/mois

## Unblockers managés

| Provider | $/1000 req | Taux succès | Anti-bot |
|----------|------------|-------------|----------|
| **Scrapfly** | 3,37 $ | 99% overall (benchmark Scrapeway), ~96% Imperva/DD revendiqué | `asp=True`, pas de facturation sur échec, 1000 crédits gratuits |
| **Zyte API** | 0,13-1,27 $ (HTTP) à 1,01-16,08 $ (navigateur) | **93,14%** (benchmark Proxyway déc. 2025, 15 sites protégés) | Pas de facturation sur échec, 5$ free |
| **Firecrawl** | 5 cr/req stealth | **33,69%** à 2 req/s (Proxyway benchmark) | Ne pas utiliser pour anti-bot dur — fait pour LLM-ready |
| **Bright Data WU** | ~3 $/1000 PAYG | 95-98% indépendant | Pay-per-success, mini 499$/mois plan fixe |

## CapSolver pricing (anti CAPTCHA)

| Type | $/1000 |
|------|--------|
| reCAPTCHA v2 | 0,80 $ |
| Cloudflare Turnstile/Challenge | 1,20 $ |
| AWS WAF | 2,00 $ |
| DataDome | 2,50 $ |
| Imperva/reese84 | Support via instance custom (pas de prix public) |

## Sites où même payant ça ne marche pas

- **French Bee** : Imperva reese84 + Amadeus stateful (Flight Offers Search → Price → Create Order). **✅ Résolu** — curl_cffi form + headful Xvfb Playwright contourne Imperva/Reese. Le scraping direct fonctionne, pas besoin d'unblocker.
- **Corsair** : hCaptcha + WAF lourd. CapSolver ne supporte pas le payload spécifique.
- **Tout site Imperva + GDS** en général : ne pas scraper directement, passer par agrégateur.

## ROI par cible

| Cible | Solution | Budget/mois | Gain |
|------|----------|-------------|------|
| YouTube (proxies) | Résidentiel rotatif | 10-25 $ | 0% → fonctionnel |
| Immobilier (Cloudflare/DD) | Web Unlocker | 15-40 $ | +35-45 pts succès |
| Transcription (Groq) | API Groq Whisper Turbo | 1-5 $ | Libère RAM locale |
| Vols (Corsair direct uniquement) | **Abandon** → agrégateur | 0 $ | Évite puits sans fond |

## Sources

- Proxyway Web Scraping API Report (déc. 2025) — benchmark 12 providers × 15 sites protégés
- Scrapeway benchmark Scrapfly (mai 2026)
- CapSolver pricing page (juin 2026)
- Prix vérifiés en juin 2026 — à recouper avant engagement