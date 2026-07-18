# Session 2026-07-03 — Known-context activation failure

## Trigger

Moufadal corrected Hermes after an Android/S25 debugging exchange. The immediate technical issue was ADB Wireless Debugging requiring Wi-Fi while he was outside, but the real complaint was broader: Hermes had already researched/documented likely blockers and next paths, yet let him rediscover the blocker instead of proactively guiding from existing knowledge.

## Failure mode

Do not misclassify this as only a domain-specific Android skill gap. The class-level failure is:

- knowledge exists in memory/Obsidian/artifacts/skills;
- the user starts an action inside that known territory;
- Hermes answers the local symptom instead of activating the prior research, known failure modes, and next-best path.

Common names/frames:

- knowledge activation failure;
- failure to reuse lessons learned;
- context engineering / agentic memory retrieval problem;
- lessons-learned system gap.

## Correct durable response

1. Patch the class-level skill governing review/routing/recovery first.
2. Add or patch a domain skill only if it still improves that domain.
3. Update user memory if the correction expresses a stable interaction preference.
4. If a deep library cleanup is needed, run Skill Creator/SkillOps as a background pass with snapshots and approval-needed for destructive consolidation.

## What happened in this session

- A first patch was made to `android-remote-control`; useful but too local.
- The broader preference was then saved in user memory: previously researched/documented topics should be activated proactively with steps, blockers, community issues, and best path.
- `project-skill-router` gained a Known Context Check.
- A background Skill Creator deep pass was launched with snapshots, safe reversible fixes, SkillOps gates, P4-lite smoke, and Claude read-only critique.

## Future checklist

When the user says an issue was already researched, or implies “we knew this would happen”:

- search/inspect known context before prescribing more steps;
- tell Moufadal what was already known, what is new, and what path should replace the fragile one;
- avoid apologizing only; patch the class-level skill that failed;
- do not create a narrow one-session skill unless no umbrella exists.
