#!/usr/bin/env python3
"""Post-process generated article HTML to repair prose-level issues without re-migrating.
Operates OUTSIDE <pre> and inline <code> so code is never touched. Idempotent.

Fixes:
  1. Notion <pdf src="..."> embeds -> a link
  2. all Notion backslash escapes in prose (\\|  \\[  \\<  \\  ...) -> removed
  3. literal &lt;br&gt; -> real <br>; strip &lt;span ...&gt; color wrappers
  4. fold an "Image source:/Source:/Credit:" paragraph after a figure into its <figcaption>
  5. remove failed-image placeholder figures
"""
import glob, re, os, sys
from urllib.parse import urlparse

site = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), '..', 'site')

def fix_prose(seg):
    # Notion PDF embed block -> link (URL may contain &amp;)
    seg = re.sub(r'&lt;pdf\s+src="(.*?)".*?&gt;',
                 lambda m: f'<a href="{m.group(1).replace("&amp;","&")}">\U0001F4C4 View PDF</a>', seg)
    seg = seg.replace('&lt;/pdf&gt;', '')
    # escaped angle brackets carrying stray backslashes -> keep just the escaped char
    seg = re.sub(r'\\+&lt;', '&lt;', seg)
    seg = re.sub(r'\\+&gt;', '&gt;', seg)
    # backslash before any punctuation
    seg = re.sub(r'\\+([^\w\s&])', r'\1', seg)
    # any remaining backslashes in prose are Notion escapes -> drop
    seg = seg.replace('\\', '')
    # inline HTML Notion emits
    seg = re.sub(r'&lt;br\s*/?&gt;', '<br>', seg)
    seg = re.sub(r'&lt;span[^&]*&gt;', '', seg)
    seg = seg.replace('&lt;/span&gt;', '')
    return seg

def process(t):
    # protect <pre>...</pre> AND inline <code>...</code>
    parts = re.split(r'(<pre>.*?</pre>|<code>.*?</code>)', t, flags=re.S)
    for i in range(0, len(parts), 2):
        parts[i] = fix_prose(parts[i])
    t = ''.join(parts)
    # fold a caption-like <p> right after a figure into that figure's <figcaption>
    MARKER = re.compile(r'image by author|img by author|image by|photo by|image source|source\s*[:.]|src\s*[:.]|credit', re.I)
    def _fold(m):
        fig, p = m.group(1), m.group(2)
        if '<figcaption' in fig:            # figure already captioned -> leave the <p> as prose
            return m.group(0)
        plain = re.sub(r'<[^>]+>', '', p).strip()
        if not plain:
            return m.group(0)
        looks = bool(MARKER.search(plain)) or (len(plain) <= 70 and not plain.endswith(('.', '!', '?', ':')))
        if not looks:
            return m.group(0)
        return fig[:-len('</figure>')] + '\n  <figcaption>' + p.strip() + '</figcaption>\n</figure>'
    t = re.sub(r'(<figure>.*?</figure>)\s*<p>(.*?)</p>', _fold, t, flags=re.S)

    # clean mangled "src: <link to raw image url>" captions -> a simple Source link
    def _capclean(m):
        inner = m.group(1); plain = re.sub(r'<[^>]+>', '', inner)
        am = re.search(r'href="([^"]+)"', inner)
        if am and re.match(r'^\s*src\s*[:.]', plain, re.I) and ('">' in inner or (plain.count('http') >= 1 and re.search(r'miro\.medium|cdn-images|prod-files|\.(gif|png|jpe?g|webp)', am.group(1), re.I))):
            url = re.sub(r'<[^>]+>', '', am.group(1)).split('&quot;')[0].split('"')[0].strip()
            return f'<figcaption><a href="{url}">Source ↗</a></figcaption>'
        return m.group(0)
    t = re.sub(r'<figcaption>(.*?)</figcaption>', _capclean, t, flags=re.S)

    # standalone long links (Notion bookmark blocks) -> preview cards
    def _card(m):
        inner = m.group(1).strip()
        am = re.fullmatch(r'<a href="([^"]+)">(.*?)</a>', inner, re.S)
        if not am:
            return m.group(0)
        url = am.group(1); text = re.sub(r'<[^>]+>', '', am.group(2)).strip()
        # skip: empty, in-page anchors, and comma-separated enumerations (e.g. author lists)
        if not text or url.startswith('#') or text.count(',') >= 2:
            return m.group(0)
        dom = re.sub(r'^www\.', '', urlparse(url).netloc)
        return (f'<a class="linkcard" href="{url}">'
                f'<span class="lc-title">{text}</span>'
                f'<span class="lc-domain">{dom}</span></a>')
    t = re.sub(r'<p>(.*?)</p>', _card, t, flags=re.S)

    # clean polluted alt attributes (leaked ">url" from mangled src captions)
    t = re.sub(r'(<img\b[^>]*\balt=")[^"]*&quot;&gt;[^"]*(")', r'\1\2', t)
    # strip stray <em>/</em> that leaked inside an href value
    t = re.sub(r'(href="[^"]*?)</?em>([^"]*")', r'\1\2', t)
    # remove failed-image placeholder figures
    t = re.sub(r'<figure>\s*<div class="figph">[^<]*</div>\s*(?:<figcaption>.*?</figcaption>\s*)?</figure>\s*',
               '', t, flags=re.S)
    return t

changed = 0
for f in glob.glob(os.path.join(site, '*.html')):
    orig = open(f, encoding='utf-8').read()
    new = process(orig)
    if new != orig:
        open(f, 'w', encoding='utf-8').write(new); changed += 1
print(f'postfix: updated {changed} files')
