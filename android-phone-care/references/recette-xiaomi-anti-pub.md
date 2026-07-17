# Recette Xiaomi anti-pub / anti-junk (sans root, réversible)

> ⚠️ **À dérouler en session supervisée (scrcpy + toi aux commandes), jamais en aveugle ni en cron.**
> Chaque commande ci-dessous est **réversible**. On confirme d'abord que le package existe, puis on agit UN par UN.
> Rien ici ne lit un message ou une photo : on agit sur des applications, pas sur du contenu.

## Étape 0 — Repérer ce qui est réellement présent

Avant de désarmer quoi que ce soit, lister les packages suspects du système Xiaomi :

```bash
adb shell pm list packages | grep -iE "miui|xiaomi|mipicks|msa|analytics|ad"
```

Note les noms EXACTS retournés — ils varient selon le modèle et la région (`.global` vs pas). N'agis que sur ceux qui apparaissent vraiment.

## Étape 1 — Réglages à couper à la main (via scrcpy)

Le plus gros de la pub Xiaomi se coupe dans les réglages, sans commande :

- **Réglages → Mots de passe et sécurité → Autorisations → « Recevoir des recommandations » = OFF.**
- Ouvrir chaque appli Xiaomi qui montre de la pub (Sécurité, Nettoyage/Cleaner, Téléchargements, Thèmes, Météo, Fichiers) → dans ses paramètres, désactiver **« Recommandations »** / **« Recevoir des recommandations publicitaires »**.
- **NE PAS** utiliser l'app « Sécurité/Nettoyage » de Xiaomi pour nettoyer (elle-même source de pub + faux « boost »).

## Étape 2 — Désarmer les composants pub via ADB (réversible)

`disable-user` = désactive pour l'utilisateur courant, **réactivable** ensuite. Préféré à la désinstallation pour les composants système.

```bash
# Moteur de pub système MSA (le principal)
adb shell pm disable-user --user 0 com.miui.msa.global
adb shell pm disable-user --user 0 com.miui.systemAdSolution

# Télémétrie / analytics (souvent liée à la pub)
adb shell pm disable-user --user 0 com.miui.analytics

# GetApps / magasin d'apps parasite = canal n°1 des installs surprises
adb shell pm disable-user --user 0 com.xiaomi.mipicks
```

> Adapter les noms exacts à ce qu'a retourné l'Étape 0. Si un `disable-user` refuse, ne pas forcer : noter et passer au suivant.

### Pour ANNULER (tout réactiver)

```bash
adb shell pm enable com.miui.msa.global
adb shell pm enable com.miui.systemAdSolution
adb shell pm enable com.miui.analytics
adb shell pm enable com.xiaomi.mipicks
```

## Étape 3 — Junk tiers (apps installées par les enfants / fausses applis)

Ce sont des apps **tierces** → repérées par le bilan santé (`pm list packages -3 -i`). Désinstallation propre :

```bash
# Voir qui a installé quoi (l'installer "com.xiaomi.mipicks" = GetApps = suspect)
adb shell pm list packages -3 -i

# Désinstaller une appli junk confirmée (réversible via réinstall)
adb shell pm uninstall --user 0 <nom.du.package>
```

## Étape 4 — Anti-pub réseau (bonus, 1 champ)

Sur le téléphone : **Réglages → Connexions → DNS privé → nom d'hôte du fournisseur → `dns.adguard-dns.com`.**
Bloque une partie des pubs sur plusieurs apps d'un coup, sans installer d'app.

## Étape 5 — Prévention

- Couper **« Installer des applications inconnues »** pour GetApps + le navigateur (Réglages → Applications → Accès spécial).
- Envisager un **lanceur senior** (BaldPhone, F-Droid) masquant GetApps + le junk.

## Garde-fous

- Ne **jamais** faire un balayage aveugle `pm uninstall` sur tout ce qui contient "com.miui" ou "com.android" → risque de **bootloop**. On agit ciblé, un package à la fois.
- Toujours garder cette liste des commandes d'annulation à portée.
- Une grosse MAJ HyperOS peut réactiver certains composants → re-vérifier après mise à jour.
