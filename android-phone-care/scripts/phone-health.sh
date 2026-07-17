#!/usr/bin/env bash
# phone-health.sh — Bilan santé d'un téléphone Android via ADB.
# 100% MÉTADONNÉES : mesure tailles, apps, batterie. Ne lit AUCUN contenu privé
# (aucun message, aucune photo, aucun fichier ouvert). Aucune modification.
#
# Usage : ./phone-health.sh
# Pré-requis : un seul appareil connecté en ADB (USB ou wifi), débogage autorisé.
# Testable dès maintenant sur le S25 de Moufadal (mannequin d'entraînement).

set -u

# --- Localiser adb même si le PATH n'a pas été rechargé (Windows/winget) ---
if ! command -v adb >/dev/null 2>&1; then
  LINKS="$HOME/AppData/Local/Microsoft/WinGet/Links"
  [ -e "$LINKS/adb.exe" ] && PATH="$LINKS:$PATH"
  for d in "$HOME"/AppData/Local/Microsoft/WinGet/Packages/Google.PlatformTools_*/platform-tools; do
    [ -e "$d/adb.exe" ] && PATH="$d:$PATH"
  done
fi
if ! command -v adb >/dev/null 2>&1; then
  echo "❌ adb introuvable dans le PATH."
  echo "   Ferme et rouvre ton terminal (winget a mis à jour le PATH), puis relance."
  exit 1
fi

line() { printf '%s\n' "----------------------------------------"; }
title() { printf '\n### %s\n' "$1"; }

# --- 0. Vérifier qu'un appareil est connecté ---
DEV_COUNT=$(adb devices | grep -cw "device" || true)
if [ "$DEV_COUNT" -eq 0 ]; then
  echo "❌ Aucun appareil ADB connecté (autorisé)."
  echo "   Branche le téléphone + accepte l'invite 'Autoriser le débogage USB'."
  echo "   Puis relance. (adb devices pour vérifier)"
  exit 1
fi
if [ "$DEV_COUNT" -gt 1 ]; then
  echo "⚠️  Plusieurs appareils connectés. Débranche-en pour n'en garder qu'un."
  adb devices
  exit 1
fi

echo "========================================"
echo " BILAN SANTÉ TÉLÉPHONE — $(date '+%Y-%m-%d %H:%M')"
echo " (métadonnées seulement, aucun contenu lu)"
echo "========================================"

# --- 1. Identité de l'appareil ---
title "Appareil"
BRAND=$(adb shell getprop ro.product.brand | tr -d '\r')
MODEL=$(adb shell getprop ro.product.model | tr -d '\r')
ANDROID=$(adb shell getprop ro.build.version.release | tr -d '\r')
MIUI=$(adb shell getprop ro.miui.ui.version.name | tr -d '\r')
echo "Marque   : $BRAND"
echo "Modèle   : $MODEL"
echo "Android  : $ANDROID"
[ -n "$MIUI" ] && echo "MIUI     : $MIUI (téléphone Xiaomi → voir recette anti-pub)"

# --- 2. Stockage (priorité n°1 de Moufadal) ---
title "Stockage"
adb shell dumpsys diskstats 2>/dev/null | grep -E "Data-Free|Cache-Free|System-Free" \
  | sed 's/^/  /'
echo "  (Data-Free = espace utilisateur libre / total. % free = ce qui reste.)"

# --- 3. Poids de WhatsApp (mesure du dossier média, sans l'ouvrir) ---
title "WhatsApp — poids des médias"
WA_NEW="/sdcard/Android/media/com.whatsapp/WhatsApp/Media"
WA_OLD="/sdcard/WhatsApp/Media"
FOUND=0
for P in "$WA_NEW" "$WA_OLD"; do
  if adb shell "[ -d '$P' ]" 2>/dev/null; then
    echo "  Dossier : $P"
    echo "  Détail par type (du plus lourd au plus léger) :"
    adb shell du -sh "$P"/* 2>/dev/null | sort -rh | head -8 | sed 's/^/    /'
    adb shell "du -ch '$P'/* 2>/dev/null | tail -1" | sed 's/^/  TOTAL médias : /'
    FOUND=1
    break
  fi
done
[ "$FOUND" -eq 0 ] && echo "  (Dossier média WhatsApp introuvable — WhatsApp non installé ou chemin différent.)"

# --- 4. Applications tierces (celles installées par l'utilisateur/enfants) ---
title "Applications tierces (installées hors usine)"
NB3=$(adb shell pm list packages -3 2>/dev/null | grep -c "package:" || true)
echo "  Nombre d'apps tierces : $NB3"
echo "  Qui a installé quoi (repérer junk / GetApps) :"
adb shell pm list packages -3 -i 2>/dev/null | sed 's/^/    /' | head -40

# --- 5. Batterie (niveau + température ; PAS l'usure, indispo sans root) ---
title "Batterie"
adb shell dumpsys battery 2>/dev/null | grep -E "level:|temperature:|health:" \
  | grep -v "ACTION_BATTERY_CHANGED" | head -5 | sed 's/^/  /'
echo "  (temperature en dixièmes de °C : 368 = 36.8°C ; health 2 = bon ; usure réelle indispo sans root)"

line
echo "Fin du bilan. Aucun contenu privé n'a été lu ni modifié."
