#!/usr/bin/env python3
"""Catalogue viewer type validator.

Input JSON shape: list of objects with at least:
  {
    "type_fliping": "FLIPPING V2",
    "enseigne": "...",
    "nom": "...",
    "nb_pages": 3,
    "lien_prospectus": "https://..."
  }

Captures browser-rendered screenshots, network image/json/pdf responses, and a print-to-PDF proof per catalogue type.
Requires Playwright Python with Chromium installed in the execution environment.
"""
import argparse, hashlib, json, re
from pathlib import Path
from playwright.sync_api import sync_playwright

MOBILE_UA = (
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
)

def safe(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9._-]+", "_", str(value))[:80].strip("_") or "item"

def interesting(url: str, content_type: str) -> bool:
    low = url.lower()
    return (
        content_type.startswith("image/")
        or "json" in content_type
        or "pdf" in content_type
        or any(x in low for x in ["jpg", "jpeg", "png", "webp", "pdf", "publication", "page", "api", "magazine", "config", "assets"])
    )

def extension_for(content_type: str, body: bytes) -> str:
    ct = content_type.lower()
    if "pdf" in ct or body[:4] == b"%PDF": return ".pdf"
    if "jpeg" in ct or "jpg" in ct or body[:3] == b"\xff\xd8\xff": return ".jpg"
    if "png" in ct or body[:8] == b"\x89PNG\r\n\x1a\n": return ".png"
    if "webp" in ct or body[:4] == b"RIFF": return ".webp"
    if "svg" in ct: return ".svg"
    if "json" in ct: return ".json"
    return ".bin"

def validate(items, outdir: Path, wait_ms: int, scrolls: int):
    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-dev-shm-usage"])
        for item in items:
            t = item.get("type_fliping") or item.get("type") or "unknown"
            out = outdir / safe(t) / "browser"
            out.mkdir(parents=True, exist_ok=True)
            ctx = browser.new_context(viewport={"width": 390, "height": 844}, user_agent=MOBILE_UA)
            page = ctx.new_page()
            responses, saved = [], []

            def on_response(resp):
                try:
                    url = resp.url
                    ct = (resp.headers.get("content-type") or "").lower()
                    if not interesting(url, ct):
                        return
                    rec = {"url": url, "status": resp.status, "ct": ct}
                    responses.append(rec)
                    if ct.startswith("image/") or "pdf" in ct:
                        body = resp.body()
                        ext = extension_for(ct, body)
                        fn = out / f"asset_{len(saved)+1:04d}_{hashlib.sha256(url.encode()).hexdigest()[:8]}{ext}"
                        fn.write_bytes(body)
                        saved.append({**rec, "file": str(fn), "bytes": len(body)})
                except Exception:
                    pass

            page.on("response", on_response)
            error = None
            title = ""
            html_len = 0
            screenshot = out / "screenshot.png"
            pdf = out / "browser_print.pdf"
            try:
                page.goto(item["lien_prospectus"], wait_until="domcontentloaded", timeout=45000)
                page.wait_for_timeout(wait_ms)
                for _ in range(scrolls):
                    page.mouse.wheel(0, 1200)
                    page.wait_for_timeout(max(1000, wait_ms // 3))
                page.screenshot(path=str(screenshot), full_page=True)
                try:
                    page.pdf(path=str(pdf), print_background=True, width="390px", height="844px")
                except Exception as e:
                    error = "pdf:" + str(e)[:180]
                title = page.title()
                html_len = len(page.content())
            except Exception as e:
                error = type(e).__name__ + ": " + str(e)[:250]
            finally:
                ctx.close()

            result = {
                "type_fliping": t,
                "catalogue": item,
                "error": error,
                "title": title,
                "html_len": html_len,
                "network_relevant_count": len(responses),
                "asset_count": len(saved),
                "significant_asset_count": sum(1 for x in saved if x.get("bytes", 0) > 50000),
                "saved_assets": saved[:100],
                "responses": responses[:200],
                "screenshot": str(screenshot) if screenshot.exists() else None,
                "browser_pdf": str(pdf) if pdf.exists() else None,
                "browser_pdf_ok": pdf.exists() and pdf.stat().st_size > 1000,
            }
            (out / "browser_network.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
            results.append(result)
        browser.close()
    (outdir / "browser_type_validation_results.json").write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    return results

def main():
    ap = argparse.ArgumentParser(description="Validate catalogue viewer types by browser-network capture.")
    ap.add_argument("--selected", required=True, help="JSON list of selected catalogue items")
    ap.add_argument("--outdir", required=True, help="Output directory")
    ap.add_argument("--wait-ms", type=int, default=10000)
    ap.add_argument("--scrolls", type=int, default=1)
    args = ap.parse_args()
    items = json.loads(Path(args.selected).read_text())
    outdir = Path(args.outdir); outdir.mkdir(parents=True, exist_ok=True)
    results = validate(items, outdir, args.wait_ms, args.scrolls)
    print(json.dumps(results, ensure_ascii=False, indent=2)[:30000])

if __name__ == "__main__":
    main()
