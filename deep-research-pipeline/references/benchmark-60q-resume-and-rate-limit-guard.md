# 60-query benchmark resume + rate-limit guard

Session lesson: when resuming a Deep Research benchmark, distinguish diagnostic smoke checks from the actual benchmark objective.

## Durable pattern

For the 50–60 distinct-query benchmark, the run should be crash-safe and continue collecting rows even when optional channels are degraded.

### Guardrails

- A P0 smoke test that depends on Exa/Jina/search availability is **diagnostic**, not a hard precondition for the 60-query benchmark.
- If Exa/MCP returns repeated 429/rate-limit failures, record those rows as failed for the Exa-only method, but do not abort the whole benchmark by default.
- Only abort on consecutive Exa failures when explicitly requested, e.g. `DEEP_RESEARCH_ABORT_ON_EXA_FAILURES=1`.
- Preserve partial artifacts continuously: `rows_partial.json`, `benchmark_report_partial.md/html`, logs.
- Report honestly: external channel failure is a benchmark finding, not proof the research module is finished or broken.

## Wrapper script pattern

In a benchmark wrapper, use:

```bash
PYTHONPYCACHEPREFIX=/tmp/hermes_pycache python3 /opt/data/tests/test_deep_research_runner.py || \
  echo "WARN: P0 smoke failed; continuing benchmark because this is expected when Exa is rate-limited"
```

Then run the real benchmark.

## Python abort gate pattern

```python
if exa_failures >= 5 and os.environ.get('DEEP_RESEARCH_ABORT_ON_EXA_FAILURES') == '1':
    write_reports(out_root, rows, queries, started_iso, final=False)
    raise SystemExit('Aborting: 5 consecutive Exa/mcporter failures, likely quota or service outage')
```

Default behavior: continue and encode failures in rows/summary.

## Recovery checklist

1. Inspect the handoff/progress file.
2. Check whether the process is running and whether partial rows are advancing.
3. If the job exited early before reports, inspect whether a diagnostic preflight failed before the benchmark started.
4. Patch wrapper/preflight so optional-channel failures do not mask the benchmark objective.
5. Relaunch in background with completion notification and write a resume note with process id, log path, output root, and rollback patch.
