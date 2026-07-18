# Research-first prerecon protocol

Use this before hands-on scraping/debugging when the user asks for feasibility, scraping, veille, data collection, or automation against a web property.

## Why

The user explicitly corrected the workflow: do not spend the early phase on isolated tool tinkering. Start with field reality, community patterns, probability of success, and high-leverage reconnaissance.

## Sequence

1. **Reality brief first**
   - What do people do in practice for this class of site?
   - Expected success bands: direct API / HAR replay, Playwright/codegen, stealth, CAPTCHA/proxies, paid services.
   - Cost, fragility, and ethical/TOS line.

2. **GitHub search before browser tinkering**
   - Search real code and issues before writing custom Playwright.
   - Examples:
     ```bash
     gh search code "playwright airline booking" --limit 20
     gh search code "angular datepicker readonly playwright" --limit 20
     gh search issues "playwright formControlName fill" --limit 20
     gh search repos "scraper playwright airline" --sort stars --limit 20
     ```

3. **Perplexity Pro as pre-recon, not truth source**
   - If the user has Perplexity Pro/credits, ask them or use their pasted result as an orientation layer.
   - Treat endpoints/headers from Perplexity as hypotheses until confirmed by HAR/mitmproxy/curl.

4. **Human-in-the-loop capture early**
   - Do not wait for multiple failed scripts to suggest it.
   - Use Playwright codegen, DevTools HAR, or mitmproxy while a human performs the search flow.
   - Goal: capture real XHR/fetch payloads.

5. **Artifact or it did not happen**
   - Save at least one of: HAR, screenshot, curl export, raw JSON response, replay script, ADR note.
   - No feasibility conclusion without a reproducible artifact.

## Perplexity prompt template

```text
I want to investigate this site for personal, reasonable monitoring: [URL].

Goal: understand how the search/form flow works and which network/API calls are likely triggered.

Return a field-reality investigation, not generic advice:
1. Probable technology stack: React/Angular/Vue/CMS/widgets/CDN/consent manager.
2. Confirmed vs probable vs hypothetical endpoints/API patterns.
3. XHR/fetch calls to watch in DevTools during the human action.
4. GitHub search keywords for similar scripts or issues.
5. Headers/tokens/cookies likely to matter.
6. Clean HAR capture procedure.
7. curl/requests replay plan.
8. Pitfalls for this site class: readonly datepicker, Angular formControlName, React state, CookieYes overlays, Cloudflare, anti-bot.
9. Reproducible test protocol.
10. Artifact checklist.

Never present an endpoint as certain unless observed. Separate: confirmed, probable, hypothesis, to verify.
```

## Output shape for the user

Before executing, give a concise checkpoint:

- Field reality: …
- Best first move: …
- Why this beats manual scripting: …
- Artifact expected: …
- Cost/quota impact: …
