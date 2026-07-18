---
name: community-validation-before-fragile-tech
description: "Valider une méthode technique contre la communauté et la doc AVANT d'agir, et estimer sa probabilité de succès. À utiliser avant de s'engager sur une technique fragile, contournante ou incertaine (scraping, contournement, API non officielle, hack de config) — pour éviter de « réparer » un stack qui n'a pas de vrai problème ou de partir sur une voie sans issue."
version: 1.0.0
license: MIT
platforms: [linux, macos, windows]
---

# Community validation before technical action

Use this skill broadly when a task involves an audit, installation, architecture choice, uncertain method, moving-target system, or when the agent starts struggling on a non-trivial technical problem. It is mandatory for scraping, anti-bot, YouTube/yt-dlp, auth cookies, captchas, VPS/datacenter IPs, undocumented APIs, provider limits, browser automation, CLI installs, model/provider setup, and any method that could waste user effort if wrong. Do not overuse it for trivial checks or obvious one-command fixes.

If the work also involves building or designing a non-trivial module/feature/workflow, load `search-first-before-build` as the upstream gate: first determine whether to adopt, extend, or build based on local prior art + external prior art, then use this skill to validate fragile methods.

## Required loop

1. **State the hypothesis**
   - What method is being proposed?
   - What exact failure/error are we trying to solve?

1.5 **Check our own field experience FIRST**
   - Before searching community/docs, check if **we already have working scripts/artifacts** for this exact target. `/opt/data/scripts/` and `/opt/data/artifacts/` contain years of field work.
   - Existing scripts may have solved problems that external reports claim are "infeasible" — our specific combo (e.g. curl_cffi + headful Xvfb → Amadeus Override.action for Imperva sites) may work where generic one-size-fits-all approaches fail.
   - Hierarchy of evidence for this VPS: **field experience > our artifacts > community reports > research reports**. A research report that says "X is impossible" does NOT override a working `frenchbee_solver.py` with confirmed price data.

2. **Check authoritative sources**
   - Official docs/wiki/changelog.
   - GitHub issues in the main repo, sorted by recent dates.
   - GitHub code search for real-world implementation patterns.

3. **Check community terrain**
   - Search issue titles/comments for the exact error string.
   - Look for confirmations: `works`, `fixed`, `resolved`, `successfully`, `same issue`.
   - Look for failures and caveats: banned accounts, expired cookies, IP blocks, PO tokens, rate limits.

4. **Compare with our environment**
   - VPS/datacenter IP vs residential/local.
   - Installed versions.
   - Auth/session availability.
   - Whether current error matches community error exactly.

5. **Give a probability estimate before user action**
   - Always include a numeric success probability when uncertainty exists.
   - First-try probability.
   - Probability with one fallback.
   - Main reasons for failure.
   - Lowest-effort smoke test.

6. **Run smoke test before full pipeline**
   - Test 1–2 representative targets.
   - Verify logs for positive/negative indicators.
   - Do not scale to all targets until smoke test passes.

## Useful commands

```bash
# GitHub recent issues via gh
gh search issues 'repo:OWNER/REPO exact error string' --limit 20

# GitHub REST search when gh quoting is flaky
python3 - <<'PY'
import urllib.parse, urllib.request, json
q='repo:yt-dlp/yt-dlp "Sign in to confirm" cookies created:>2026-05-01'
url='https://api.github.com/search/issues?'+urllib.parse.urlencode({'q':q,'sort':'created','order':'desc','per_page':20})
print(json.dumps(json.load(urllib.request.urlopen(url)), indent=2)[:5000])
PY
```

## Output format

Before asking the user for effort, provide:

- **Verdict:** theory / community validated / currently broken / unknown.
- **Recentness:** last verified evidence date.
- **Implementation used by people.**
- **Known traps.**
- **Probability:** first try + with fallback.
- **Smoke test:** exact command and success indicators.

## Pitfalls

- Do not treat a doc recommendation as sufficient if recent issues show breakage.
- Do not treat metadata/descriptions as transcripts.
- Do not ask the user for credentials/cookies until the method is community-validated and the exact export procedure is known.
- Do not run the full batch before a smoke test.
- **Do not let a research report's claim override existing working field solutions.** Reports generalize; your specific combo (e.g. curl_cffi + headful Xvfb → Amadeus Override.action) may have solved what the report says is unsolvable. Always consult `/opt/data/scripts/` and `/opt/data/artifacts/` for proven solutions before citing impossibility claims from external sources.
- **Manual phone-as-proxy setups need boundary validation and a user-fatigue escape hatch.** For Android/Termux/Tailscale/residential-egress workflows, validate phone-local proxy → VPS-host proxy → container access in that order. Do not keep stacking SSH/socat/firewall fixes after the user shows fatigue; switch to community/docs validation and rank alternatives. If the user rejects direct phone testing or paid proxy, drop those paths and focus on non-paid server-egress options such as Tailscale Android exit node, with explicit risks and smoke proof before route changes. When the user complains about copy-paste/friction, do VPS-side prep yourself and reduce their role to one clearly-located action at a time. If sudo is unavailable, consider a local Tailscale userspace SOCKS probe before asking for root. See `references/android-phone-residential-proxy-options.md`.
- **Reddit access: cookies are a fallback, not “all Reddit.”** For Reddit research, prefer indirect `site:reddit.com` discovery plus official OAuth/API for small compliant usage. Browser cookies may help on a few logged-in pages but do not bypass private/deleted content, rate limits, or anti-bot reliably, and they export an active account session. Treat API/OAuth as likely free enough for personal/dev use within limits, but separate agreement/fees may apply for commercial, high-volume, or restricted data use. See `references/reddit-cookies-oauth-access-2026-06-29.md`.
