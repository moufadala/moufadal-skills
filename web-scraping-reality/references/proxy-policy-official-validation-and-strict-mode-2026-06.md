# Proxy scraping — validation officielle/communauté et mode strict

## Quand utiliser

Utiliser cette référence quand une campagne de scraping dépend d'un proxy mobile/résidentiel Tailscale/SOCKS et qu'il faut décider si un fallback direct VPS est acceptable.

## Sources/constats durables

- Tailscale userspace networking expose typiquement un proxy local SOCKS/HTTP, par exemple `127.0.0.1:1055`; c'est le chemin approprié quand le VPS ne doit pas modifier son routage global.
- Playwright/Chromium doit recevoir le proxy explicitement via `launch(proxy={"server": "socks5://127.0.0.1:1055"})` ou option équivalente. Ne pas supposer que `ALL_PROXY` route le navigateur.
- Pour les clients HTTP type curl/requests/curl_cffi, préférer `socks5h://127.0.0.1:1055` quand on veut que la résolution DNS parte côté proxy; `socks5://` peut résoudre localement selon client.
- Les vieux ponts SOCKS ou ports historiques ne doivent pas être fallback silencieux: ils masquent les pannes et créent de faux diagnostics anti-bot.

## Politique de fallback recommandée

Chaque source ou runner doit être explicite sur sa politique:

- `require_proxy`: la campagne échoue proprement si le proxy attendu est indisponible. À utiliser pour tests anti-bot/proxy stricts.
- `allow_direct_fallback`: le scraper peut tester en direct VPS si le proxy est down, mais doit écrire `proxy_status` dans les artefacts et annoter le résultat comme direct.
- `manual_only`: source utile mais trop fragile/risquée pour cron; exécutions manuelles seulement.

Pattern opérationnel validé:

1. Preflight direct vs SOCKS: archiver IP directe VPS et IP via proxy.
2. Écrire un `proxy_status.json` par run: proxy configuré, reachable, utilisé, fallback direct ou non, variable de strict-mode.
3. Si `HERMES_REQUIRE_PROXY=1` ou équivalent est actif et que le proxy est down, sortir avec une erreur structurée type `proxy_required_but_unreachable` avant de lancer un navigateur coûteux.
4. Si fallback direct est autorisé, continuer seulement avec annotation visible; ne jamais vendre le résultat comme test proxy/mobile.
5. Le registry central doit porter la politique (`require_proxy`, `allow_direct_fallback`, `manual_only`) plutôt que de cacher ce choix dans chaque script.

## Anti-pitfalls

- Ne pas conclure “site bloqué” quand le proxy n'a pas été effectivement transmis à Playwright.
- Ne pas conclure “proxy inutile” à partir d'un run qui a fallback direct sans annotation.
- Ne pas réactiver une source fragile en cron juste parce qu'un smoke manuel a réussi; il faut une politique de proxy, des retries/backoff et une classification registry.
- Ne pas stocker d'identifiants, cookies, tokens HAR ou clés API dans les rapports/artefacts lisibles par défaut.

## Preuve attendue dans un rapport

- URL/source testée, méthode, statut HTTP ou état UI.
- `proxy_status.json` ou extrait non secret.
- Chemin d'artefact horodaté.
- Classification: `prod-candidate`, `needs-hardening`, `blocked-antibot`, `bug-local`, `low-value`, ou `manual-only`.
- Prochain test unique qui réduit l'incertitude.