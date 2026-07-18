# Windows remote rescue: helper fatigue, Termux handoff, and OpenSSH key planning — 2026-07-09

## Context

Remote Windows PC lost Chrome Remote Desktop / Claude Code Remote Control. Hermes could initially Taildrop files through Tailscale, then needed a non-technical local helper to run admin PowerShell launchers. The helper fatigued after several rounds. A temporary OpenSSH rescue path eventually worked via a dedicated `hermes_rescue` user and Tailscale-scoped firewall.

## Durable lessons

### 1. Treat the local helper as a scarce resource

Do not iterate through multiple scripts unless absolutely necessary. For a spouse/non-technical helper, the first admin launcher should be as close to final as possible:

- one obvious `.cmd` file, ASCII-only filename, no accents/apostrophes/spaces that confuse file association;
- no separate `.ps1` for the helper to choose;
- explicit screen success marker such as `DONE_FOR_HERMES_TEST`;
- Desktop log path;
- rollback script delivered at the same time;
- include all likely future access keys up front if known or generate a future key-management path that does not need another admin click.

If the helper has already done two or three attempts, stop asking for more manual actions unless the user explicitly says “last try”.

### 2. ProgramData `Match User` is robust but hard to mutate later

Windows OpenSSH can be made reliable with:

```text
Match User hermes_rescue
    AuthorizedKeysFile C:/ProgramData/ssh/hermes_rescue_authorized_keys
```

This bypasses user-profile ACL quirks, but the file is normally readable/writable only by administrators/SYSTEM. After SSH is working as non-admin `hermes_rescue`, Hermes may not be able to add a second key later. If Termux/S25 access may be needed, prefer one of these at first admin-run:

- include both the VPS rescue key and the Termux/S25 public key if already available;
- or configure `AuthorizedKeysFile .ssh/authorized_keys C:/ProgramData/ssh/hermes_rescue_authorized_keys` and verify both actually work;
- or avoid the ProgramData override if user-profile ACLs have been proven valid.

Do not tell the user “key added” as sufficient proof unless a real SSH login with that key succeeds.

### 3. UAC from SSH is not a plan

From a Windows OpenSSH session, `Start-Process -Verb RunAs` can fail with:

```text
Cette opération nécessite une station Windows interactive.
```

This is expected: UAC needs an interactive desktop. If no one is at the PC and no prior admin channel exists, admin network repair is blocked. Keep working only on non-admin paths or phone/VPS relay paths.

### 4. Separate three facts before recommending Claude on the PC

Before saying Claude Code / Claude Remote Control can run on the PC, verify:

1. PC is reachable over Tailscale/SSH now.
2. Claude binary exists in the relevant Windows user context, e.g. `C:\Users\user\AppData\Roaming\npm\claude.cmd`.
3. PC has outbound TCP 443 to Anthropic/Google, or a user-level proxy/tunnel exists.

If outbound internet is dead, launching Claude on the PC is likely useless even if the binary exists. But do not present that as a final fact without attempting a bounded actual smoke test when SSH is available:

```powershell
cmd.exe /c "C:\Users\user\AppData\Roaming\npm\claude.cmd -p ""Réponds exactement PC_CLAUDE_OK"" --allowedTools ""Read"" --max-turns 1 --output-format json"
```

Run it with a short timeout and save the raw output.

### 5. Termux handoff: compact commands and no private key in Telegram

When switching to the user's phone, give one compact paste block. Termux may not have a `tailscale` package; if the Android Tailscale app is already connected, SSH can still use the tailnet IP directly without Termux Tailscale CLI.

Safe Termux bootstrap:

```bash
pkg update -y && pkg install -y openssh
mkdir -p ~/.ssh && chmod 700 ~/.ssh
[ -f ~/.ssh/hermes_pc ] || ssh-keygen -t ed25519 -f ~/.ssh/hermes_pc -N "" -C "termux-s25-to-pc-hermes"
chmod 600 ~/.ssh/hermes_pc
cat ~/.ssh/hermes_pc.pub
```

Never paste an existing private rescue key into Telegram. If a private key must be transferred, use an authenticated file channel and plan to revoke it after repair.

## Reporting posture

If the user challenges “did you actually try?”, run the bounded smoke test if the transport is available. If the PC is offline, say precisely that the test could not run because transport failed; do not rely only on earlier network inference.
