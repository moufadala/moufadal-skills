# Last30days thin-evidence recovery for niche/community topics

Session lesson from a request about “Ashara Mubaraka 1448 London”. Last30days returned only one Reddit item and no YouTube/web results, but manual follow-up found useful public evidence.

## When to use

Use this pattern when Last30days reports thin evidence for a niche religious/community/local topic, especially when the likely discussion happens in YouTube titles/descriptions, WhatsApp-forwarded text, X/Instagram, or private/community channels.

## Pattern

1. Run `last30days --diagnose` first and report missing source classes honestly, especially X/Twitter and ScrapeCreators-backed TikTok/Instagram.
2. Run Last30days normally and save the raw Markdown artifact.
3. If Last30days returns `Evidence is thin`, do not stop there. Run targeted exact-query web searches and YouTube-specific probes.
4. For YouTube, `yt-dlp` flat search can still recover titles/IDs even when full extraction hits bot/login checks:

```bash
yt-dlp "ytsearch10:<topic>" --flat-playlist --print "%(upload_date)s | %(title)s | %(id)s | %(url)s" --skip-download
```

5. Use `web_extract` on the recovered YouTube URLs to get metadata, descriptions, and transcripts where available.
6. Separate strict-window evidence from near-window context. A video just outside the 30-day window can be relevant context but must be labeled as outside strict Last30days coverage.
7. For Reddit, if full extraction is blocked, label it as snippet/Last30days evidence only; do not overstate comment contents unless retrieved.
8. Synthesize cautiously: distinguish “public web signal is weak” from “nothing is being said”. Private/community channels may hold the real conversation.
9. Save a short Markdown synthesis artifact with verified links and limitations, instead of pasting raw Last30days output into Telegram.

## Reporting language

Use phrasing like:

- “Signal public faible mais réel.”
- “Couverture sociale incomplète: X/Twitter, TikTok, Instagram non couverts.”
- “Ce résultat prouve une activité publique visible, pas une mesure exhaustive de ce que la communauté se dit.”
- “Snippet-only / source partielle” for Reddit or blocked pages.

## Pitfalls

- Do not treat Last30days `0 web / 0 YouTube` as final when YouTube flat search may reveal relevant uploads.
- Do not claim a debate is absent; say the open-web evidence is thin.
- Do not mix exact 30-day evidence and older context without labeling the date-window mismatch.
- Do not present private WhatsApp-forwarded text as verified community consensus; it is one UGC signal unless corroborated.
