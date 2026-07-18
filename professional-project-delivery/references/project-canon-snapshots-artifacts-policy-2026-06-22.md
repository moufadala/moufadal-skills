# Project canon/snapshot/artifact-policy decisions — 2026-06-22

Session pattern: after an overnight build/audit, the user listed structural decisions: whether a React/Vite workbench becomes canonical, whether to fix ownership, whether to initialize git/snapshots, artifact archive policy, and choosing a V1 for a product.

Reusable decision defaults:

- Workbench canon: recommend `canonique dev` first, not public/prod replacement. Require QA and rollback before switching public routes.
- Ownership repair: allow targeted, logged ownership fixes only after listing problematic paths. Avoid broad `chown -R` over shared scripts or secrets. Capture before/after manifests.
- Git/snapshots: treat as P0 before broad modifications. Use git for durable projects and timestamped tar snapshots for experimental or shared folders.
- Artifacts policy: prefer archive-first over delete-first. Keep final reports, handoff HTML, QA manifests, and screenshots; compress old runs; delete caches/temp only with a manifest.
- Product V1 selection: resist “scrape/build everything”. Define the user job, representative sources, proof threshold, and go/no-go before downstream UI/extraction.

Good response shape:

1. Say “oui, tu comprends exactement” only if the list is genuinely the structural gate.
2. Give a recommendation for each decision, including risk and what not to do.
3. Offer one clear authorization phrase for the user if execution requires side effects.
