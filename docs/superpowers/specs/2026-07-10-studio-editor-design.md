# Studio — a local editor for the personal website

**Date:** 2026-07-10
**Status:** approved

## Goal

A local, Notion/Medium-like editor that lets Marcello:

1. **Write new articles** in the same Tufte style as the existing ones — with
   sidenotes, images, GIFs, YouTube videos, embeds (any site / Google Slides),
   code, and math.
2. **Edit Travels** — add/edit countries and their side-peek content (year, text,
   multiple images).

Hard constraint: **must never break the live site.** Everything is written under
git and previewed before saving.

## Key decisions

- **Same repo, `editor/` folder.** The editor is tightly coupled to this repo's
  files and to `tools/notion2tufte.py`. The published site is only `site/`, so the
  editor is never served/exposed. A separate repo would only add path-config
  friction.
- **Editor paradigm: Markdown + live preview + insert toolbar.** Not a from-scratch
  WYSIWYG (fragile to map to exact Tufte HTML). The toolbar inserts the right
  syntax and uploads images, so the user rarely types raw markdown; the preview is
  the *real* rendered article.
- **Conversion reuses `tools/notion2tufte.py` verbatim** (subprocess) so new
  articles are byte-identical in style to the existing 49.
- **Backend: Python standard library only** (`http.server`) — no `pip install`.
- **Publish model: save-always, publish-optional.** Save writes files locally; a
  separate Publish button commits + pushes after showing the diff.

## Architecture

```
editor/
  studio.py            # stdlib http.server backend (router + file I/O + git)
  static/
    index.html         # single-page UI
    studio.css
    studio.js
  content/
    <slug>.md          # source-of-truth for each Studio-authored article
                       #   (YAML-ish front matter: title, date, subtitle)
    travels.json       # source-of-truth for Travels (seeded from travels-data.js)
  README.md
```

Run: `python3 editor/studio.py` → serves `http://localhost:8787` and opens it.

### Backend endpoints

| Method | Path | Purpose |
|---|---|---|
| GET  | `/` , `/static/*` | serve the SPA |
| GET  | `/site/*` | serve `site/` files (so previews load tufte.css/custom.css/images) |
| GET  | `/api/countries` | valid country names from `tools/country-names.txt` |
| GET  | `/api/articles` | list Studio-managed articles (`content/*.md`) |
| GET  | `/api/article?slug=` | load one managed article (front matter + markdown) |
| POST | `/api/preview` | `{title,date,subtitle,markdown}` → rendered article HTML |
| POST | `/api/save-article` | write `content/<slug>.md`, regenerate `site/<slug>.html`, update index |
| POST | `/api/upload` | `{slug,filename,dataBase64}` → `site/images/<slug>/…` |
| GET  | `/api/travels` | travels.json (seed from travels-data.js on first run) |
| POST | `/api/save-travels` | write travels.json → regenerate `site/travels-data.js` |
| POST | `/api/upload-travel-image` | `{filename,dataBase64}` → `site/images/travels/…` |
| GET  | `/api/status` | `git status --short` (list of changed files) |
| POST | `/api/publish` | `{message}` → `git add -A && commit && push` |

Uploads are sent as base64 JSON (stdlib-friendly; avoids multipart parsing).

### Article conversion

`notion2tufte.py <fetchfile> <sitedir> <slug> <title> <date>` reads the fetch file
as enhanced-markdown and writes `site/<slug>.html`. Studio writes the editor's
markdown to a temp file and calls the converter. Preview does the same to a temp
sitedir and returns the HTML with `<base href="/site/">` so relative asset paths
resolve through the `/site/*` route.

### Enhanced-markdown syntax the toolbar targets

- Headings `#`…`######`; `**bold**`, `*italic*`, `` `code` ``, `[text](url)`
- Sidenote — a parenthetical line on its own right after a paragraph: `(aside)`
- Image / GIF — `![alt](images/<slug>/file)` (uploads handled by the toolbar)
- Video — `<video src="https://youtu.be/ID">caption</video>` (YouTube facade)
- Embed — `<embed src="https://…">caption</embed>` (iframe; Google Slides normalized)
- Code — ` ```lang `; math — `$inline$`, `$$block$$`
- Callout — `<callout icon="💡" color="blue_bg">…</callout>`
- Table of contents — `<table_of_contents>`

### index.html — safe managed insertion

Studio maintains a marked region at the top of `<ul class="postlist">`:

```
<!-- studio:posts:start -->  … managed <li> entries (newest first) …  <!-- studio:posts:end -->
```

On each save the region is regenerated from `content/*.md` (sorted by date desc).
If the markers are absent they're inserted just after `<ul class="postlist">`. The
existing static `<li>` entries below are never touched.

### Travels generation

`travels.json` (`{ "Country": {year, text, photos:[…]}, … }`) → generator emits the
exact `site/travels-data.js` shape the map already consumes (`window.TRIPS = …`)
inside the current commented wrapper. The live `travels.html` keeps loading
`travels-data.js` unchanged.

## Safety

- Studio only creates/updates its own managed files (`content/*`, `site/<slug>.html`
  for slugs it owns, `site/images/<slug>/*`, `site/images/travels/*`,
  `site/travels-data.js`) plus the marked `index.html` region.
- It never edits the 49 imported articles or any other article's HTML.
- Preview-before-save; git history makes every change revertable; Publish shows the
  diff and asks for confirmation.
- Slug/required-field validation; refuses to overwrite a non-managed file.

## Scope (v1)

- **In:** create + re-edit Studio-authored articles; full Travels editing; save +
  publish; live preview; image/GIF/video/embed/sidenote/code/math via toolbar.
- **Out (v1):** editing the 49 pre-existing Notion-imported articles (they stay as
  static HTML); complex Notion tables authored in-editor (can be pasted as raw
  `<table>` markup if needed); Notebooks/Lectures editing.

## Success criteria

- A new article written in Studio renders identically to existing articles and
  appears at the top of the home Writing list after Save.
- Adding a country + images + text in Studio updates the map and its side-peek with
  no manual file editing and no change to how the site loads data.
- Nothing outside Studio's managed files changes; the live site works exactly as
  before when Studio isn't running.
