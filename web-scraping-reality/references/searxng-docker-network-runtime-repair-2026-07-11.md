# SearXNG Docker network runtime repair — 2026-07-11

## When this applies

Use when SearXNG is configured to proxy outbound requests through `http://hermes-gateway:1056`, the mobile/Tailscale SOCKS preflight is PASS, but SearXNG returns zero results with HTTP connection errors.

## Durable lesson

A PASS on `socks5h://127.0.0.1:1055` proves the host/mobile proxy path, but not the container path used by SearXNG. If SearXNG is only on Docker `bridge` while `hermes-gateway` lives on a user-defined network, Docker DNS will not resolve `hermes-gateway` from inside `searxng`; engines then fail even though the mobile proxy itself is healthy.

## Safe sequence

1. Verify exact names; do not assume:

```bash
docker ps --format '{{.Names}}' | grep -E 'searxng|hermes-gateway'
docker network ls --format '{{.Name}}' | grep hermes_default
```

2. Mandatory proxy preflight before any SearXNG conclusion:

```bash
curl -sS --max-time 10 --proxy socks5h://127.0.0.1:1055 https://ifconfig.me
```

Classify as FAIL if it errors, is empty, or equals the direct VPS IP. Do not use SearXNG evidence as proof when this fails.

3. Baseline the fault from inside SearXNG:

```bash
docker exec searxng sh -lc 'wget -qO- "http://127.0.0.1:8080/search?q=test&format=json" | head -c 200'
docker exec searxng getent hosts hermes-gateway || echo "hermes-gateway NON resolu"
```

4. Read-only network disambiguation before mutation. This matters if both `hermes_default` and similarly named networks exist:

```bash
docker inspect -f 'hermes-gateway networks={{json .NetworkSettings.Networks}}' hermes-gateway
docker inspect -f 'searxng networks={{json .NetworkSettings.Networks}}' searxng
```

5. Minimal reversible runtime fix, only after the target network is confirmed:

```bash
docker network connect hermes_default searxng 2>&1 || echo "deja connecte (OK)"
docker exec searxng getent hosts hermes-gateway
```

Rollback:

```bash
docker network disconnect hermes_default searxng
```

6. Definition of done: prove real results after the last mutation:

```bash
docker exec searxng sh -lc 'wget -qO- "http://127.0.0.1:8080/search?q=hermes%20agent&format=json"'
```

Parse/inspect the JSON and require `results_count > 0` and no HTTP connection errors in `unresponsive_engines` before saying repaired.

## Stop conditions

- Proxy preflight FAIL: stop; report `proxy FAIL`; do not touch Docker network.
- Fixing the issue would require restarting or editing `hermes-gateway`: stop unless explicitly authorized.
- DNS resolves after network connect but search still returns zero results: classify separately; the runtime network fix is not sufficient.

## Durability caveat

`docker network connect` is runtime state and may not survive container recreation. Durable repair belongs in the compose definition or the SearXNG/proxy watchdog script, but changing that stack/script is a separate configuration mutation and should be shown as a diff for validation when the user asked for runtime-only repair.

## Documentation hygiene

When writing Obsidian/vault notes, record PASS/FAIL and commands, but avoid copying mobile IPs, tokens, cookies, or other sensitive network details. It is enough to say the proxy IP differed from the direct VPS IP.
