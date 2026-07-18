# ChatGPT Agent prompt pack — vols + immobilier Réunion

## Quand réutiliser

Quand l'utilisateur veut exploiter ChatGPT Agent / navigateur agentique comme pré-recon externe pour débloquer ou durcir des scrapers, notamment sur un périmètre multi-sites Réunion : vols RUN et immobilier location.

## Leçons de session

L'utilisateur a explicitement préféré **deux prompts séparés** plutôt qu'un prompt global unique :

1. un prompt ChatGPT Agent dédié aux vols ;
2. un prompt ChatGPT Agent dédié à l'immobilier ;
3. idéalement livrés en fichiers prêts à coller, voire PDF téléchargeables.

Correction utilisateur importante : ne pas seulement demander « cherche tout ». Il faut **demander le maximum actionnable dans chaque prompt** : navigateur, code source, JS bundles, DevTools/Network/HAR si disponible, Copy-as-cURL, screenshots/descriptions, endpoints XHR/fetch, anti-bot, pagination/complétude, et artefacts exacts à fournir à Hermes. Le prompt doit imposer un contrat de sortie strict pour éviter un rapport joli mais non exploitable.

Le prompt combiné peut exister en secours, mais ne doit pas être recommandé en premier si l'objectif est un rapport exploitable. Le risque d'un prompt global est un rapport superficiel et difficile à traduire en implémentation.

## Forme recommandée du livrable

Produire un dossier d'artefacts avec :

- `00_context_local_verifie.md` : faits locaux déjà vérifiés, séparés des hypothèses ;
- `01_READY_TO_PASTE_prompt_immobilier_agent.md` ;
- `02_READY_TO_PASTE_prompt_vols_agent.md` ;
- `03_READY_TO_PASTE_prompt_combine.md` seulement comme option ;
- `04_contract_sortie.md` : structure obligatoire du rapport ;
- `05_capture_humaine_a_demander.md` : HAR, Copy-as-cURL, NetLog Android, screenshots ;
- PDF téléchargeables séparés si demandé.

## Pattern général de prompt à imposer

Chaque prompt doit commencer par :

> Tu es ChatGPT Agent avec navigateur web. Ta mission est de produire une pré-recon technique maximale pour aider Hermes Agent à construire/durcir des scrapers. Utilise tout ce que ton environnement permet : navigateur réel, inspection visuelle, code source HTML, scripts JS chargés, endpoints XHR/fetch, DevTools/Network/HAR si disponible, Copy-as-cURL si disponible, screenshots ou descriptions précises, observation pagination/filtres/anti-bot. Ne fais pas un rapport générique : donne preuves, URLs, observations concrètes, endpoints, ou les artefacts exacts qu’il faut capturer ensuite.

Puis ajouter :

- contexte local vérifié ;
- périmètre de sources ;
- méthode obligatoire par source ;
- champs à extraire ;
- verdicts autorisés ;
- format de sortie ;
- interdictions anti-hallucination.

## Contrat à imposer à ChatGPT Agent

Pour chaque source, demander explicitement :

1. verdict : `prod-candidate`, `needs-hardening`, `blocked-antibot`, `low-value`, `unknown` ; pour les vols ajouter aussi `indicative` ;
2. ce qui a été réellement observé ;
3. hypothèses séparées des faits ;
4. preuves : URLs, statuts HTTP, fragments de réponse, screenshots décrits, endpoints, code source, HAR si possible ;
5. méthode robuste recommandée : API directe, HAR replay, NetLog Android, CDP profil humain, Playwright, proxy, CapSolver, abandon ;
6. champs à extraire ;
7. pagination / complétude / polling ;
8. anti-bot, coût, risque ;
9. QA minimale et artefacts attendus ;
10. captures à fournir à Hermes ;
11. prochaine action unique qui réduit le plus l'incertitude.

Interdire les endpoints inventés : si aucune réponse brute n'est disponible, l'agent doit écrire `hypothèse à vérifier`.

## Contenu indispensable — vols RUN

Inclure l'état terrain connu avant de demander à l'agent externe :

- Routes prioritaires : RUN ↔ ORY/CDG, RUN ↔ MRU, RUN ↔ DZA/TNR, RUN → Inde éventuellement via hub.
- French Bee : Drupal/Amadeus `Preload.action` / `Override.action`, `ENC` dynamique, profil browser/headful fragile, RUN↔ORY partiellement confirmé.
- Air Austral : succès partiels Amadeus `Override.action` mais Cloudflare/403 sur `/ajaxResa.php`; piste clé `/ajaxResa.php?...method=getCryptData2...`; demander vraie valeur `d=`, cookies/headers, HAR/Copy-as-cURL ou NetLog Android.
- Air Mauritius : prix/cache marketing possibles mais pas live ; UI booking fragile, Imperva/hCaptcha ; priorité NetLog Android/API mobile.
- Kiwi : fallback agrégateur indicatif, contrôle de cohérence contre officiels.
- Corsair : hCaptcha, hors périmètre sauf piste concrète.
- Kayak/Skyscanner/Google Flights : API officielle/partenaire ou low-value ; ne pas scraper UI sans preuve.

