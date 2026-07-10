#!/usr/bin/env python3
"""Generate site/lectures.html — an index of courses taught, from tools/lectures.tsv
(id \t slug \t title \t year \t tags). Links to the per-course detail pages."""
import os, html as H

HERE = os.path.dirname(__file__)
SITE = os.path.join(HERE, '..', 'site')
rows = [l.split('\t') for l in open(os.path.join(HERE, 'lectures.tsv'), encoding='utf-8').read().splitlines() if l.strip()]

items = "\n".join(
    f'      <li><a class="title" href="{slug}.html">{H.escape(title)}</a>'
    f'<span class="date">{year} · {H.escape(tags)}</span></li>'
    for _id, slug, title, year, tags in rows)

HEAD = '''<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="tufte.css">
<link rel="stylesheet" href="custom.css">
<link href="https://fonts.googleapis.com/css?family=Lato:400,400italic" rel="stylesheet">
<link rel="icon" href="images/avatar.png">'''

page = f'''<!doctype html>
<html lang="en">
<head>
<title>Lectures — Marcello Politi</title>
{HEAD}
</head>
<body class="layout-post">
  <header>
    <nav class="group">
      <a href="index.html">Home</a>
      <a href="about.html">About me</a>
      <a href="notebooks.html">Notebooks</a>
      <a href="lectures.html">Lectures</a>
      <a href="travels.html">Travels</a>
    </nav>
  </header>
  <article>
    <h1>Lectures</h1>
    <p class="subtitle">Courses and workshops I have taught.</p>
    <ul class="postlist">
{items}
    </ul>
  </article>
<script src="highlight.min.js"></script>
<script src="site.js"></script>
</body>
</html>
'''
open(os.path.join(SITE, 'lectures.html'), 'w', encoding='utf-8').write(page)
print(f"generated lectures.html ({len(rows)} courses)")
