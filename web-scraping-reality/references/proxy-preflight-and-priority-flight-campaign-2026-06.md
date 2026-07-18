# Proxy mobile Tailscale — préflight strict et campagne vols prioritaire

## Contexte réutilisable

Quand l'utilisateur active le proxy mobile Tailscale pour des scrapers anti-bot, il peut être pressé de désactiver l'exit node parce que cela semble impacter son téléphone. Il faut donc éviter de gaspiller la fenêtre proxy sur des tests non critiques.

## Leçon principale

Ne jamais conclure qu'un scraper est cassé avant d'avoir isolé les couches réseau :

1. Téléphone visible sur le tailnet.
2. Téléphone annoncé comme exit node utilisable côté VPS (`tailscale exit-node list` ou JSON `ExitNodeOption: true`).
3. Routes internet publiées (`AllowedIPs` contient `0.0.0.0/0` et `::/0`).
4. SOCKS local réellement différent de l'IP VPS.
5. Scraper/Playwright lancé avec proxy explicite, pas seulement variables d'environnement.

Les logs `wgengine`, `magicsock`, `DERP`, `disco` prouvent seulement la connectivité Tailscale, pas l'egress mobile.

## Préflight minimal obligatoire

```bash
TS=/opt/data/tools/tailscale/tailscale
SOCK=/opt/data/tailscale-userspace.sock
$TS --socket=$SOCK exit-node list
$TS --socket=$SOCK status --json | python3 - <<'PY'
import json,sys
d=json.load(sys.stdin)
for n in d.get('Peer',{}).values():
    if 's25' in (n.get('HostName','')+' '+n.get('DNSName','')).lower():
        print({k:n.get(k) for k in ['HostName','Online','ExitNode','ExitNodeOption','AllowedIPs']})
PY
printf 'direct='; env -u HTTP_PROXY -u HTTPS_PROXY -u ALL_PROXY -u http_proxy -u https_proxy -u all_proxy curl -4 -sS --max-time 10 https://api.ipify.org; echo
printf 'socks=';  env -u HTTP_PROXY -u HTTPS_PROXY -u ALL_PROXY -u http_proxy -u https_proxy -u all_proxy curl -4 -sS --max-time 20 --socks5-hostname 127.0.0.1:1055 https://api.ipify.org; echo
```

Succès attendu : `socks != direct`. Exemple validé : `direct=148.230.103.174`, `socks=80.12.x.x`.

## Diagnostic d'états fréquents

- Android `Connected`, mais `EXIT NODE = None` : téléphone connecté mais pas exit node.
- Admin console affiche un badge `Exit Node`, mais CLI VPS dit `no exit nodes found` : ne pas croire l'UI seule; vérifier `ExitNodeOption` et `AllowedIPs`.
- `ExitNodeOption: False`, `AllowedIPs` seulement `100.x/32` : pas utilisable comme sortie internet.
- `ExitNodeOption: True`, `AllowedIPs` contient `0.0.0.0/0` et `::/0` : exit node utilisable.
- `curl --socks5-hostname 127.0.0.1:1055` retourne encore l'IP VPS : classer `network-preflight-failed`, pas scraper cassé.

## Pattern campagne quand la fenêtre proxy est courte

1. Vérifier le proxy juste avant lancement.
2. Prioriser les cibles qui dépendent vraiment de l'IP mobile (ex. French Bee / anti-bot) avant les sources qui marchent déjà sans proxy.
3. Ne pas lancer une campagne large qui commence par des cas peu critiques si l'utilisateur risque de couper le proxy.
4. Si un script contient `--no-proxy`, le retirer explicitement ou créer une variante proxy-priority.
5. Lancer en background avec `notify_on_complete=true` et artefacts par cas.
6. Après succès prioritaire, seulement ensuite lancer la campagne complète.

## Pattern superviseur auto-goal

Quand l'utilisateur dit qu'il peut laisser le proxy actif et demande un mode autonome :

- créer un superviseur borné qui :
  1. exécute le préflight initial ;
  2. attend le run prioritaire ;
  3. refait le préflight ;
  4. lance la campagne complète ;
  5. produit un rapport consolidé ;
  6. refait un préflight final.
- Ne pas laisser un agent se contenter d'un auto-rapport : relire les `case_result.json`, `stdout`, `stderr`, prix détectés, flags anti-bot.

## Piège de communication

Si l'utilisateur signale “tu aurais dû vérifier avant”, reconnaître l'erreur et corriger la méthode immédiatement. La bonne réponse n'est pas de défendre l'ancien diagnostic mais de refaire les preuves : process, logs, exit-node list, `ExitNodeOption`, IP direct vs SOCKS, puis seulement verdict scraper.
