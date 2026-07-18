# Scrapling — évaluation ciblée pour scrapers existants (2026-07-06)

## Contexte

Moufadal a demandé si l'article Korben sur Scrapling pouvait améliorer les scrapers actuels : immobilier Réunion, vols RUN, et lapub.re.

Sources consultées pendant la session :
- Article Korben `scrapling-scraper-python-auto-repare`.
- GitHub `D4Vinci/Scrapling` : ~68k stars, BSD-3-Clause, version récente `0.4.10`.
- PyPI `scrapling 0.4.10` : Python >=3.10, statut beta, extras `fetchers`, `ai`, `shell`, `all`.
- Docs Scrapling : fetchers `Fetcher`, `DynamicFetcher`, `StealthyFetcher`; parser HTML; adaptive désactivé par défaut; response expose status/cookies/headers/body/captured_xhr.

## Règle de décision durable

Ne pas migrer un scraper vers Scrapling parce que Scrapling est nouveau ou promet "self-healing". Classer par type de douleur :

```text
API JSON/GraphQL stable -> ne pas migrer
RSS/XML stable -> ne pas migrer le cœur; éventuellement parser les pages détail HTML
HTML regex fragile -> candidat fort à pilote Scrapling adaptive selectors
Playwright/anti-bot bloqué -> candidat à benchmark StealthyFetcher, sans promesse
Chaîne déjà validée et très spécifique -> éviter la migration, risque > gain
```

## Verdict par famille RUN

| Famille | État actuel observé | Verdict Scrapling |
|---|---|---|
| Bien'ici immo | API JSON directe `realEstateAds.json` | Ne pas migrer |
| OFIM immo | RSS XML + pages détail HTML regex/meta | Pilote secondaire sur détail HTML uniquement |
| Immo multi-sources | beaucoup de regex HTML, timeout récent observé | Pilote #1 |
| SeLoger CDP | CDP/Playwright + DataDome/HTML | À considérer seulement après source-health, pas premier pilote |
| Kiwi vols | GraphQL direct replay | Ne pas migrer |
| French Bee vols | `curl_cffi` Drupal -> Amadeus Override -> Chromium headful; chemin déjà validé | Ne pas migrer |
| Air Austral/Air Mauritius | anti-bot/Playwright fragile | Pilote #2 avec StealthyFetcher + proxy explicite, benchmark obligatoire |
| lapub.re API/MAGZ | sitemap/API prospectus/MAGZ payload; tests locaux OK | Ne pas migrer |
| lapub.re FLIPPING V2 | regex sur HTML Next/RSC pour URLs `datas.lapub.re` | Pilote secondaire si regex casse |

## Exemples avant/après utiles

### HTML regex immo -> selectors adaptatifs

Avant :

```python
arts = re.findall(r'<article>(.*?)</article>', text, re.I | re.S)
price = re.search(r'<div class=["\\']price-result["\\'][^>]*>\\s*<b>\\s*([^<]+)', a)
url = re.search(r'href=["\\']([^"\\']*/annonce/locations/[^"\\']+)["\\']', a)
```

Après pilote Scrapling :

```python
from scrapling.fetchers import Fetcher

Fetcher.adaptive = True
page = Fetcher.get(url, selector_config={"adaptive": True})
cards = page.css("article", auto_save=True)
for card in cards:
    title = card.css("h2::text").get()
    price = card.find_by_regex(r"\d[\d\s.,]*\s*€")
    link = card.css("a[href*='/annonce/locations/']::attr(href)").get()
```

Mesurer : nombre d'annonces, champs remplis, durée, erreurs, diff avec ancien parser, et comportement si une classe CSS change.

### Anti-bot vols -> benchmark, pas promesse

```python
from scrapling.fetchers import StealthyFetcher

page = StealthyFetcher.fetch(target_url, headless=True, network_idle=True)
prices = page.find_by_regex(r"à partir de\s*€[\d\s.,]+", first_match=False)
```

À tester avec le proxy résidentiel/mobile explicitement transmis si le chemin existant l'exige. Verdict seulement avec artefacts : status, URL finale, screenshot/HTML, prix extraits, temps, nombre de succès/échecs.

## Gains réalistes

- Maintenance : gain fort là où le code a beaucoup de regex HTML et peu d'API stable.
- Robustesse DOM : gain possible via `auto_save=True` puis `adaptive=True` quand le DOM change.
- Performance parsing : gain seulement si on remplace BeautifulSoup/regex lourdes; pas de gain notable face à API JSON/GraphQL.
- Anti-bot : possible amélioration avec `StealthyFetcher`, mais ce n'est pas un bypass garanti pour Akamai/Imperva/DataDome/Cloudflare sévère.

## Risques / garde-fous

- PyPI indique encore un statut beta : pinner la version et garder l'ancien scraper en fallback.
- `scrapling[fetchers]` + `scrapling install` peut télécharger navigateurs et dépendances; faire en sandbox/venv, pas directement dans un cron prod.
- L'adaptive stocke de l'état : choisir un dossier de stockage par source/projet, versionner ou sauvegarder si nécessaire.
- Ne jamais remplacer une source API stable par un browser/fetcher plus lourd.
- Pour une source critique déjà validée (French Bee), la migration doit être rejetée sauf preuve chiffrée supérieure.

## Contrat de pilote recommandé

1. Pilote #1 : une sous-source de `realestate_multi_sources_scraper.py`.
2. Produire un comparatif ancien vs Scrapling : `items`, `fields_non_null`, `duration_s`, `errors`, `raw_artifacts`.
3. Ne pas écrire en DB au premier run; JSON artefact only.
4. Si PASS, ajouter fallback : ancien parser si Scrapling échoue ou retourne trop peu d'items.
5. Seulement ensuite envisager OFIM détail ou lapub FLIPPING V2.
