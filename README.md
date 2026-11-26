# BarNone website

A multi-page static site for GitHub Pages.

## Pages

| File | Page |
| --- | --- |
| index.html | Home |
| research.html | Research |
| same-crime-more-prison.html | Research Brief No. 1: Similar violent crime, far more prison (Idaho) |
| long-sentences.html | Research Brief No. 2: Long and life sentences in Washington |
| review-act.html | Research Brief No. 3: Who would benefit from the Review Act |
| smart-on-crime-washington.html | Research Brief No. 4: Smart on Crime, Smart on the Budget: Washington; full brief: smart-on-crime-washington.pdf |
| smart-on-crime-idaho.html | Research Brief No. 5: Smart on Crime, Smart on the Budget: Idaho; full brief: smart-on-crime-idaho.pdf |
| smart-on-crime-oregon.html | Research Brief No. 6: Smart on Crime, Smart on the Budget: Oregon; full brief: smart-on-crime-oregon.pdf |
| session.html | 2027 session bill tracker (reads bills.json) |
| about.html | About |
| toolkit.html | Advocacy Toolkit |
| reentry.html | Reentry Help |
| reentry-idaho.html, reentry-washington.html, reentry-oregon.html | State reentry guides (dated "Last checked") |
| events.html | Events |
| contact.html | Contact |

Shared files: `site.css` (all styles), `site.js` (menu, copy buttons, motion), `phoenix.png`, `barnone-logo.png` and `favicon.png`. Each brief has a share image (`og-*.png`); Briefs 4 to 6 also have a PDF and a cover image (`*-cover.png`). All files sit in one folder, with no subfolders. Change a style once in `site.css` and every page picks it up.

## Editing the menu

The menu and footer are repeated at the top and bottom of every page. To add or rename a page, update the `<nav class="site-nav">` list and the footer "Explore" list on every page. The current page's menu link carries `aria-current="page"`, which underlines it in red.

## Publishing on GitHub Pages

1. Upload every file in this folder to the root of your repository.
2. In the repository, go to Settings > Pages, set the source to the main branch and the root folder, and save.
3. For the custom domain, enter it under Settings > Pages > Custom domain, then add the DNS records GitHub shows you at Namecheap.

Links between pages use plain file names (`research.html`), so the site also works when you open `index.html` straight from your computer.

## Research briefs

Briefs share one template in `site.css`: a `brief-head` with eyebrow "Research Brief No. N · State", key findings, numbered figures, a "Read with care" section, sources and a suggested citation. Add each new brief to the list on `research.html` and, if it is the newest, to the feature on `index.html`.

## Brief PDFs

The PDFs come from two scripts in `_tools/` (Jekyll doesn't publish that folder).

- **Briefs 1, 2, 3 and 6:** `python3 _tools/build_brief_pdfs.py` prints each brief's own web page to PDF.
- **Briefs 4 and 5 (Washington and Idaho):** these are designed booklets, so each has its own print source in `_tools/print/`: `smart-on-crime-washington.html` and `smart-on-crime-idaho.html`, sharing `print.css` and `print.js`. Each `<section class="page">` is one letter-size page. Edit the text there, then run `python3 _tools/build_print_pdfs.py`. It stops if any page's text runs into the footer, and it rewrites the PDF and its `-cover.png`. Keep the page count a multiple of 4 so the briefs still print as ledger booklets.

No Chrome on hand? Pushing a change under `_tools/print/` runs the "Build print PDFs" GitHub Action, which checks every page and offers the PDFs as a download (`print-pdfs`). To have it commit the rebuilt PDFs and covers for you, start it from the Actions tab on your branch with "Commit the rebuilt files" ticked. When a PDF's size changes, update the size shown next to its download link on the brief's page.

The print fonts in `_tools/print/fonts/` (Bitter, Nunito Sans and Michroma) are under the SIL Open Font License; see `OFL.txt` there.

## Session tracker data

`session.html` reads `bills.json` from this folder. Until it has bills, the page shows a "tracking opens with the session" note. Expected format:

```json
{
  "updated": "January 14, 2027",
  "bills": [
    {
      "bill": "HB 1125",
      "area": "Corrections and reentry",
      "summary": "Lets a judge review a long sentence after time served.",
      "status": "In committee",
      "last_action": "Public hearing, House Community Safety",
      "last_action_date": "Jan. 13, 2027",
      "url": "https://app.leg.wa.gov/billsummary?BillNumber=1125&Year=2027"
    }
  ]
}
```

`area` must be one of: Corrections and reentry; Voting rights; Jails and local justice; State workforce and higher education. A scheduled GitHub Action can regenerate this file; keep any API keys in the repository's Actions secrets, never in the page.

## Tabled work

The DOC year-end spending brief (formerly No. 4) was taken off the site on Nov. 22, 2026, until the research is finished. Its files now live in the private `barnone-drafts` repository. Give it the next open number when it returns.

Drafts: work on unpublished briefs in the private `barnone-drafts` repository, not on branches here. This repository is public, and every branch in it can be read by anyone.
