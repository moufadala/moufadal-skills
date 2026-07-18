# Session 2026-07-12 — Skill source-of-truth and Hermes external dirs

## Trigger

Moufadal asked for a read-only factual report to decide how to avoid drift between skills that exist both as Hermes-native local skills and as neutral portable `SKILL.md` files in a git repo such as `moufadal-skills`.

## Durable lesson

Before recommending a zero-copy skill architecture, inspect Hermes' actual skill-loading mechanism and collision behavior. Do not assume a git repo can simply be cloned into the local skills tree without drift risk.

## Findings captured from the session

- Hermes' active skills root on this VPS was `/opt/data/skills`, resolved from `HERMES_HOME=/opt/data` and `get_skills_dir() = get_hermes_home() / "skills"`.
- Hermes skills use the Agent-Skills-style package shape: a directory containing `SKILL.md` with YAML frontmatter (`name`, `description`, etc.) and optional `references/`, `templates/`, `scripts/`, `assets/` support dirs.
- Config supports additional skill sources through:

```yaml
skills:
  external_dirs: []
```

- Code path observed: local skills are scanned first, then `skills.external_dirs`.
- `skill_view()` has collision detection: if a bare name matches multiple `SKILL.md` candidates across local and external dirs, it refuses to guess and reports an ambiguous skill name.
- `skills_sync` indexes `external_dirs` to avoid shadowing externally-delegated skills when bundled/local sync runs.

## Practical decision rule

For a shared source of truth:

1. If a skill is mostly neutral and can be owned by the repo, use `skills.external_dirs` and remove/disable the same local active name to avoid collisions.
2. If a Hermes-local skill is strongly coupled to Moufadal/VPS/Hermes paths, tools, Telegram, cron, Claude/Codex, or `/opt/data`, prefer a thin Hermes-specific wrapper/layer above the neutral base rather than replacing it blindly.
3. Never create a VPS clone of a repo merely to satisfy an audit check when the architecture says the PC/repo is the source of truth. Absence of a clone can be expected.

## What to patch next time

- Protected `hermes-agent` would be the natural home for public Hermes mechanics, but bundled/protected skills must not be edited.
- Use this `conversation-to-skill-review` reference when the task is about skill-library drift, source-of-truth decisions, or deciding whether to patch local skills versus external repo skills.

## Pitfalls

- Treating `external_dirs` as collision-free. It is configurable, but duplicate active `name:` values can create ambiguity.
- Treating zero-copy as automatically better. For Moufadal's operational skills, many local skills contain environment-specific procedures and should remain local overlays unless deliberately refactored.
- Capturing transient missing-repo state as a red error. The durable rule is about source-of-truth architecture, not local clone presence.
