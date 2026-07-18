# Pré-recon RUN vols + immobilier 974 — leçons réutilisables

Date: 2026-06-03

## Contexte

Pré-reconnaissance Perplexity + vérification VPS pour deux familles de scraping:

- prix vols depuis La Réunion `RUN`;
- annonces de location immobilière à La Réunion `974`.

## Leçon principale

Perplexity est utile comme **carte de chasse**, pas comme preuve finale. Ses affirmations doivent être converties en artefacts locaux:

1. `curl`/`requests` bas niveau;
2. HTML/JSON brut archivé;
3. inventaire liens/forms;
4. screenshot si site JS;
5. HAR/Network si formulaire dynamique;
6. replay `curl` seulement après endpoint réel observé.

## Workflow qui a bien marché

1. Faire produire à Perplexity un rapport structuré avec:
   - routes/sites;
   - difficulté estimée;
   - screenshots ou descriptions visuelles;
   - requêtes GitHub;
   - protocole HAR;
   - schéma SQLite/notifications.
2. Extraire le rapport PDF/notes et vérifier s'il est tronqué.
3. Compléter les parties manquantes par OCR de screenshots si l'utilisateur envoie des images.
4. Lancer un probe HTTP local sur les cibles prioritaires.
5. Classer par preuves, pas par intuition.

## Résultats vérifiés localement

### Vols

- `air-austral.com` et `ajaxResa.php?method=getCryptData2&language=FR` → 403 Cloudflare en HTTP direct. Ne pas conclure impossible: passer à Playwright/HAR avec session navigateur.
- `airmauritius.com/flights-from-reunion-to-nairobi` et `/flights-from-reunion-to-india` → 404 mais HTML riche retourné; les URLs SEO Perplexity peuvent être obsolètes. Explorer routes officielles `/fr/reservation-et-gestion/reservation/vol` et horaires.
- `frenchbee.com/fr` → 200, formulaire détecté `frenchbee-amadeus-search-flights-form` avec champs `from`, `to`, `departure_date`, `return_date`, `passengers`, `qsp_travel_type`.
- `flycorsair.com/fr` → 200, domaine `/fr` confirmé; `/fr-fr` probablement mauvais.

### Immobilier

- `ofim.fr/liste-location.html` → meilleur premier scraper: HTML direct, liens annonces, pages catégories location.
- `immo974.com` → formulaire POST `resultat-de-recherche`, champs nombreux, alerte email native probable.
- `zimo.fr/annonces/location` → HTML direct avec annonces/prix, mais agrégateur national: filtrage strict 974 + dédoublonnage nécessaires.
- `locamoi.fr` → homepage Next.js accessible mais URL recherche supposée `/recherche?type=location` a retourné 404; retrouver l'URL via browser/sitemap avant scraping.
- `bienici.com` → app JS légère; endpoint communautaire `realEstateAds.json` à confirmer par GitHub/HAR.

## Requêtes GitHub utiles extraites du rapport

```bash
# Air Austral / Navitaire
gh search code "air-austral booking" --limit 20
gh search code "Navitaire plnext scraping" --limit 20
gh search code "book.air-austral.com" --limit 10

# French Bee
gh search code "frenchbee.com flight search" --limit 20
gh search code "frenchbee API" --limit 20

# Corsair
gh search code "flycorsair.com" --limit 20

# Skyscanner
gh search code "skyscanner flight search api" --limit 20
gh search code "skyscanner conductor fps3" --limit 20
gh search issues "skyscanner playwright" --limit 20

# Amadeus
gh search code "Amadeus flight search payload RUN" --limit 20
gh search code "Amadeus shopping offers" --limit 20

# Immobilier
gh search code "bienici realEstateAds.json" --limit 20
gh search code "seloger scraping" --limit 20
gh search code "immo974 scraping" --limit 10
gh search code "0x6e69636f api-sites-immo" --limit 10
```

## Priorité recommandée après vérification

### Premier livrable immobilier

OFIM location → `requests + BeautifulSoup` → SQLite → notification nouvelles annonces.

### Premiers tests vols

1. French Bee: formulaire HTML détecté, tenter extraction/form/HAR.
2. Corsair: accessible, capturer formulaire et XHR.
3. Air Mauritius: explorer vraie page réservation, pas les URLs SEO obsolètes.
4. Air Austral: Playwright/HAR requis à cause Cloudflare direct.

## Piège à éviter

Ne pas mélanger “rapport Perplexity dit X” et “preuve locale X”. Toujours libeller:

- **Perplexity affirme**;
- **curl local confirme/infirme**;
- **HAR nécessaire**;
- **replay réussi**.
