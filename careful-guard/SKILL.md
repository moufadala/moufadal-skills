---
name: careful-guard
description: "Garde-fou avant une action potentiellement destructrice, irréversible, affectant une prod, ou de large portée : rm/rmdir, git reset/force-push, DROP/TRUNCATE, suppression d'artifacts/logs/backups, chmod/chown sur de gros arbres, arrêt de services, suppression de volumes Docker, édition de credentials, ou modif hors du projet courant. Barrière de sécurité avant l'appel d'outil."
version: 1.0.0
license: MIT
platforms: [linux, macos, windows]
---
# Garde-fou avant action risquée

## Principe
Certaines actions ne se rejouent pas. Avant de les lancer, marquer un **temps d'arrêt** : annoncer, vérifier la cible, attendre confirmation. Une pause de 10 secondes ne coûte rien ; un `rm -rf` sur le mauvais dossier coûte tout.

## Déclencheurs (s'arrêter et confirmer AVANT)
- **Suppression** : `rm`, `rmdir`, vider une corbeille, effacer artifacts / logs / backups.
- **Git destructif** : `git reset --hard`, `git clean -fd`, `push --force`, réécriture d'historique.
- **Données** : `DROP`, `TRUNCATE`, migration destructive, suppression de volume / conteneur.
- **Système** : couper un service, `chmod`/`chown` récursif large, éditer des credentials.
- **Portée** : toute édition **hors du projet actif**, ou touchant un système partagé / une prod vivante.

## Le rituel (avant l'action)
1. **Regarder la cible.** Lister ce qui sera affecté (`ls` avant `rm`, `--dry-run`, `git status` avant reset). Ce que je trouve contredit-il ce que je crois ?
2. **Annoncer** en clair : action exacte, périmètre, ce qui est irréversible.
3. **Vérifier qu'il existe une sortie** : backup, branche, corbeille, snapshot. Sinon, en créer une d'abord.
4. **Attendre une validation explicite** pour l'irréversible ou le sortant. Ne pas supposer qu'une autorisation passée couvre ce cas-ci.

## Règle
En cas de doute sur la réversibilité → traiter comme irréversible. Choisir l'option la plus sûre qui atteint le but. Ne jamais lancer un destructif « pour gagner du temps ».
