# Catalogue/PDF/product scraping reconnaissance pattern

Use when a user wants a system that monitors online catalogues/flyers, reconstructs PDFs, extracts product data, stores it, and later supports alerts or visual search.

## Hard reset rule

If the user says the project is new or corrects that it has nothing to do with prior dashboards/courses, immediately reset scope. Name the new project, stop reusing old artifacts, and record a clean `docs/vision.md` before technical work.

## Recon sequence

1. **Catalogue index API first**
   - Check `robots.txt`, sitemap, homepage scripts, Next.js/RSC data, and browser network.
   - Look for JSON endpoints listing catalogues: metadata, merchant, dates, page count, cover image, sectors, viewer URL.
   - Archive raw responses and distinguish API-public-by-observation from official API.

2. **Viewer/page asset proof**
   - For at least one catalogue, fetch viewer HTML with plain HTTP/curl **without JS** and count page asset URLs.
   - If zero, use Playwright network capture and mark fetcher as browser-dependent.
   - Download page images as binaries, not just URLs. URLs may expire or be changed; local storage is the archival truth.

3. **PDF reconstruction proof**
   - Build a PDF from downloaded page images.
   - Verify PDF header `%PDF`, EOF marker, page count/source manifest, file size, and source URLs.
   - Be precise: “faithful image-assembled PDF” is not the same as searchable/text-layer PDF.

4. **Do not overgeneralize one catalogue**
   - Enumerate catalogue/viewer types (`type_fliping`, viewer vendor, PDF/HTML5/Adobe/etc.).
   - Test one catalogue per type before claiming V1 feasibility for all.
   - Produce matrix: type → HTML raw pages? → image download? → page order reliable? → PDF build? → method required.

5. **Product extraction is a separate proof**
   - Catalogue pages as images do not imply structured product data.
   - If a marketplace/product API exists, treat it as a separate data source until proven linked to catalogue pages.
   - For catalogue extraction, expect OCR/vision/layout segmentation with confidence scores, product crops, page coordinates, and human review for low confidence.

6. **Headers/rate/ethics checks**
   - Test bare Python client vs browser User-Agent. If Python UA gets 403 and browser UA gets 200, note soft bot protection and implement polite headers/rate limits.
   - Test pagination/limits and whether parameters are ignored.
   - Robots disallow on `/api/` is a real legal/ethical/commercial risk, not just a technical detail.

## Deliverables for this class of task

- `docs/vision.md` capturing the product vision and out-of-scope items.
- Dated recon report with matrix and proof paths.
- Raw JSON/HTML/network artifacts.
- Screenshot(s) from browser/mobile.
- Downloaded page image(s), reconstructed PDF, and manifest JSON.
- A senior critique/review step before coding V1 if the system could become a product.

## Acceptance gate before coding V1

Do not build the durable collector until:

- catalogue index endpoint is proven and archived;
- all active catalogue/viewer types are enumerated;
- at least one catalogue per major type has a page/PDF proof or a documented blocker;
- rate/header behavior is known;
- product extraction is explicitly classified as structured API vs OCR/vision task.

## Field pattern: multi-viewer catalogue platforms

When the catalogue index exposes a format/vendor field (example names seen in the field: `FLIPPING V2`, `MAGZ`, `ADOBE`, `FLIPHTML5`, `FLIPPING LAPUB`), do **not** write a single scraper from the first successful catalogue. Build adapters by viewer family:

- **FLIPPING V2 / Next.js viewer**: often exposes direct page JPEGs from a data host. Watch for spaces/accents in paths; parse and URL-encode full paths carefully. Good V1 target for image→PDF reconstruction.
- **MAGZ / interactive-catalogue style**: browser network may reveal JSON like `/view/magazine/<slug>?pagination=N&detail=true&provider=...`. The JSON can contain `pages`, `pdfpage`, `thumbnail`, and HTML `content` with item images. Test direct `assets/pdf/<page>.pdf`; this can be the best bridge between faithful PDF recovery and later product extraction.
- **ADOBE / InDesign online**: look for embedded manifest (`readerViewDataFromServer`, `MANIFEST_BODY`) and a `content.json`. Expect many separate assets (product PNG/JPEG/SVG, videos, page HTML) rather than one simple page image. Useful for extraction but more complex for faithful page assembly.
- **FLIPHTML5**: avoid guessing `files/large/1.jpg`. Pages may be hashed `.webp` paths from `javascript/config.js`; use config parsing or a browser-network fallback.
- **FlippingBook / FLIPPING LAPUB**: static HTML may only show generic loader files; browser network can reveal `files/assets/common/page-html5-substrates/page0001_1.webp?...` or similar page substrates.

Reusable validation loop:

1. Select one active catalogue per viewer type from the index API.
2. Run a static probe first: raw HTML, config files, manifest JSON, direct assets/PDF page URLs.
3. Run a Playwright network capture second: mobile viewport, wait/scroll, save screenshots, collect image/json/pdf responses and write them to disk.
4. Summarize per type: metadata page count, HTML raw page count, image count, significant images, direct PDF availability, browser PDF proof, method required, and blocker.
5. Promote only the proven adapters into V1; leave unsupported types as documented backlog, not silent failures.

Reusable helper: `scripts/catalogue_type_browser_validator.py` captures mobile Playwright network responses, screenshots, saved assets, and browser PDF proof for a JSON list of selected catalogue items.

## POC ingestion gate: infrastructure is not product value

After the type matrix, build a deliberately narrow ingestion POC before UI/alerts/comparison features:

1. Use TDD or at least executable smoke tests for:
   - parser functions for each viewer family;
   - URL encoding of asset paths with spaces/accents;
   - SQLite schema creation;
   - an offline fixture path so the core logic can be tested without network.
2. Ingest only 1-2 proven high-value formats first, usually:
   - `FLIPPING V2`: direct page images → faithful image-assembled PDF;
   - `MAGZ`: structured JSON + page PDFs/content HTML → best first candidate for product extraction.
3. Store, at minimum:
   - `catalogues`: merchant, name, dates, type, viewer URL, local directory, local PDF if built, raw JSON;
   - `catalogue_pages`: page number, source URL, local file, page PDF URL, thumbnail URL;
   - `assets`: kind, source URL, local file, bytes, sha256, content type;
   - `product_candidates` only if extraction is still heuristic.
4. If Pillow/ImageMagick/img2pdf are unavailable, a dependency-free PDF builder can embed JPEG page images directly using PDF `/Image` XObjects with `/DCTDecode`. Verify `%PDF` header and `%%EOF`; this is good enough for a faithful image PDF, not a searchable PDF.
5. For `MAGZ`, treat page PDFs and HTML `content` as raw material. A first extraction may produce page-level text/price candidates, but **do not call them products** until validated.

### Product-extraction acceptance gate

Do not advance to alerts, price comparison, visual search, or polished UI until product-level extraction has a measured proof:

- Create a real `products` table separate from `product_candidates`.
- Produce at least 20 structured products from one catalogue/type.
- For each product verify manually: `name`, `price`, page, corresponding image/crop, and source evidence.
- Report precision/recall proxy or at least `correct / checked`, target ≥80% before scaling.
- Label uncertain rows with confidence and keep source text/bbox/crop for audit.

This avoids the common overclaim: “we ingested pages/assets” ≠ “we extracted products/prices”. The former proves infrastructure; the latter proves business value.
