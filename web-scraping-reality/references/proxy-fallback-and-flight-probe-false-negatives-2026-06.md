# Proxy fallback + flight probe false negatives (2026-06)

Use this when flight or anti-bot scrapers fail immediately on proxy connection errors, especially after mobile/Tailscale changes.

## Durable lessons

- Treat `ERR_PROXY_CONNECTION_FAILED`, `curl: (7) Failed to connect to 127.0.0.1:1055`, or old `172.16.1.1:1080` failures as **local routing/preflight failures**, not as site anti-bot evidence.
- Do not silently fall back to a retired legacy proxy bridge. If the canonical mobile proxy is `127.0.0.1:1055`, make legacy `1080` opt-in only (for example `HERMES_ENABLE_LEGACY_SOCKS=1`).
- For Playwright scrapers, run a quick TCP preflight on the configured SOCKS endpoint before launch:
  - if reachable: pass `launch(proxy={"server": "socks5://127.0.0.1:1055"})` explicitly;
  - if not reachable and the source can work direct: run direct and write `proxy_status.json` so the artifact explains the fallback;
  - if the source requires mobile egress: mark `blocked-prerequisite`, not `blocked-antibot`.
- For curl/curl_cffi scrapers, never let a dead proxy be the only path unless the source is explicitly marked proxy-required.

## FrenchBee / Amadeus one-way pitfall

FrenchBee's Drupal/Amadeus form uses:

- `search_flights_travel_type="R"` for round-trip / `Aller-Retour`;
- `search_flights_travel_type="O"` for one-way / `Aller simple`.

If `return_date` is empty but the scraper posts `travel_type="R"`, the browser can reach a real FrenchBee/Amadeus error page (`French bee - Erreur`) with text like `La date de retour est incorrecte (10035)`. That is a local payload bug, not an anti-bot block.

For one-way probes, `cheapest_combo` must accept an outbound-only cheapest fare instead of requiring both outbound and return bounds. A successful one-way proof should record `trip_type: one_way`, flight number, fare, price, currency, and artifact directory.

## Air Austral proxy preflight pitfall

If an Air Austral Playwright probe launches with a dead SOCKS proxy, `Page.goto` can fail before touching the site with `net::ERR_PROXY_CONNECTION_FAILED`. Add a proxy preflight and direct fallback when allowed, then include `proxy_status` in the extracted JSON:

```json
{
  "proxy_configured": "socks5://127.0.0.1:1055",
  "proxy_used": false,
  "reason": "unreachable: [Errno 111] Connection refused"
}
```

A direct fallback that returns visible prices is evidence that the previous proxy error was a local false negative.

## Registry discipline

When manually probing disabled fragile sources:

- keep `enabled=false` unless the user explicitly approves production/cron activation;
- add `last_manual_probe` evidence with `ok`, classification, artifact path, and observation;
- update `next_method` to separate technical proof from operational activation policy;
- keep browser-proxy fallback probes skipped when `1055` is down, rather than producing known false negatives.
