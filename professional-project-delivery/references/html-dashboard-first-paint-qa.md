# HTML dashboard first-paint QA

## Lesson
For autonomous HTML dashboards and Telegram-delivered artifacts, Playwright-after-load QA is not enough. A mobile preview, screenshot, or Telegram file viewer can capture the page before the JavaScript render loop has populated the DOM. The user will see contradictions such as summary stats saying `79 items` while the feed says `0 item`.

## Durable pattern
When generating a self-contained HTML dashboard from data:

1. Render meaningful fallback content directly into the initial HTML:
   - initial cards/items list;
   - source rows/statuses;
   - initial counter using the real data count;
   - initial reader/detail panel with the first item or a useful empty state.
2. Let JavaScript enhance the page after load for search, filters, sorting, and clicks.
3. QA both states:
   - raw/static DOM parsed from the HTML file before JS execution;
   - browser DOM after JS execution.
4. Add explicit regression checks for:
   - `#items .item` count before JS is greater than zero when the dataset is non-empty;
   - `#count` does not contain a stale `0 item` placeholder;
   - `#sources .src` exists before JS;
   - reader/detail panel has useful content and a source link before JS;
   - browser console remains error-free after enhancement.

## Anti-pattern
Do not ship a dashboard where the HTML body contains empty placeholders like:

```html
<p id="count">0 item</p>
<div id="items"></div>
<div id="sources"></div>
```

unless there is also a no-JS fallback or the empty state is intentionally correct.

## Recommended wording in QA reports
Mention both:

- `Static first paint: N cards, M sources, reader ready`
- `Browser enhanced state: filters/search/clicks pass, console clean`
