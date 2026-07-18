# Airline official family fare search — RUN ⇄ Paris pattern (2026-06)

## When to use

Use this when the user asks for flight prices for a family/group and explicitly prefers **compagnies aériennes / official airline sites** over aggregators. Aggregators are still useful for broad date discovery, but the final recommendation should prioritize official airline evidence when available.

## Key lesson

For family travel, do **not** stop at Kiwi/aggregator results. Aggregators can mix airports/airlines and add booking volatility. The better workflow is:

1. Use an aggregator scan to find promising date windows quickly.
2. Re-check the best windows on official airline sites.
3. Rank official direct airline fares first if they are comparable or cheaper.
4. Keep aggregator offers as benchmark/fallback, clearly labeled OTA/mixed-airport if applicable.

Concrete session result: Kiwi found 6–20 July RUN→CDG + ORY→RUN at ~€4,332 for 2 adults + 3 children, but French Bee official later found a cleaner RUN⇄ORY 14–28 July fare at **€4,194.50**, so the official result became the recommendation.

## French Bee official pattern

Existing solver supports family passenger mix:

```bash
python3 /opt/data/scripts/frenchbee_solver.py \
  --origin RUN --destination ORY \
  --depart-date DD/MM/YYYY --return-date DD/MM/YYYY \
  --adults 2 --children 3 --infants 0 \
  --render-timeout 180000 --extra-wait 45000 --pretty
```

Important pitfalls:

- Run French Bee official searches **sequentially**, not in parallel, unless the script is changed to use a unique browser profile/display per task. Parallel runs can fail with Chromium persistent profile collision: `Opening in existing browser session`.
- The price extracted by `cheapest_combo` is the total for the passenger mix requested, not a per-adult fare, because the submitted form includes `search_flights_passenger_ADT`, `CHD`, `INF`.
- Label baggage carefully. `BEE LIGHT+` / official fare name is evidence; included baggage still needs final booking-page confirmation before payment.

## Air Austral official family pattern

The old Air Austral checkers were 1 adult only. For family checks, the backend accepted parameters of this shape:

```text
np=5
uu=1
tv=R
cl=LOISIRS
dep1=RUN
arr1=CDG
dep2=CDG
arr2=RUN
date_dep=YYYY-MM-DD
date_ret=YYYY-MM-DD
tp_1=ADT hi_1=FALSE
tp_2=ADT hi_2=FALSE
tp_3=CHD hi_3=FALSE
tp_4=CHD hi_4=FALSE
tp_5=CHD hi_5=FALSE
```

Endpoint used from page context after loading homepage cookies:

```text
https://www.air-austral.com/ajaxResa.php?method=getCryptData2&language=FR&tm=1&d=RUN&a=CDG
```

Then submit returned `fin_url` fields to returned `url` (Amadeus `plnext/Override.action`).

Air Austral page text may explicitly say:

> Les prix sont pour l'ensemble des passagers et taxes incluses

So, when this text appears, treat displayed `à partir de €...` amounts as total-family fare candidates for the requested passenger mix, not per-person amounts.

Parsing pitfall: Air Austral rendered text can normalize `€1,968,10` or `€1.968.10` inconsistently. Parse by treating the **last separator followed by two digits** as the decimal separator and stripping earlier separators as thousands separators.

## Ranking output for this user

For this user, keep the final answer compact:

- verdict first: best official airline price and dates;
- then direct alternatives;
- then aggregator fallback only if relevant;
- call out airport mismatch explicitly (`CDG` vs `ORY`);
- state bagage/final-payment caveat without over-explaining.

Recommended wording:

```text
Meilleur compagnie officielle trouvé: French Bee officiel, RUN⇄ORY, 14→28 juillet, 2 adultes + 3 enfants, total €X. C'est meilleur/propre que Kiwi car même aéroport et réservation compagnie directe. Bagages à vérifier avant paiement.
```

## Evidence discipline

Save:

- official stdout JSON;
- `08_output.json` / rendered page text for French Bee;
- Air Austral `params.json`, `getcrypt_response.json`, `result_text.txt`, `extracted.json`;
- a concise Markdown report comparing official vs aggregator.

Do not present aggregator as final truth when official evidence exists and is cheaper/cleaner.