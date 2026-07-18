# Multi-theme Deep Research pack pattern — 2026-06-29

## When this applies

Use this pattern when Moufadal asks for broad exploration across several strategic axes, especially when the output should become an action plan rather than a simple answer.

Example session themes:

- Obsidian + AI memory + VPS architecture
- Android control from Hermes/VPS
- Premium mobile-first MIHAM site
- GSAP / motion design workflow
- Hermes/Claude/Codex inspired by Anthropic Fable-style autonomous agents

## Pattern that worked

1. **Batch each theme separately** with the DeepP0 runner instead of one giant query.
   - Each theme gets its own out_dir, `research_state.json`, `research_report.md`, and raw evidence.
   - Keep metrics per theme: sources collected, pages fetched, notes extracted, duration, channels.
2. **Create a top-level manifest** linking all theme outputs.
3. **Ask Claude Code for a synthesis/critique pass** over the manifest + per-theme state/report files.
   - Contract: identify what is actionnable, risks, top sources, unsupported claims, and 30-day priorities.
   - Log the Claude call with tri-agent logging.
4. **Generate human-readable artifacts**:
   - one `index.html` with global verdict + cards per theme;
   - one HTML page per theme with verdict, do/avoid, next action, top sources, and candidate evidence notes;
   - one Markdown synthesis;
   - one `qa_and_audit_notes.md` documenting Claude/Codex audits and limitations.
5. **Run Codex audit before Telegram final** and tone down claims according to the audit.
6. **QA locally**:
   - py_compile generator scripts with `PYTHONPYCACHEPREFIX=/tmp/...` to avoid root-owned `__pycache__` permission issues;
   - assert artifacts exist and are non-trivial size;
   - local-link check for generated HTML;
   - browser snapshot or screenshot for at least the index page.

## Important caveats to preserve in final answer

Do not overclaim.

- `sources_total` means collected candidates, not human-verified sources.
- `fetched_ok` pages were actually read; this number is the stronger evidence count.
- Evidence notes are candidate quotes; they still need claim-support verification before strong technical/product conclusions.
- If runs show `channels=["exa"]`, say so. GitHub URLs may appear via Exa, but that is not the same as a separate GitHub retrieval channel.
- Avoid labels like “Claude audit” unless there is a separate audit artifact; “Claude synthesis pass” is safer when Claude produced synthesis and risks but not a formal verification report.

## Telegram final shape that worked

Keep it short and operational:

- Verdict: completed, but strategic pack not definitive proof.
- Where we are: 5 axes consolidated into HTML + Markdown.
- Actions: metrics, artifacts generated, QA passed, Claude/Codex logged.
- Simple meaning: rank which axes are mature vs which need validation.
- Limits: collected != verified; candidate evidence; Android security; license checks.
- Next recommended action: one concrete P0, e.g. create the Obsidian “Moufadal OS” vault before building dependent projects.
- Paths: index HTML, Markdown synthesis, QA notes, per-theme HTML.
- Rollback/reprise commands.

## Suggested file layout

```text
/opt/data/artifacts/moufadal-deep-research/<timestamp>/
  manifest.json
  index.html
  <theme-id>.html
  moufadal_deep_research_synthesis.md
  synthesis_summary.json
  qa_and_audit_notes.md
  local_link_check.json
  <theme-id>/
    theme_result.json
    runner_stdout.txt
    runner_stderr.txt
```

## Pitfalls discovered

- Generated reports can accidentally overstate confidence (“directly actionnable”, “corpus solide”). Run a final claim-tone audit and replace with “P0 recommendation / under validation” when appropriate.
- Long artifact paths must be styled with wrapping (`word-break: break-all`) in HTML.
- Browser may fail to navigate to a local HTTP server even when `curl` works; verify via `file://` browser navigation or curl rather than declaring render failure.
- Killing temporary HTTP servers after QA avoids orphaned processes.
