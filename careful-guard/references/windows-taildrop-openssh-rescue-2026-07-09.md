# Windows Taildrop + temporary OpenSSH rescue pattern (2026-07-09)

## Context

Moufadal's Windows laptop was reachable over Tailscale but Chrome Remote Desktop and Claude Code Remote Control were not usable. Hermes could Taildrop files to the laptop but had no execution channel.

## Lessons

1. **Taildrop delivery is not execution.** `tailscale file cp` can place files on a Windows target, but it does not run them. Expect local human execution until a shell channel exists.
2. **Windows Taildrop receive location:** on modern Tailscale for Windows, received files normally land in `C:\Users\<user>\Downloads`; older versions may use Desktop. Tell the helper to check Downloads first, then Desktop.
3. **Non-technical helpers need one obvious launcher.** Do not ask them to choose between `.ps1` and `.bat`. Provide a single friendly-named `.bat` such as `coucou ... clique ici.bat`, plus the `.ps1` engine it depends on in the same folder. Tell them to double-click the `.bat`, not the `.ps1`.
4. **`.ps1` commonly opens in VS Code instead of running.** If a photo shows Visual Studio Code with the PowerShell script, the helper opened the engine file, not the launcher. Correct instruction: close VS Code, go back to Downloads, double-click the `.bat` or right-click it → Open / Run as administrator.
5. **For Windows batch files that invoke npm-installed Claude Code, use `call claude ...`.** `claude` may be a `claude.cmd`; without `call`, control may not return to the `.bat`, so later commands/logging do not run.
6. **Remote Control cannot be verified by probing inbound ports.** Claude Remote Control uses outbound HTTPS to Anthropic and opens no inbound listener. Verification must come from the local window, `claude.ai/code`, a photo/QR/link, or an established shell channel.
7. **Temporary SSH rescue is a red action.** If the user explicitly authorizes broader access, implement a reversible, narrow OpenSSH setup: key auth only, dedicated key, firewall scoped to known Tailscale VPS IPs, log file on Desktop, and a rollback script that removes the key and firewall rule. Do not present it as zero-risk.
8. **Test before claiming access.** After the helper runs the launcher, verify with Tailscale ping, TCP port 22 probe, then SSH attempts with the dedicated key. If port 22 times out, the script was not executed successfully or OpenSSH/firewall failed locally.

## Minimal verification sequence from VPS

```bash
TS=/opt/data/tools/tailscale/tailscale
SOCK=/opt/data/tailscale-userspace.sock
KEY=/opt/data/artifacts/.../ssh-rescue/moufadal_pc_rescue_ed25519
HOST=100.115.209.33
"$TS" --socket="$SOCK" ping --timeout=5s --c=3 laptop-n5md8n96
python3 - <<'PY'
import socket
s=socket.socket(); s.settimeout(5)
try: s.connect(('100.115.209.33',22)); print('SSH_PORT_OPEN')
except Exception as e: print('SSH_PORT_NOT_OPEN', type(e).__name__, e)
finally: s.close()
PY
ssh -i "$KEY" -o BatchMode=yes -o StrictHostKeyChecking=no -o ConnectTimeout=5 user@$HOST 'hostname; whoami'
```

## User-facing phrasing

- “Le fichier `.ps1` est le moteur, pas celui à cliquer.”
- “Le fichier à double-cliquer est le `.bat` au nom explicite.”
- “C’est acceptable temporairement via Tailscale, mais pas comme accès permanent; rollback après réparation.”
