# Marcello Politi — personal website

A writing-first personal site (essays + technical articles), styled after
[nicola.io](https://nicola.io) using **Tufte CSS + ET Book**. Content is migrated
from a Notion workspace. The output is a **static site** — no build step needed to
serve it; just host the `site/` folder.

## Layout

```
site/          the deployable static site
  index.html   home (bio + reverse-chron writing list)
  <slug>.html  one file per article (49)
  images/<slug>/   per-article images (+ images/favicons/ for link cards)
  tufte.css    base theme (from nicola.io)
  custom.css   all site-specific styling (cards, captions, code, footnotes, math, layout)
  hljs.css, highlight.min.js   code syntax highlighting (highlight.js, GitHub light)
  site.js      click-to-play video facade + hljs init
  fonts/       ET Book / ETBembo + icomoon
sources/       the Notion source (enhanced-markdown) for each article — the build input
tools/         the migration/build pipeline (see below)
```

## Viewing locally

```
cd site && python3 -m http.server 8765
# open http://127.0.0.1:8765/index.html
```
(Everything renders over `file://` too, except inline YouTube playback, which needs an http origin.)

## Rebuilding

The pipeline (all in `tools/`):

1. `notion2tufte.py <source> <site_dir> <slug> "<title>" "<date>"` — converts one
   Notion source into `site/<slug>.html` + downloads/reuses `site/images/<slug>/`.
   Handles headings, code (with syntax classes), tables, TOC, callouts/deep-dives,
   `$…$`/`$$…$$` math, images (any host + Wikimedia for `file://`), videos, bookmarks,
   footnotes, subtitle detection, etc.
2. `postfix.py site` — idempotent HTML cleanup (backslash escapes, `<br>`, color spans,
   fold image captions, turn standalone links into preview cards, remove failed images).
3. `linkicons.py site` — adds site favicons to link-preview cards.
4. `articles.py` — regenerates `index.html` + `articles.tsv` (id / slug / title / date).

Rebuild everything from the saved sources (no Notion access needed — images are reused
if already present):

```
while IFS=$'\t' read -r id slug title date; do
  python3 tools/notion2tufte.py "sources/$slug.txt" "$PWD/site" "$slug" "$title" "$date"
done < tools/articles.tsv
python3 tools/postfix.py site && python3 tools/linkicons.py site && python3 tools/articles.py
```

To pull fresh content from Notion, re-fetch the page via the Notion integration into a
source file, then run the same steps.

## Hosting

Static — deploy the `site/` folder to GitHub Pages, Netlify, Vercel, etc.
