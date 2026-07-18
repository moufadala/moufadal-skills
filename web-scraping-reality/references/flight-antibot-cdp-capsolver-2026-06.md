# Notes terrain — sites de vols RUN protégés (CDP/Xvfb/CapSolver)

Validation session 2026-06-03. À utiliser comme référence de détails, pas comme conclusion permanente : re-tester les endpoints et protections avant production.

## Discipline utilisateur observée

Quand une cible fonctionne déjà partiellement, ne pas la polir avant d'avoir poussé les cibles cassées jusqu'à un vrai verdict. Pour les missions de scraping multi-sites, l'utilisateur préfère :

1. classer les sites cassés / incertains ;
2. pousser chacun jusqu'à blocage démontré ou flux débloqué ;
3. capturer screenshots + réseau + scripts reproductibles ;
4. revenir seulement ensuite au scraper déjà gagnant pour le rendre propre.

## Corsair

- URL utile testée : `https://www.flycorsair.com/fr?fsopen=true`.
- CDP/Xvfb charge le challenge au lieu d'une page blanche.
- Protection observée : Imperva + hCaptcha image grid.
- CapSolver extension configurée seule n'a pas suffi dans ce run : interaction partielle, mauvais item sélectionné, pas de passage au formulaire.
- Artefacts type à produire : screenshot du challenge, events réseau, HTML final, script de probe.
- Prochaine approche durable : CapSolver API token/injection callback ou profil Chrome humain persistant warm-up, pas seulement extension auto.

## Air Mauritius

- Formulaire accueil maîtrisable en Playwright/CDP :
  - origine `.route-selection-origin`, input `Origin1`, option `.airport-option` avec `.airport-option-iata` ;
  - destination `.route-selection-destination`, input `Destination1` ;
  - dates via React DayPicker `.DayPicker-Day[aria-label]` (ex. `Sat Jul 18 2026`).
- Flux testé RUN→MRU, dates 18→25 juillet 2026 : sélection + bouton Search OK.
- Après submit, redirection vers `booking.airmauritius.com/plnext/AirMauritiusDX/Override.action...` puis Imperva CAPTCHA `PARDON OUR INTERRUPTION`.
- Le problème n'est donc plus le formulaire, mais la barrière post-submit Amadeus/Imperva.
- `departure.json` contient les aéroports (`RUN`, `MRU`, etc.). `arrival.json` a retourné `[]` dans ce run : ne pas conclure que la route est impossible sans vérifier le JS/payload exact.

## French Bee

- Playwright headless avait montré un problème HTTP/2, mais CDP/Xvfb sur `https://re.frenchbee.com/fr` charge la page.
- Formulaire visible : `Saint-Denis(RUN)`, destination, aller-retour, passagers, date départ/retour.
- Cible prometteuse après Air Austral : remplir en CDP/Xvfb, capturer XHR/fetch, puis chercher un replay direct.

## Pattern technique réutilisable

- Lancer Chrome visible sous Xvfb + CDP quand headless échoue : `--remote-debugging-port=9222`, profil writable sous `/opt/data/tmp/...`, screenshots systématiques.
- Pour une extension CAPTCHA, ne pas modifier l'extension root-owned : copier dans un dossier writable, injecter la clé/config, lancer Chrome avec `--disable-extensions-except` et `--load-extension`.
- Ne jamais conclure sur anti-bot sans capture visuelle : la différence entre page blanche, hCaptcha, Imperva image grid et formulaire chargé change totalement la stratégie.
