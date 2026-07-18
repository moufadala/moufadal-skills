# Campagnes vols fragiles — classification des résultats (2026-06-11)

Contexte: campagne RUN multi-sources avec French Bee, Air Mauritius, Air Austral, Kiwi, Kayak. Plusieurs résultats utiles étaient cachés par des `exit_code` faux négatifs ou par un résumé `ok_hint` trop naïf.

## Leçons durables

### Lire les artefacts complets, pas seulement `SUMMARY.json`
- `SUMMARY.json` et `stdout_tail` peuvent tronquer la partie utile.
- Pour tout `winner` manquant ou résultat suspect, relire le `stdout_file` complet.
- Extraire le JSON entre le premier `{` et `\nend=` quand le stdout est enveloppé par un runner.

### Ne pas confondre `exit_code` et valeur métier
- Air Mauritius a retourné `exit_code=1` alors que la page contenait `Air Mauritius - vols`, des vols RUN→MRU et des prix `EUR301,70`.
- Règle: si la page contient un titre résultats + prix + segment de route, marquer `business_ok=true` même si le script sort non-zéro; le non-zéro devient `parser_bug` ou `postprocess_bug`.

### Les `ok_hint` doivent être spécifiques par source
- Kiwi live capture renvoyait `ok: true`, `itineraries_count_api: 22`, `price_eur`, mais n'était pas compté comme winner car le résumé ne détectait pas ce format.
- Air Austral officiel peut fournir des prix dans `prices`/`sections` sans `ok_hint` générique.
- French Bee officiel fournit des tarifs structurés dans `flights[].fares[].price`.

Signaux de succès par source:
- Kiwi: `ok=true`, `parsed.itineraries_count_api > 0`, `offers[].price_eur`.
- French Bee: `ok=true`, `browser.pardon=false`, `flights[].fares[].price`.
- Air Mauritius: titre `Air Mauritius - vols`, route demandée, prix `EUR\d+,\d{2}`, vols MK.
- Air Austral: titre `Air Austral - Vols` ou `Calendrier`, `prices[]` avec `€`, route demandée.
- Kayak HTTP brut: `status=200` seul ne suffit pas; si `has_captcha_or_bot=true` et `price_count=0`, classer non exploitable.

### Sérialiser les scrapers à profil navigateur persistant
- French Bee est robuste end-to-end, mais fragile en campagne parallèle si plusieurs tâches partagent le même profil Chromium.
- Symptômes locaux: `Opening in existing browser session`, `TargetClosed`, Xvfb absent.
- Règle: limiter ces familles à `max_concurrency=1` ou générer un `user-data-dir` unique par tâche; lancer sous Xvfb pour les navigateurs headed.

### Format utilisateur attendu
Pour ce type de campagne, répondre compactement:
- verdict d'abord;
- exploitables vs non exploitables;
- meilleurs prix/vols avec source et artefact;
- bugs locaux séparés des blocages site;
- prochaines corrections concrètes.

Ne pas noyer l'utilisateur dans le dump des 79 tâches: écrire un `COMPACT_REPORT.md` et citer le chemin.

### Mid-run Telegram / vocaux
Si l'utilisateur envoie des vocaux pendant ou juste après un background scraping et signale que des instructions ont été manquées, récupérer/transcrire les audios récents avant de finaliser le bilan. Le bon réflexe est de reconstruire les demandes, puis rattacher chaque résultat aux demandes vocales, plutôt que de supposer que le résumé du process couvre tout.
