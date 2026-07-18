# LapubRe — validation gros catalogues avant extraction produits (2026-06-12)

## Quand réutiliser

Pour les projets de monitoring/extraction de catalogues ou prospectus où l'étape suivante serait de parser les produits : ne pas passer à l'extraction produit fine avant d'avoir prouvé l'ingestion complète de plusieurs catalogues récents et volumineux.

## Contrat de validation recommandé

Tester au moins 2–3 catalogues récents avec beaucoup de pages, idéalement des formats différents.

Critères stricts par catalogue :

- `nb_pages` attendu identifié depuis l'API/index.
- Pages DB = pages attendues.
- Fichiers locaux = pages attendues.
- Pas de doublon de numéro de page.
- Chaque asset local existe, taille cohérente, type valide (`%PDF` + EOF pour PDF, JPEG/PNG/WebP pour images).
- Pour les images reconstruites en PDF : PDF final valide et nombre de pages détecté = attendu.
- Manifest d'ingestion par catalogue avec erreurs restantes et retries.
- Run reproductible/idempotent : relance possible sans doublons ni corruption.

Go/no-go : avancer vers l'extraction produits seulement si au moins 2 catalogues passent strictement, et documenter les limites restantes.

## Techniques validées pendant la session

### API publique LAPUB.RE : source de vérité metadata/viewer

Endpoint vérifié live le 2026-06-12 :

```text
GET https://lapub.re/api/prospectus/{uuid}
```

Pour les UUID issus du sitemap, cet endpoint retourne `success`, `data`, `stats`. Dans `data`, champs observés : `id`, `enseigne_id`, `rang_pub`, `nom`, `lien_prospectus`, `date_diffusion`, `date_debut`, `date_fin`, `descriptif_mini`, `nb_pages`, `page_couverture_url` et autres champs selon catalogue.

Règle : ne pas deviner le viewer depuis le HTML public quand cet endpoint répond. Pipeline recommandé : sitemap → UUID → `/api/prospectus/{uuid}` → router selon `lien_prospectus` / type viewer / `nb_pages` → télécharger assets → QA `nb_pages == assets récupérés`.

Exemple vérifié : `7856e1a6-c6ad-48eb-a732-1f317d8552f4` retourne `lien_prospectus=https://cata.lapub.re/prospectus/141` et `nb_pages=3`.

#### Pattern CLI/API-first validé dans le projet LapubRe

Dans `/opt/data/projects/lapub-re`, l’ingestor supporte maintenant une sélection API-first :

```bash
python3 src/lapubre_ingestor.py \
  --discover-api \
  --discover-limit 5 \
  --min-pages 30 \
  --types 'FLIPPING V2,MAGZ' \
  --write-selected artifacts/<run>/selected_api_first.json
```

Puis ingestion :

```bash
python3 src/lapubre_ingestor.py \
  --selected artifacts/<run>/selected_api_first_top3.json \
  --db artifacts/<run>/api-first.sqlite \
  --outdir artifacts/<run>/ingested \
  --types 'FLIPPING V2,MAGZ'
```

Validation réelle 2026-06-12, API-first, 3 catalogues récents FLIPPING V2 :

- ADAMS — `LE CONFORT À PRIX CONFORTABLE` — 38/38 images, PDF 38 pages, 0 erreur.
- ODORALINE — `FETE DES PERES` — 34/34 images, PDF 34 pages, 0 erreur.
- CONFORAMA — `AUX PREMIÈRES LOGES` — 30/30 images, PDF 30 pages, 0 erreur.

Après relance dans la même DB/outdir : `catalogues=3`, `pages=102`, `assets=102`. Le pattern d’upsert/idempotence tient pour ce cas.

Artefacts session : `artifacts/20260612-api-first-validation/qa-api-first-report.md` et `qa-api-first-summary.json`.

### MAGZ / interactive-catalogue : pagination JSON par lot

Le premier endpoint ne retourne pas forcément toutes les pages :

```text
https://preprod.interactive-catalogue.com/view/magazine/{slug}?pagination=1&detail=true&provider=preprod
```

Exemple observé : catalogue Leader Price `NOS ESSENTIELS`, `totalPages=99`, mais :

- `pagination=1` → pages 1–11
- `pagination=2` → pages 12–21
- ...
- `pagination=10` → pages 92–99
- `pagination=11` → 404

Règle : lire `detail.totalPages`, accumuler les `pages` jusqu'à atteindre ce total, puis arrêter. Ne pas supposer que `pagination=1` est complet.

### Next/RSC / FLIPPING V2 : ne pas décoder tout le HTML avec `unicode_escape`

Erreur rencontrée : appliquer `bytes(html, 'utf-8').decode('unicode_escape')` sur tout le HTML corrompt les caractères UTF-8 réels dans les URLs de catalogue.

Symptôme :

```text
DÉFENSEUR → DÃFENSEUR
D’ACHAT → DâACHAT
```

Conséquence : URLs `datas.lapub.re` en 404 alors que les assets existent.

Pattern plus sûr :

```python
text = html.unescape(text)
text = text.replace('\\"', '"').replace('\\/', '/')
```

Puis parser les paires `url` / `pageNumber`. Garder les caractères Unicode intacts et laisser l'étape d'encodage URL percent-encoder le chemin juste avant la requête HTTP.

### Timeouts asset : retry ciblé, pas échec global immédiat

Sur gros catalogues, des timeouts TLS ponctuels peuvent arriver sur 1–2 assets. Dans le cas testé, deux PDFs MAGZ manquants ont été récupérés au premier retry ciblé.

Règles :

- Une erreur page/asset ne doit pas aborter tout le catalogue.
- Enregistrer l'erreur dans un manifest local.
- Commit DB même si certaines pages sont manquantes, avec `local_file=null` pour reprise.
- Relancer uniquement les pages manquantes avec retry/backoff court.
- Le verdict final doit être basé sur la QA après retry, pas sur la première passe brute.

## Exemple de résultats validés

Campagne finale : 3/3 catalogues passés strictement après corrections/retry.

- MAGZ Leader Price — 99/99 pages, 99 fichiers, 2233 assets, 2 timeouts corrigés par retry.
- FLIPPING V2 E.Leclerc — 72/72 images, PDF reconstruit 72 pages, ~38 MB.
- FLIPPING V2 Le Coin des Petits — 66/66 images, PDF reconstruit 66 pages, ~30 MB.

## Piège de séquence projet

Si l'utilisateur demande ou suggère de vérifier la robustesse avant l'extraction produit, il a probablement raison : l'extraction produit fine est prématurée tant que l'ingestion multi-page n'est pas prouvée. Réordonner le plan : validation gros catalogues → rapport go/no-go → seulement ensuite table produits / validation manuelle.
