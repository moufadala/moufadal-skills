---
name: systematic-debugging
description: "Débogage par cause racine en 4 phases : comprendre le bug AVANT de le corriger. À utiliser pour toute panne technique — test qui échoue, bug en prod, comportement inattendu, build cassé, lenteur — surtout sous pression quand « un petit fix rapide » est tentant."
version: 1.0.0
license: MIT
platforms: [linux, macos, windows]
---

# Systematic Debugging

## Overview

Random fixes waste time and create new bugs. Quick patches mask underlying issues.

**Core principle:** ALWAYS find root cause before attempting fixes. Symptom fixes are failure.

**Violating the letter of this process is violating the spirit of debugging.**

## The Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

If you haven't completed Phase 1, you cannot propose fixes.

## When to Use

Use for ANY technical issue:
- Test failures
- Bugs in production
- Unexpected behavior
- Performance problems
- Build failures
- Integration issues

**Use this ESPECIALLY when:**
- Under time pressure (emergencies make guessing tempting)
- "Just one quick fix" seems obvious
- You've already tried multiple fixes
- Previous fix didn't work
- You don't fully understand the issue

**Don't skip when:**
- Issue seems simple (simple bugs have root causes too)
- You're in a hurry (rushing guarantees rework)
- Someone wants it fixed NOW (systematic is faster than thrashing)

## The Four Phases

You MUST complete each phase before proceeding to the next.

---

## Phase 1: Root Cause Investigation

**BEFORE attempting ANY fix:**

### 1. Read Error Messages Carefully

- Don't skip past errors or warnings
- They often contain the exact solution
- Read stack traces completely
- Note line numbers, file paths, error codes

**Action:** Use `read_file` on the relevant source files. Use `search_files` to find the error string in the codebase.

### 2. Reproduce Consistently

- Can you trigger it reliably?
- What are the exact steps?
- Does it happen every time?
- If not reproducible → gather more data, don't guess

**Action:** Use the `terminal` tool to run the failing test or trigger the bug:

```bash
# Run specific failing test
pytest tests/test_module.py::test_name -v

# Run with verbose output
pytest tests/test_module.py -v --tb=long
```

### 3. Check Recent Changes

- What changed that could cause this?
- Git diff, recent commits
- New dependencies, config changes

**Action:**

```bash
# Recent commits
git log --oneline -10

# Uncommitted changes
git diff

# Changes in specific file
git log -p --follow src/problematic_file.py | head -100
```

### 4. Gather Evidence in Multi-Component Systems

**WHEN system has multiple components (API → service → database, CI → build → deploy):**

**BEFORE proposing fixes, add diagnostic instrumentation:**

For EACH component boundary:
- Log what data enters the component
- Log what data exits the component
- Verify environment/config propagation
- Check state at each layer

Run once to gather evidence showing WHERE it breaks.
THEN analyze evidence to identify the failing component.
THEN investigate that specific component.

### 5. Trace Data Flow

**WHEN error is deep in the call stack:**

- Where does the bad value originate?
- What called this function with the bad value?
- Keep tracing upstream until you find the source
- Fix at the source, not at the symptom

**Action:** Use `search_files` to trace references:

```python
# Find where the function is called
search_files("function_name(", path="src/", file_glob="*.py")

# Find where the variable is set
search_files("variable_name\\s*=", path="src/", file_glob="*.py")
```

### Phase 1 Completion Checklist

- [ ] Error messages fully read and understood
- [ ] Issue reproduced consistently
- [ ] Recent changes identified and reviewed
- [ ] Evidence gathered (logs, state, data flow)
- [ ] Problem isolated to specific component/code
- [ ] Root cause hypothesis formed

**STOP:** Do not proceed to Phase 2 until you understand WHY it's happening.

---

## Phase 2: Pattern Analysis

**Find the pattern before fixing:**

### 1. Find Working Examples

- Locate similar working code in the same codebase
- What works that's similar to what's broken?

**Action:** Use `search_files` to find comparable patterns:

```python
search_files("similar_pattern", path="src/", file_glob="*.py")
```

### 2. Compare Against References

- If implementing a pattern, read the reference implementation COMPLETELY
- Don't skim — read every line
- Understand the pattern fully before applying

### 3. Identify Differences

- What's different between working and broken?
- List every difference, however small
- Don't assume "that can't matter"

### 4. Understand Dependencies

- What other components does this need?
- What settings, config, environment?
- What assumptions does it make?

---

## Phase 3: Hypothesis and Testing

**Scientific method:**

### 1. Form a Single Hypothesis

- State clearly: "I think X is the root cause because Y"
- Write it down
- Be specific, not vague

### 2. Test Minimally

- Make the SMALLEST possible change to test the hypothesis
- One variable at a time
- Don't fix multiple things at once

