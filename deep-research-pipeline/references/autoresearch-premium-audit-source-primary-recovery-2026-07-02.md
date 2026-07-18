# AutoResearch Premium audit — source-primary recovery pattern (2026-07-02)

Use this when a Premium Research / AutoResearch audit relies on external descriptions of `karpathy/autoresearch` or similar agent-loop repos.

## Lesson

A DeepResearch runner may discover the right GitHub source but fail to fetch it through the web fetch path (example: HTTP 451 on `github.com/karpathy/autoresearch` pages). Do **not** leave the synthesis supported only by DeepWiki/blog/community mirrors if the repo itself can still be cloned.

## Recovery sequence

1. Keep the DeepResearch pack as discovery/evidence material.
2. Attempt source-primary recovery outside the fetcher:

```bash
git clone --depth 1 https://github.com/karpathy/autoresearch.git <run_dir>/external/autoresearch
git -C <run_dir>/external/autoresearch rev-parse HEAD
```

3. Extract the specific primary-source lines needed for the claim into a dated artifact, e.g. `SOURCE_PRIMARY_RECOVERY.md`:

```bash
grep -nE 'run|agent|score|commit|reset|improve|experiment|benchmark|val_bpb|time' README.md | head -80
grep -nE 'score|commit|reset|rollback|improve|worse|val_bpb|branch|time|experiment' program.md | head -120
```

4. Patch the final report to distinguish:
   - runner/web-fetch failure (`HTTP 451`) as a retrieval limitation;
   - successful source-primary clone as the stronger proof for implementation details.

## Claims verified in the session

For `karpathy/autoresearch` commit `228791fb499afffb54b46200aca536f79142f117`, primary files confirmed:

- `README.md`: agent modifies `train.py`, fixed 5-minute experiments, metric `val_bpb`, approx. 12 experiments/hour and ~100 overnight.
- `program.md`: `prepare.py` is read-only; experiment loop commits before running; reads `val_bpb` / `peak_vram`; logs `results.tsv`; keeps commit if `val_bpb` improves; resets if equal/worse; timeout >10 min counts as failure; autonomous loop should not pause after launch.

## Pitfall

Do not say “repo inaccessible” as a final limitation until clone/mirror recovery has been attempted. The durable lesson is **source-primary recovery after web-fetch failure**, not “GitHub is unavailable”.
