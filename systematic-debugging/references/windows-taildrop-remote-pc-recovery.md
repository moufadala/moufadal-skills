# Windows PC recovery via Tailscale Taildrop (session pattern)

Use when a remote Windows PC is reachable on Tailscale but no shell/control channel is available, and a non-technical helper can operate the keyboard locally.

## Core boundaries

- Taildrop can **deposit** files; it does not prove the agent can execute or delete them remotely.
- On Windows Tailscale v1.34+, received Taildrop files normally land in `C:\Users\<user>\Downloads`; older versions may use the Desktop.
- If the PC responds to `tailscale ping` and Windows ports like `135/445/5357` are open, do not describe it as “not in Tailscale”. Say: network path exists, but no execution/control channel is available.
- Chrome Remote Desktop and Claude Code Remote Control are separate recovery paths. A generic “restart everything” script may not fix both.

## Helper-friendly delivery

For a spouse/family helper, avoid multi-file instructions as the primary UX. Prefer a single clearly named `.bat` launcher such as:

```text
coucou ma chérie clique ici pour réparer Claude.bat
```

Then explain:

1. Open File Explorer.
2. Go to Downloads.
3. Double-click the exact filename.
4. If SmartScreen appears: “More info” → “Run anyway”.
5. If UAC appears: click “Yes”.
6. If a Claude/PowerShell window opens: leave it open and send a photo.

If the launcher depends on a `.ps1`, send both files and explicitly say they must remain in the same folder. Better: keep the launcher self-contained when possible.

## Claude Code Remote Control Windows `.bat` pitfalls

- Claude installed via npm on Windows is often `claude.cmd`. In a `.bat`, call it with `call claude ...`; otherwise control can transfer to `claude.cmd` and the rest of the script never runs.
- Clear `ANTHROPIC_BASE_URL` only in the current window before launching Remote Control:

```bat
set "ANTHROPIC_BASE_URL="
```

Do not make persistent env edits unless the user explicitly approves.

- Log diagnostics (`where claude`, `claude auth status`, `claude doctor`) to a Desktop log, but do **not** redirect `claude remote-control --verbose` output by default, because the pairing URL/QR code must remain visible to the local helper.
- Use a robust Desktop path fallback because Windows Desktop may be redirected to OneDrive.

Minimal pattern:

```bat
@echo off
setlocal EnableExtensions
chcp 65001 >nul
set "ANTHROPIC_BASE_URL="
set "DESK=%USERPROFILE%\Desktop"
if not exist "%DESK%" set "DESK=%USERPROFILE%\OneDrive\Desktop"
if not exist "%DESK%" set "DESK=%USERPROFILE%"
set "LOG=%DESK%\claude_remote_recovery.log"
where claude >> "%LOG%" 2>&1
call claude auth status >> "%LOG%" 2>&1
call claude doctor >> "%LOG%" 2>&1
call claude remote-control --name "Moufadal PC recovery" --verbose
pause
```

## Google Chrome Remote Desktop caveat

A service restart can help only if the Chrome Remote Desktop Host service is installed and merely stopped. If the page still shows offline, the next proof is a local screenshot of `https://remotedesktop.google.com/access` / `/support`; Google may require account sign-in, reinstallation, or Windows permission confirmation that cannot be solved blindly from the VPS.

## Verification contract

From VPS:

- `tailscale ping <host>` proves network reachability only.
- TCP probes for `22/3389/5985/5986/8765/8770/9222` prove whether an execution/control channel exists.
- Claude Remote Control does not expose an inbound port; success is visible as a local URL/QR code or from `claude.ai/code`, not via a VPS port scan.

Final report should distinguish:

- **deposited** file,
- **executed locally** by helper,
- **control channel restored**,
- **Google/Claude verified from the target app/site**.
