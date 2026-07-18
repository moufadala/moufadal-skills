# Emergency vs search-first calibration — Moufadal

Use this reference when Moufadal asks whether Hermes should repair locally first or search externally first during an outage, broken service, fragile scraper, agent/Hermes issue, or production-like incident.

## Canonical rule

Do **not** choose between “act” and “research” abstractly. Classify the incident by reversibility, clarity, blast radius, and expected time loss.

```text
1. Stabilize if needed.
2. Run local checks if cause is obvious/reversible.
3. If unclear, fragile, security/prod-related, or >~15 min without proof → search-first.
4. If architecture/security/scraping/agents/skills decision may cost ~30 min–1 h+ if wrong → external search + verdict before durable change.
5. If high risk → Niveau 3: Claude Code critique + second external search loop + artifact.
```

## Decision matrix

### A. Local-first, no external search yet

Use when all are true:
- symptom is local and narrow;
- cause is likely visible from logs/config/status;
- action is reversible and low blast radius;
- expected time to prove/fix is under ~15 minutes;
- no durable architecture/security/tool choice is being made.

Examples:
- `immo-dashboard` container is stopped → check Docker status/logs, restart if safe, verify HTTP.
- Cron did not send a message → inspect job status/log/output, rerun the exact job if safe.
- A script has a syntax error after an edit → run syntax/test, patch line, rerun.
- Disk almost full from logs/cache → inspect sizes, rotate/compress safe logs; do not delete unknown project data.
- SearXNG HTTP relay returns 502 but local service is down → check service/container first.

User-facing wording:
```text
Incident clair/local : je fais d'abord les checks réversibles pendant ~15 min. Si la cause n'est pas prouvée rapidement, je bascule en search-first.
```

### B. Search-first after local preflight

Use when:
- local checks do not prove cause within ~15 minutes;
- fix would alter durable config, routing, cron policy, Docker topology, MCP, skills, or auth;
- multiple plausible causes compete;
- known anti-bot/API/tool behavior may have changed;
- prior fix failed or created a regression.

Examples:
- Docker/Traefik routing issue not explained by container status/logs → check local config then docs/community before changing labels/network.
- Hermes gateway behavior changed after update → inspect logs/config, then docs/releases/issues before patching runtime behavior.
- Claude/Codex auth problem not solved by known token sync → check local token state, then docs/issues before rewriting auth flow.
- Android/S25 control path flaky → verify ADB/Tailscale/MCP local state, then docs/community if not obvious.

User-facing wording:
```text
Local preflight insuffisant : je bascule en search-first. Requêtes prévues : [...]. Verdict avant changement durable.
```

### C. External search immediately

Use when the first action would otherwise be a guess in a fragile or moving domain:
- scraping/anti-bot, mobile API, hCaptcha/Cloudflare/Imperva;
- security/auth/secrets/OAuth permissions;
- system upgrade or breaking version change;
- installing/adopting a new tool, MCP server, plugin, agent, package, or major workflow;
- architecture choice with cost of wrong path ≥ ~30 min–1 h;
- user explicitly asks “cherche”, “comment les gens font”, “meilleure pratique”, or “ne réinvente pas”.

Examples:
- Air Austral/French Bee/Imperva flow changed → do not tweak blindly; inspect local NetLog/history and search current community/docs.
- New MCP/mobile control server → search docs/repo/issues before install.
- New Obsidian/LifeOS structure → benchmark existing vault templates and local notes before designing custom.
- Skill-routing/golden-case redesign → inspect local skill state and search docs/best practices first.

User-facing wording with query visibility:
```text
Recherche externe justifiée : domaine fragile ou décision durable. Requêtes utilisées : [2–4 requêtes courtes].
```

### D. Niveau 3 immediately or very early

Niveau 3 = Claude Code critique/réfutation + second external search loop + artifact/report before final decision.

Trigger when any applies:
- production/VPS/security incident with unclear cause;
- durable architecture or routing change;
- scraping anti-bot fragile where blind attempts waste hours;
- auth/credentials/token flow change;
- skill/agent operating-model change affecting many future sessions;
- a `BUILD` verdict is being considered while local/external evidence is weak or contradictory;
- repeated false positives/false negatives on the search-first threshold, or multiple user corrections about when Hermes should have searched;
- repeated failed local fix;
- potential exposure of private data/secrets;
- user has corrected the same threshold/pattern multiple times.

User-facing wording:
```text
Je pense que niveau 3 est justifié : [signal concret]. Je peux faire un fix local minimal si nécessaire, mais la décision durable doit passer par Claude + seconde recherche.
```

## Boundary examples

- **Container down after reboot** → Local-first. If restart fails or logs show unknown Traefik/Docker error → Search-first.
- **Public dashboard 404 after known deploy script** → Local-first with `qa-public.sh`. If Docker volume/Traefik behavior unclear → Search-first.
- **Scraper blocked by 403/Cloudflare/Imperva** → Search-first immediately; local retries without new evidence are noise.
- **Skill typo or broken link** → Local-first. **Skill-routing policy or many skills affected** → Search-first + maybe Niveau 3.
- **Hermes answer style correction** → Local-first memory/skill patch if narrow. **SOUL/operating contract change** → Search-first and artifact.
- **Security/secrets suspicion** → Stop broad action, local containment, then search/docs if tool behavior unknown; Niveau 3 likely.

## Default if uncertain

If uncertain whether to search, do a **local preflight with explicit stop condition**:

- first 5 minutes: logs/status/config and obvious reversible checks;
- hard maximum around 15 minutes without a proven cause/fix; then search-first before durable change.

```text
Je fais un préflight local court : logs/status/config. Si je n'ai pas une cause prouvée avant ~15 min maximum, je cherche externe avant de toucher au durable.
```

## What not to do

- Do not spend 45 minutes tweaking a fragile issue without external validation.
- Do not use “urgence” as an excuse to make durable config/security changes blindly.
- Do not search the web for obvious local restarts/log inspection.
- Do not hide queries during the 4-day calibration window when external search is used.
