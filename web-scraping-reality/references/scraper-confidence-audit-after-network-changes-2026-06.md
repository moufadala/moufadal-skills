# Scraper confidence audit after network/proxy changes

Use when the user challenges whether recent network/Tailscale/Traefik/CDP changes actually left scrapers working, especially with wording like “tu es sûr ?”, “pas de bricolage ?”, or “scrapper et compagnie”.

## Core lesson

Do **not** answer “tout marche” from prior memory or from an infra-only check. Prove the active scraping path with a non-destructive registry/smoke run and explicitly separate:

- **active gate sources** that are currently enabled and tested;
- **historical or disabled sources** that exist in scripts/registry but are not covered by the gate;
- **site blocks** such as 403/503/CAPTCHA;
- **local/tooling bugs** such as parser warnings, `__pycache__` permissions, or namespace-specific localhost failures.

## Recommended sequence

1. Load scraping reality/health guidance.
2. Run infra preflight:
   - Docker containers and networks.
   - Direct VPS IP vs `socks5h://127.0.0.1:1055` mobile proxy IP.
   - CDP from the namespace that scrapers actually use, often `docker exec hermes-gateway curl http://chromium-cdp:9223/json/version`.
   - SearXNG from Docker network as well as host/localhost; localhost can be a namespace false negative.
3. Inventory the registry, not just script filenames:
   - total sources;
   - enabled/disabled;
   - quick/non-quick;
   - proxy policy;
   - classification rules.
4. Run the quick gate first; if it is intentionally silent on success, state exactly what it proves and what it does not.
5. Run the full enabled non-destructive gate, e.g. `scraper_smoke_runner.py --all-enabled --max-workers 2 --out-root <artifact-dir>`.
6. Read `SUMMARY.json`, per-source `parsed_stdout.json`, and non-empty `stderr.txt`; do not trust exit code alone.
7. For published dashboards/apps, verify the exported data file and public URL separately: count listings, image coverage, price coverage, by-source distribution, HTTP status/title.
8. If you patch a scraper during the audit, re-run the affected source only before claiming the patch is safe.

## Reporting contract

The final answer should lead with a direct confidence statement:

- “Chemin actif prouvé: oui/non.”
- “Tout l’historique scraper prouvé: oui/non.”
- “Sources cassées/non couvertes: …”

Then cite artifact paths and key counts. Avoid overclaiming: a registry where FrenchBee/AirAustral are disabled proves Kiwi/active sources, not official airline scrapers.

## Pitfalls captured

- A container can be `Up` while `localhost:<port>` fails from the current tool namespace. Test from the consuming container before declaring service down.
- `quick_gate` can intentionally produce no stdout on success; that only proves the quick/preflight scope.
- Python scripts embedding JavaScript in triple-quoted strings can emit `SyntaxWarning` or break JS when escape handling changes. Prefer raw Python strings for `page.evaluate(r"""...""")`, but verify JS regex/string literals still parse in Playwright.
- `python3 -m py_compile` may fail on root-owned/script-owned `__pycache__`. For validation, use `PYTHONPYCACHEPREFIX=/tmp/<name>` or `PYTHONDONTWRITEBYTECODE=1` where appropriate; capture the fix, not a claim that compile is broken.
