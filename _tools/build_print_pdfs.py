"""Build the designed print PDFs (Briefs 4 and 5) from their HTML sources in _tools/print/.

Usage (from the repository root):
    python3 _tools/build_print_pdfs.py                 # both briefs
    python3 _tools/build_print_pdfs.py smart-on-crime-idaho

Each source is a set of fixed US Letter pages (<section class="page">). The script
renders them with Chrome, stops if any page's content runs into its footer, and writes
<slug>.pdf and <slug>-cover.png (816 x 1056) to the repository root.

Needs: playwright (Chrome or Chromium) and pypdf. Fonts are bundled in _tools/print/fonts,
so nothing else needs installing. GitHub Actions can also run this for you: see
.github/workflows/build-pdfs.yml.
"""
import asyncio, functools, http.server, io, pathlib, sys, threading
from playwright.async_api import async_playwright
from pypdf import PdfReader, PdfWriter

ROOT = pathlib.Path(__file__).resolve().parent.parent

BRIEFS = {
    "smart-on-crime-washington": "Smart on Crime, Smart on the Budget: Washington (BarNone Research Brief No. 4)",
    "smart-on-crime-idaho": "Smart on Crime, Smart on the Budget: Idaho (BarNone Research Brief No. 5)",
}


def serve():
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(ROOT))
    handler.log_message = lambda *a, **k: None
    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd


async def build(browser, base, slug, title):
    page = await browser.new_page(viewport={"width": 816, "height": 1056})
    await page.goto(f"{base}/_tools/print/{slug}.html", wait_until="networkidle")
    await page.evaluate("document.fonts.ready")
    missing = await page.evaluate(
        "[...document.fonts].filter(f => f.status !== 'loaded').map(f => f.family)")
    if missing:
        raise SystemExit(f"{slug}: fonts did not load: {missing}")
    report = await page.evaluate("checkOverflow()")
    bad = [r for r in report if r["overflow_px"] > 0]
    for r in report:
        print(f"  page {r['page']:>2}: room at bottom {r['room_px']:>6}px"
              + (f"  OVERFLOW {r['overflow_px']}px" if r["overflow_px"] else ""))
    if bad and "--force" not in sys.argv:
        raise SystemExit(f"{slug}: content runs into the footer on page(s) "
                         + ", ".join(str(r["page"]) for r in bad))
    await page.locator(".page").first.screenshot(path=str(ROOT / f"{slug}-cover.png"))
    pdf = await page.pdf(prefer_css_page_size=True, print_background=True,
                         margin={"top": "0", "right": "0", "bottom": "0", "left": "0"})
    await page.close()
    reader = PdfReader(io.BytesIO(pdf))
    writer = PdfWriter()
    for p in reader.pages:
        writer.add_page(p)
    writer.add_metadata({"/Title": title, "/Author": "BarNone", "/Subject": "Discussion draft, November 2026"})
    with open(ROOT / f"{slug}.pdf", "wb") as fh:
        writer.write(fh)
    n = len(reader.pages)
    note = "" if n % 4 == 0 else "  (not a multiple of 4: add or trim a page for ledger booklets)"
    print(f"{slug}.pdf: {n} pages{note}")


async def main():
    slugs = [a for a in sys.argv[1:] if not a.startswith("--")] or list(BRIEFS)
    httpd = serve()
    base = f"http://127.0.0.1:{httpd.server_address[1]}"
    async with async_playwright() as p:
        try:
            browser = await p.chromium.launch(channel="chrome")
        except Exception:
            browser = await p.chromium.launch()
        for slug in slugs:
            print(slug)
            await build(browser, base, slug, BRIEFS[slug])
        await browser.close()
    httpd.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
