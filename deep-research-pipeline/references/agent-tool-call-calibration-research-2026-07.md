# Agent tool-call calibration research — source separation lesson (2026-07)

## Context

Moufadal asked for a deep research pass on whether other people/systems face the same problem: Hermes deciding when external internet search is justified, learning from human feedback, and knowing when to escalate to a heavier review.

## Key lesson

Separate two neighboring questions before synthesis:

A. **Search-first / build-vs-buy before coding** — avoid reinventing code, templates, plugins, workflows, or architectures that already exist.

B. **Tool-use / web-search calibration** — decide whether the agent should call an external tool/search now, given uncertainty, utility, cost, latency, and noise.

A source about A does not prove B. If the user's real concern is “when do you launch internet?”, use B sources first and treat A sources as supporting context only.

## Strong sources for B

- `Position: Agent Should Invoke External Tools ONLY When Epistemically Necessary` — https://arxiv.org/html/2506.00886v2
  - Normative criterion: call external tools only when the task cannot be completed reliably via internal reasoning over current context.
- `LLM Agents Already Know When to Call Tools - Even Without Reasoning` / When2Tool — https://arxiv.org/html/2605.09252 and https://github.com/Trustworthy-ML-Lab/when2tool
  - Agents call tools too often; unnecessary calls cost latency/API fees. Hidden-state signal of tool necessity is linearly decodable; Probe&Prefill reduced tool calls substantially in their setting.
- `To Call or Not to Call: A Framework to Assess and Optimize LLM Tool Calling` — https://arxiv.org/pdf/2605.00737
  - Use necessity, utility, and affordability as the decision dimensions for web-search/tool calls.
- `SMARTCAL` — https://aclanthology.org/2024.emnlp-industry.59.pdf
  - Tool-abuse / overconfidence; self-aware calibration and multi-agent/self-verification improve tool-use reliability.
- `The Confidence Dichotomy` — https://arxiv.org/pdf/2601.07264
  - Evidence tools like web search can increase overconfidence because retrieved information is noisy; deterministic verification tools ground reasoning better.

## Useful eval/tooling sources

- Braintrust agent evals — https://www.braintrust.dev/docs/best-practices/agents
- LangSmith evaluation — https://docs.langchain.com/langsmith/evaluation
- DeepEval ToolCorrectnessMetric — https://deepeval.com/docs/metrics-tool-correctness
- Promptfoo skill testing — https://www.promptfoo.dev/docs/guides/test-agent-skills
- Anthropic skill best practices — https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices

## Search-first/build-vs-buy sources for A

- `shimo4228/search-first` — https://github.com/shimo4228/claude-skill-search-first
- `mturac/skill-hunter` — https://github.com/mturac/skill-hunter

Treat these as evidence that people encode search-before-build as agent skills, but not as primary evidence for live web-search routing.

## Recommended Hermes framing

Before external web search, briefly evaluate:

```text
Necessity: can I answer reliably from current context/local artifacts?
Utility: will external search likely improve correctness materially?
Affordability: is the cost/latency/noise justified for this task?
```

If the answer is unclear and the decision is high-risk, propose level 3: independent Claude critique + second search/research loop + report.

## Critique-lane pitfall

In this session, Claude Code correctly identified that the first research pack under-fetched two high-value sources and mixed A/B. When a critique lane identifies a missing high-relevance source, fetch it before final synthesis; do not defend the initial pack.
