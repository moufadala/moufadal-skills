# Tailscale Taildrop Windows helper recovery pattern

Use when a remote Windows PC is reachable through Tailscale/Taildrop, but Hermes has no execution channel (no SSH/WinRM/RDP/agent) and a non-technical person must perform the recovery locally.

## Key facts

- Taildrop can **deposit** files on the Windows PC, but it does **not** let Hermes execute or delete them remotely.
- On Windows, received Taildrop files are normally placed in `C:\Users\<username>\Downloads` for Tailscale v1.34+, and older versions may place them on the Desktop.
- The Tailscale mobile app screen is not where the helper should look; the helper must use Windows File Explorer on the PC.
- A `.ps1` is too technical for a non-technical helper. Provide a clearly named `.bat` launcher that wraps the PowerShell script with `ExecutionPolicy Bypass` and admin prompt if required.

## Recommended helper package

Send two files via Taildrop to the target machine:

1. `coucou ma chérie je t'aime clique ici s'il te plaît.bat` or another unmistakable human-friendly launcher name chosen by Moufadal.
2. The underlying `REPAIR_*.ps1` in the same folder.

The `.bat` should:

- display a calm explanation;
- pause once before doing anything;
- run PowerShell elevated only for the bounded repair script;
- say that if a Claude Remote Control window opens, it must stay open;
- avoid changing DNS/proxy/routes/firewall unless explicitly approved.

Example BAT wrapper:

```bat
@echo off
setlocal
title Reparer acces distant Moufadal PC
echo Coucou, merci. Si Windows demande une autorisation, clique OUI.
echo Si une fenetre Claude s'ouvre, ne la ferme pas.
pause
powershell -NoProfile -ExecutionPolicy Bypass -Command "Start-Process PowerShell -Verb RunAs -ArgumentList '-NoProfile -ExecutionPolicy Bypass -File "%~dp0REPAIR_PC_REMOTE_MINIMAL.ps1"'"
pause
```

## Telegram instructions for the helper

Keep it short and concrete:

1. On the PC, open **Explorateur de fichiers**.
2. Open **Téléchargements / Downloads**.
3. If not found, check **Bureau / Desktop**.
4. Double-click only the friendly `.bat` file.
5. If Windows shows a blue warning: **Informations complémentaires** → **Exécuter quand même**.
6. If Windows asks permission: **Oui**.
7. If a Claude window opens: **leave it open**.

## Verification contract

Before claiming recovery is done, collect at least one proof:

- Tailscale ping/port probe from Hermes changes from partial reachability to an actual control channel;
- Claude Remote Control appears online in `claude.ai/code` or produces a visible session URL/window;
- Chrome Remote Desktop becomes available from the user's phone;
- helper sends the generated diagnostic/repair log from the Desktop/Downloads folder.

## Pitfalls

- Do not tell a non-technical helper to run raw `.ps1` unless necessary.
- Do not assume Taildrop files are visible inside the Tailscale app; they are regular files in Downloads/Desktop on Windows.
- Do not promise Google/Chrome Remote Desktop will be fixed: a service restart may help, but account reauth, Windows permissions, firewall, or antivirus may still block it.
- Do not say Hermes can delete Taildrop files from the PC unless a real execution/control channel exists; Taildrop deposit is one-way for this purpose.
