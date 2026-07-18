# Réunion immobilier — gate photo 100% annonces actives (2026-06-15)

## Quand utiliser

Utiliser cette référence quand l'utilisateur demande que les annonces immobilières affichées aient toutes une photo exploitable, ou quand un scraper immo doit être durci pour produire `image_url` fiable.

## Principe métier validé

Le critère de livraison n'est pas “toutes les lignes historiques ont une photo”, mais :

- **toutes les annonces actives / présentées ont `image_url`** ;
- une annonce sans photo publique récupérable est **désactivée réversiblement**, jamais supprimée ;
- la DB est sauvegardée avant le gate ;
- le rapport doit distinguer `active_with_image`, `active_missing_image`, `inactive_missing_image`.

Ce choix évite de présenter des annonces incomplètes tout en gardant la traçabilité et la possibilité de réactiver si une photo est récupérée plus tard.

## Pipeline recommandé

1. Inventaire DB par source : total actif, avec image, sans image.
2. Dry-run par source avec artefacts bruts horodatés.
3. Enrichir les scrapers avec extraction image multi-stratégies.
4. Valider syntaxe sans dépendre de `__pycache__` si les permissions bloquent : `ast.parse(open(path).read())` ou `PYTHONDONTWRITEBYTECODE=1`.
5. Écrire/mettre à jour les lignes avec `image_url`.
6. Générer un rapport coverage JSON/Markdown.
7. Sauvegarder la DB.
8. Désactiver réversiblement les annonces actives encore sans image.
9. Vérifier par SQL : `active_missing_image == 0`.

## Extraction image robuste

Chercher dans cet ordre :

- meta `og:image`, `twitter:image` ;
- JSON-LD `image` si présent ;
- `img.currentSrc`, `src`, `data-src`, `data-original`, autres lazy attrs ;
- `srcset` / `source[srcset]`, prendre la première URL exploitable ou la plus grande si facile ;
- fallback regex sur HTML pour URLs `.jpg/.jpeg/.png/.webp` ;
- normalisation URL relative avec base page/listing.

Toujours filtrer les faux positifs avant de compter une photo :

- logos, sprites, favicons ;
- placeholders : `placeholder`, `nophoto`, `blank`, `blank-1x1` ;
- avatars/agences/pro : `/pro/photos/`, `/images/agences/` ;
- assets layout : `jumbotron`, `no_bien` ;
- diagnostics/DPE : `getDpe`, `cons-*`.

## Leçons source par source Réunion

### SeLoger

- CDP/DOM peut fournir les cards même quand HTTP direct est protégé.
- Les cards `[id^="classified-card-"]` peuvent contenir des images en thumbnail `mms.seloger.com?...&h=50`.
- Pour UI, normaliser vers haute résolution : remplacer ou ajouter `h=800`.
- Vérifier au moins un échantillon HTTP 200 `image/jpeg` sur `h=800` avant d'importer.
- Ne pas confondre “items scrapés” et “lignes importées” : doublons/IDs peuvent faire 269 scrapés mais 268 upsertés.

### Domimmo

- Les pages détail peuvent être SPA/quasi vides au fetch.
- Parser les listings `<li class="list__ul__li">` et extraire l'image depuis la carte.
- Certaines cartes exposent volontairement `nophoto`; ces annonces doivent être désactivées si elles resteraient actives sans autre image.

### OFIM RSS

- Le flux RSS peut ne pas contenir l'image.
- Visiter la page détail OFIM pour extraire `og:image`/images de page.

### FNAIM

- Attention aux faux positifs : `jumbotron-detail.jpg`, `no_bien`, `/images/agences/`, `getDpe/cons-*`.
- Les vraies photos sont souvent sous `/images/biens/.../original/...jpg`.

### Zimo

- Certaines images CDN (`img.e-xiste.com`) peuvent renvoyer 403 sans `Referer`.
- Tester avec `Referer: https://www.zimo.fr/` ; si la future UI affiche depuis un autre domaine, prévoir un proxy image ou serveur qui ajoute le referer.

### Superimmo

- Si HTTP direct renvoie 503 et le navigateur montre “Prouvez que vous êtes un humain” / hCaptcha, classer `blocked-antibot`.
- Ne pas compter ses anciennes annonces comme actives si elles n'ont pas d'image.
- Une intégration CapSolver/profil humain/proxy résidentiel est une branche séparée ; ne pas masquer le blocage par des placeholders.

## Rapport final attendu à l'utilisateur

Format compact :

- verdict d'abord : `0 annonce active sans photo` ;
- couverture par source `source: with_image/total` ;
- nombre de lignes désactivées réversiblement ;
- blocages non résolus (ex. Superimmo hCaptcha) ;
- chemins artefacts : backup DB, report JSON/Markdown, raw source run.

Ne pas dire “tout l'historique a des photos” si des lignes inactives sans image subsistent. Dire précisément : “toutes les annonces actives/présentées ont une photo”.
