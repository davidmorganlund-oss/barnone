"""Build print PDFs and cover images for BarNone briefs whose full text is on the web page.

Usage (from the repository root):
    python3 _tools/build_brief_pdfs.py            # all briefs below
    python3 _tools/build_brief_pdfs.py long-sentences

Each brief is rendered from its live HTML page, so the PDF always matches the page.
Output: <slug>.pdf (letter size, page count a multiple of 4 for ledger booklets)
and <slug>-cover.png (816 x 1056), both in the repository root.

Needs: playwright (Chromium), pypdf, and the Archivo, Public Sans and Michroma fonts
installed locally (Google Fonts requests are blocked so local fonts are used).
This folder starts with an underscore, so GitHub Pages does not publish it.
"""
import asyncio, base64, io, pathlib, sys
from playwright.async_api import async_playwright
from pypdf import PdfReader, PdfWriter

ROOT = pathlib.Path(__file__).resolve().parent.parent

BRIEFS = {
    "same-crime-more-prison": dict(
        no=1, place="Idaho",
        title=["Similar violent crime,", "far more prison"], accent=1,
        sub="Idaho and Utah report nearly the same violent crime. Idaho imprisons people at 2.6 times Utah's rate.",
        stat="2.6&times;",
        stat_note="Idaho's state imprisonment rate compared with Utah's (490 vs. 186 per 100,000, 2023)",
        meta="November 2026 &middot; Updated Nov. 24, 2026 &middot; Idaho and its six neighbors",
        short="Similar Violent Crime, Far More Prison",
    ),
    "long-sentences": dict(
        no=2, place="Washington",
        title=["Long and life sentences", "in Washington"], accent=1,
        sub="Washington imprisons fewer people than its neighbors, and keeps many of them for a very long time.",
        stat="49%",
        stat_note="of people in Washington prisons were sentenced to more than 10 years or to life (Sept. 2026)",
        meta="November 2026 &middot; Washington, with Idaho and Oregon for comparison",
        short="Long and Life Sentences in Washington",
    ),
    "review-act": dict(
        no=3, place="Washington",
        title=["Who would benefit", "from the Review Act"], accent=1,
        sub="A judge takes a second look at a long sentence. Nobody is released automatically.",
        stat="About 3,035",
        stat_note="people in Washington prisons would become eligible to ask for review, from 37 of 39 counties",
        meta="November 2026 &middot; Washington, by county",
        short="Who Would Benefit from the Review Act",
    ),
    "smart-on-crime-oregon": dict(
        no=6, place="Oregon",
        title=["Smart on crime,", "smart on the budget:", "Oregon"], accent=2,
        sub="Close the Oregon State Penitentiary. Don't build another one.",
        stat="$1.22 billion",
        stat_note="to design and build a new penitentiary in DOC's 2027-29 facility plan; about $2.06 billion with 25 years of interest",
        meta="November 2026 &middot; Updated Nov. 24, 2026 &middot; Oregon, 2027 session",
        short="Smart on Crime, Smart on the Budget: Oregon",
    ),
}

FONTS = """
:root{--navy:#201c3a;--red:#e01e14;--ember:#f2a33a;--ink:#1b1930;--navy-ink:#f1f0f7;--navy-muted:#b9b6cc}
*{box-sizing:border-box}html,body{margin:0;padding:0}
body{font-family:"Public Sans",sans-serif;-webkit-print-color-adjust:exact;print-color-adjust:exact}
"""

def cover_html(b):
    title = "<br>".join(
        f'<span class="acc">{t}</span>' if i == b["accent"] else t for i, t in enumerate(b["title"]))
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{FONTS}
@page{{size:8.5in 11in;margin:0}}
.cv{{width:816px;height:1056px;background:var(--navy);color:var(--navy-ink);position:relative;overflow:hidden;
  padding:96px 72px 56px;display:flex;flex-direction:column}}
