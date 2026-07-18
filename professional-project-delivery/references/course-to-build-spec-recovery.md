# Course / research handoff → build spec recovery pattern

Use this when a session produced a pedagogical course/report and the user then says a short continuation like “Travail”, “continue”, or complains that prior voice instructions contained more work.

## Pattern

1. **Do not start coding blindly.** Treat the course/report as product context, not the implementation artifact.
2. **Convert the course into a short acceptance spec** under the project workspace, e.g.:
   - `/opt/data/projects/<project>/artifacts/<timestamp>/product-spec.md`
3. **Inspect the current project state before rebuilding.** Look for existing dashboards, QA reports, screenshots, `.latest_run`, and tests.
4. **If an artifact already exists, rerun its QA before modifying.** Do not trust old reports without execution.
5. **Compare existing QA to the new spec.** Add a complementary QA script for missing product checks instead of rewriting the artifact unnecessarily.
6. **Patch the QA vocabulary to the artifact’s real schema when product semantics match.** Example: an existing dashboard may use `priority` + `priority_reason` instead of the cleaner future fields `priority_score` + `priority_level`; test top-ranked items and visible reasons rather than forcing a refactor solely for naming.
7. **Only code the dashboard if QA reveals a real product failure or the existing artifact lacks the required behavior.**
8. **Final response should give:** spec path, dashboard path, QA paths, pass/fail counts, and honest remaining model/schema gaps.

## Pitfalls

- Don’t treat a course/PDF as the final build contract unless it has been distilled into acceptance criteria.
- Don’t rebuild over an existing working artifact before checking it.
- Don’t let old “33/33 passed” reports stand without rerunning them.
- Don’t over-normalize schema names if the user-facing product behavior is already correct; record the schema cleanup as a next hardening step.

## Useful QA additions

For news/watch dashboards, add complementary checks for:

- mobile 390px rendering;
- 3–5 top priorities visible/exploitable;
- every top priority has a human-readable reason;
- source button visible on mobile;
- user actions visible on mobile;
- screenshot artifact created;
- console errors = 0.
