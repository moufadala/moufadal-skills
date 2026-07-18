# Forensic version recovery after public regression

Use this when a user says the live/public artifact is an older version or that recent work was lost.

## Do not do this

- Do not keep patching the currently served artifact just because it is reachable.
- Do not declare recovery because one local build works.
- Do not overwrite public/prod before proving the candidate and creating rollback.
- Do not commit from a broad accidental repo root that can include secrets or unrelated VPS state.

## Recovery loop

1. **Acknowledge the correction.** Treat the user's memory as a product signal, not as a complaint to smooth over.
2. **Freeze publication.** No destructive public overwrite until a candidate is proven.
3. **Inventory candidates.** Search project dirs, `artifacts/`, backups, old `dist/`, screenshots, and handoff files for product markers: page titles, H1 copy, counts, UX terms, data shapes, local assets.
4. **Recover the product contract.** Use handoffs/session notes/screenshots to identify the real expected version.
5. **Compare candidates.** Criteria should include user-described UX, source workspace, stack, data count, photo/gallery behavior, generated files, and whether it is a clean reboot or old workbench.
6. **Build candidate.** Use the durable source project, not just generated files if avoidable.
7. **QA before publish.** Verify title, first screen, data counts, interactions, image natural dimensions, console errors, and public reachability.
8. **Snapshot rollback.** Copy/archive current public artifact before replacement.
9. **Publish atomically.** Prefer a script that validates then copies to public and sets permissions.
10. **Patch upstream refresh/publish jobs.** A restored app that the nightly job overwrites is not fixed.
11. **Write handoff and protection.** Include source of truth, rollback path, exact QA outputs, scripts touched, and what must not be restored again.
12. **Targeted Git/snapshot.** If the repo root is too broad, initialize/commit only the recovered source workspace and archive exact source/public artifacts with SHA256.

## QA evidence shape

Collect enough proof to make the final claim non-ambiguous:

```json
{
  "title": "expected title",
  "h1": "expected hero copy",
  "cards": 736,
  "badImgs": 0,
  "modal": true,
  "console_errors": 0
}
```

Also include HTTP output for public endpoints and at least one rollback/snapshot path.

## Pipeline hardening checklist

- [ ] Dedicated publish script exists and validates the expected version marker.
- [ ] Public QA asserts old title/marker is absent.
- [ ] Daily refresh publishes the recovered product last, after technical/data generation.
- [ ] Permissions are reset for web server readability.
- [ ] Handoff says which old artifact is workbench/technical-only.
- [ ] Source workspace is protected with targeted Git or source snapshot.
- [ ] Public artifact snapshot includes built assets and media needed to render.