### 3. Verify Before Continuing

- Did it work? → Phase 4
- Didn't work? → Form NEW hypothesis
- DON'T add more fixes on top

### 4. When You Don't Know

- Say "I don't understand X"
- Don't pretend to know
- Ask the user for help
- Research more

---

## Phase 4: Implementation

**Fix the root cause, not the symptom:**

### 1. Create Failing Test Case

- Simplest possible reproduction
- Automated test if possible
- MUST have before fixing
- Use the `test-driven-development` skill

### 2. Implement Single Fix

- Address the root cause identified
- ONE change at a time
- No "while I'm here" improvements
- No bundled refactoring

### 3. Verify Fix

```bash
# Run the specific regression test
pytest tests/test_module.py::test_regression -v

# Run full suite — no regressions
pytest tests/ -q
```

### 4. If Fix Doesn't Work — The Rule of Three

- **STOP.**
- Count: How many fixes have you tried?
- If < 3: Return to Phase 1, re-analyze with new information
- **If ≥ 3: STOP and question the architecture (step 5 below)**
- DON'T attempt Fix #4 without architectural discussion

### 5. If 3+ Fixes Failed: Question Architecture

**Pattern indicating an architectural problem:**
- Each fix reveals new shared state/coupling in a different place
- Fixes require "massive refactoring" to implement
- Each fix creates new symptoms elsewhere

**STOP and question fundamentals:**
- Is this pattern fundamentally sound?
- Are we "sticking with it through sheer inertia"?
- Should we refactor the architecture vs. continue fixing symptoms?

**Discuss with the user before attempting more fixes.**

This is NOT a failed hypothesis — this is a wrong architecture.

---

## Red Flags — STOP and Follow Process

If you catch yourself thinking:
- "Quick fix for now, investigate later"
- "Just try changing X and see if it works"
- "Add multiple changes, run tests"
- "Skip the test, I'll manually verify"
- "It's probably X, let me fix that"
- "I don't fully understand but this might work"
- "Pattern says X but I'll adapt it differently"
- "Here are the main problems: [lists fixes without investigation]"
- Proposing solutions before tracing data flow
- **"One more fix attempt" (when already tried 2+)**
- **Each fix reveals a new problem in a different place**

**ALL of these mean: STOP. Return to Phase 1.**

**If 3+ fixes failed:** Question the architecture (Phase 4 step 5).

## Interactive HTML/dashboard QA pitfalls

When debugging a generated HTML dashboard or other static interactive artifact:

1. **Reproduce with a real browser, not only static HTML checks.** Use Playwright/CDP to click the actual buttons and inspect console/page errors.
2. **Scope selectors to the UI region under test.** If the same item is rendered in multiple places (`#top-now`, `#items`, reader panes), generic selectors like `[data-action="save"][data-id="..."]` can click only one duplicate and hide a broken region. Test each rendered zone explicitly.
3. **Verify both state and DOM.** For persistent actions (`Vu`, `Garder`, `Masquer`), assert localStorage/state *and* visible class/removal in every relevant container.
4. **Add a regression before fixing.** Example checks: click in the top section, confirm `.seen`/`.saved` appears there, then click hide and assert the item is gone from the top and from the full list.
5. **Do not claim “functional” from presence of buttons alone.** A button existing in HTML is not evidence; a successful browser click with DOM/state assertions is evidence.

## User-operated terminal sessions (copy/paste safety)

When the fix must be performed by the user in their own SSH/root terminal, treat command delivery as part of the debugging surface:

### Network tunnels, Docker, and firewall changes

When debugging user-operated SSH tunnels, reverse proxies, Docker host/container reachability, or firewall rules:

1. **Do not jump straight to firewall mutation.** First prove each boundary independently: client-side service listening, SSH forward accepted, host-side `curl`/TCP smoke test, then container-side reachability.
2. **Use authoritative docs before asking the user for risky host changes.** For Docker networking/firewall questions, validate against Docker docs (`DOCKER-USER`, bridge networking, host networking, iptables/nftables behavior). For SSH remote forwarding, validate against OpenSSH `ssh -R` and `GatewayPorts` docs.
3. **Prefer a host-side smoke test before Docker integration.** If a reverse SOCKS tunnel is bound on the VPS host, test from the host with `curl --socks5-hostname 127.0.0.1:<port> https://ifconfig.me` before diagnosing Docker. If this fails, the problem is tunnel/proxy/client-side; if it succeeds, Docker integration is a separate layer.
4. **Separate “tunnel accepted” from “proxy usable.”** `remote forward success` proves SSH forwarding only; it does not prove the local SOCKS process is running or that the egress IP is the intended mobile/residential IP.
5. **For Telegram/Termux users, ship corrected command bundles as `.txt` artifacts.** Include exact expected success strings and a short list of error strings to report; avoid making the user copy multi-line commands from chat formatting.
## User-operated terminal sessions (copy/paste safety)

