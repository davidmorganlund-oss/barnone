# BarNone website

A multi-page static site for GitHub Pages.

## Pages

| File | Page |
| --- | --- |
| index.html | Home |
| research.html | Research |
| same-crime-more-prison.html | Research Brief No. 1: Same crime, more prison (Idaho) |
| long-sentences.html | Research Brief No. 2: Long and life sentences in Washington |
| review-act.html | Research Brief No. 3: Who would benefit from the Review Act |
| session.html | 2027 session bill tracker (reads bills.json) |
| about.html | About |
| toolkit.html | Advocacy Toolkit |
| reentry.html | Reentry Help |
| events.html | Events |
| donate.html | Donate |
| contact.html | Contact |

Shared files: `site.css` (all styles), `site.js` (menu, copy buttons, motion), `phoenix.png` and `favicon.png`. All files sit in one folder, with no subfolders. Change a style once in `site.css` and every page picks it up.

## Editing the menu

The menu and footer are repeated at the top and bottom of every page. To add or rename a page, update the `<nav class="site-nav">` list and the footer "Explore" list on every page. The current page's menu link carries `aria-current="page"`, which underlines it in red.

## Publishing on GitHub Pages

1. Upload every file in this folder to the root of your repository.
2. In the repository, go to Settings > Pages, set the source to the main branch and the root folder, and save.
3. For the custom domain, enter it under Settings > Pages > Custom domain, then add the DNS records GitHub shows you at Namecheap.

Links between pages use plain file names (`research.html`), so the site also works when you open `index.html` straight from your computer.

## Research briefs

Briefs share one template in `site.css`: a `brief-head` with eyebrow "Research Brief No. N · State", key findings, numbered figures, a "Read with care" section, sources and a suggested citation. Add each new brief to the list on `research.html` and, if it is the newest, to the feature on `index.html`.

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
