# Reddit access for research: cookies vs OAuth/API

Session lesson for research/scraping tasks that need Reddit coverage.

## Practical verdict

Do not treat logged-in browser cookies as a route to “all Reddit”. Cookies can help with some public pages, but they do not provide unlimited, complete, or stable Reddit access.

Prefer this order:

1. **Indirect discovery**: search engines / SearXNG with `site:reddit.com` for broad discovery.
2. **Official OAuth/API**: personal/dev usage where rate limits and Data API terms are acceptable.
3. **Browser cookies**: narrow fallback for a small number of pages where a logged-in view is necessary and the user explicitly accepts account/session risk.

## What cookies can help with

- Pages that behave differently for anonymous visitors.
- NSFW or preference-gated content if the account is configured for it.
- Occasional browser-only extraction where public search found a URL but anonymous fetch fails.

## What cookies cannot solve

- Private subreddits the account cannot access.
- Deleted, removed, or moderator-hidden content.
- Unlimited rate limits.
- Stable large-scale crawling from a datacenter VPS.
- Complete Reddit coverage.

## Security risk

Exported cookies are an active account session. Storing or replaying them from a VPS can trigger lock/abuse signals and exposes the account if the host or logs leak. Do not request or store Reddit cookies unless the source class is required and the user approved the risk.

## OAuth/API cost stance

Creating a Reddit OAuth app for personal scripts/dev usage is generally not the same as paying for Reddit data access. However Reddit’s Data API terms reserve separate agreements/fees for commercial use, high-volume/research beyond limits, and disallowed uses such as training models without permission.

Report as:

- “OAuth/API is probably free enough for a small personal research crawler within limits.”
- “It is not a license to scrape all Reddit or build a commercial/high-volume dataset.”

## Smoke-test before scaling

Before building a Reddit-heavy lane:

1. Test 1–2 public Reddit URLs from indirect search.
2. Test one OAuth/API call with a clear User-Agent and rate-limit handling.
3. Only if needed, test one cookie-backed browser fetch in an isolated profile.
4. Record whether each path returns content, 403/429, login wall, or bot wall.
