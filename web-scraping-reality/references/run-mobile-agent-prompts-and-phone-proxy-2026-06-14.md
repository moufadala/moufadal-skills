# RUN Watch scoped GPT Agent prompts and phone proxy notes (2026-06-14)

## Durable correction: scope must stay narrow

For RUN Watch immo/vols prompts, do **not** ask ChatGPT Agent to test every plausible site. The user explicitly corrected this: prompts should only cover sources already verified or actively in chantier.

Bad pattern:

- broad immo prompt listing generic portals outside the project;
- broad vols prompt listing every flight meta-search or airline;
- even naming out-of-scope sites in a “do not test” list.

Good pattern:

- build the source list from current scripts/artifacts/reports;
- include only verified/in-progress sources;
- if the agent sees something outside scope, it should write only `hors scope détecté` and not name/open/test it;
- require HAR/Network/endpoint/payload/screenshots, with secrets redacted;
- **make the mobile axis explicit**: the prompt must say `MOBILE-FIRST COMPLÉMENTAIRE`, and explain that mobile is not an automatic replacement; it is a complementary path to compare against the current desktop/API scraper.

## Durable correction: mobile is a complement, not just a side note

The user corrected the workflow after reviewing the GPT Agent prompt set: the goal was not a generic prerecon and not simply “try mobile if convenient”. The strategy is: for every source already in RUN Watch scope, test whether the mobile/responsive/mobile-UA path is easier or more robust, then use it as a complement to harden existing scrapers.

Future prompts to ChatGPT Agent / browser agents should require, **per source**:

```text
Desktop actuel:
Mobile testé: oui/non
Méthode mobile: m-domain / responsive viewport / mobile user-agent / app-like API / aucun
Verdict mobile: meilleur / complément utile / pas mieux / bloqué / inconclusive
Endpoint(s) desktop:
Endpoint(s) mobile:
Payload nettoyé:
Replay curl/requests: oui/non/à vérifier
Patch recommandé RUN Watch:
```

Do not accept a report that only lists endpoints or prices without this desktop-vs-mobile comparison. If the agent finds no mobile advantage, the useful output is still `mobile_pas_mieux` with evidence.

## Current scoped source sets from the session

### Immo RUN Watch

Use only sources already in the watch/chantiers:

- OFIM / OFIM RSS
- Bien’ici
- SeLoger
- FNAIM
- 97immo
- Immo974
- DOMimmo
- Superimmo
- Alter Immobilier Réunion
- Citya Réunion

Important nuance: after local dry-run, 97immo and Citya were not merely “inconclusive”; existing code extracted them (`97immo=9`, `citya=24`). Future prompts should say “harden existing connector”, not “discover from scratch”.

### Vols RUN Watch

Use only sources already verified or in chantier:

- French Bee
- Air Austral
- Corsair
- Air Mauritius
- Kiwi
- Kayak
- Momondo
- Trip.com

Do not broaden to additional airlines/meta-searches unless the user explicitly asks.

## Phone proxy nuance

A local SOCKS command like:

```text
ssh -N -D 127.0.0.1:1080 user@148.230.103.174
```

means traffic flows:

```text
phone → SSH tunnel → VPS → website
```

The website sees the VPS IP, not the phone’s residential/mobile IP. To use the phone’s residential/mobile proximity, either browse/test directly from the phone/mobile network, or set up the reverse direction:

```text
VPS/agent → reverse SSH tunnel → proxy on phone → mobile Internet → website
```

### Reverse tunnel pattern for phone residential egress

On the phone/Termux, run a local SOCKS proxy first:

```text
pkg update
pkg install openssh curl microsocks
microsocks -i 127.0.0.1 -p 1081
```

In a second Termux tab, expose that phone-local proxy back to the VPS:

```text
ssh -N -R 127.0.0.1:1082:127.0.0.1:1081 \
  -o ExitOnForwardFailure=yes \
  -o ServerAliveInterval=20 \
  -o ServerAliveCountMax=3 \
  -o TCPKeepAlive=yes \
  -o ConnectTimeout=20 \
  USER@VPS_IP
```

Then the VPS can test whether egress is really the phone with:

```text
curl -4 -s https://ifconfig.me
curl -4 -s --socks5-hostname 127.0.0.1:1082 https://ifconfig.me
```

The second IP must differ from the direct VPS IP. If it equals the VPS IP, the tunnel is not providing phone residential egress. If `127.0.0.1:1082` is closed, the reverse tunnel is not up.

### Docker/container caveat for Hermes

Hermes may run inside Docker while `sshd` and the `ssh -R` listener bind on the VPS host. In that case, testing `127.0.0.1:1082` from inside Hermes can be a false negative because it checks the container loopback, not the host loopback.

For Hermes-on-Docker, test multiple candidates before declaring the phone proxy absent:

```text
curl -4 -s --socks5-hostname 127.0.0.1:1082 https://ifconfig.me
curl -4 -s --socks5-hostname <docker-host-gateway>:1082 https://ifconfig.me
curl -4 -s --socks5-hostname <vps-public-ip>:1082 https://ifconfig.me
```

Find the Docker host gateway without relying on `ip` being installed:

```text
python3 - <<'PY'
from pathlib import Path
import socket, struct
for line in Path('/proc/net/route').read_text().splitlines()[1:]:
    parts=line.split()
    if parts[1] == '00000000':
        print(socket.inet_ntoa(struct.pack('<L', int(parts[2], 16))))
PY
```

If the reverse tunnel must be reachable from the container, the Termux `-R` may need a non-loopback bind such as:

```text
ssh -N -R 0.0.0.0:1082:127.0.0.1:1081 USER@VPS_IP
```

or a specific VPS address. If this fails, capture `ssh -vvv` and look for `remote port forwarding failed`, `GatewayPorts`, `administratively prohibited`, or `Permission denied`. A failure here usually means server-side `AllowTcpForwarding`/`GatewayPorts` policy, not a scraper bug.

Security: binding `0.0.0.0:1082` can expose the phone proxy publicly while the tunnel is open. Use only for short tests, restrict firewall if possible, and close with `Ctrl+C` immediately after validation.

`connect_to <tracker-domain>: unknown host` lines in SSH SOCKS logs often indicate DNS/tunnel instability for third-party tracker/CDN domains, not necessarily failure of the target site itself. Validate with the IP comparison above before drawing conclusions.