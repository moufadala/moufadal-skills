# Decision dashboards and recovery after unusable UI

Session lesson: a dashboard can look premium and still fail if it does not help Moufadal decide what to do next. For dashboards that rank opportunities, leads, scrapers, products, properties, flights, or tasks, visual polish is secondary to decision value.

## Acceptance contract for decision dashboards

Every decision dashboard should make these fields explicit before implementation:

- **Priority / rank**: why this item is above another.
- **Provenance**: source link, capture time, extraction method, confidence/trust.
- **Freshness**: last seen / last updated / stale markers.
- **Action**: what Moufadal should do next, not only what the item is.
- **Reason**: concise explanation of why the item matters.
- **Risk / caveat**: missing data, uncertain parse, anti-bot fragility, duplicate risk, price mismatch, etc.

QA should prove usefulness, not just aesthetics:

- Browser render check.
- Console check.
- Screenshot or visual QA.
- If public: public URL check.
- At least one decision walkthrough: from dashboard item → source/proof → recommended action.

## Recovery when user says it is not usable

Do not defend the previous artifact or only tweak colors/cards. Switch back to product semantics:

1. Acknowledge the miss directly.
2. Identify missing decision fields/actions.
3. Preserve or archive the previous artifact.
4. Ship V2 separately or keep rollback path; do not overwrite blindly.
5. Add acceptance criteria that prove the user can decide faster.
6. Re-QA with a real sample item and evidence chain.

Useful response shape:

> Tu as raison: c'est joli mais pas décisionnel. Je garde la V1 comme archive, je refais une V2 qui expose priorité, source, fraîcheur, confiance, raison et prochaine action. Le test d'acceptation sera: en ouvrant une carte, tu sais immédiatement pourquoi elle est prioritaire et quoi faire ensuite.
