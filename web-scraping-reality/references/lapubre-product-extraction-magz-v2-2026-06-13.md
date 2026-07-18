# LapubRe — extraction produits/prix MAGZ V2 (2026-06-13)

## Pourquoi cette note existe

Session LapubRe où le scraping catalogue était déjà validé, mais l'utilisateur a corrigé la séquence attendue: avant de passer à l'extraction massive, il faut expliquer et prouver la méthode d'extraction produits/prix, les difficultés, les options et les critères de validation.

Leçon principale: **scraper toutes les pages d'un catalogue ≠ extraire des produits/prix fiables**. Pour les brochures, il faut traiter l'association produit ↔ prix ↔ preuve visuelle comme un problème distinct.

## Séquence recommandée pour brochures/catalogues

1. Valider d'abord la récupération complète des catalogues récents/gros:
   - `expected_pages > 0`
   - `downloaded_pages == expected_pages`
   - aucun trou, doublon, fichier illisible.
2. Avant de coder l'extraction massive, livrer un mini-cours/rapport court au décideur:
   - options possibles: API produit, HTML/JSON viewer, OCR/layout, vision LLM;
   - difficultés: prix au kg/litre/dose, remises, prix barrés, blocs multi-produits, association image/prix;
   - critères Go/No-Go mesurables.
3. Commencer par **20 produits candidats validables humainement**, pas par 2000 lignes OCR.
4. Stocker séparément:
   - `product_candidates`: hypothèses machine avec preuve/source/confiance;
   - `products`: uniquement produits validés/corrigés.
5. Ne promouvoir dans `products` que les lignes explicitement `validated` ou `corrected`.

## Pattern MAGZ V2 observé

Sur un catalogue MAGZ Leader Price récent:

- Le JSON/HTML MAGZ contenait des blocs texte riches mais parfois multi-produits.
- Une V1 naïve faisait souvent un candidat par bloc et choisissait le dernier prix: dangereux.
- La V2 doit segmenter autour des prix produits réguliers pour créer un candidat par produit probable.

Correctifs durables:

- Classer `prix en caisse`, `remise immédiate` comme `discount_or_cashback`, jamais comme prix produit choisi.
- Classer `0,06€ la dose`, `0,28€ la capsule`, `Soit le kilo/litre X€` comme `unit_price`, jamais comme prix produit choisi.
- Si un segment ne contient que des prix unitaires/dose, ne pas créer de candidat produit.
- Garder tous les prix détectés dans `prices_json`, mais choisir `chosen_price_cents` seulement parmi les vrais prix produit.

## Validation humaine et DB

Schéma de travail recommandé:

```text
MAGZ JSON/HTML → product_candidates.json/csv/html
              → humain valide/corrige le CSV
              → import CSV
              → products seulement si status = validated/corrected
```

Champs utiles côté candidat:

- `catalogue_id`
- `page_number`
- `source_kind` (`magz_html_segmented`, `ocr_text`, etc.)
- `raw_text`
- `product_name_guess`
- `prices_json`
- `chosen_price_cents`
- `unit_price_cents`
- `crop_path` ou au minimum image de page complète
- `confidence_score`, `confidence_reasons_json`
- `validation_status`

## Preuve visuelle

Dans cette session, les PDFs MAGZ page par page n'avaient pas de calque texte exploitable (`text_len=0`, `spans=0`). Le raccourci PyMuPDF texte/bbox ne marche donc pas toujours.

Approche robuste:

- rendre les PDF page en PNG via PyMuPDF/Pillow dans un venv isolé;
- attacher au moins l'image de page au candidat;
- pour crops précis, étape suivante: parser coordonnées HTML/CSS MAGZ si disponibles ou lancer OCR/layout sur PNG.

## OCR/layout V2 — leçons ajoutées après parallélisation

Quand le catalogue MAGZ n'a pas de calque texte PDF exploitable, une stratégie locale légère peut quand même améliorer la preuve visuelle sans tout confier à un LLM vision:

1. Rendre toutes les pages PDF en PNG avec PyMuPDF/Pillow dans un venv isolé.
2. Tester un OCR à bboxes sur quelques pages avant de l'industrialiser. Pattern validé: `rapidocr-onnxruntime` installé via `uv pip install --python <venv>/bin/python rapidocr-onnxruntime`.
3. Les prix retail sont souvent détectés en morceaux (`19` + `99`, `11` + `49`) plutôt qu'en `19,99€`. Le matching doit donc associer:
   - euros exacts;
   - centimes exacts;
   - proximité géométrique droite/bas;
   - score OCR minimal;
   - puis union des bboxes pour créer un crop élargi.
4. Ne pas forcer les non-matchs OCR: les garder comme signaux QA. Un candidat produit/prix dont le prix choisi n'est pas retrouvé visuellement peut indiquer une confusion `prix produit` vs `prix unité` / `remise` / `texte voisin`.
5. Pour le pack de validation, utiliser deux niveaux de preuve:
   - crop OCR précis autour du prix quand match trouvé;
   - fallback image page complète quand le crop exact manque.

Résultat terrain de référence: sur 20 candidats MAGZ sélectionnés, le rendu complet a donné `99/99` pages PNG sans erreur; RapidOCR a fourni un crop prix précis pour `14/20`; les `6/20` non-matchés ont été conservés en validation manuelle plutôt que masqués.

## HTML/CSS MAGZ — prudence coordonnées

Le HTML MAGZ peut contenir beaucoup d'assets, classes et attributs `data-*`, mais pas forcément de coordonnées simples `left/top/width/height` dans le HTML brut. Ne pas promettre des crops produit via HTML tant que les styles/classes externes n'ont pas été résolus et convertis en bboxes. Utiliser le HTML surtout pour texte/prix candidats; utiliser rendu PNG + OCR/layout pour preuve visuelle.

## Artefacts de référence produits pendant la session

- Code: `/opt/data/projects/lapub-re/src/product_extraction_v1.py`
- Tests: `/opt/data/projects/lapub-re/tests/test_product_extraction_v1.py`
- Pack V2: `/opt/data/artifacts/overnight_lapubre_scrapers_20260613/lapubre_products_v2/`
- Rapport pédagogique: `/opt/data/projects/lapub-re/docs/extraction-produits-prix-mini-cours.md`
- Rapport final V2: `/opt/data/artifacts/overnight_lapubre_scrapers_20260613/lapubre_products_v2/FINAL_PRODUCTS_V2_REPORT.md`
- Pack validation 20: `/opt/data/artifacts/overnight_lapubre_scrapers_20260613/lapubre_products_v2/final_20_review/validation_20_products.html`

Ces chemins sont session-spécifiques; reprendre le pattern, pas les chemins comme vérité permanente.
