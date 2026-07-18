# SearXNG — durabiliser le rattachement réseau via watchdog (2026-07-11)

## Quand utiliser

Utiliser cette référence quand SearXNG renvoie 0 résultat alors que le proxy mobile/Tailscale est PASS, et que la cause est un rattachement Docker runtime non durable : `searxng` doit résoudre `hermes-gateway` pour utiliser le relais HTTP `http://hermes-gateway:1056`.

## Pattern validé

1. **Préflight proxy obligatoire** avant tout verdict SearXNG : comparer sortie directe VPS et `socks5h://127.0.0.1:1055`. Si proxy FAIL, STOP.
2. **Prouver le problème avant mutation** :
   - requête SearXNG depuis le conteneur -> `results: []` / erreurs moteur HTTP ;
   - `docker exec searxng getent hosts hermes-gateway` -> non résolu.
3. **Rattachement runtime minimal** : `docker network connect <réseau confirmé de hermes-gateway> searxng`, jamais `hermes-gateway`.
4. **Durabilité sans compose** : ajouter au watchdog un bloc idempotent qui connecte uniquement si `searxng` n'est pas déjà sur le réseau.
5. **QA de durabilité** : lancer le script deux fois ; le 2e run ne doit pas afficher le message de connexion. Ensuite vérifier `results_count > 0` et `unresponsive_count=0`.
6. **Tracer backup + rollback** dans le runbook, sans copier d'IP mobile ni secrets.

## Bloc idempotent type

À placer après les fonctions de démarrage proxy et avant les self-checks réseau du watchdog :

```bash
ensure_searxng_network() {
  if ! command -v docker >/dev/null 2>&1; then
    echo "[ensure] WARN docker CLI absent"
    return 0
  fi
  if ! docker ps --format '{{.Names}}' | grep -qx 'searxng'; then
    echo "[ensure] WARN conteneur searxng absent"
    return 0
  fi
  if ! docker network ls --format '{{.Name}}' | grep -qx 'hermes_default'; then
    echo "[ensure] WARN reseau hermes_default absent"
    return 0
  fi
  if ! docker inspect -f '{{json .NetworkSettings.Networks}}' searxng | grep -q hermes_default; then
    docker network connect hermes_default searxng && echo "[ensure] searxng connecte a hermes_default"
  fi
  docker exec searxng getent hosts hermes-gateway >/dev/null && echo "[ensure] hermes-gateway resolu OK" || echo "[ensure] WARN hermes-gateway non resolu"
}

start_tailscale
start_http_proxy
ensure_searxng_network
```

## Commandes QA minimales

```bash
bash -n /opt/data/scripts/ensure_searxng_mobile_proxy_stack.sh
bash /opt/data/scripts/ensure_searxng_mobile_proxy_stack.sh | tee /tmp/searxng_watchdog_run1.out
bash /opt/data/scripts/ensure_searxng_mobile_proxy_stack.sh | tee /tmp/searxng_watchdog_run2.out
! grep -q 'searxng connecte a hermes_default' /tmp/searxng_watchdog_run2.out

docker exec searxng sh -lc 'wget -qO- "http://127.0.0.1:8080/search?q=hermes%20agent&format=json"' \
  | python3 -c 'import json,sys; d=json.load(sys.stdin); print(len(d.get("results",[])), len(d.get("unresponsive_engines",[]))); assert len(d.get("results",[]))>0'
```

## Garde-fous

- Ne jamais restart/configurer `hermes-gateway` pour cette réparation.
- Vérifier le nom exact du réseau de `hermes-gateway` avant de coder en dur `hermes_default`.
- Sauvegarder le script avant édition : `cp -a script script.bak.$(date +%Y%m%dT%H%M%S)`.
- Le fix déclaratif propre reste le compose réseau natif, mais il peut recréer le conteneur : demander validation explicite avant d'y toucher.
- Si le job watchdog annoncé n'existe pas réellement, le recréer/valider via l'outil cron avant de dire durable.

## Rollback

```bash
cp -a /opt/data/scripts/ensure_searxng_mobile_proxy_stack.sh.bak.TIMESTAMP /opt/data/scripts/ensure_searxng_mobile_proxy_stack.sh
# si besoin seulement, supprimer/pauser le job cron associé
```
