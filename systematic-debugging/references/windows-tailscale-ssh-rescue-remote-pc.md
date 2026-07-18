# Windows PC rescue over Tailscale — SSH access + nontechnical operator pitfalls

Use this when Moufadal loses remote control of a Windows PC but Tailscale still reaches it, and a nontechnical person is physically near the PC.

## Key lessons from 2026-07-09 session

### 1. Do not make the local helper run many files
If the operator is Moufadal’s wife or another nontechnical helper, avoid a sequence like `.bat` → `.ps1` → fix script → another fix script. It creates fatigue and mistakes.

Preferred pattern:
- create **one short ASCII-named launcher** (`HERMES_DERNIERE_TENTATIVE.cmd`), no accents/apostrophes/spaces if possible;
- make it self-contained via `powershell -EncodedCommand ...` when practical;
- show only 3 operator instructions: double-click, click Yes, wait for a success marker;
- write a clear Desktop log (`HERMES_LAST_ATTEMPT_LOG.txt`);
- include a visible terminal marker such as `DONE_FOR_HERMES_TEST`.

Avoid names with accents or apostrophes (`chérie`, `t'aime`) for Windows launcher files; they can confuse file associations, copy/paste, or the helper.

### 2. Taildrop deposits files, but does not execute them
From Hermes/VPS we can send files with `tailscale file cp`, but unless another execution channel exists we cannot delete or execute them remotely. On Windows Taildrop files normally land in `C:\Users\<user>\Downloads` on modern Tailscale, sometimes Desktop on old versions.

If Windows asks “choose an app,” the helper is usually clicking a `.ps1` or Windows file association is confused. Send/use a `.cmd` launcher with a simple ASCII name, and tell them to run that only.

### 3. Use SSH rescue as a temporary, scoped bridge — not a backdoor
If Tailscale ping works but Remote Desktop/Claude Remote Control do not, a temporary OpenSSH bridge is often the fastest repair path.

Safer shape:
- generate a dedicated ED25519 key for the incident;
- install/start Windows OpenSSH Server;
- create a temporary local user like `hermes_rescue` instead of fighting the existing/admin account’s `authorized_keys` behavior;
- use `Match User hermes_rescue` in `%ProgramData%\ssh\sshd_config` with a dedicated key file in `%ProgramData%\ssh\hermes_rescue_authorized_keys`;
- firewall port 22 only to known Tailscale VPS IPs;
- prepare rollback that removes the user + firewall rule + restarts `sshd`.

Windows OpenSSH admin accounts are tricky: users in Administrators may use `%ProgramData%\ssh\administrators_authorized_keys`, with strict ACL requirements. If public key auth keeps failing for `user`, `Administrator`, etc. after port 22 is open, switch to a dedicated non-admin rescue user rather than repeatedly asking the helper to run more micro-fixes.

### 4. Remote shell may be non-admin even when setup was admin
A successful `ssh hermes_rescue@...` may not have privileges for `Get-Service`, `Get-ScheduledTask`, WFP, network resets, or service restarts. Use it first for diagnosis. For risky repair, either:
- deploy a single admin launcher for a bounded fix, or
- use Windows mechanisms designed for privilege elevation if already configured.

Do not silently attempt broad network resets from a non-admin shell.

### 5. Diagnose network layer before blaming Claude/Google
If both Claude Remote Control and Chrome Remote Desktop fail, test general Internet from the PC:
- `curl https://remotedesktop.google.com`
- `curl https://api.anthropic.com`
- `curl https://www.google.com`
- `curl http://neverssl.com`
- `ping 1.1.1.1`, `ping 8.8.8.8`
- `nslookup google.com`
- `route print`, `ipconfig /all`, `tracert -d -h 8 1.1.1.1`

Interpretation from the incident:
- LAN/Livebox OK: `ping 192.168.1.1` works;
- DNS OK: `nslookup google.com` resolves;
- Tailscale OK: VPS can SSH/ping;
- Internet TCP/ping KO: external `curl` and pings timeout;
- therefore the root problem is not Claude/Google directly but PC/box/ISP/filter/VPN-kill-switch/WFP outbound connectivity.

### 6. Operator fatigue is a debugging constraint
If the helper is tired, stop escalating asks. Summarize current proof, park the task, or send one final self-contained file. Do not continue with “just one more script” loops. Moufadal explicitly objected to repeated manual steps.
