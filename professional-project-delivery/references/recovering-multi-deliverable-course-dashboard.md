# Recovering a multi-deliverable course + dashboard session

Use this reference when a session asks for a course/report plus a product artifact and the conversation suffers compaction/freezing.

## Pattern observed

The user asked for a research-backed course adapted to their context, then expected the remaining engineering loop to continue. A context compaction made the assistant over-focus on a smaller side topic and miss the broader work ledger.

Correct recovery:

1. Search/reconstruct the full thread, not only the last message.
2. Inspect durable artifact folders and manifests.
3. Verify already-generated course files before claiming them.
4. Continue the remaining product deliverable instead of stopping at the course.
5. Produce or update a contract, implementation, QA report, screenshot, and handoff.

## Good deliverable shape

For a research-backed dashboard course + implementation:

- `cours-...md`, `cours-...html`, `cours-...pdf`
- manifest with file paths, sizes, and PDF status
- dashboard artifact in a project workspace
- `contract-v2.md`
- autonomous HTML dashboard
- `qa-report-v2.md`
- screenshot evidence
- handoff HTML

## Product semantics that mattered

The dashboard should not be a card gallery. It should be a decision tool:

- each item has `priority_reason`
- each item has `trust_status`
- each item has `recommended_action`
- card click opens internal detail
- source link is a separate explicit action
- user actions exist: seen/saved/hidden/copy-to-brief
- actions persist in localStorage for static HTML prototypes

## QA gates

Minimum browser QA for this class:

- embedded data count is plausible
- first paint has non-empty cards before JS enhancement
- all items have source URL + priority reason + trust status + recommended action
- card click updates reader panel
- Seen changes state/class
- Saved changes state/class and appears in saved filter
- Hidden removes the item from the visible feed
- search returns expected results
- localStorage contains state after actions
- screenshot saved
- console has no errors

## Pitfall

If a generated artifact exists but was produced during a freeze/compaction, existence is not enough. Verify sizes, parse/QA, and then resume the next pending deliverable.