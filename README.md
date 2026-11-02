# BarNone website

A multi-page static site for GitHub Pages.

## Pages

| File | Page |
| --- | --- |
| index.html | Home |
| research.html | Research |
| review-act.html | Research brief: Who would benefit from the Review Act |
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
