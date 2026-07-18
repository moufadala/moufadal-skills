# Bounded parallel subagent waves

Use this reference when the user asks to “régler le nombre max de sous-agents”, launch an ultra-parallel push, or run several independent audits/implementation axes.

## Durable lesson

Parallelism is useful only when the controller keeps a strict integration gate. The safe pattern is a bounded wave, not unbounded delegation.

## Pattern

1. **State the cap before launching.** Use the runtime's actual limit (often 3 concurrent `delegate_task` children unless configuration says otherwise) and say the work will be split into at most that many independent axes.
2. **Choose axes with minimal file overlap.** Good axes are research/audit, QA/browser, and isolated feature/data logic. Avoid parallel implementers touching the same source files.
3. **Make subagents return verifiable artifacts.** Require paths, test commands, observed outputs, URLs, or exact diffs. Do not accept “done” as proof.
4. **Controller integrates, not the children.** Hermes/main agent owns final patches, conflict resolution, test selection, publication, git status/log verification, and the user-facing verdict.
5. **Run a unified final gate.** After merging useful findings, run the project’s real acceptance suite/public QA/browser check. Report the consolidated PASS/FAIL, not three separate optimistic summaries.
6. **Write a durable handoff when the wave changes production state.** Include commit, QA matrix/result paths, public URL if relevant, and known non-blocking leftovers.

## Reporting contract

Final report should include:

- cap used and axes launched;
- what was integrated vs intentionally deferred;
- commit or artifact paths;
- exact verification commands/results;
- remaining risk/next axis without pretending it is already solved.

## Pitfalls

- More subagents are not automatically better: beyond the runtime cap, they serialize or fail and add coordination overhead.
- Parallel audit PASS does not equal product PASS until the controller runs an end-to-end/public gate on the final integrated artifact.
- Do not let every child commit independently unless the repository workflow explicitly supports stacked commits; prefer one controller-owned atomic commit after integration for tightly coupled product fixes.