When the fix must be performed by the user in their own SSH/root terminal, treat command delivery as part of the debugging surface:

1. **Prefer single-line commands or one complete fenced block.** Avoid heredocs (`<<'PY'`, `<<'SH'`) unless absolutely necessary; they are fragile over chat and can leave the user stuck at the shell continuation prompt (`>`).
2. **Separate phases when reliability matters:** install command first, wait for the prompt to return, then run a minimal verification command. Do not chain a complex install plus verbose introspection if the user is already fighting paste errors.
3. **Use minimal import/health checks first.** For Python module checks, start with `python3 -c 'import module; print("OK")'`. Only print versions after imports are known-good, and use defensive `getattr(mod, "__version__", "OK")` if version output is needed.
4. **Do not ask the user to paste or rerun traceback text as commands.** If the user accidentally pastes errors into the shell, reset the interaction with a single safe next command and explicitly say not to paste old traceback lines.
5. **Account for host vs container vs venv.** Always identify which Python is being tested (`host`, `container`, `venv`, `user site`) and give commands scoped to that environment. A dependency can be installed in one Python while missing in another.
6. **End by creating a durable check command only after the manual fix is verified.** The check should hide fragile details like `PYTHONPATH` and expose one simple command the user can reuse.
7. **For multi-boundary network chains, prove each boundary before fixing the next.** Example: phone proxy local → reverse tunnel listener on VPS host → host-side curl via proxy → container/Hermes access. If an earlier boundary fails, stop discussing later Docker/firewall fixes.
8. **If the user becomes fatigued by manual tunnel work, switch from debugging to alternatives.** Offer lower-friction routes (direct phone test, Tailscale exit node, paid proxy) instead of repeatedly asking for another SSH/socat/firewall command.

This is especially important for this user: they prefer grouped copy/paste commands with clear expected output and minimal manual editing.

This is especially important for this user: they prefer grouped copy/paste commands with clear expected output and minimal manual editing.

Reference: `references/phone-socks-reverse-ssh-docker-bridge.md` captures the reverse-SSH phone SOCKS + Docker bridge pattern, including the common `ssh -D` wrong-direction pitfall, Termux logging issues, and the verification contract.

Reference: `references/tailscale-exit-node-boundary-proof.md` captures the Tailscale Android exit-node proof order: phone state, VPS `ExitNodeOption`, default routes, direct-vs-SOCKS IP, then scraper launch with explicit proxy.

Reference: `references/pc-remote-control-tailscale-outage-2026-07-09.md` captures the recovery pattern for a reachable PC whose Claude Code Remote Control and Chrome Remote Desktop are down: prove Tailscale reachability separately from execution capability, probe safe ports, avoid destructive network resets, and use Taildrop to deliver PowerShell diagnostic/repair scripts when no shell is available.

Reference: `references/tailscale-taildrop-windows-helper-recovery.md` captures the user-helper version of the same class: Taildrop can deposit files but not execute/delete them remotely; on Windows tell the helper to look in Downloads/Desktop, send a single human-friendly `.bat` launcher plus the underlying `.ps1`, and give exact double-click/UAC instructions.

Reference: `references/windows-taildrop-remote-pc-recovery.md` captures the consolidated remote Windows PC recovery pattern: distinguish Tailscale reachability from control-channel availability, avoid overcomplicated helper instructions, use one-click `.bat` launchers, account for Taildrop Downloads/Desktop placement, and handle Claude Code Remote Control `.bat` pitfalls such as `call claude` and keeping pairing output visible.

Reference: `references/windows-tailscale-taildrop-openssh-rescue-2026-07-09.md` captures the Windows PC rescue escalation when one-click repair is insufficient and temporary SSH is needed: Taildrop is delivery-only, use one ASCII `.cmd` launcher, install OpenSSH with a dedicated key and Tailscale-only firewall, treat `22:OPEN` as only service proof, and fix Windows `authorized_keys`/ACL issues before reinstalling.

Reference: `references/windows-tailscale-ssh-rescue-remote-pc.md` captures the later lesson from the same class: if helper fatigue appears, stop micro-iteration and send one self-contained ASCII launcher; prefer a dedicated non-admin `hermes_rescue` account with `Match User` and a ProgramData authorized_keys file; after SSH works, prove general outbound Internet before blaming Claude/Google.

### Windows/Taildrop helper-file pitfalls

When a non-technical local helper must run a repair file on Windows:

