# Campagnes larges sur scrapers vols fragiles — 2026-06-11

## Déclencheur

L'utilisateur corrige une trajectoire de scraping vols avec un signal du type :

- “ça marche, mais c'est fragile” ;
- “optimise au maximum” ;
- “essaie plein de destinations / dates / départs” ;
- “test plein plein” ;
- “ne bloque pas la ligne avec moi”.

## Pattern recommandé

Ne pas lancer un scraper fragile en boucle sans garde-fous. Construire une campagne bornée :

1. **Matrice large mais utile**
   - Plusieurs dates autour de la cible, pas seulement une date.
   - Plusieurs destinations probables (`PAR/ORY/CDG`, `MRU`, `DZA`, `TNR`, etc. selon contexte RUN).
   - Aller simple + aller-retour quand le site expose mieux les tarifs en RT.

2. **Quotas par famille de scraper**
   - Scrapers navigateur/Amadeus/headful validés mais fragiles : petite concurrence (`1–2`).
   - Sites protégés ou instables : concurrence `1`.
   - Probes HTTP légers : concurrence plus élevée (`5–10`) si sans browser.

3. **Timeouts et isolation**
   - Timeout par tâche (`90–420s` selon poids).
   - Un fichier `stdout`, `stderr`, `status` par tâche.
   - Pas de suppression de résultats précédents.

4. **Observabilité continue**
   - `tasks.json` listant la campagne.
   - `progress_<family>.json` pendant l'exécution.
   - `SUMMARY.json` final avec : total, exit codes, indices de succès, prix trouvés, chemins d'artefacts.

5. **Exécution Telegram-safe**
   - Lancer en background avec `notify_on_complete=true`.
   - Répondre immédiatement avec le `session_id`, le périmètre testé et les quotas.
   - Ne pas attendre la fin dans le tour si la campagne est longue.

## Exemple de shape

```text
family=frenchbee      max_parallel=2   RUN→ORY dates J..J+9 OW + RT J+7
family=airmauritius  max_parallel=1   RUN→CDG/MRU dates J..J+5
family=airaustral    max_parallel=1   RUN→CDG/DZA/TNR/MRU dates J..J+3
family=kayak_probe   max_parallel=8   RUN→PAR/ORY/CDG/MRU/DZA/TNR HTTP probes
family=kiwi_capture  max_parallel=1   capture live pour régénérer template/API
```

## Pièges à éviter

- Ne pas surcharger Chromium/CDP avec 10 browsers headful concurrents.
- Ne pas conclure “site bloqué” si l'échec est un artefact local (`template missing`, bug screenshot, crash browser).
- Ne pas polir uniquement la source gagnante si l'utilisateur demande d'optimiser large.
- Ne pas bloquer Telegram : préférer background + notification.

## Sortie utilisateur attendue

Réponse courte :

- process/session id ;
- dossier artefacts ;
- matrice testée ;
- limites de parallélisme ;
- promesse de bilan automatique à la fin, sans prétendre aux résultats avant exécution.
