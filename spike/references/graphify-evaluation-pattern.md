# Graphify evaluation pattern for coding-agent context tools

Use this reference when spiking a codebase-context/navigation tool such as Graphify before adding it to a permanent Hermes/Claude/Codex stack.

## Core lesson

Do not judge a code-context tool by install success or README claims. Validate it on real local corpora with:

- non-destructive execution (`uvx` or temp venv, no global install/hooks first);
- code-only mode first to preserve the “no extra LLM/token cost” value proposition;
- artifact capture (`results.json`, `REPORT.md`, generated graph/report/html);
- realistic natural-language queries from the user’s workflows;
- at least one negative/control case where the tool should not help;
- independent critique before recommending stack adoption.

## Recommended spike contract

1. **No global mutation first**
   - Do not run platform installers or hooks until the tool proves value.
   - For Graphify specifically, avoid these during evaluation:
     - `graphify install --platform hermes`
     - `graphify install --platform claude`
     - `graphify hook install`

2. **Create mirrors, not edits**
   - Copy candidate source files to an artifact directory, excluding dependencies/build/downloads.
   - Exclude common noise: `.git`, `node_modules`, `.venv`, `venv`, `__pycache__`, `.cache`, `dist`, `build`, `.next`, `.pytest_cache`, `graphify-out`, `artifacts`, `screenshots`, `downloads`, `tmp`, `cache`, `browsers`, `playwright-browsers`.

3. **Start code-only**
   - Include source extensions such as `.py`, `.js`, `.jsx`, `.ts`, `.tsx`, `.sh`, `.sql`, `.toml`, etc.
   - Be careful with `.yaml`, `.json`, `.html`, `.css`: Graphify may classify them as docs and require an LLM key. If the point is local/no-token operation, exclude them in the first pass.

4. **Measure more than “it ran”**
   Capture:
   - code files copied;
   - extract and cluster timings;
   - nodes/links counts;
   - output size;
   - benchmark output;
   - `GRAPH_REPORT.md` size/head;
   - query hit rate for workflow-specific prompts;
   - false negatives in `affected` / impact commands.

5. **Use threshold-based adoption**
   Graph/navigation tools are often not worth it for small projects. A practical gate from the 2026-06-21 Graphify spike:
   - `<20` real code files: usually skip; direct file reading is simpler.
   - `20–50` files: use only if the project is dense or unfamiliar.
   - `≥50` Python/Shell files: worthwhile to test as a pre-step for Claude/Codex reconnaissance.

## Graphify-specific findings from the session

Graphify `0.8.44` via `uvx --from graphifyy graphify` worked on the VPS in code-only mode.

Observed useful case:

- `/opt/data/scripts`
  - 143 code files
  - 857 nodes / 1357 links
  - extract+cluster around 2 seconds
  - generated compact `GRAPH_REPORT.md`
  - workflow queries such as “youtube transcript proxy”, “morning brief dashboard”, and “tailscale socks proxy” found relevant files/functions.

Observed weak cases:

- Small projects with 4–10 real code files produced graphs but few useful query hits.
- Simple frontend/JSX landing-style projects did not justify the extra layer.
- `graphify affected` on a shell script returned no affected nodes; treat shell impact analysis as incomplete and do not use it as proof of no impact.

## Adoption recommendation pattern

For Graphify-like tools, final recommendations should distinguish:

- **punctual scanner**: OK for large/unfamiliar code corpora;
- **permanent stack layer**: only if repeated spikes prove value;
- **global install/hooks**: avoid until there is strong evidence and a rollback plan.

Suggested wording:

> Use as a temporary reconnaissance scanner for large corpora, not as a mandatory Hermes/Claude/Codex layer. Keep invocation via `uvx` and artifacts until a real multi-file refactor proves repeatable value.
