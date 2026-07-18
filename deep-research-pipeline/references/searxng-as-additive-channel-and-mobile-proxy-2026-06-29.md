# SearXNG as an additive DeepResearch channel + mobile proxy/high-throughput lesson

## User correction

Moufadal corrected the framing: for DeepResearch, SearXNG should be a **complementary broadening channel**, not merely a fallback when other search providers fail.

Practical implication: do not report “SearXNG works” as a binary fallback status. Measure whether it adds unique sources/domains and which upstream engines are healthy. Preserve candidates/snippets/metadata where useful, but do not keep CAPTCHA/noisy engines in the default high-throughput path just to inflate apparent coverage.

## Canonical runtime path

Use Docker DNS from containers/jobs whenever possible:

```text
http://searxng:8080/search
```

The host-mapped endpoint may exist, but `127.0.0.1:8888` can be a namespace false negative during Hermes/containerized runs or immediately after restarts. Treat Docker DNS as canonical for DeepResearch scripts and cron jobs.

## Mobile proxy pattern

On 2026-06-29, SearXNG was reachable via Docker (`searxng:8080`) but several upstream engines were blocked/degraded from the VPS datacenter IP. A Tailscale Android/mobile exit node was re-enabled without globally routing the VPS:

- Tailscale userspace SOCKS: `127.0.0.1:1055`
- direct VPS IP observed in that run: `148.230.103.174`
- mobile/proxy IP observed in that run: `80.12.253.192`

SearXNG's container lacked direct SOCKS support for the running Python/http stack, so a Docker-network-only HTTP proxy bridge was used:

```bash
python3 /opt/data/scripts/http_proxy_via_socks.py 172.16.1.4 1056 127.0.0.1 1055
```

Then SearXNG `outgoing.proxies` was configured:

```yaml
outgoing:
  proxies:
    http:
      - http://hermes-gateway:1056
    https:
      - http://hermes-gateway:1056
```

See the detailed operational recipe in the `scraping-health` skill reference:

- `references/searxng-tailscale-mobile-proxy-bridge.md`

## High-throughput optimization lesson

The later 2026-06-29 optimization showed that “more engines” was actively worse for DeepResearch benchmark/night runs. Some engines worked once but generated CAPTCHA, `403`, parse errors, or `unresponsive_engines` under repeated queries.

Durable defaults added to `/opt/data/scripts/deep_research_v2.py`:

```text
DEEP_RESEARCH_SEARXNG_PROFILE=balanced  # default
```

Profiles:

- `fast`: `so,gh,hn,ddg,mwm`, max 6 expanded queries.
- `balanced`: `so,gh,hn,arx,ddg,oa,mwm,gl`, max 9 expanded queries.
- `max`: `so,gh,hn,arx,gos,ddg,oa,mwm,cr,gl,pub`, max 12 expanded queries.

Manual overrides:

```bash
DEEP_RESEARCH_SEARXNG_PROFILE=max /opt/data/scripts/deep_research_v2.py "question" --channels searxng
DEEP_RESEARCH_SEARXNG_BANGS=gh,hn,arx,ddg /opt/data/scripts/deep_research_v2.py "question" --channels searxng
DEEP_RESEARCH_SEARXNG_REDDIT_BANGS=ddg,g /opt/data/scripts/deep_research_v2.py "question" --channels searxng
```

Use `balanced` for normal DeepResearch; reserve `max` and manual bangs for “recherche premium”, overnight, or one-off diagnostics where latency/noise are acceptable.

## Engines: observed policy

Keep in default/balanced when currently healthy enough:

- SearXNG aggregate, after removing toxic general engines.
- DuckDuckGo where it is not CAPTCHAing.
- arXiv for academic/technical queries.
- GitHub/HackerNews/StackOverflow when query class matches.
- OpenAlex/GitLab/Mwmbl as breadth additions when useful.

Exclude from high-throughput default unless current probes prove otherwise:

- Google general web: can work one-off, but repeated probes triggered CAPTCHA and polluted aggregate results.
- Startpage/Brave: noisy/rate-limited in repeated probes.
- Reddit direct: upstream `403`/access denied.
- Reddit indirect (`site:reddit.com` via DDG/Google): often 0 useful results + CAPTCHA/noise; enable only for diagnostic or premium attempts.
- Yahoo/Semantic Scholar/Qwant/Mojeek/Presearch/Yep: previously noisy, blocked, timed out, or JSON/parse-error prone in this environment.
- Bing News (`!bng`): can return results but had parsing errors in some contexts; keep out of balanced until re-probed.

If a toxic engine is still enabled in SearXNG aggregate and creates repeated `unresponsive_engines`, disable it in the SearXNG settings volume with a backup, then restart SearXNG. In the 2026-06-29 run, Google general was disabled in the Docker volume config and a default aggregate smoke improved to 62 results with `unresponsive: []`.

## Verification pattern

Before declaring SearXNG healthy for DeepResearch:

1. Probe the canonical Docker endpoint:

```bash
curl -s 'http://searxng:8080/search?q=python%20requests%20timeout&format=json'
```

2. Probe shortcuts/bangs separately (`!gh`, `!hn`, `!arx`, `!ddg`, etc.) and record:
   - HTTP status
   - result count
   - `unresponsive_engines`
   - parse/CAPTCHA/rate-limit messages
3. Run a DeepResearch smoke with `--channels searxng --fetch-top 0` to validate discovery separately from full-page fetching.
4. Interpret `status: partial` carefully: with `--fetch-top 0`, partial usually means “discovery-only smoke”, not a failed research result.
5. Store artifacts under `/opt/data/artifacts/searxng-*` or the relevant DeepResearch benchmark directory.

Useful smoke expectation from the optimized 2026-06-29 balanced run:

- `ok: true`
- `candidates_total`: around 39 for the test query
- `sources_total`: around 31
- `unresponsive_packets`: `[]`
- duration: about 56s for 3 subquestions

Do not hard-code these values as future pass/fail thresholds; they are a reference for order-of-magnitude and noise level.

## DeepResearch acceptance update

For a serious DeepResearch run, SearXNG should be evaluated as an additive channel:

1. Include `searxng` alongside Exa/GitHub/HN/StackOverflow/Reddit where relevant.
2. Track `channel_status` and `unresponsive_engines`, not just aggregate source counts.
3. Compare unique domains/URLs contributed by SearXNG after dedupe.
4. If SearXNG is proxied globally, watch for engines that become slower or worse through the mobile path.
5. Do not claim Reddit/Brave/Google are covered by SearXNG unless current probes show real results under the intended run volume.
6. For benchmark claims, separate “SearXNG discovery health” from final evidence quality; discovery-only smoke is not proof of final answer quality.

## Pitfalls

- JSON probes must shell-quote URLs; otherwise `&format=json` can be swallowed by the shell and the probe falsely receives HTML.
- SearXNG API OK does not mean upstream engines are OK. Always probe by shortcuts (`!g`, `!ddg`, `!sp`, `!br`, `!re`, etc.) when changing engine policy.
- A mobile proxy is an expander, not a guarantee. Preserve other retrieval channels instead of replacing them with SearXNG.
- A transient bridge process needs a watchdog or service wrapper before calling the setup durable.
- `python3 -m py_compile` can be blocked by `__pycache__` permissions in `/opt/data/scripts`; use `ast.parse` as a syntax check if bytecode write permission is the only blocker.
