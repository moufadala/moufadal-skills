---
name: dogfood-qa
description: "QA exploratoire d'une app/page web : trouver les bugs avec preuve, tester les vrais parcours utilisateur, inspecter console/réseau/états mobile, produire un rapport QA actionnable. À utiliser quand l'utilisateur demande de vérifier un dashboard/site/app, de prouver qu'une UI est utilisable, de tester une URL, ou de valider un HTML généré avant livraison."
version: 1.0.0
license: MIT
platforms: [linux, macos, windows]
---
# Dogfood — QA exploratoire

## Principe
« Ça a l'air de marcher » n'est pas une validation. On **utilise réellement** le produit comme un utilisateur, on suit les vrais parcours, et on trouve les bugs **avec preuve** avant que l'utilisateur (ou le client) ne les trouve.

## Quand l'utiliser
Avant de livrer un dashboard / site / HTML généré ; pour valider qu'une URL publique fonctionne ; quand l'utilisateur demande « prouve que c'est utilisable ».

## La démarche
1. **Parcours réels d'abord** : dérouler les scénarios utilisateur de bout en bout (pas juste la page d'accueil). Chaque action attendue doit aboutir.
2. **Cas limites & erreurs** : entrées vides/invalides, données manquantes, clics dans le désordre, double soumission.
3. **Inspecter sous le capot** : console (erreurs JS), réseau (requêtes en échec, 404/500), état de chargement, comportement **mobile** (largeur réduite, tactile).
4. **Preuve pour chaque bug** : étapes de repro + ce qui se passe vs attendu + capture / message de console. Un bug sans repro n'est pas actionnable.

## Le rapport QA
- Liste des bugs **classés par gravité** (bloquant → cosmétique).
- Pour chacun : repro, symptôme, preuve.
- Verdict clair : **livrable / pas livrable**, et ce qui manque pour livrer.

## Règle de qualité (anti-complaisance)
Ne pas valider une UI qu'on n'a pas réellement exercée. Si un parcours casse, le dire avec la preuve — « ça marche » sans l'avoir testé est un mensonge poli. Lié à `definition-of-done`.
