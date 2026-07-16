# Brief extraction HTML page pattern

Use when the user asks a quick question like “les nouveautés X c’est quoi ? tout ça dans une page HTML” and the data already exists in a generated monitoring/brief HTML artifact.

## Pattern

1. Treat the source brief as the ground truth artifact; do not invent or re-run unrelated collectors unless the user asks for fresh data.
2. Locate the latest relevant brief HTML and inspect the specific panels/cards the user names.
3. Extract only the `is-new` / `data-isnew=true` cards for each requested category, preserving source URLs, titles, dates/channels, and snippets.
4. Add an honest editorial verdict:
   - mark clearly relevant items as “à lire / pertinent”;
   - mark obvious false positives as “bruit / hors sujet”;
   - call out likely module/query bugs instead of presenting noise as real news.
5. Produce a self-contained HTML page optimized for phone reading: executive summary first, category sections, cards with source links, and a final verdict/action list.
6. Verify: file exists, parse/syntax sanity, expected card/link counts, browser open if available, console errors if JS exists.

## Avoid

- Do not dump the full original dashboard when the user asked “c’est quoi ?”. Summarize and classify.
- Do not make every detected item sound useful. If the source module returned Windows/gaming/general-course results under Dawoodi Bohra or kiné, say it is noise.
- Do not over-design with dashboards/charts; this is a reading artifact, not an ops surface.
