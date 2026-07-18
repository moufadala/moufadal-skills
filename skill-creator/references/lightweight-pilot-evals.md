# Lightweight pilot evals for skills

Use this when a session produces a proposed skill improvement but the change should be validated before broad edits.

## Pattern

1. Pick 2–3 class-level skills, not a random long list.
2. Write 2 realistic prompts per skill.
3. For each prompt, write 4–6 verifiable expectations that check the doctrine the skill is supposed to encode.
4. Run paired outputs:
   - `with_skill`: prompt plus the relevant SKILL.md guidance.
   - `without_skill`: same prompt with general instructions only.
5. Save each output under a workspace shaped like Skill Creator eval output:
   - `eval-XX-name/with_skill/outputs/response.md`
   - `eval-XX-name/with_skill/grading.json`
   - `eval-XX-name/without_skill/outputs/response.md`
   - `eval-XX-name/without_skill/grading.json`
6. Create `benchmark.json` using Skill Creator's benchmark schema:
   - `runs[].configuration` must be exactly `with_skill` or `without_skill`.
   - `runs[].result.pass_rate` must be nested under `result`.
7. Generate a static review page:

```bash
python3 /opt/data/skills/software-development/skill-creator/eval-viewer/generate_review.py \
  "$WORKSPACE" \
  --skill-name "Pilot skills: ..." \
  --benchmark "$WORKSPACE/benchmark.json" \
  --static "$OUT/pilot-evals-review.html"
```

8. Open the viewer and verify:
   - Outputs tab shows only the human-readable `response.md`, not raw JSON blobs.
   - Benchmark tab shows pass rate, time, tokens and per-eval breakdown.
   - Feedback textarea and next/previous navigation are usable.

## Pitfalls

- Do not let raw Claude CLI JSON dominate the viewer. Store `raw_result.json` outside `outputs/` or it will be embedded as a giant output file.
- Treat heuristic keyword grading as a pilot signal, not statistical truth.
- Prefer small targeted patches from the failed expectations; do not rewrite the whole skill library because one pilot found gaps.
- A skill that improves pass rate but costs more tokens can still be worthwhile if it prevents expensive wrong directions, especially for Hermes/Claude orchestration and tool-sprawl decisions.

## Good output

A useful pilot produces:

- `evals/evals.json` or equivalent prompt/assertion set;
- individual responses for review;
- `benchmark.json`;
- `benchmark.md` summary;
- static viewer HTML;
- a short recommendation: patch, keep, or retire.
