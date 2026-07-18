# Tailscale SSH host activation without resetting prefs — 2026-07-06

## Trigger

Moufadal asked to enable Tailscale SSH on the real VPS node `vps-hermes-host`, explicitly warning to use `tailscale set` and not `tailscale up`, because `up` can reset exit-node/routes/proxy preferences.

## Durable lesson

When Hermes runs inside its gateway/container, the container may not have the host `tailscale` binary even though Docker access can inspect/control the host. Do not conclude Tailscale is absent. First prove containerization (`/.dockerenv`, PID 1 `s6-svscan`, Docker hostname), then either ask for a real host shell or use a privileged/nsenter host command path if already available and appropriate.

## Safe command

On the real host only:

```bash
tailscale set --ssh=true
```

Rollback:

```bash
tailscale set --ssh=false
```

Do **not** use `tailscale up` for this one-setting change.

## Host nsenter pattern used

The first attempt with a normal Hermes image entrypoint failed because the image entrypoint expected to be PID 1. The reliable pattern was an explicit `nsenter` entrypoint:

```bash
docker run --rm --privileged --pid=host --net=host -v /:/host \
  --entrypoint /usr/bin/nsenter nousresearch/hermes-agent:v2026.7.1 \
  --target 1 --mount --uts --ipc --net --pid \
  sh -lc 'hostname; tailscale status; tailscale debug prefs'
```

Then activation:

```bash
docker run --rm --privileged --pid=host --net=host -v /:/host \
  --entrypoint /usr/bin/nsenter nousresearch/hermes-agent:v2026.7.1 \
  --target 1 --mount --uts --ipc --net --pid \
  sh -lc 'tailscale set --ssh=true'
```

## Verification contract

Before and after, capture `tailscale debug prefs`, but redact private/profile fields. Compare only safe fields:

- `Hostname`
- `RunSSH`
- `RouteAll`
- `ExitNodeID`
- `ExitNodeIP`
- `InternalExitNodePrior`
- `ExitNodeAllowLANAccess`
- `AdvertiseRoutes`
- `AdvertiseTags`
- `AdvertiseServices`
- `ShieldsUp`
- `WantRunning`

Acceptance: diff shows only `RunSSH: false -> true`.

Also run `tailscale status` and confirm both nodes if relevant:

```text
vps-hermes-host       moufadal@  linux
vps-hermes-userspace  moufadal@  linux
```

## SSH user choice

Tailscale SSH activation does not choose the Linux user. The ACL `ssh` section controls which identities can SSH as which Linux accounts. Inspect host users with `getent passwd root hermes moufadal ubuntu debian`. In this session only `root` existed on the host, so the immediate test target was `root@vps-hermes-host`. Cleaner long-term setup: create a dedicated user such as `moufadal`, grant controlled sudo, then restrict Tailscale SSH ACLs to that user and optionally to a source node like `immich-pc`.

## Caveat

A local self-test from the host to itself can fail on normal SSH known-host checks (`Host key verification failed`) even when Tailscale SSH is enabled. The real proof is a connection from Moufadal's client node according to tailnet ACLs.