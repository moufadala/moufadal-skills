# DeepSearch background-completion recovery pattern — 2026-06-29

## When this applies

Use this when a long DeepSearch / benchmark / overnight orchestrator reports completion through a background-process notification, especially if the run included Claude audit tasks, resume crons, or a later fixed-run benchmark.

## Durable lesson

A completed background process is only a **signal to inspect artifacts**, not proof that the research module is validated. Treat the notification as a handoff and rebuild the truth from files/processes/cron state.

## Recovery checklist

1. **Locate the canonical artifact root** from the completed command or `latest_*.txt` pointer.
2. **Read summary and rows files directly**:
   - `benchmark/summary.json` / `results.jsonl` for matrix runs;
   - `benchmark_summary_partial.json` / `benchmark_summary_final.json` / `benchmark_rows_*.json` for V2 A/B runs.
3. **Classify the run honestly**:
   - If Claude final audit ended `error_max_turns`, say the audit did not complete.
   - If the run started before a patch/fixed runner, use it as throughput/execution evidence only.
   - If final summary is missing, report current partial progress, not success.
4. **Build a deterministic audit artifact** when LLM audit failed:
   - parse rows;
   - count distinct queries, OK rows, complete rows, failed/partial rows;
   - compute average sources, fetch attempts, fetched OK, snippet-only evidence, notes, final answer chars;
   - write `*_deterministic_audit.json` and `.md/.html` beside the run.
5. **Run a compact one-turn Claude critique** over the deterministic JSON if useful. Keep the prompt small and `--max-turns 1`; the purpose is critique, not another long audit loop.
6. **Check and prune stale resume jobs**. If a resume cron is now obsolete or already errored after the main run completed, remove it instead of letting it collide with the fixed benchmark.
7. **Verify the fixed/current benchmark separately**. If a newer V2/fixed 60-query job is scheduled or running, track that artifact root and do not let the older completed run stand in for it.

## Specific bug pattern observed

A DeepResearch V2 row crashed with:

```text
NameError: name 'urlparse' is not defined. Did you mean: 'argparse'?
```

The durable fix is not to import a new bare `urlparse`; use the existing module import consistently:

```python
import urllib.parse
urllib.parse.urlparse(url)
```

Then compile the runner and benchmark script before relaunching:

```bash
PYTHONPYCACHEPREFIX=/tmp/pycache-deepfix python3 -m py_compile \
  /opt/data/scripts/deep_research_v2.py \
  /opt/data/scripts/research_stack_benchmark_v2_ab.py
```

## Reporting language

Use this wording discipline:

- ✅ “run exécuté / throughput prouvé / artefacts présents”
- ✅ “benchmark V2 corrigé en cours : X/60 requêtes”
- ❌ not “module validé” until the current fixed runner has `benchmark_summary_final.json`, non-zero evidence metrics, complete checks, and a final audit.

## Anti-pitfalls

- Do not trust a truncated process notification as the complete log.
- Do not equate `exit_code=0` with research-quality validation.
- Do not reuse a pre-patch benchmark as proof for a post-patch implementation.
- Do not leave stale resume crons alive when they can duplicate/collide with the canonical run.
