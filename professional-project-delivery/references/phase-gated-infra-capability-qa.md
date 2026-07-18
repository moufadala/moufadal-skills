# Phase-gated infra capability QA

Use this pattern when Moufadal asks for a multi-phase infrastructure or agentic foundation rollout where each phase must stop for approval before the next one.

## Trigger

- User explicitly says phase-by-phase / “une seule phase” / stop after QA.
- The phase changes routing, monitoring, cron, Docker, credentials, scraping egress, or any VPS capability.
- Acceptance criteria include real-world failure/recovery proof, not just “service is up”.

## Operating rule

Do **one phase only**. After proof, stop and wait for the explicit next-phase phrase. If QA fails or is incomplete, report the exact missing proof and do not work around it.

## Acceptance contract shape

For each phase, write the contract as:

```text
Phase: <name>
Mutation allowed: <exact scope>
Must not touch: <containers/services/routes/credentials>
Proof required: <observable outputs>
Recovery/rollback: <exact command or path>
Stop condition: <what ends the phase>
```

## Capability heartbeat pattern

For per-capability egress, scraping, or proxy-like routes, a heartbeat must validate the **real capability**, not just that a machine responds.

Good heartbeat examples:

- `curl ifconfig.co` through the exact proxy/exit-node path.
- API probe through the exact network namespace/container/process used by the capability.
- Push monitor that only emits `OK` if the end-to-end capability is true.

Bad heartbeat examples:

- “PC is online” when the requirement is “curl exits through the PC”.
- “container is healthy” when the requirement is “new data arrived”.
- “cron ran” when the requirement is “alert was received”.

## False-proof guard for egress

A public IP alone may be ambiguous when two residential devices share the same ISP/NAT. Pair IP proof with a control-plane proof showing the selected route/exit-node:

- direct public IP vs proxied public IP;
- Tailscale status/prefs showing the selected exit-node and online state;
- script logic that refuses to push OK unless the selected node is active;
- stored artifact with timestamped status and curl output.

## Down/recovery proof

For monitoring phases, require both sides:

1. **Failure path:** intentionally break the capability, then capture monitor transition (`PENDING`/`DOWN`, `important=1`, logs/DB row) and user-confirmed alert receipt if the destination is external Telegram/email.
2. **Recovery path:** restore the capability and capture monitor transition back to `UP` with the same end-to-end proof.

If the assistant cannot observe the final destination (e.g. the user's Telegram inbox), ask for a short confirmation. Do not claim “alert received” from Kuma DB alone.

## Durable artifacts

Save under `/opt/data/artifacts/<project>/<phase-run>/`:

- pre/post status;
- control-plane state;
- direct/proxied probe output;
- monitor DB/log excerpts;
- final Markdown report with rollback.

Keep secrets out of vault and reports. Redact tokens and store operational credentials under `/opt/data/...` with restrictive permissions.

## Common pitfalls

- Advancing to the next phase after a partial PASS.
- Treating `UP` heartbeat as enough without failure/recovery proof.
- Routing the entire VPS when the requirement is per-capability egress.
- Letting a cron or monitor send OK based only on process health.
- Reporting a monitor DOWN as “Telegram alert received” without user or API-side evidence.
