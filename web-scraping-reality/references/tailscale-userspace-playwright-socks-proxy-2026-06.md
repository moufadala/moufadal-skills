# Tailscale userspace + Android exit node + Playwright SOCKS explicite

## Quand utiliser

Quand un VPS doit tester un site via une IP téléphone/résidentielle sans modifier la route globale du serveur, en particulier pour des scrapers Playwright/Chromium ou des comparaisons anti-bot.

## Pattern validé

1. Ne pas router globalement tout le VPS si l'objectif est seulement de tester des scrapers : lancer Tailscale en userspace avec un SOCKS local.
2. Utiliser le téléphone Android comme exit node Tailscale, approuvé côté admin console.
3. Vérifier l'IP avant/après avec deux probes indépendants.
4. Pour Playwright, passer le proxy explicitement au browser launch. Les variables `ALL_PROXY`/`HTTPS_PROXY` seules peuvent ne pas être respectées correctement par Chromium/Playwright et produire de faux négatifs (`ERR_CONNECTION_RESET`).
5. Classer séparément :
   - blocage site réel (`403`, Cloudflare, captcha, page challenge) ;
   - bug local de routage/proxy (`ALL_PROXY` ignoré, reset, mauvais proxy transmis au navigateur).

## Commande daemon userspace type

```bash
/opt/data/tools/tailscale/tailscaled \
  --tun=userspace-networking \
  --socks5-server=127.0.0.1:1055 \
  --state=/opt/data/tailscale-userspace.state \
  --socket=/opt/data/tailscale-userspace.sock
```

CLI associé :

```bash
/opt/data/tools/tailscale/tailscale \
  --socket=/opt/data/tailscale-userspace.sock status
```

## Preuves minimales à archiver

```bash
curl -s https://ifconfig.me
curl -s --socks5-hostname 127.0.0.1:1055 https://ifconfig.me
curl -s --socks5-hostname 127.0.0.1:1055 https://httpbin.org/ip
```

Attendu : IP directe VPS différente de l'IP via téléphone/SOCKS.

## Playwright : forme correcte

```python
launch_kwargs = {
    "headless": True,
    "args": ["--no-sandbox", "--disable-dev-shm-usage"],
}
if proxy:
    launch_kwargs["proxy"] = {"server": proxy}  # ex: socks5://127.0.0.1:1055
browser = p.chromium.launch(**launch_kwargs)
```

CLI recommandé pour les scrapers Playwright :

```bash
python3 scraper.py --proxy socks5://127.0.0.1:1055
```

Ou supporter `PLAYWRIGHT_PROXY` en variable d'environnement, mais toujours la convertir en `chromium.launch(proxy={...})`.

## Pièges

- `ALL_PROXY=socks5://127.0.0.1:1055 python3 playwright_scraper.py` peut donner un faux échec : Chromium n'utilise pas forcément le proxy comme attendu.
- Un exit node Android actif ne signifie pas que tous les sites passeront : Cloudflare peut encore répondre `403` même via IP mobile.
- Pour les scrapers HTTP `urllib`/anciens wrappers, le proxy SOCKS peut provoquer des resets selon la stack ; ne pas forcer le proxy si le direct fonctionne déjà.
- Sans privilèges root/sudo, ce pattern reste utile car il ne requiert pas de TUN système ni de service systemd. Prévoir cependant une relance manuelle/runner au reboot si aucun superviseur utilisateur n'est installé.

## Décision pratique

Utiliser le proxy téléphone de manière sélective :
- oui pour Playwright/Chromium et tests anti-bot ciblés ;
- oui pour comparer datacenter vs mobile sur une source fragile ;
- non par défaut pour un pipeline productif qui marche déjà en direct ;
- non comme preuve que Cloudflare est contourné tant qu'un artefact page/prix/API n'est pas obtenu.
