# Windows PC rescue via Tailscale Taildrop + OpenSSH — 2026-07-09

## Trigger

Use when Moufadal loses remote access to a Windows PC (Claude Code Remote Control, Chrome Remote Desktop, etc.) but the PC still appears on Tailscale and a non-technical person can click files locally.

## Key lessons

1. **Taildrop can deposit files but cannot execute them.** Treat it as file delivery only. The user/local helper must run something on the PC unless an execution channel already exists.
2. **Give the helper one obvious ASCII launcher.** Accents, apostrophes, long French filenames, `.ps1` files, and code-editor associations confuse Windows. Prefer `CLIQUE_ICI_REPARER_PC.cmd` or similar.
3. **Do not ask them to open `.ps1`.** Windows/VS Code may open the script in Restricted Mode instead of executing it. Ship a `.cmd`/`.bat` wrapper that runs PowerShell elevated:
   ```bat
   powershell -NoProfile -ExecutionPolicy Bypass -Command "Start-Process PowerShell -Verb RunAs -ArgumentList '-NoProfile -ExecutionPolicy Bypass -File "%~dp0SCRIPT.ps1"'"
   ```
4. **If Windows asks “choose an app”, they clicked the wrong file or extension association is broken.** Tell them to use the `.cmd` launcher, or choose `C:\Windows\System32\cmd.exe` / right-click Open / Run as administrator.
5. **For Claude Code recovery scripts on Windows, use `call claude ...`.** Claude installed via npm is often `claude.cmd`; without `call`, a batch file may transfer control to `claude.cmd` and never continue.
6. **Remote Control is outbound-only.** Claude Remote Control does not open a useful inbound port. Verify by user-visible URL/QR/log, not by VPS TCP probe.
7. **Temporary SSH is useful but sensitive.** Make it Tailscale-only, key-only, with a dedicated key, explicit firewall remote addresses, and a rollback script.
8. **Windows OpenSSH admin key behavior is special.** If the account is an administrator, OpenSSH may use `%ProgramData%\ssh\administrators_authorized_keys`, not only `%USERPROFILE%\.ssh\authorized_keys`. Permissions must be strict: SYSTEM + Administrators for the admin file.
9. **Port 22 open is not enough.** If SSH says `Permission denied (publickey,password,keyboard-interactive)`, the service/firewall are working and the next target is key placement/permissions/username.
10. **Keep proof local and visible.** Each script should write a Desktop log (`hermes_ssh_access_install.log`, `hermes_ssh_auth_fix.log`) and keep the window open with `Read-Host`/`pause` so the helper can photograph errors.

## Recommended sequence

1. From VPS: verify Tailscale ping and TCP probes to the Windows node.
2. Taildrop a simple `.cmd` launcher + `.ps1` payload + rollback.
3. Have helper double-click only the `.cmd` launcher and approve UAC.
4. Retest `tailscale ping`, TCP `22`, then SSH with the dedicated key.
5. If port 22 opens but key auth fails, ship a targeted auth-permissions fix rather than reinstalling OpenSSH.
6. Once repaired, run rollback or convert to a documented durable access pattern.

## Safety boundaries

- Do not claim “I can now take over” until SSH command execution succeeds with `hostname/whoami` proof.
- Do not leave temporary SSH access active indefinitely; schedule/perform rollback after the incident.
- Do not broaden firewall to `Any` unless explicitly approved and justified.
