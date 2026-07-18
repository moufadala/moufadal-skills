# Réunion immobilier — comparaison SeLoger vs sources existantes (2026-06)

## Contexte durable

Pour décider s'il faut investir dans le scraping d'un site immobilier difficile (ex. SeLoger), ne pas commencer par l'anti-bot. D'abord mesurer la valeur métier par comparaison d'un échantillon manuel/assisté contre la base existante.

Cas validé : PDF manuel SeLoger locations Réunion comparé à `/opt/data/data/reunion_watch.db`.

## Sources déjà couvertes dans la base

Dernière base active observée pendant la session :

- `zimo`
- `bienici`
- `ofim`
- `locamoi`
- `immo974`
- `superimmo`

Ces sources couvrent plusieurs annonces SeLoger, mais pas toutes.

## Méthode de comparaison recommandée

1. Extraire l'échantillon SeLoger fourni par l'utilisateur : PDF, CSV, texte ou capture.
2. Normaliser chaque annonce avec au moins : type, loyer, pièces, surface, ville/localisation, agence, description courte.
3. Comparer contre `rental_listings` par scoring métier :
   - loyer exact ou ±5 € : fort signal ;
   - surface ±1 m² : fort signal ;
   - pièces identiques : signal moyen ;
   - ville normalisée : signal moyen ;
   - chevauchement agence/description/référence : signal complémentaire.
4. Classer : `doublon_sûr`, `doublon_probable`, `unique_probable`.
5. Ne pas conclure sur l'intérêt de scraper avant d'avoir chiffré le taux d'unique probable.

## Seuils de décision utiles

- `<10%` unique probable : source peu prioritaire, sauf niche/agence stratégique.
- `10–25%` unique probable : veille ponctuelle ou extraction semi-manuelle.
- `>25–30%` unique probable : source prioritaire à investiguer techniquement.

Dans le cas SeLoger Réunion testé : 44 annonces extraites, 9 doublons sûrs, 6 doublons probables, 29 uniques probables (~66%). Verdict : SeLoger mérite une investigation haute priorité.

## Pièges de parsing PDF/tableau

Les exports PDF peuvent couper les types sur plusieurs lignes :

- `Colocation /` + `appartement`
- `Maison` + `plain-pied`

Éviter un parseur uniquement basé sur les types simples. Ancrer plutôt sur les lignes de loyer (`^[0-9 ]+ € (CC|HC)?$`) puis reconstruire type, caractéristiques, localisation, agence et description autour de l'ancre.

## Bon réflexe terrain

Pour une source dure à scraper mais potentiellement riche :

- commencer par un échantillon humain ou semi-manuel ;
- comparer à la base existante ;
- seulement si le taux d'unique justifie l'effort, passer à DevTools/HAR/API/pagination/Playwright.

Cela évite de perdre du temps sur un anti-bot pour une source qui serait majoritairement doublonnée.