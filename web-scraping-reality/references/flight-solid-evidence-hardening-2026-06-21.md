# Flight scraper hardening — evidence solide avant bilan

Contexte: pendant une consolidation de scrapers vols RUN, un premier bilan multi-source était trop faible: mélange de probes HTTP anti-bot, faux positif prix (`Erreur 500` → regex `eur 500`), scripts locaux cassés, et seulement quelques vrais résultats. Correction utilisateur: “continue, il n’y a rien de solide”.

## Règle de sortie renforcée

Pour déclarer une source vols “solide”, exiger au moins un de ces artefacts:

- `result.json` / `summary.json` structuré avec prix, route, dates, passagers, segments/vols, compagnie, et idéalement booking URL;
- matrice fonctionnelle avec plusieurs cas terminés et classification `price-found`, pas seulement une page chargée;
- blocage prouvé par contenu brut/screenshot/log réseau (`captcha`, `Access denied`, 403, challenge), séparé des bugs locaux.

Ne pas appeler “solide”:

- un prix détecté par regex sans validation sémantique;
- un `exit_code=0` si le JSON dit `ok=false` ou `prices=[]`;
- une source testée sur une seule route/date adulte;
- un runner qui échoue à cause d’un template, chemin, venv, profil Chrome, screenshot, ou parser local.

## Pattern de durcissement appliqué

1. Séparer le rapport “inventaire large” du rapport “preuves solides uniquement”.
2. Relire les artefacts complets, pas seulement `SUMMARY.json` ou `stdout_tail`.
3. Corriger les faux positifs explicitement:
   - exemple: Corsair `Erreur 500` ne doit pas devenir `eur 500`.
4. Convertir `bug-local` en action de réparation avant de conclure:
   - si un script pointe vers un ancien template absent, chercher le template maintenu;
   - patcher le script;
   - relancer un smoke réel immédiatement.
5. Quand une source agrégateur produit de vrais JSON, lancer une mini-matrice ciblée:
   - plusieurs profils passagers;
   - plusieurs dates;
   - mêmes axes fonctionnels;
   - produire `SUMMARY_SOLID.json` + `REPORT_SOLID.md`.
6. Dans le message utilisateur, dire clairement:
   - “solide maintenant”;
   - “non solide / à ne pas vendre”;
   - “encore en cours”.

## Exemple Kiwi RUN⇄Paris

Kiwi GraphQL A/R est devenu solide seulement après un run structuré:

- profils: `1ADT+0CHD`, `2ADT+2CHD`, `2ADT+3CHD`;
- 4 dates par profil;
- `12/12` dates OK;
- prix total, prix par personne, segments aller/retour, vols French Bee, booking URLs;
- artefacts `summary.json`, `report.md`, `SUMMARY_SOLID.json`.

Kiwi direct one-way était initialement `bug-local` car un script pointait vers un ancien template. Le fix durable n’est pas “Kiwi direct marche/ne marche pas”, mais:

- préférer le template maintenu `artifacts/kiwi-direct-replay/latest_template/request.json`;
- supporter la forme courante `{url, method, headers, post_data}` et les anciennes captures `{responses:[...]}`;
- relancer un smoke réel avec IDs Kiwi canoniques (`AutonomousTerritory:RE`, `City:paris_fr`);
- vérifier que l’API retourne `itineraries_count_api`, `offers`, segments et booking URL.

## Format de bilan compact recommandé

- `Source — statut — preuve`
- `Couverture`: nombre cas OK / testés, axes couverts
- `Meilleur prix`: prix, route, dates, passagers, compagnie, vols
- `Artefact`: chemin du rapport/summary
- `Limite`: ce qui n’est pas encore prouvé

Éviter les longs récits défensifs quand l’utilisateur signale que rien n’est solide. Répondre par action: patch, relance ciblée, rapport solid-only.
