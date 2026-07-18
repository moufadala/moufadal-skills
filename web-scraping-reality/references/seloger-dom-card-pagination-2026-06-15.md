# SeLoger Réunion — DOM card pagination beats text fallback (2026-06-15)

## Trigger

Use this when SeLoger loads in CDP/Playwright but the extractor returns implausible prices/surfaces, e.g. `9m² | 2100€`, `61050€`, `272200€`, or counts only visible text candidates.

## Durable lesson

For SeLoger SERP pages, do **not** promote a global text fallback as production. The reliable path observed for La Réunion rentals is:

1. Load the classified-search URL in existing CDP/Playwright browser.
2. Remove cookie/consent overlays (`usercentrics-root`, Didomi/OneTrust patterns) before card extraction and pagination clicks.
3. Extract real listing cards via DOM selector `[id^="classified-card-"]`.
4. For each card, preserve:
   - `id` from `classified-card-*`
   - first SeLoger detail URL in the card
   - full `innerText` for parsing/debug
   - `prix`, `surface`, `nb_pieces`, `nb_chambres`, `type_bien`
5. Paginate via buttons whose `aria-label` contains `à la page N`; collect each page and dedupe by card id.
6. QA-gate before activation: at least 10 normalized cards with URL + price + surface, and reject impossible price/surface combos.

## Price parsing pitfall

SeLoger cards often begin with a gallery counter before the price:

```text
1 / 13
960 € /mois
```

Flattened regexes can parse this as `13960`. Also French thousands separators can be narrow NBSP (`\u202f`) or NBSP (`\xa0`):

```text
1 345 € /mois
2 200 € /mois
```

Parse **line by line**, prefer the line containing `€`, then remove `space`, `NBSP`, and `narrow NBSP` from the matched number immediately before `€`.

Known-good examples:

- `1 / 13\n960 € /mois` → `960`
- `1 / 18\n2 200 € /mois` → `2200`
- `Nouveau\n1 050 € /mois` → `1050`
- `1 / 7\n1 345 € /mois` → `1345`

## Smoke-run contract

For registry runners, make scrapers print one final machine-readable JSON line after human logs:

```json
{"ok": true, "source": "seloger_cdp_reunion_rentals", "total": 270, "with_price": 270, "artifact": "/path/to/results.json"}
```

If the smoke runner also sees Python dict logs such as `{'clicked': True}`, its stdout JSON extractor should prefer the **last valid JSON line** before trying to parse from the first `{` in the output.

## Verified artefact pattern

A good SeLoger validation should report roughly:

- pages clicked with 30 cards/page;
- total listings around the visible site count;
- all/most listings with price;
- normalized sample showing plausible values like `Maison 148m² — 2100€`, not fused text numbers;
- registry classification `prod-candidate` only after smoke runner parses the final JSON line.
