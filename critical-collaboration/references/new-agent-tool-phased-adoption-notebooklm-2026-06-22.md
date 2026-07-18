# New agent-tool phased adoption — NotebookLM example (2026-06-22)

Use this as a concrete reference when evaluating/installing a new agent-facing research tool without creating tool-sprawl.

## Context

The user wanted to install `notebooklm-py` before continuing a broader backlog. The VPS uses Python 3.13, PEP 668, and `uv` is available. The tool is unofficial and has optional browser/cookies/MCP features.

## Pattern that worked

1. **Research current package status first**
   - PyPI/GitHub showed `notebooklm-py` latest `0.7.2`, Python `>=3.10`, unofficial Google NotebookLM API, beta status.
   - Installation docs recommend isolated CLI install on Debian/Ubuntu: `uv tool install "notebooklm-py[browser]"`.

2. **Install isolated base + browser extra only**
   ```bash
   uv tool install "notebooklm-py[browser]"
   ```
   Result: installed CLI `notebooklm`, package `notebooklm-py==0.7.2`, Playwright dependency.

3. **Verify without claiming auth readiness**
   ```bash
   /opt/data/home/.local/bin/notebooklm --version
   /opt/data/home/.local/bin/notebooklm --help
   /opt/data/home/.local/bin/notebooklm doctor --json || true
   /opt/data/home/.local/bin/notebooklm auth check --json || true
   ```
   Expected pre-login state: CLI works, but auth fails because `~/.notebooklm/profiles/default/storage_state.json` does not exist.

4. **Fix shell discovery without global/system pip**
   ```bash
   uv tool update-shell
   bash -lc 'command -v notebooklm && notebooklm --version'
   ```
   On this VPS, a fresh login shell found `/opt/data/home/.local/bin/notebooklm`.

5. **Install bundled agent skill after CLI verification**
   ```bash
   notebooklm skill install
   notebooklm skill status
   ```
   Verified user-scope skill paths:
   - `/opt/data/home/.claude/skills/notebooklm/SKILL.md`
   - `/opt/data/home/.agents/skills/notebooklm/SKILL.md`

6. **Defer fragile or expanding features**
   - Do **not** install `[cookies]` by default on Python 3.13 because `rookiepy` is known fragile there.
   - Do **not** configure MCP immediately unless the user has a concrete workflow that needs it.
   - Treat Google login as a separate user-present step:
     ```bash
     notebooklm login
     notebooklm auth check --test --json
     ```
     Require `status: ok` and token fetch success before saying it is authenticated.

## Decision language

Good final wording:

- “Installed and CLI verified.”
- “Agent skill installed and status verified.”
- “Not authenticated yet; login requires the user’s Google session.”
- “Skipped cookies/MCP intentionally to avoid tool-sprawl until the base tool proves useful.”

Avoid:

- “NotebookLM is ready” when auth is absent.
- Global `pip install` on PEP 668 systems.
- Installing every extra just because it exists.
