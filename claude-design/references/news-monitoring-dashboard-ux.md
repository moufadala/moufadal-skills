# News / monitoring dashboard UX notes

Use these notes when designing a veille, RSS, media-monitoring, or current-events dashboard.

## Correction captured

A prior decorative dashboard pass was rejected because it looked like a generic design artifact instead of a practical feed reader. The key failure was not visual style alone: the feed items were not obviously actionable enough for a news-monitoring workflow.

## Baseline expectations

A monitoring dashboard should provide, at minimum:

1. **Source access** — every article/event card must expose the original URL via clickable title/card or an explicit “open source” action.
2. **Fast scan** — source, date, type, priority, and short excerpt visible without opening the item.
3. **Progressive detail** — click card to reveal a 1-minute summary, “why it matters”, and source actions in a details panel/drawer/right reader.
4. **Filtering** — all / important / news / events or equivalent saved views.
5. **Search** — full-feed keyword filtering.
6. **Sorting** — at least relevance/priority; date and source sorting when the data supports it.
7. **Provenance** — source names and tested source count visible; avoid invented metrics.
8. **Verification** — browser-check interactions: card click, source link count, filter counts, search result count, sort listener, console errors.

## Reference patterns found useful

- **Swello monitoring**: display by date or relevance; actions include “Read the article”; search by keyword or period; alerts based on selected monitored sources and filters.
- **Feedly / RSS readers**: categories/folders, multiple display modes, excerpt first, click through to detailed view, link to full article on original site.
- **Veille informationnelle tools**: usefulness comes from good queries, targeted diffusion, signal/noise filtering, and signaux faibles — not from decorative stats.
- **Notion / Airtable / Mintlify style systems**: useful visual vocabulary for a clear working UI: warm white surfaces, whisper borders, restrained accent color, dense-but-readable typography, functional sidebars and reader panes.

## Pitfalls

- Do not interpret a user’s reference to a prior brand/site as a request to clone the brand. Ask/ infer whether they mean the design *process/tooling effort* or the literal style.
- Do not ship a news feed with dead cards or no source link.
- Do not over-index on dark/premium style for dashboards unless explicitly requested; monitoring surfaces often need clarity and legibility first.
- Do not use fake metrics. Counts should come from actual collected data.
