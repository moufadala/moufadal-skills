# Flight aggregator vs official coherence campaigns

Use when the user asks whether aggregator prices are trustworthy compared with airline official sites.

## User-specific reporting rule

The user dislikes long narrative reports. Default output must be compact but complete:
- route/date/source;
- price official vs aggregator;
- delta in EUR and %;
- same flight? same time? same airline?;
- verdict: `exact/live`, `probably live`, `indicative`, `non-conclusive`.
Put raw details in artifacts, not in the chat.

## Method

1. Do not stop at one route or one date. Build a small campaign:
   - 2–4 routes per official airline;
   - 2–3 departure periods;
   - one-way and round-trip explicitly separated.
2. For Air Austral, prioritize RUN routes such as DZA, TNR, MRU, CDG when relevant.
3. For French Bee, prioritize RUN↔ORY/Paris; do not assume it applies to Mayotte/Madagascar.
4. Exclude any official airline source that has not been validated end-to-end. If it appears inside aggregators, label it as an observed aggregator offer only, not a source of truth.
5. Aggregator extraction must go beyond headline minimum price when possible:
   - all visible offers, not just cheapest;
   - airline, flight number, schedule, duration;
   - direct vs stops and stop airports;
   - fare family/cabin/baggage if exposed;
   - booking URL or provider;
   - timestamp and source URL.
6. Distinguish price types:
   - `official live selectable`: price from airline booking flow;
   - `aggregator live offer`: concrete itinerary/bookable result;
   - `indicative/from-price`: route page, calendar average, static “à partir de”;
   - `failed-local-tooling`: browser crash/screenshot timeout, not site block;
   - `blocked-site`: CAPTCHA/403/robot/Imperva/etc.
7. Never call a result simply “coherent”. Always compute or state:
   - delta EUR;
   - delta % when comparable;
   - whether same flight/time/airline;
   - whether comparison is one-way vs one-way or round-trip vs round-trip.
8. If comparing aggregator one-way against official round-trip, say it is not directly comparable and only use it as an order-of-magnitude signal.

## Compact output template

```text
Route DATE
- Official Air X: 248.20€ — UU276 15:50→17:00 direct
- Kayak: 288€ — same UU276/time — delta +39.80€ (+16.0%) — probably live
- Trip.com: from 226€ — same route/time shown — indicative/from-price
Verdict: Kayak reliable on this sample; Trip.com useful for orientation only.
```

## Campaign conclusion format

End with:
- sources to use as truth;
- sources for monitoring;
- sources only indicative;
- failed/non-conclusive tests and exact reason;
- next best test.
