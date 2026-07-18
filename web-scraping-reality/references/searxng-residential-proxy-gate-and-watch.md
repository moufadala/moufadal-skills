# SearXNG residential proxy gate and silent watch pattern

Use whenever SearXNG participates in research, benchmarking, diagnostics, scraping, query expansion, or proving absence of results.

## Rule

Before any SearXNG use, run a residential/mobile proxy preflight and save the result with the research artifact.

Acceptance for `proxy_status=PASS`:

- direct IP is collected;
- SOCKS proxied IP is collected;
- proxied IP is not equal to direct VPS IP;
- SearXNG service is reachable from the namespace that will use it;
- timestamp, command, and impact statement are recorded.

If the proxy fails, SearXNG output can be retained for debugging but must be marked `non fiable / à rerun` and must not be used as proof that no result exists or that a site is blocked.

## Gate before benchmarks

Wrap long benchmark/research scripts in a gate:

```bash
if ! /opt/data/scripts/searxng_residential_preflight.sh "$RUN_DIR"; then
  echo '{"gate":"BLOCKED","reason":"proxy_status is not PASS"}' > "$RUN_DIR/searxng_benchmark_rerun_gate.json"
  exit 20
fi
exec /opt/data/scripts/deepresearch_v2_fixed_60q_benchmark_20260629.sh
```

## Silent watch pattern

If the proxy depends on an Android phone, avoid noisy polling in Telegram. Use a no-agent cron that:

- runs the preflight periodically;
- writes local JSON while FAIL;
- outputs a Telegram message only when the proxy transitions to PASS or on a real safety issue;
- has a bounded repeat count for campaign windows.

This keeps the chat usable while still allowing a rerun to start once the phone/proxy is back.

## Diagnostic interpretation

- Tailscale status showing an Android node or exit-node label is not enough. The proof is direct-vs-SOCKS IP from the VPS namespace.
- A SOCKS handshake or local listener is not enough. `curl --socks5-hostname 127.0.0.1:1055 https://api.ipify.org` must return an external IP different from the VPS.
- For Playwright/CDP, pass the proxy explicitly to browser launch; environment variables alone can create false negatives.
