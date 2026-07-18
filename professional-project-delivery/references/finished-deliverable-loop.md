# Finished Deliverable Loop — session notes

Use this reference when a project has started drifting into “plausible artifact” territory and the user asks to make the necessary changes so future work actually finishes.

## Durable pattern

For serious deliverables, prefer a durable project workspace plus run-specific artifacts:

```text
/opt/data/projects/<project-slug>/
  README.md
  project.yaml
  data/
  src/
  tests/
  artifacts/
    <YYYYMMDD-HHMMSS-task-slug>/
      contract.md
      plan.md
      dashboard.html or final artifact
      qa-report.md
      screenshots/
      handoff.html
```

Do not move or destroy legacy artifacts unless explicitly asked. Copy useful inputs into the clean project and leave old `/opt/data/artifacts/...` paths intact.

## QA standard that counted as “finished”

A finished UI/dashboard deliverable should have a machine-readable or scripted QA report, not just a visual claim. The useful checks in this session were:

- artifact exists and is non-empty;
- HTML parses and title/doctype are present;
- expected data is embedded and counts match the source contract;
- filter buttons work for every category;
- search terms return expected non-zero results;
- browser interaction test opens the artifact, clicks cards, verifies the detail/reader panel;
- browser console has no blocking JS errors after interactions;
- screenshot is saved under the run artifact directory;
- final handoff explains what changed, how to use it, what was tested, and remaining limits.

## User-signal pitfall

When the user says short prompts like “Alors ?” after a long operation, treat it as a status/accountability check. Immediately report verified current state and paths; do not re-explain the whole plan or continue silently.

When the user says “go fait les modifs nécessaires”, infer the default: implement the durable delivery loop and verify it, unless a risky destructive change would be required.

## Final response shape

Keep the Telegram reply compact:

- “C’est fait” only if real QA passed.
- list durable paths;
- include `MEDIA:` links for the main artifact, handoff, and screenshot when available;
- include exact pass/fail count from QA;
- explicitly state what was not broken or moved if migration was involved.
