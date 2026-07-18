# Full Library Audit and Self-Check Pattern

Use this reference when Moufadal asks to audit/check “all skills”, run Skill Creator over the library, or challenges whether Skill Creator is being used systematically.

## Required stance

- Treat the request as a Skill Creator task: load/use `skill-creator` before auditing or editing skills.
- Be active, but do not rewrite the library indiscriminately. The goal is class-level health with rollback, not a one-session sprawl of narrow skills.
- If the user asks “are you using Skill Creator systematically?”, answer directly and operationally:
  - Yes for skill creation/modification/optimization/audit/eval/cleanup tasks.
  - No for unrelated task classes where another skill governs the work.
  - Then prove current usage by naming the loaded skill and the artifacts/actions it drove.

## Audit workflow

1. Create a dated artifact directory and snapshot every readable `SKILL.md` before edits.
2. Audit all relevant skill roots, not just `/opt/data/skills`:
   - `/opt/data/skills`
   - `/opt/data/home/.claude/skills`
   - `/opt/data/home/.agents/skills`
3. Check at least:
   - readability and permissions;
   - YAML frontmatter presence and required fields `name` + `description`;
   - recommended metadata `version`, `author`, `license`;
   - name/folder mismatches;
   - duplicated skill names across roots;
   - deprecated/generic stub triggers;
   - oversized `SKILL.md` files;
   - linked bundled files under `references/`, `scripts/`, `templates/`, `assets/`.
4. Filter false positives before patching:
   - Strip markdown anchors (`references/foo.md#section`) before checking file existence.
   - Ignore placeholders/globs like `references/*.md`, `scripts/<file>`, and style variables like `<style>.md`.
   - Treat duplicated Claude/Hermes/agent-installed skills as potentially intentional until a canonical strategy is explicit.
   - Treat large skills as warnings, not automatic split candidates.
5. Apply only low-risk, reversible fixes automatically:
   - add missing recommended frontmatter metadata;
   - add pointers to existing references;
   - downgrade generic deprecated skills’ trigger descriptions if needed.
6. Do not delete, consolidate, rename, or quarantine duplicates without explicit approval unless the Skill Creator reference already authorizes that exact safe operation.
7. For root-owned/unreadable skills, attempt only a targeted permission check/fix if safe; if refused, record exact `stat`/`chmod` output and the minimal host command needed. Do not run broad `chown`/`chmod`.
8. Rerun the audit after fixes and produce both machine-readable and human-readable outputs.

## Evidence to save

Save these under the audit artifact directory:

- `snapshot_manifest.json`
- `skills_inventory.json`
- `AUDIT_RAW.md`
- `duplicates.json`
- missing bundled-file lookup results
- Claude/reviewer critique if used
- `safe_fixes_diff.patch`
- rollback script for any edits
- Markdown/HTML report with final summary, blockers, and exact next command

## Reporting standard

Report counts before/after, exact files changed, exact blockers, and rollback. Do not claim “all skills fixed” if any skill remains unreadable, has missing bundled references, or requires owner/root action.