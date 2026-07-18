# Découverte d'APIs via l'analyse de fichiers JavaScript

Cette méthode est cruciale lorsque les sites web dynamiques (Single Page Applications, SPAs) ne révèlent pas leurs données via le HTML initial statique, mais chargent le contenu via des appels réseau asynchrones déclenchés par JavaScript.

## Processus d'analyse

1.  **Collecte des fichiers JavaScript :**
    *   Utiliser Playwright (ou un outil similaire) pour naviguer vers la page cible (ex: page de recherche de vols, résultats d'annonces).
    *   Capturer tous les appels réseau effectués pendant le chargement de la page et l'interaction initiale. Les fichiers `.js` sont souvent chargés via des balises `<script src="...">` dans le HTML, ou référencés dans les réponses XHR.
    *   Identifier et télécharger les fichiers JavaScript potentiellement pertinents (ceux qui semblent liés à la logique applicative, aux requêtes réseau, ou qui sont volumineux).

2.  **Extraction des points d'intérêt dans le code JS :**
    *   Il s'agit généralement d'analyser des fichiers minifiés ou obfusqués, donc l'objectif est de rechercher des **patterns textuels** révélateurs.
    *   **Termes clés à rechercher :**
        *   `API`, `fetch`, `axios`, `XMLHttpRequest`, `ajax`, `request`
        *   Noms de frameworks/librairies : `amadeus`, `travelport`, `react`, `vue`, `angular`, `jquery` (pour détecter les interactions)
        *   Endpoints courants : `departure`, `arrival`, `prices`, `booking`, `search`, `destination`, `origin`, `flight`, `availability`, `redirect`, `data`, `json`, `config`, `api/`
        *   Schémas d'URL : `/vols`, `/annonces`, `/location`, `/realEstateAds.json`, `https://.../.json`, `/api/...`
        *   Paramètres de requête : `tripType`, `date`, `adult`, `child`, `infant`, `promoCode`, `Class`, `iata`, `city`, `propertyType`, `rent`.
    *   Utiliser des outils comme `grep` ou la fonction `search_files` avec des patterns regex sur le contenu des fichiers JS téléchargés.

3.  **Interprétation des résultats :**
    *   Analyser les chaînes de caractères trouvées. Les chemins relatifs (ex: `/departure.json`) sont souvent combinés avec une URL de base.
    *   Identifier les fonctions JavaScript qui semblent orchestrer ces appels (ex: `runBookAFlight`, `fetchPrices`).
    *   Repérer les objets ou structures de données qui correspondent aux paramètres de recherche (ex: objets contenant `origin`, `destination`, `dateFrom`, `adults`).
    *   Dans les fichiers JS volumineux, les `webpackChunk` ou autres bundlers peuvent séparer le code. Cherchez les fichiers qui contiennent un grand nombre de ces termes clés ou qui semblent être des modules principaux.

4.  **Tentative de Replay API (si des endpoints sont trouvés) :**
    *   Une fois des URLs d'API potentielles identifiées, tenter d'appeler ces endpoints directement via `curl` ou un script Python (`requests`, `urllib`) en mimant la requête (headers, méthode POST/GET, payload).
    *   Si l'appel échoue (400, 500, protection), il faudra peut-être analyser plus finement les appels réseau capturés par Playwright pour comprendre les headers exacts, les cookies, ou les payloads nécessaires.

## Exemple : French Bee et Air Austral

*   **French Bee :** L'analyse de `frenchbee_fr.html` et des JS associés a révélé des scripts Amadeus et des appels potentiels comme `/departure.json`, `/prices/roundtrip.json`. Ces pistes suggèrent que, malgré une page dynamique, une interaction API pourrait être possible.
*   **Air Austral :** L'analyse JS (`410.82d19ece.js`, `869.8074d47d.js`) a révélé des endpoints comme `/departure.json`, `/prices/roundtrip.json`, etc., ainsi que des termes comme `runBookAFlight`, `departureDate`, `origin`, `destination`, `tripType`. Cela confirme une API sous-jacente, bien que des protections (Cloudflare) et des erreurs serveur (500) aient empêché le replay direct.

## Précautions

*   Les fichiers JS peuvent être très volumineux et obfusqués. La recherche par patterns textuels est la méthode la plus efficace.
*   Les noms de fonctions et d'endpoints peuvent changer. Ce qui fonctionne aujourd'hui peut nécessiter une adaptation demain.
*   L'identification d'une API ne garantit pas son accessibilité ou sa stabilité.

Cette méthode est particulièrement utile pour les sites utilisant des frameworks modernes (React, Vue, Angular) et des chargements de données asynchrones.
