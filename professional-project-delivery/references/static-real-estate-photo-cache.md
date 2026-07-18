# Static real-estate photo cache / thumbnail proxy

Use when a scraped/static real-estate dashboard depends on third-party listing photos and the user reports missing photos, slow loads, hotlink failures, or poor mobile UX.

## Trigger

- Cards point directly at external photo hosts (Seloger, Citya, Zimo, Bien'ici, agency CDNs, etc.).
- Browser QA shows images pending/failed even though `image_url` exists.
- The user expects a reliable mobile product, not a research spreadsheet.

## Product rule

For a client-facing/static dashboard, do not depend on hotlinked photos for primary card images. Cache at least the primary thumbnail locally and serve it from the same origin as the app:

```text
/artifacts/app/thumbs/<hash>.<ext>
```

Keep the original `image_url` as provenance/fallback, but render `local_image_url || image_url`.

## Implementation pattern

1. Inventory image URLs from the exported app JSON.
   - Count listings, listings with `image_url`, unique URLs, hosts, and source sites.
2. Download unique URLs idempotently.
   - Hash URL to filename.
   - Use browser/mobile User-Agent.
   - Add per-source `Referer` where helpful.
   - Validate `Content-Type` starts with `image/`.
   - Validate min/max bytes to reject HTML block pages and tiny placeholders.
   - Use retries and bounded concurrency.
3. Patch the exported data.
   - Add `local_image_url: "/thumbs/<file>"`.
   - Add `photo_cached: true/false` or `photo_ok/photo_failed`.
4. Patch every data source consumed by the static app.
   - `listings.json` is not enough if `index.html` embeds data in `<script type="application/json">`.
   - Patch the embedded JSON too, or rebuild and then re-run the cache patcher.
5. Patch rendering.
   - Cards: `const imgSrc = it.local_image_url || it.image_url`.
   - Modal/gallery: same fallback chain.
   - Keep text fields sufficient so cards still make sense if a photo fails.
6. For mobile first-screen results, avoid photo carousels and avoid requiring horizontal image scrolling.
   - Show one primary photo, compact metadata, and a `+N photos` marker only after galleries are actually cached.
   - If only the primary photo is cached, say so explicitly; do not imply full gallery support.

## QA gates

Terminal/public:

```bash
# Example checks
python3 scripts/cache_listing_images.py
python3 tests/audit_filters_v3.py
./deploy/qa-public.sh
curl -I https://<host>/thumbs/<sample>.webp
curl https://<host>/thumbs/<sample>.webp | wc -c
```

Browser:

```js
new Promise(resolve => setTimeout(() => {
  const imgs = [...document.images];
  resolve({
    total: imgs.length,
    loaded: imgs.filter(i => i.complete && i.naturalWidth > 0).length,
    failed: imgs.filter(i => i.complete && i.naturalWidth === 0).length,
    pending: imgs.filter(i => !i.complete).length,
    srcs: imgs.slice(0, 10).map(i => ({
      src: i.currentSrc || i.src,
      nw: i.naturalWidth,
      nh: i.naturalHeight,
      complete: i.complete,
    })),
  });
}, 3000));
```

Also test `fetch()` for sample thumbnails if `<img>` appears pending; it distinguishes server availability from rendering/lazy-loading behavior.

## Known pitfall: embedded JSON

Static dashboards often embed the dataset for instant load:

```html
<script id="embeddedData" type="application/json">...</script>
```

If you patch only `listings.json`, the browser can still use stale external `image_url`s from the embedded JSON. Patch both or make the app fetch `listings.json` only.

## Known pitfall: lazy-loading in small mobile tests

When only a small result set is rendered above the fold, `loading="lazy"` can leave images pending in automation or constrained mobile viewports. After local caching, `loading="eager"` for the visible cards may be the right trade-off. Keep the result count bounded or virtualize before making many images eager.

## Reporting standard

Report:

- listings count;
- unique URLs;
- download OK/fail counts and fail reasons;
- listings patched with local images;
- cache size;
- sample public thumbnail HTTP headers;
- browser loaded/failed/pending counts;
- explicit limit: primary thumbnail vs full gallery.

Do not claim “all photos” if only the primary listing photo was available/cached. Say “primary photo for every displayed listing” unless detail-page gallery scraping was implemented.