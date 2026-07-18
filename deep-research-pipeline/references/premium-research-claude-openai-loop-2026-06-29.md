# Premium Research loop — Claude + OpenAI Deep Research

Session learning date: 2026-06-29

## Trigger

When Moufadal says **“recherche premium”**, DeepResearch must not be treated as a normal Hermes web search. It means a multi-lane research workflow:

1. **Hermes / local DeepResearch lane**
   - Frame the research contract and acceptance criteria.
   - Run the local auditable pipeline: Agent Reach/Exa, SearXNG breadth, GitHub/community/specialist channels where relevant.
   - Fetch key pages, dedupe, score source trust, preserve weak/snippet-only candidates without silently discarding useful metadata.
   - Write raw artifacts + Markdown/HTML report.

2. **Claude lane**
   - Mandatory independent research/critique pass using Claude Code/Claude CLI from the VPS.
   - Ask for missing angles, weak evidence, contradictions, source classes not covered, and alternative interpretations.
   - Do not let Claude validate its own synthesis. Hermes reconciles Claude’s output against local artifacts.

3. **OpenAI Deep Research lane**
   - Preferred when actual API access exists.
   - Official OpenAI API docs describe Deep Research through the Responses API using models such as `o3-deep-research` or `o4-mini-deep-research`, with at least one data source: web search, remote MCP, or file search/vector stores.
   - This is **not the same** as Hermes’ current `openai-codex:gpt-5.5` brain doing tool-based research.
   - If no OpenAI API key/model access is available, state that clearly and continue with Hermes local DeepResearch + Claude. Do not pretend the native OpenAI Deep Research API was invoked.

## Output discipline

A premium research final should include:

- lanes run: local / Claude / OpenAI Deep Research;
- evidence artifacts for each lane;
- disagreement matrix or short conflict notes;
- claim-to-citation support check;
- weak/source-limited findings marked as such;
- explicit note if OpenAI native Deep Research was unavailable.

## Pitfall corrected

Do not answer “yes, GPT can deepresearch” ambiguously. Split the answer:

- **Yes**: Hermes/GPT can run our local DeepResearch workflow with tools and artifacts.
- **Different thing**: OpenAI’s native Deep Research API requires API access to the deep-research models and should be invoked/verified separately.
