# Scrapling prod wiring — Python venv, raw XML, CDP, Playwright cache (2026-07-07)

Contexte validé sur le portail immo Réunion: passage d'un refresh prod `python3` système vers un venv projet pour activer Scrapling.

## Leçons vérifiées

1. **Installer `scrapling` seul ne suffit pas toujours.**
   - `scrapling==0.4.10` s'importait, mais `scrapling.fetchers` échouait sans `curl_cffi` puis `browserforge`.
   - Smoke obligatoire avant prod:
     ```bash
     .venv/bin/python - <<'PY'
     import sys, json
     sys.path.insert(0, '/opt/data/scripts')
     import scrapling_fetch as sf
     print(json.dumps(sf.probe_scrapling(), indent=2))
     out=sf.fetch_html('https://example.com/', mode='scrapling', engine='http')
     print(out.summary())
     PY
     ```
   - Preuve minimale attendue: `Fetcher=true` et un fetch réel `mode='scrapling'`, HTTP 200.

2. **Pour XML/RSS, privilégier le body brut avant `html_content`.**
   - Scrapling peut exposer un `html_content` transformé en `<html><body><rss...`, ce qui casse `ElementTree`.
   - L'adaptateur doit lire `body/content/text` avant `html_content/html`.

3. **Recâbler un refresh prod vers `$PY` peut déplacer des dépendances.**
   - Les étapes Playwright qui marchaient par hasard avec le Python système peuvent échouer dans le venv si `PLAYWRIGHT_BROWSERS_PATH` pointe ailleurs.
   - Fix validé: exporter explicitement un cache connu, ex. `/opt/data/home/.cache/ms-playwright`, via une variable projet (`IMMO_PLAYWRIGHT_BROWSERS_PATH`).

4. **CDP sidecar + extension CapSolver peut casser DevTools sur Chrome 148.**
   - Symptôme: container `chromium-cdp` up, proxy 9223 répond `Empty reply`, Chrome vivant mais 9222 ne listen pas.
   - Test minimal sans extension sur un autre port peut passer.
   - Fix validé: rendre l'extension optionnelle (`CDP_ENABLE_CAPSOLVER_EXT=1`) plutôt que chargée par défaut, puis restart et vérifier `/json/version`.

5. **Le build manifest peut refuser une prod générée depuis un script source modifié non committé.**
   - Si `build_manifest_audit` échoue sur `git.source_dirty`, committer uniquement le changement source pertinent ou renoncer explicitement au gate; ne pas bypasser silencieusement.

## Contrat de fin

Ne dire que la prod utilise Scrapling qu'après:
- venv import/probe OK;
- fetch réel `mode=scrapling` sur au moins une source cible;
- refresh officiel complet `exit_code=0`;
- tous les `.status` du run à `rc=0`;
- QA publique HTTP 200 + counts cohérents;
- limites explicites: ex. `StealthyFetcher=false` si seulement le moteur HTTP est actif, et tout fallback résiduel doit être cité.
