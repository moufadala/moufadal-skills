---
name: android-phone-care
description: "Entretenir/surveiller un téléphone Android à distance via ADB, en métadonnées-only (sans lire messages ni photos) : bilan santé (stockage, poids WhatsApp, apps tierces, batterie), désarmement des pubs/junk (recette Xiaomi/MIUI réversible), et pilotage d'écran ponctuel via scrcpy. À utiliser pour aider le téléphone d'un proche âgé (mémoire pleine, WhatsApp qui gonfle, adware), connecter un téléphone en ADB sans-fil via Tailscale, ou produire un rapport de santé d'appareil sans toucher au contenu privé."
version: 1.0.0
license: MIT
platforms: [linux, macos, windows]
---
# Android phone care — maintenance à distance, métadonnées-only

## Principe
On soigne l'**appareil** (mesurer, nettoyer le jetable, désarmer l'adware, alerter) **sans jamais lire le contenu privé** (messages, photos, contacts, contenu de fichiers). Métadonnées 🟢 = auto/OK ; contenu 🔴 = uniquement en session supervisée (scrcpy), jamais en cron. Le shell ADB (uid 2000, sans root) est de toute façon **bloqué par Android** hors des données privées des apps.

## Pré-requis
- **`adb`** (Android platform-tools) installé et joignable. Sur Windows via winget (`Google.PlatformTools`) ; sur Linux/Hermès en général déjà présent.
- **Le téléphone doit avoir le débogage sans-fil armé** et **la clé ADB de CETTE machine autorisée** :
  - Débogage sans-fil (Android 11+) : Options développeur → « Débogage sans fil » → « Associer avec un code ». Récupérer les **2 ports** (appairage + connexion) et le **code**.
  - Chaque machine (PC, Hermès) a sa **propre** clé (`~/.android/adbkey`). **Ne jamais copier la clé d'une machine à l'autre** (= secret). Autoriser chaque machine séparément sur le téléphone.
- **Réseau** : connexion sans-fil **uniquement via Tailscale** (l'IP `100.x`), **jamais** l'IP WiFi locale en clair (`adb tcpip`/5555 exposé = surface d'attaque, port 5555 scanné par des vers).

## Connexion (ADB sans-fil via Tailscale)
```bash
# 1) Appairage (une fois) — ports + code lus sur l'écran "Débogage sans fil"
adb pair <IP_TAILSCALE>:<PORT_APPAIRAGE> <CODE_6_CHIFFRES>
# 2) Connexion
adb connect <IP_TAILSCALE>:<PORT_CONNEXION>
adb devices   # doit montrer "<ip>:<port>  device" (pas "unauthorized")
```
Note : si la machine a déjà été autorisée, `adb connect` suffit (l'appairage peut renvoyer une erreur inoffensive). La connexion sans-fil **tombe au reboot du téléphone** (Android < 17) → à ré-armer ; c'est le point à tester avant tout cron nocturne.

## Bilan santé (métadonnées-only)
```bash
bash scripts/phone-health.sh
```
Affiche : identité (marque/modèle/Android), stockage (`dumpsys diskstats`), poids des médias WhatsApp (`du`), apps tierces + qui les a installées (`pm list packages -3 -i`, repère le junk/GetApps), batterie (niveau/temp/santé — usure réelle indispo sans root). Le script **auto-localise adb** même si le PATH n'est pas rechargé (Windows/winget). N'écrit rien, ne lit aucun contenu.

## Désarmer pubs & junk (Xiaomi/MIUI surtout)
Voir `references/recette-xiaomi-anti-pub.md`. Sur Xiaomi, une grande partie des pubs vient du **système** (MSA, GetApps, analytics) → se désactive **sans root, réversible** (`pm disable-user`). **À dérouler en session supervisée, un package à la fois, jamais en aveugle** (risque de bootloop). Junk tiers : `pm uninstall --user 0 <pkg>` (réversible).

## Pilotage d'écran (gestes "contenu", supervisé)
`scrcpy` affiche l'écran sur le PC via ADB (rien installé sur le téléphone). Pour les gestes qui touchent au contenu (régler WhatsApp, ranger des PDF, montrer). Interactif/GUI → **PC seulement** (une machine headless comme Hermès ne peut pas afficher).

## Portée & partage (cf. Registre skills et outils)
- Le **bilan santé** est portable (bash + adb) : exécutable depuis le PC **ou** Hermès, à condition que la clé ADB de la machine soit autorisée sur le téléphone.
- **scrcpy = exception PC-local** (affichage local requis).
- Ne jamais mettre de secret ici. Les clés ADB restent locales à chaque machine.

## Garde-fous
- Jamais lire messages/photos/contacts. La base WhatsApp (`msgstore.db` dans `/data/data`, `.crypt15` chiffrés) est inaccessible sans root et hors périmètre.
- « Surveiller l'appareil, pas la personne » ; consentement + droit de veto de la personne.
- Toute suppression (app, média) = geste supervisé et réversible, jamais dans un cron automatique.
