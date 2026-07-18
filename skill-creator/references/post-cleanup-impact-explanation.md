# Explaining impact after a skill-library cleanup

Use this reference when the user asks what improved after a skill-library audit/cleanup, whether skills were not triggering before, or whether past projects lost capability because the library was dirty.

## Response posture

- Be direct: a dirty skill library can cause under-triggering, wrong-triggering, noisy context, and broken execution paths.
- Do not overclaim: unless you replay old sessions or inspect session traces, phrase project-level impact as probability/risk, not proof.
- Separate **measured defects** from **likely behavioral effects**.
- If the user expresses frustration that the agent stopped early, answer that first, then continue safe/reversible cleanup work if any remains.

## Evidence buckets to cite

When available, cite before/after counts from the latest audit report:

- `description_too_short` / generic descriptions → skills may not be selected or may be selected too broadly.
- `missing_category`, `missing_title`, missing frontmatter → weaker routing, inventory, and human discoverability.
- `broken_linked_file_ref` → skill may trigger but fail during execution because references/scripts are missing or misread.
- `oversized_skill_md` → useful skill may overload context; split into `references/` for progressive disclosure.
- duplicate skill names across runtime roots → ambiguous source of truth; remove or archive only after verifying canonical copies remain.
- false-positive audit rules → wasted cleanup effort; recalibrate auditor and state the policy explicitly.

## How to answer “did we lose skills/capabilities before?”

Recommended wording:

> Yes, probably some skills were less likely to trigger or less useful when triggered. I can prove the structural defects from the audit; I cannot honestly prove a specific old project would have succeeded without replaying that session. The likely loss was time, reliability, and correct workflow selection, not disappearance of the underlying knowledge.

Then give concrete domains affected by the actual audit, e.g. Hermes/VPS setup, web search/scraping, YouTube/proxy workflows, document/OCR/PowerPoint, Claude Code orchestration, or project delivery.

## What to avoid

- Do not say “all skill problems are solved” just because gates pass.
- Do not imply deleted duplicate roots were useless unless canonical copies remain and the runtime impact was checked.
- Do not turn a dated audit into a permanent memory fact; store session-specific run paths in this reference or the final report, not in user memory.
- Do not create one narrow skill per audit incident. Patch the class-level skill and add references.
