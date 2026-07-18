# API mobile / NetLog Android en priorité anti-bot — 2026-06-11

## Déclencheur

Pour tout scraping de site protégé par Cloudflare, Imperva, DataDome, Akamai, Bot Fight Mode ou hCaptcha, ne pas commencer par plusieurs variantes Playwright desktop. Chercher d'abord si le parcours mobile expose une API plus simple.

## Ordre de priorité durable

1. **API mobile via NetLog Android** : `chrome://net-export/` avec `Include raw bytes`, puis parcours réel sur le site mobile.
2. **Endpoint JSON desktop** : DevTools Network / HAR / Copy as cURL.
3. **CDP avec navigateur réel authentifié** : profil/cookies humains si nécessaire.
4. **Playwright + proxy résidentiel** : dernier recours, pas première stratégie.

## Procédure utilisateur rapide

Sur Chrome Android :

1. Ouvrir `chrome://net-export/`.
2. Cocher `Include raw bytes`.
3. `Start logging`.
4. Effectuer le parcours complet sur le site mobile : formulaire, recherche, résultats.
5. `Stop logging`.
6. Envoyer le JSON NetLog.

## Exploitation agent

- Parser le NetLog pour URLs, méthodes, headers, payloads et réponses utiles.
- Identifier l'appel gagnant plutôt que reproduire tout le parcours UI.
- Rejouer en `requests`/`curl_cffi` avec headers/cookies minimaux.
- Classer les secrets/cookies NetLog comme sensibles : ne pas les recopier en clair dans prompts, logs ou rapports publics.

## Leçon terrain

Le postmortem 2026-06-11 sur Air Austral et Air Mauritius a montré une perte de temps lorsque la piste API mobile / NetLog Android a été proposée seulement après Playwright, patchright, curl_cffi et proxy résidentiel. Cette piste doit être proposée tôt dès qu'un anti-bot bloque le desktop.