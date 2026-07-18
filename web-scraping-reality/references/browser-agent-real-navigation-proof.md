# Browser-agent pré-recon — preuve obligatoire de navigation réelle

Contexte: quand l'utilisateur envoie un rapport produit par ChatGPT Agent / Comet / navigateur agentique pour des scrapers, il peut être bien structuré mais ne pas avoir réellement ouvert/interagi avec un navigateur. Ne pas traiter un rapport long comme preuve de navigation.

## Signal d'alerte

Un rapport externe est suspect s'il contient surtout :
- "HAR non disponible" sans actions browser détaillées ;
- "URL observée" / "page expose" / "méthode recommandée" sans clics ni champs remplis ;
- endpoints présentés comme confirmés sans statut HTTP, extrait brut ou source réseau ;
- prix mentionnés sans URL finale, contexte aller simple/A/R, screenshot ou étape de recherche ;
- aucune liste de sites réellement ouverts, recherches soumises, pages résultats atteintes.

## Gate d'acceptation pour rapports de navigateur agentique

Avant d'exploiter le rapport, exiger en tête :

```text
Navigateur réel disponible : oui/non
DevTools/HAR disponible : oui/non
Screenshots disponibles : oui/non
Nombre de sites ouverts réellement :
Nombre de recherches réellement soumises :
Nombre de pages résultats réellement atteintes :
```

Si `Navigateur réel disponible = non`, le rapport doit s'arrêter avec :

```text
ÉCHEC : je n'ai pas pu utiliser de navigateur réel/interactif. Je ne fournis pas de pré-recon simulée.
```

## Fiche minimale par source

Pour chaque source, demander :
- URL exacte ouverte ;
- heure approximative ;
- action utilisateur réelle: clic, champ rempli, sélection ville/date/passagers, bouton recherche ;
- route/date/passagers testés ;
- résultat visible après action ;
- prix exact si visible ;
- URL finale après recherche ;
- message d'erreur/challenge ;
- screenshot ou description visuelle précise ;
- HAR/Network disponible oui/non ;
- endpoints réellement observés vs seulement supposés ;
- prochaine action unique pour Hermes.

## Règle de triage

Classer séparément :
- `observé navigateur`: action et résultat visibles ;
- `observé réseau`: statut HTTP/extrait brut/HAR/Copy-as-cURL ;
- `déduit/plausible`: cohérent mais non prouvé ;
- `contredit localement`: probe Hermes ou artefact local contredit le rapport.

Les artefacts locaux/HAR/curl priment sur un rapport externe. Un endpoint annoncé comme JSON par l'agent mais qui retourne Cloudflare/403 depuis Hermes devient une **cible HAR/NetLog**, pas un endpoint prêt à coder.

## Prompt correctif compact

Quand un rapport externe a probablement été produit sans vraie navigation, renvoyer un prompt de correction qui force :
- statut navigateur en tête ;
- échec explicite si pas de navigateur interactif ;
- au moins une action utilisateur par source ;
- URL finale et résultat visible ;
- séparation endpoints observés / hypothèses ;
- interdiction de rapport de substitution si le navigateur n'est pas disponible.