### Vols — captures à demander explicitement

- French Bee : HAR complet avec contenu, `Preload.action`, `Override.action`, `ENC`, cookies redacted, screenshots formulaire/prix, Copy-as-cURL.
- Air Austral : HAR complet, appel `/ajaxResa.php?...method=getCryptData2...`, vraie valeur `d=`, réponse JSON brute, URL `Override.action` redacted, screenshots, protocole NetLog si 403.
- Air Mauritius : HAR web si possible, NetLog Android/mitmproxy prioritaire, endpoints `availability/offer/price/fare/search/booking`, screenshots app, version app, marché/devise.
- Agrégateurs : endpoint API/polling, session token, deeplinks/agents, preuve prix/dispo, classification `indicative` si non officiel.

## Contenu indispensable — immobilier Réunion

Inclure l'état terrain connu :

- Bien'ici : prod-candidate, à durcir pagination/schema/QA.
- SeLoger : prod-candidate mais DataDome/CDP/BFF/HAR à clarifier.
- OFIM : source bonus low-value.
- Multi-sources : besoin de séparer succès, 403, scoring, dédup.
- Règles métier : ne pas supprimer pendant stabilisation, stale uniquement si source vue avec succès, exclure locaux/parking/box/coloc par défaut, dédup ville+loyer+surface+pièces.

### Immobilier — sources à couvrir

Demander au moins : Bien’ici, SeLoger, Logic-Immo, Leboncoin, PAP, FNAIM/agences locales, OFIM, LNA/L'Adresse/Orpi/Century 21/Nestenn/Guy Hoquet et agences locales réunionnaises pertinentes.

### Immobilier — captures et preuve à demander explicitement

- `robots.txt`, `sitemap.xml`, flux RSS si présents ;
- URLs de recherche avec paramètres ;
- HTML/code source ;
- JSON-LD/schema.org ;
- XHR/fetch de recherche et détail ;
- pagination (`page`, `offset`, `limit`, `cursor`, infinite scroll, bouton voir plus) ;
- 2–3 pages détail par source candidate ;
- screenshots/descriptions : formulaire, filtres, résultats, détail, erreur/challenge.

## Champs minimaux — immobilier

- `source_site`, `source_id`, `url`, `canonical_url`, `title`, `description_short`, `city`, `district`, `postal_code`, `property_type`, `transaction_type`, `rent_eur`, `charges_eur`, `deposit_eur`, `surface_m2`, `rooms`, `bedrooms`, `floor`, `furnished`, `agency_or_owner`, `agency_name`, `published_at`, `updated_at`, `seen_first_at`, `seen_last_at`, `photos_count`, `latitude`, `longitude`, `raw_json_path`, `raw_html_path`, `content_hash`, `parse_status`, `confidence`.

## Champs minimaux — vols

- `source_site`, `confidence`, `origin_iata`, `destination_iata`, `departure_date`, `return_date`, `adults`, `children`, `infants`, `cabin`, `currency`, `price_total`, `taxes_fees_included`, `fare_family`, `baggage_included`, `segments`, `carrier`, `flight_number`, `departure_time_local`, `arrival_time_local`, `duration`, `stops`, `booking_url`, `deeplink`, `availability_confirmed`, `raw_json_path`, `raw_har_path`, `raw_html_path`, `screenshot_price_path`, `captured_at`, `parse_status`.

## Génération PDF sans dépendances système lourdes

Si `pandoc`/`wkhtmltopdf` ne sont pas installés mais que le sidecar Chromium CDP est disponible, convertir markdown → HTML avec Python `markdown`, puis appeler CDP `Page.printToPDF` via `websockets`.

Détails utiles :

- Sur certaines images Chrome, `/json/new?...` exige la méthode HTTP `PUT`; `GET` renvoie `405 Method Not Allowed`.
- Vérifier le PDF par signature plutôt qu'avec `file` si la commande est absente : début `%PDF-`, fin `%%EOF`, taille non nulle.

## Discipline de vérité

Le rapport ChatGPT Agent est une pré-recon. Hermes doit ensuite vérifier localement chaque endpoint, payload, protection et règle de pagination avec artefact brut avant implémentation.

Quand le rapport revient en PDF : extraire le texte, classer les claims (`confirmé`, `plausible`, `contredit`, `hypothèse`), tester rapidement seulement les endpoints de forte valeur, puis convertir les claims sur-vendus en checklist HAR/Copy-as-cURL/NetLog.