.cv:before{{content:"";position:absolute;left:0;right:0;top:0;height:14px;background:var(--red)}}
.brand{{display:flex;align-items:center;gap:18px}}
.brand img{{width:64px;height:auto}}
.wm{{font-family:Michroma,sans-serif;font-size:22px;letter-spacing:.32em;border-bottom:2px solid var(--navy-ink);padding-bottom:6px}}
.eb{{margin-top:120px;color:var(--ember);font-weight:700;letter-spacing:.18em;font-size:15px;text-transform:uppercase}}
h1{{font-family:Archivo,sans-serif;font-stretch:112%;font-weight:800;font-size:62px;line-height:1.06;margin:18px 0 0;letter-spacing:-.01em}}
.acc{{color:#ff4136}}
.sub{{margin-top:26px;font-size:22px;line-height:1.45;max-width:560px;color:var(--navy-ink)}}
.stat{{margin-top:auto;font-family:Archivo,sans-serif;font-stretch:112%;font-weight:800;font-size:96px;line-height:1;color:#ff4136}}
.note{{font-size:16px;color:var(--navy-muted);margin-top:10px;max-width:600px;line-height:1.4}}
.foot{{display:flex;justify-content:space-between;margin-top:56px;font-size:14px;color:var(--navy-muted);letter-spacing:.04em}}
</style></head><body><div class="cv">
<div class="brand"><img src="data:image/png;base64,{base64.b64encode((ROOT/'phoenix.png').read_bytes()).decode()}" alt=""><span class="wm">BARNONE</span></div>
<p class="eb">Research Brief No. {b['no']} &middot; {b['place']}</p>
<h1>{title}</h1>
<p class="sub">{b['sub']}</p>
<p class="stat">{b['stat']}</p><p class="note">{b['stat_note']}</p>
<div class="foot"><span>{b['meta']}</span><span>barnoneinc.org</span></div>
</div></body></html>"""

PRINT_CSS = """
@page{size:8.5in 11in;margin:.7in .75in .8in}
html,body{background:#fff !important}
body{font-size:11pt;line-height:1.5}
.site-head,.site-foot,.skip,.back,.toc-brief,#download,.btns{display:none !important}
.brief-head{background:#fff !important;color:var(--ink) !important;padding:0 0 .25in !important;border:0 !important}
.brief-head h1{font-size:28pt !important;color:var(--ink) !important}
.brief-head .lede{color:var(--ink) !important;font-size:12.5pt !important;max-width:none !important}
.brief-head .eyebrow{color:var(--red-text) !important}
.brief-meta{color:var(--muted) !important}
.brief-meta a,.brief-meta span{color:var(--muted) !important}
.wrap{max-width:none !important;padding-left:0 !important;padding-right:0 !important}
.section{padding-top:.3in !important;padding-bottom:.3in !important}
.brief-body,.brief-body>section{display:block !important}
.brief-body>section+section{margin-top:.35in !important}
.brief-body>section>*+*{margin-top:1.1em}
h2{font-size:18pt !important;break-after:avoid}
h3{font-size:13pt !important;break-after:avoid}
.section-head{break-after:avoid;break-inside:avoid}
.eyebrow{break-after:avoid}
.reveal{opacity:1 !important;transform:none !important}
figure,.figure,.fact,tr,.findings li,svg,.callout,.stat-card,blockquote{break-inside:avoid}
.fig-scroll,.table-scroll{overflow:visible !important}
table{font-size:9pt !important;width:100% !important}
.split{display:block !important}
.split>*+*{margin-top:.15in}
.prose{max-width:none !important}
a{color:inherit;text-decoration:none}
sup a{color:var(--red-text)}
#sources a,#notes a,.sources a{word-break:break-word}
.timeline,.prose{display:block !important}
.timeline li{break-inside:avoid;display:block !important;position:relative;padding-left:7.5rem !important}
.timeline li>.when{position:absolute;left:0;top:1.3rem}
.prose ul,.prose ol,.brief-body ul{display:block !important}
.prose li+li,.brief-body ul li+li{margin-top:.35em}
.prose>*+*{margin-top:.8em}
#sources ol,#notes ol,.sources ol{padding-left:2.4em !important}
.pdf-blank{break-before:page;height:1px}
.pdf-back{break-before:page;height:8.6in;display:flex;flex-direction:column;justify-content:flex-end}
.pdf-back .box{background:var(--navy);color:var(--navy-ink);padding:.35in .4in;font-size:10.5pt;line-height:1.55}
.pdf-back .box p+p{margin-top:.12in}
.pdf-back strong{color:#fff}
"""

BACK = """<div class="pdf-back"><div class="box">
<p><strong>BarNone, Inc.</strong> is a nonpartisan 501(c)(3) research and policy organization focused on incarceration in Idaho, Washington, and Oregon. We turn public data into plain-language findings that lawmakers, reporters, and communities can use.</p>
<p>Read all of our briefs, with sources and data, at <strong>barnoneinc.org</strong>. Corrections and questions: admin@barnoneinc.org.</p>
<p>Research. Policy. Grace, bar none.</p></div></div>"""

def footer(short):
    return ('<div style="width:100%;text-align:center;font-family:\'Public Sans\',sans-serif;'
            f'font-size:7.5pt;color:#59566e;letter-spacing:.03em">{short} &middot; BarNone &middot; '
            '<span class="pageNumber"></span></div>')

async def render_body(page, slug, b, blanks):
    await page.goto((ROOT / f"{slug}.html").as_uri(), wait_until="load")
    await page.add_style_tag(content=PRINT_CSS)
    await page.evaluate("""([back, blanks]) => {
      document.documentElement.setAttribute('data-theme','light');
      document.documentElement.classList.remove('js-motion');
      document.querySelectorAll('.reveal').forEach(e=>e.classList.remove('reveal'));
      document.querySelectorAll('.chart').forEach(e=>e.classList.add('in'));
      document.querySelectorAll('script').forEach(s=>s.remove());
      const main = document.querySelector('main');
      // a throwaway first page so the footer numbers start at 2 (the cover replaces it)
      const d = document.createElement('div'); d.style.cssText='height:1px;break-after:page'; main.prepend(d);
      for (let i=0;i<blanks;i++){const x=document.createElement('div');x.className='pdf-blank';main.append(x);}
      main.insertAdjacentHTML('beforeend', back);
    }""", [BACK, blanks])
    await page.evaluate("document.fonts.ready")
    return await page.pdf(format="Letter", print_background=True, display_header_footer=True,
                          header_template="<span></span>", footer_template=footer(b["short"]),
                          margin=dict(top="0.7in", bottom="0.8in", left="0.75in", right="0.75in"),
                          prefer_css_page_size=False)

async def build(slug):
    b = BRIEFS[slug]
    async with async_playwright() as p:
        br = await p.chromium.launch(channel="chrome")
        ctx = await br.new_context(color_scheme="light", reduced_motion="reduce", viewport=dict(width=816, height=1056))
        await ctx.route("**/fonts.googleapis.com/**", lambda r: r.abort())
        await ctx.route("**/fonts.gstatic.com/**", lambda r: r.abort())
        page = await ctx.new_page()

        # cover: PDF page and PNG image
        await page.set_content(cover_html(b), wait_until="load")
        await page.evaluate("document.fonts.ready")
        await page.screenshot(path=str(ROOT / f"{slug}-cover.png"), clip=dict(x=0, y=0, width=816, height=1056))
        cover_pdf = await page.pdf(format="Letter", print_background=True, margin=dict(top="0", bottom="0", left="0", right="0"))

        # body: render once to count, then pad so cover + body is a multiple of 4
        body = await render_body(page, slug, b, 0)
        n = len(PdfReader(io.BytesIO(body)).pages)  # includes throwaway page 1, which the cover replaces
        blanks = (-n) % 4
        if blanks:
            body = await render_body(page, slug, b, blanks)
        await br.close()

    w = PdfWriter()
    w.add_page(PdfReader(io.BytesIO(cover_pdf)).pages[0])
    for pg in PdfReader(io.BytesIO(body)).pages[1:]:
        w.add_page(pg)
    w.add_metadata({"/Title": f"{b['short']} (BarNone Research Brief No. {b['no']})",
                    "/Author": "BarNone, Inc.", "/Subject": f"https://barnoneinc.org/{slug}.html"})
    out = ROOT / f"{slug}.pdf"
    with open(out, "wb") as f:
        w.write(f)
    print(f"{out.name}: {len(w.pages)} pages ({blanks} blank before back cover), {out.stat().st_size/1e6:.2f} MB")

if __name__ == "__main__":
    for s in (sys.argv[1:] or BRIEFS):
        asyncio.run(build(s))
