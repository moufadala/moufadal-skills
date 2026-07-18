# Hermes container vs VPS host — Tailscale/ADB diagnostic correction (2026-07-01)

## Trigger

Use this note when Moufadal asks Hermes to diagnose or repair host-level networking, Tailscale, systemd services, ADB-over-TCP, USB/Android control, or anything that may run either inside the Hermes container or on the real VPS host.

## Lesson captured

A prior diagnostic incorrectly treated `tailscale: command not found` and failed ADB reachability inside the Hermes runtime as if it described the real VPS host. Moufadal corrected the workflow: first prove which environment Hermes is executing in.

## Required environment identity gate

Before making host-level conclusions, run only harmless read commands:

```bash
whoami
hostname
pwd
uname -a
cat /etc/os-release 2>/dev/null || true
command -v sudo || true
command -v tailscale || true
command -v systemctl || true
ip addr 2>/dev/null | head -80 || true
[ -f /.dockerenv ] && echo '/.dockerenv present' || true
ps -p 1 -o pid,comm,args 2>/dev/null || true
cat /proc/1/cgroup 2>/dev/null | head -20 || true
```

Interpretation from the corrected session:

- `/.dockerenv present` + Docker-like hostname + PID 1 such as `s6-svscan` => Hermes container / isolated runtime, not the host.
- Missing `sudo`, `systemctl`, or `tailscale` inside the container does **not** prove the host lacks them.
- Failed ping/ADB from the container to a Tailscale IP is not enough to conclude the host cannot reach it, because the host Tailscale interface may not be exposed to the container.

## Safe stop condition

If Hermes is inside the container and lacks host privileges/tools, do **not** install or start Tailscale there. Say clearly:

> Il faut ouvrir une vraie session SSH root sur le VPS Hostinger depuis le téléphone.

Explain that installing Tailscale in the container would likely create a separate/confusing node and would not repair the real host node shown in the Tailscale app.

## Correct next step for Moufadal

From a real SSH root/admin session on the VPS host, ask Moufadal to run:

```bash
whoami
hostname
command -v sudo || true
command -v tailscale || true
command -v systemctl || true
tailscale version
tailscale status
tailscale ip -4
tailscale ping <phone-tailscale-ip>
ping -c 3 <phone-tailscale-ip>
```

Only after host Tailscale sees the phone should ADB be tested:

```bash
adb kill-server
adb connect <phone-tailscale-ip>:5555
adb devices -l
```

If ADB is unavailable on the real host, install it there with the distro package manager (`apt install android-tools-adb`) or a deliberate local platform-tools install.

## Safety boundaries for Android control

Until explicit confirmation, do not click, type personal text, open banking/payment apps, send messages, make purchases, or validate sensitive prompts. For safe ADB-only checks, restrict to read-only/display diagnostics or explicit non-sensitive keyevents such as wakeup if the user authorized it.
