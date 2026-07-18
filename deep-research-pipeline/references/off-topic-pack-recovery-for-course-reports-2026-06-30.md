# Off-topic DeepResearch pack recovery for course/report deliverables — 2026-06-30

## Context

During an overnight/premium research-course job about controlling a Galaxy S25 with Hermes Agent, the local DeepP0 runner produced some packs whose superficial metrics looked good (`fetched_ok`, notes, PASS) but the actual evidence was off-topic GitHub issue noise (for example unrelated issue numbers caused by terms like `2026`, `Android 15`, etc.). Some packs had zero sources, while a Claude critique lane also ended with `error_max_turns`.

The deliverable still needed a high-quality HTML/Markdown course by wake-up, so the correct recovery was not to trust the runner PASS and not to declare failure prematurely. Hermes recovered by reading the reports, identifying noise, fetching direct authoritative sources, and clearly documenting the limitation in QA.

## Durable lesson

For premium/course reports, **metrics are not enough**. A pack can have fetched pages and notes while being substantively useless. Always inspect the top source titles and representative evidence notes before using them.

## Recovery pattern

1. Read the contract, manifest, run log, pack paths, raw outputs, GitHub JSON, and critique artifacts.
2. Open each `research_report.md` for the key packs; inspect:
   - top source titles/domains;
   - whether evidence notes actually mention the topic;
   - `sources_collected`, `fetched_ok`, and `notes` together, not alone.
3. If packs are off-topic or empty, mark them as weak/noisy and recover with direct source retrieval:
   - official docs first;
   - GitHub project repos/readmes;
   - arXiv/papers for research claims;
   - vendor docs for device-specific claims;
   - pragmatic tooling docs for alternatives.
4. Keep the report synthesis anchored to recovered authoritative sources, not to the noisy pack notes.
5. In `QA_REPORT.md`, explicitly state:
   - which automated pack evidence was noisy or incomplete;
   - which direct sources replaced it;
   - what QA was actually run;
   - what remains unverified.
6. Do not claim runtime/product completion when only the report/course artifact is complete.

## Example source classes used in the Android/Hermes course recovery

- Android official: ADB, AccessibilityService, UI Automator, background tasks, Android Enterprise/Management API.
- Tool repos/docs: scrcpy, Shizuku docs/GitHub, Termux/proot-distro.
- Device/vendor: Samsung Galaxy S25 official page, Android 15 enterprise docs.
- Pragmatic automation: Tasker, MacroDroid, Home Assistant Companion notification commands, Tailscale docs.
- Research state of the art: AutoGLM, Mobile-Agent, AppAgent, AndroidWorld arXiv/GitHub.

## Pitfalls

- Do not treat `fetched_ok: true` as evidence quality.
- Do not use irrelevant GitHub issue pages just because source scoring says trust is high.
- Do not hide the recovery: say that the initial automated pack was noisy and cite the stronger replacement sources.
- If browser QA fails due local/CDP availability, do not hard-code “browser broken”; record the alternative QA actually performed (HTML parser, tokens, section counts, link counts, file sizes) and leave visual QA as a remaining limit.
