# Deep library audit recovery and residual classification

Use this reference when a skill-library cleanup/audit is broad, backgrounded, or has already hit a blocker. The goal is to preserve class-level skill hygiene without claiming false completion.

## Durable lesson

A deep skill-library pass is not complete just because one script exits or a report file exists. Treat the pass as complete only after independent gates run clean and the residual warnings are classified into: fixed, false positive, approval-needed, protected/external, or genuinely open.

## Recovery pattern after a noisy or partial background run

1. Find the run directory and preserve every existing artifact; do not overwrite the only copy of a possibly-corrupt report.
2. Re-run the smallest deterministic checks, not the whole destructive/fix loop first.
3. Patch the audit/fix script so permission errors become reported blockers instead of aborting the entire pass.
4. Re-apply only safe, reversible fixes:
   - frontmatter metadata;
   - overly short/generic descriptions;
   - obviously stale path references where the real file exists elsewhere;
   - test/golden-set schema mismatches.
5. Re-run quality gates and smoke tests from the current skill state.
6. Generate a new verified report with a different filename, e.g. `FINAL_REPORT_VERIFIED.md`, and clearly mark any earlier report as incomplete/corrupt if applicable.

## Residual classification checklist

For every remaining warning, assign one bucket:

- `fixed`: changed and verified by audit/gate/log.
- `false-positive`: the auditor misread an example command, argument string, compatibility bridge, or intentional routing shim.
- `approval-needed`: split/delete/merge would change routing or remove content; get user approval first.
- `protected-or-external`: bundled/hub/other-agent-root skills should not be silently edited.
- `open`: real missing reference, unclear stale content, or a test gap requiring a targeted follow-up.

Do not report all residual warnings as equal. A library can have passing gates while still containing approval-needed work; say that plainly.

## Common pitfalls from the 2026-07 deep pass

- A shell report generator can appear to finish while Markdown quoting/backticks caused command execution inside the heredoc. Verify the actual report file and logs, not only exit status.
- An unreadable or root-owned skill should not stop the entire pass. Catch `PermissionError`, record the path, and continue safe fixes elsewhere.
- `broken_linked_file_ref` scanners often misclassify commands like `scripts/foo.py input.pdf` as missing files even when `scripts/foo.py` exists. Check the first token before creating bogus files.
- Compatibility-bridge descriptions can look generic by design. Improve the auditor/routing tests before rewriting every bridge.
- Oversized `SKILL.md` files should usually be split into `references/`, but that is a content/routing change. Do it in a dedicated pass with tests after each split.

## Verified-report minimum fields

A final report for a deep pass should include:

- run directory and timestamp;
- before/after issue counts;
- exact gates run and exit codes/log paths;
- list of safe fixes applied;
- residual classification summary;
- approval-needed items;
- rollback command and backup locations;
- next recommended pass, narrowed to one class of work.

## Telegram/user summary rule

For Moufadal, do not say “all skill problems are solved” when only safe-fix gates pass. Say: “safe fixes verified; remaining items are approval-needed / false positives / external/protected / targeted follow-up.” This prevents overclaiming and helps him decide the next batch.