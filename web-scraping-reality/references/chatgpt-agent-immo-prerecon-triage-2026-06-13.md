# ChatGPT Agent immobilier Réunion — triage de pré-recon externe (2026-06-13)

## Quand utiliser

Quand l'utilisateur fournit un PDF/rapport ChatGPT Agent, Comet ou autre agent externe sur des sources immobilières à scraper à La Réunion. Le rapport est un accélérateur, pas une vérité de production : extraire, classer, vérifier localement, puis réécrire un plan Hermes.

## Procédure validée

1. Extraire le PDF avec `pdfx --render-if-short` ou équivalent.
2. Noter pages, caractères extraits et si OCR image nécessaire.
3. Lire le rapport complet, puis créer une matrice : source, claim, verdict externe, preuve locale, action.
4. Prober les URLs proposées depuis le VPS avec un User-Agent navigateur sobre : statut HTTP, URL finale, titre, présence prix/surface/pagination, signaux anti-bot, JSON-LD/API hints.
5. Corriger le classement : un claim `HTML accessible` peut devenir `needs-hardening` si le VPS obtient 403/404.
6. Livrer un `TRIAGE.md` avec : confirmé, contredit, hypothèse, captures nécessaires, plan d'implémentation priorisé.

## Résultat terrain de la session

Rapport analysé : `rapport_pre_recon_immo_reunion.pdf`, 11 pages, environ 26k caractères texte.

Validations sobres depuis le VPS :

- OFIM : 200, prix + surface + pagination.
- Superimmo : 200, prix + surface + pagination.
- Immo974 : 200, prix + surface + pagination ; signal captcha dans HTML mais pas blocage lecture.
- Zimo : 200, gros volume, JSON-LD/API hints ; à utiliser comme méta-agrégateur/contrôle, pas vérité primaire.
- DOMimmo : 200, prix + surface + pagination ; captcha surtout formulaire alerte.
- Citya : 200, prix + surface + pagination.
- Locamoi : 200, techniquement exploitable mais qualité faible.
- Bien’ici : 200 mais pas d'annonces/prix dans HTML brut ; HAR/CDP obligatoire.
- SeLoger robots : 200 avec routes API/BFF ; API mobile/NetLog à vérifier.
- FNAIM : URL du rapport `/locations/1-reunion-974` = 404 ; URL correcte `/locations/1` = 200 avec prix/surface/pagination.
- Logic-Immo : URL du rapport = 403 depuis VPS ; ne pas classer HTML direct sans HAR/Copy-as-cURL.
- PAP : URL maison = 403 depuis VPS ; faible valeur, ne pas investir en priorité.

## Plan recommandé après triage

### P0 — socle non destructif

Avant d'ajouter beaucoup de sources, durcir l'orchestrateur :

- `run_status` par source : `success`, `partial_success`, `blocked_403`, `blocked_429`, `captcha`, `timeout`, `parse_error`, `empty_but_valid`.
- Seuls `success` et `empty_but_valid` peuvent rendre des annonces inactives.
- `blocked_403`, `blocked_429`, `captcha`, `timeout`, `parse_error` ne déclenchent jamais de stale.
- Snapshots bruts HTML/JSON par source.
- Tests : “source bloquée n'inactive rien”.

### P1 — sources confirmées live

Implémenter d'abord des parseurs HTML sobres pour :

- Superimmo
- Immo974
- FNAIM `/locations/1`
- Citya
- DOMimmo
- OFIM en bonus

Ajouter dès le début les filtres métier résidentiels : `bureau`, `local commercial`, `commerce`, `fonds de commerce`, `terrain`, `box`, `garage`, `parking`, `entrepôt`, `chambre`, `colocation`, `saisonnier`, `vacances`.

### Captures à demander ensuite

- Bien’ici : HAR/CDP recherche location La Réunion + Copy-as-cURL de l'appel annonces.
- SeLoger : NetLog Android ou HAR mobile auth/search/count/detail.
- Logic-Immo : Copy-as-cURL depuis navigateur humain si accessible côté utilisateur.

## Pièges à retenir

- Un rapport externe peut être globalement utile tout en contenant des URL erronées ou des observations non reproductibles depuis le VPS.
- Corriger les URLs avant de déclasser une source : FNAIM était bon mais l'URL annexe était mauvaise.
- Ne pas poursuivre les sources faibles bloquées (`PAP`, `Locamoi`, `Entreparticuliers`) avant les sources confirmées utiles.
- Pour l'utilisateur, livrer un verdict court + artefact détaillé ; ne pas noyer le chat dans tout le rapport.
