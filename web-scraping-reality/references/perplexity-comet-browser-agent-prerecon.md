# Perplexity Comet — browser-agent pre-recon for scraping

## When to use

Use Comet when the user has access to Perplexity Comet and a target site is difficult for VPS/headless automation:

- airline booking widgets, travel search flows, multi-step forms;
- CAPTCHA / Cloudflare / hCaptcha uncertainty;
- sites where a real user browser can reach deeper than Playwright headless;
- situations where we need screenshots, final search URLs, or human-in-the-loop observations before coding.

Comet is not production infrastructure. Treat it as a human-assisted discovery tool.

## Durable lesson from flight-search work

The user clarified that they are not talking about Perplexity search. They mean **Perplexity Comet**, an agentic Chromium-based browser assistant that can interact with pages, click, fill forms, work across tabs, observe pages, and sometimes inspect page/source context.

So do not dismiss it as “just a search engine”. The correct response is:

1. acknowledge Comet as a browser agent;
2. use it for pre-recon where VPS/browser automation is blocked or expensive;
3. give the user a structured prompt to paste into Comet;
4. ask Comet for concrete artifacts, not a generic report;
5. locally validate any result afterward with HAR/curl/Playwright/replay.

## What to ask Comet for

Always force it to separate:

- visual observation confirmed;
- hypothesis;
- network call confirmed;
- replay not tested.

Minimum artifacts to request:

- exact URL tested;
- exact actions performed;
- screenshots or precise visual descriptions;
- final URL after successful search;
- example prices/results shown;
- captcha / Cloudflare / error messages;
- if available: XHR/fetch requests with method, full URL, status, payload/query params, headers that matter, response excerpt;
- if network is unavailable: source-code hints, field names, JS bundle/domain names, and final navigated URLs.

## Prompt skeleton

```markdown
Tu es Perplexity Comet, navigateur agentique. Objectif : explorer ce site pour découvrir comment automatiser un parcours utilisateur, sans inventer d'endpoints.

Avant de commencer, auto-évalue tes capacités pour cette mission :
- Peux-tu voir les requêtes XHR/fetch exactes ou ouvrir DevTools Network ?
- Peux-tu exporter ou produire un équivalent HAR : URL, méthode, headers importants, payload, status, réponse partielle ?
- Peux-tu lire le code source HTML / JS chargé ?
- Peux-tu prendre ou décrire des screenshots fiables ?
- Peux-tu traverser hCaptcha / Cloudflare Turnstile, ou seulement assister l'utilisateur ?
- Peux-tu conserver cookies/session pendant la navigation ?

Pour chaque site/parcours :
1. URL exacte testée.
2. Ce que tu vois visuellement : formulaire, popup cookies, captcha, page blanche, erreurs, résultats.
3. Actions exactes effectuées : clics, champs remplis, dropdowns, bouton search.
4. Si la recherche aboutit : URL finale, exemples de résultats/prix, devise, conditions.
5. Si blocage : type de blocage, message exact, screenshot/description.
6. Si réseau visible : liste des appels XHR/fetch/navigation importants : méthode, URL complète, status, payload/query params, headers indispensables, extrait de réponse.
7. Si réseau non visible : dis-le explicitement et donne au minimum URL finale, noms des champs HTML, scripts/domaines observés.

Ne conclus pas qu'une API est exploitable sans URL réelle, payload réel, ou URL finale reproductible.
```

## How to use the returned Comet report

1. Parse the report into tested / untested / blocked.
2. Prioritize artifacts with replay value: final URLs, payloads, XHR, screenshots.
3. Verify locally:
   - `curl` / `requests` for raw endpoints;
   - Playwright for form replay;
   - browser screenshot if visual claims matter.
4. Only then create or patch scraper code.

## Pitfalls

- Do not ask Comet broad research questions only; ask it to perform a concrete browser route.
- Do not accept inferred APIs as fact.
- Do not let Comet’s successful manual navigation become a production dependency.
- If Comet cannot expose Network/HAR, it is still useful for final URLs and visual proof, but not enough to claim API exploitability.
