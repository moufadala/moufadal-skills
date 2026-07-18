# Pré-recon scraping vols depuis La Réunion (RUN)

Date de validation : 2026-06-03

## Contexte réutilisable

Quand l'objectif est de monitorer des prix de vols depuis La Réunion, ne partir ni d'un seul site ni d'une API payante. Construire d'abord une carte des opérateurs et routes, puis choisir les cibles à capturer par ordre de probabilité de succès.

## Compagnies à inclure depuis RUN

Opérateurs directs observés :

- Air Austral
- Corsair
- Air Mauritius
- French Bee
- Air France
- IndiGo

Routes prioritaires :

- RUN → MRU : Air Austral, Air Mauritius, Corsair
- RUN → CDG : Air Austral, Air France
- RUN → ORY : Corsair, French Bee
- RUN → MAA/Chennai : IndiGo direct, Air Mauritius possible via MRU
- RUN → NBO/Nairobi : probablement Air Mauritius + Kenya Airways via MRU
- RUN → BOM/DEL/Inde : Air Mauritius et/ou partenaires indiens à vérifier

Plateformes de comparaison utiles pour reconnaissance, pas forcément production :

- Skyscanner
- Google Flights
- Kayak/Momondo
- Trip.com
- Opodo/eDreams
- Liligo

## Indices techniques utiles

- Air Mauritius expose des pages SEO/route associées à EveryMundo / airTRFX ; vérifier les appels GraphQL/API autour de `airtrfx` avant de piloter le moteur booking complet.
- Sur un site aérien SPA, capturer le réseau pendant une recherche réelle vaut mieux que deviner le DOM.
- Les pages de formulaire visibles ne prouvent pas que la recherche est faisable : vérifier aussi les URLs directes (`/search`, paramètres type `?fsopen=true`) et les XHR.

## Prompt Perplexity recommandé

Demander une reconnaissance structurée, mais exiger ensuite validation locale par artefacts :

- URL exacte du moteur de recherche
- endpoints XHR/GraphQL probables
- payloads et headers observables ou hypothétiques
- anti-bot/cookie/CAPTCHA
- screenshots ou étapes de reproduction
- difficulté estimée : API directe, Playwright, stealth, proxy, abandon

Ne jamais traiter le rapport Perplexity comme preuve finale : il sert à prioriser les captures HAR/Playwright.

## Discipline spécifique aux sites de vols

Pour chaque compagnie, pousser une piste jusqu'au bout avant d'en ouvrir trois autres :

1. URL directe du moteur de recherche (`/search`, query params, deep links)
2. Screenshot de ce que voit Playwright
3. Remplissage Playwright pur du formulaire minimal
4. Capture XHR/HAR pendant clic Search
5. Replay `curl` ou `requests` d'un appel gagnant
6. Classification : exploitable API / exploitable Playwright / bloqué anti-bot / abandon temporaire

Un essai est incomplet tant qu'il n'a pas produit au moins un artefact : screenshot, HAR, payload, réponse brute, ou script replay.