# Studio — local editor for the site

A small, local, Notion/Medium-like editor for writing articles and editing the
Travels map. It runs on your machine, edits the files in this repo, and (optionally)
commits + pushes. **It is not part of the published site** (only `site/` is served).

## Run it

```bash
python3 editor/studio.py
```

It opens `http://localhost:8787` in your browser. Press `Ctrl-C` to stop.
No installs needed — it uses only the Python standard library, and reuses your
existing `tools/notion2tufte.py` converter so new articles look exactly like the
old ones.

## Articles

- Click **New article**, type a **title**, pick a **date**, and (optionally) a
  **subtitle**.
- Write in the left pane. The **toolbar** inserts the right thing for you:
  - **B / I** bold / italic, **H2 / H3** headings, **🔗** link
  - **◦ note** a margin *sidenote* (a line in parentheses)
  - **🖼 Image** uploads a picture or GIF into `site/images/<slug>/`
  - **▶ Video** a YouTube link (plays inline on the site)
  - **⧉ Embed** any website or a Google Slides link (as an iframe)
  - **❝ quote**, **{ } code**, **$x$ / ∑** inline / block math, **💡 callout**, **☰ TOC**
- The right pane is a **live preview** rendered in your real site style.
- **Save** writes `site/<slug>.html` and adds it to the top of the home page's
  Writing list. You can reopen and re-edit anything you wrote here (sources live in
  `editor/content/<slug>.md`).

> The ~49 older articles imported from Notion stay as they are and aren't listed in
> Studio. Studio never edits them.

## Travels

- **Travels** tab → **Add country** (type a name; it must match the map), then set a
  **year/label**, **notes**, and **photos** (upload several; reorder with ◀ ▶; delete
  with ×).
- **Save travels** regenerates `site/travels-data.js` from `editor/content/travels.json`
  (the source of truth). The map keeps loading `travels-data.js` exactly as before.
- A country with 2+ photos shows the arrow carousel in its side panel.

## Publish

- **Save** only writes local files (safe to do often while drafting).
- **Publish…** shows exactly which files changed, lets you add a message, then
  commits and pushes to GitHub. Everything is under git, so any change is revertable.

## What Studio touches

Only its own managed files: `editor/content/*`, `site/<slug>.html` for slugs it owns,
`site/images/<slug>/*`, `site/images/travels/*`, `site/travels-data.js`, and a marked
block in `site/index.html`. Nothing else.
