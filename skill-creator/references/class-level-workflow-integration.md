# Class-level workflow integration from external skill libraries

Use this reference when Moufadal asks to make lessons from one project or an external skill library available across all future projects.

## Durable pattern

1. Audit overlaps first: list existing umbrella skills that already cover the new behavior.
2. Prefer patching those umbrellas over creating many one-off skills.
3. Create a new class-level skill only when no umbrella exists.
4. Put session-specific evidence, transcripts, external-library notes, and dated decisions in `references/`, not directly in the main SKILL.md.
5. Add or update trigger evals after the patch. A workflow is not integrated until routing is tested.
6. Report both the integration decision and the verification result.

## Useful GStack-style concepts to adapt, not blindly import

- Careful/guard/freeze -> one safety umbrella for destructive and production-affecting actions.
- Ship -> GitHub PR/CI/merge workflow, not a separate project-specific skill.
- Review -> existing code-review umbrella with security families such as OWASP/STRIDE.
- Office-hours / pre-build questioning -> product gate in the serious-project umbrella.
- Land/deploy -> post-deploy runtime verification in professional delivery.

## SkillOps P4-lite golden-set schema reminder

The runner expects a JSON object with `items`. Human-validated golden items use fields like:

```json
{
  "items": [
    {
      "id": "example-p1",
      "query": "ship this change: push a PR and watch CI",
      "expected_skill": "github-pr-workflow",
      "reason": "GitHub shipping workflow",
      "validated_by_human": true,
      "must_not_trigger": ["careful-guard"]
    }
  ]
}
```

Do not write a free-form list of `{skill, expected}` rows unless the runner explicitly supports that format.

## Reporting standard

For Telegram, give a short verdict and link to artifacts. Keep raw eval JSON/logs in artifacts. Mention limitations honestly: skills are routing instructions, not hard runtime hooks, unless a real hook/runner exists.