1. **Ship one obvious ASCII launcher.** Prefer names like `CLIQUE_ICI_REPARER_PC.cmd`; avoid accents, apostrophes, long sentimental names, and multiple similar files. Send `.ps1` payloads only as dependencies, not as the file to click.
2. **Never ask the helper to open a `.ps1` directly.** It may open in VS Code Restricted Mode instead of executing. Use a `.cmd`/`.bat` wrapper that starts elevated PowerShell and keeps windows/logs open.
3. **If Windows asks “choose an application,” reset the instruction.** They likely clicked the wrong file or extension association is broken: tell them to click the `.cmd` launcher, right-click → Open/Run as administrator, or choose `C:\Windows\System32\cmd.exe`.
4. **For Claude Code recovery on Windows, use `call claude ...` inside batch files.** NPM-installed `claude` is often `claude.cmd`; without `call`, the script can stop after the first Claude command.
5. **Port-open is not success.** For Windows OpenSSH, `22:OPEN` plus `Permission denied (publickey,...)` means service/firewall are working but key placement/permissions or username are wrong. Check `%USERPROFILE%\.ssh\authorized_keys`, `%ProgramData%\ssh\administrators_authorized_keys`, and strict ACLs before reinstalling.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Issue is simple, don't need process" | Simple issues have root causes too. Process is fast for simple bugs. |
| "Emergency, no time for process" | Systematic debugging is FASTER than guess-and-check thrashing. |
| "Just try this first, then investigate" | First fix sets the pattern. Do it right from the start. |
| "I'll write test after confirming fix works" | Untested fixes don't stick. Test first proves it. |
| "Multiple fixes at once saves time" | Can't isolate what worked. Causes new bugs. |
| "Reference too long, I'll adapt the pattern" | Partial understanding guarantees bugs. Read it completely. |
| "I see the problem, let me fix it" | Seeing symptoms ≠ understanding root cause. |
| "One more fix attempt" (after 2+ failures) | 3+ failures = architectural problem. Question the pattern, don't fix again. |

## Quick Reference

| Phase | Key Activities | Success Criteria |
|-------|---------------|------------------|
| **1. Root Cause** | Read errors, reproduce, check changes, gather evidence, trace data flow | Understand WHAT and WHY |
| **2. Pattern** | Find working examples, compare, identify differences | Know what's different |
| **3. Hypothesis** | Form theory, test minimally, one variable at a time | Confirmed or new hypothesis |
| **4. Implementation** | Create regression test, fix root cause, verify | Bug resolved, all tests pass |

## Hermes Agent Integration

### Remote Terminal Copy/Paste Pitfalls

When guiding the user to paste commands into a remote VPS shell, prefer **single-line, minimal commands** over heredocs unless the heredoc is absolutely necessary. In Telegram/SSH workflows, users commonly paste partial blocks or interrupt with `Ctrl+C`; an unterminated heredoc leaves Bash at the secondary `>` prompt and makes the session feel broken.

Rules for this class of debugging:

1. First get the user back to a clean prompt (`Ctrl+C` if they are at `>`).
2. Give one command at a time when the user is manually pasting into SSH.
3. For Python import checks, avoid verbose version-printing unless needed; use the smallest proof:
   ```bash
   python3 -c 'import bs4, requests, playwright, curl_cffi, httpx, yaml; print("IMPORTS_OK")'
   ```
4. If versions are needed, use `__version__`, not `.version`.
5. If a user interrupts an install with `Ctrl+C`, assume the install did not complete; rerun the install separately before testing.
6. When root is logged into the host but Hermes runs as another user/container, verify whether the dependency is needed in the host Python or the Hermes runtime; avoid assuming `--user` installs into the same site-packages.

### Investigation Tools

Use these Hermes tools during Phase 1:

- **`search_files`** — Find error strings, trace function calls, locate patterns
- **`read_file`** — Read source code with line numbers for precise analysis
- **`terminal`** — Run tests, check git history, reproduce bugs
- **`web_search`/`web_extract`** — Research error messages, library docs

### With delegate_task

For complex multi-component debugging, dispatch investigation subagents:

```python
delegate_task(
    goal="Investigate why [specific test/behavior] fails",
    context="""
    Follow systematic-debugging skill:
    1. Read the error message carefully
    2. Reproduce the issue
    3. Trace the data flow to find root cause
    4. Report findings — do NOT fix yet

    Error: [paste full error]
    File: [path to failing code]
    Test command: [exact command]
    """,
    toolsets=['terminal', 'file']
)
```

### With test-driven-development

When fixing bugs:
1. Write a test that reproduces the bug (RED)
2. Debug systematically to find root cause
3. Fix the root cause (GREEN)
4. The test proves the fix and prevents regression

## Real-World Impact

From debugging sessions:
- Systematic approach: 15-30 minutes to fix
- Random fixes approach: 2-3 hours of thrashing
- First-time fix rate: 95% vs 40%
- New bugs introduced: Near zero vs common

**No shortcuts. No guessing. Systematic always wins.**
