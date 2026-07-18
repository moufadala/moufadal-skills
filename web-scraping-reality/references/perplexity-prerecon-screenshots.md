# Perplexity pré-recon — exiger des screenshots utiles

Dernière validation : 2026-06-03

## Quand utiliser

Quand l'utilisateur veut utiliser Perplexity/Comet comme éclaireur avant de coder un scraper, surtout sur plusieurs sites (vols, immobilier, comparateurs, portails locaux).

## Leçon

Un rapport Perplexity purement textuel est insuffisant pour décider d'une stratégie de scraping. Demander explicitement des screenshots ou, si Perplexity ne peut pas les joindre, des descriptions visuelles structurées.

## Checklist screenshots à mettre dans le prompt

Pour chaque site prioritaire :

- homepage ou landing de recherche ;
- formulaire ouvert avec champs/filtres visibles ;
- état après remplissage d'une recherche test ;
- page résultats ou page erreur ;
- pagination ou infinite scroll ;
- bannière consentement/captcha/anti-bot ;
- détail d'une annonce ou d'un résultat ;
- labels exacts des champs, texte des boutons, état disabled/enabled ;
- indices DOM/JS visibles si disponibles.

## Immobilier — champs visuels importants

Pour les sites de location :

- recherche `location La Réunion 974` ;
- filtres ville, budget, type de bien, pièces, surface, tri nouveauté ;
- liste d'annonces ;
- page détail annonce ;
- présence d'un ID annonce, agence, date publication/mise à jour ;
- structure de l'URL et pagination.

## Rappel discipline

Perplexity fournit des hypothèses, pas une preuve. Toute conclusion doit ensuite être validée localement par artifact reproductible : screenshot, HTML brut, HAR, curl, raw JSON, replay script.
