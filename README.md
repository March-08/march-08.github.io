# Marcello Politi — personal website

A writing-first personal site (essays + technical articles), styled after
[nicola.io](https://nicola.io) using **Tufte CSS + ET Book**. Content is migrated
from a Notion workspace. The output is a **static site** — no build step needed to
serve it; just host the `site/` folder.

## Layout

```
site/            the deployable static site
  index.html     home (bio + reverse-chron writing list)
  <slug>.html    one file per article (49)
  about.html     "About me" — scroll-revealed career/education timeline
  travels.html   interactive world map; click a country for a photo/text panel
  notebooks.html, lectures.html   Colab notebooks + courses taught
  about-data.js      timeline + languages data (edit via Studio)
  travels-data.js    map data — generated from editor/content/travels.json
  images/<slug>/     per-article images (+ images/about/, images/travels/, images/favicons/)
  tufte.css      base theme (from nicola.io)
  custom.css, about.css, travels.css   site-specific styling
  hljs.css, highlight.min.js   code syntax highlighting (highlight.js, GitHub light)
  site.js        click-to-play video facade + hljs init
  fonts/         ET Book / ETBembo + icomoon
  vendor/        d3 + world geo data for the travels map
editor/          Studio — the local editor (see "Editing the site" below)
sources/         the Notion source (enhanced-markdown) for each article
tools/           the migration/build pipeline (see "Rebuilding")
docs/            design specs
```

## Viewing locally

```
cd site && python3 -m http.server 8765
# open http://127.0.0.1:8765/index.html
```
(Everything renders over `file://` too, except inline YouTube playback, which needs an http origin.)

## Editing the site (the easy way — Studio)

**Studio** is a small local editor for writing articles and editing the Travels map,
without touching files by hand. Run:

```
python3 editor/studio.py      # opens http://localhost:8787
```

- **Articles** — a Markdown editor with a toolbar (sidenotes, image/GIF upload,
  YouTube video, embeds, code, math, callouts, TOC) and a live preview in the real
  site style. Save writes the article page and adds it to the home list.
- **Travels** — add/edit countries with a year, notes and photos.
- **Publish** — shows what changed, then commits + pushes to GitHub.

Studio only touches its own managed files (new articles, their images, the Travels
data, and a marked block in `index.html`); it never edits the 49 imported articles.
Full details in [`editor/README.md`](editor/README.md).

## Rebuilding (the original migration pipeline)

For the 49 articles imported from Notion. The pipeline (all in `tools/`):

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

The repo lives (private) on GitHub at `March-08/personal-website`. It's a **static**
site — deploy the `site/` folder to GitHub Pages, Netlify, Vercel, etc. (not yet
deployed). Studio's **Publish** button pushes changes to GitHub for you.
