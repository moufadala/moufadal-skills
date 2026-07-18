# Pré-recon scraping Réunion — vols + immobilier

Date de validation : 2026-06-03

## Contexte réutilisable

Quand l'utilisateur prépare une veille locale Réunion, ne traiter pas chaque vertical séparément si le besoin est déjà multi-produit. Structurer la pré-recon en deux familles :

1. Vols depuis RUN : prix, routes, compagnies, comparateurs.
2. Locations immobilières 974 : nouvelles annonces, filtres, déduplication, notifications Telegram.

## Vols — périmètre initial RUN

Compagnies à vérifier/compléter :

- Air Austral
- Air Mauritius
- Corsair
- French Bee
- Air France
- IndiGo
- Kenya Airways si Nairobi via MRU est pertinent

Axes :

- RUN → MRU
- RUN → Paris CDG/ORY
- RUN → NBO
- RUN → Inde : MAA, BOM, DEL

Comparateurs utiles : Skyscanner, Google Flights, Kayak/Momondo, Trip.com, Opodo/eDreams, Liligo, Expedia.

## Immobilier — sites location Réunion à inclure

Inclure explicitement :

- SeLoger
- Bien'ici
- Logic-Immo
- Superimmo
- Immo974
- Zimo
- Entreparticuliers
- Locamoi
- Citya
- OFIM
- PAP / PAP Vacances
- FNAIM

Exclure en première passe si l'utilisateur le précise : SIDR.

## Screenshots obligatoires dans une pré-recon Perplexity/browser

Le prompt doit demander des screenshots, pas seulement une analyse textuelle.

Pour les vols :

- homepage ;
- formulaire ouvert ;
- formulaire rempli ;
- résultat ou erreur ;
- état du bouton Search et champs visibles.

Pour l'immobilier :

- recherche `location La Réunion 974` ;
- filtres ouverts : ville, budget, type, pièces, tri ;
- liste d'annonces ;
- page détail annonce ;
- pagination ou infinite scroll ;
- présence d'ID annonce, date, agence, JSON-LD.

Si les images ne peuvent pas être attachées, exiger une description précise de chaque capture attendue : URL, état, champs, labels, boutons, structure, indices DOM/JS.

## Immobilier — méthode sobre

Ordre recommandé :

1. robots.txt, sitemap, RSS, alertes officielles ;
2. HTML paginé + requests/BeautifulSoup ;
3. JSON-LD schema.org dans HTML ;
4. API XHR/fetch via HAR ;
5. Playwright uniquement si rendu JS nécessaire ;
6. pas de fréquence agressive.

Champs minimaux à viser : source_site, source_id, url, title, city, district, property_type, rooms, bedrooms, surface_m2, rent_eur, charges_eur, agency_or_owner, published_at, seen_first_at, seen_last_at, raw_json_path, content_hash.

## Leçon workflow

Quand le périmètre évolue pendant la préparation d'un prompt de pré-recon, patcher immédiatement l'artefact central au lieu de répondre seulement en texte. Vérifier ensuite par recherche de lignes que les nouveaux éléments critiques apparaissent bien : sites ajoutés, exclusions, screenshots obligatoires, schéma de données.