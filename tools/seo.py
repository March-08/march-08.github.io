#!/usr/bin/env python3
"""
Inject SEO metadata into every site/*.html (idempotent) and (re)generate
sitemap.xml + robots.txt. Safe to run repeatedly — it replaces a marked
<!-- seo:start -->…<!-- seo:end --> block, never duplicating.

Run after a build, and it also runs in the GitHub Pages deploy workflow so every
page (including ones just written in Studio) stays covered.

    python3 tools/seo.py [site_dir]
"""
import os, re, glob, html, json, sys

SITE   = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), '..', 'site')
BASE   = "https://march-08.github.io"
AUTHOR = "Marcello Politi"
OGIMG  = f"{BASE}/images/photo.jpeg"
HOME_DESC = ("Marcello Politi — Research Scientist at the Ethereum Foundation working on "
             "decentralized AI. Essays and technical articles on AI, machine learning, and Ethereum.")
SAMEAS = ["https://www.linkedin.com/in/marcello-politi/",
          "https://github.com/March-08",
          "https://twitter.com/_March08_",
          "https://medium.com/@marcellopoliti"]
S, E = "<!-- seo:start -->", "<!-- seo:end -->"

def clean(s):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', s or ''))).strip()

def description(text, title, is_home):
    if is_home:
        return HOME_DESC
    m = re.search(r'<p class="subtitle">(.*?)</p>', text, re.S)
    if m and clean(m.group(1)):
        return clean(m.group(1))
    # else first real paragraph, trimmed
    m = re.search(r'<article.*?<p>(.*?)</p>', text, re.S)
    d = clean(m.group(1)) if m else title
    return (d[:197] + '…') if len(d) > 200 else d

def block(url, title, desc, is_home):
    t, d = html.escape(title, True), html.escape(desc, True)
    L = [S,
         f'<meta name="description" content="{d}">',
         f'<meta name="author" content="{AUTHOR}">',
         f'<link rel="canonical" href="{url}">',
         '<meta name="robots" content="index,follow">',
         f'<meta property="og:type" content="{"website" if is_home else "article"}">',
         f'<meta property="og:site_name" content="{AUTHOR}">',
         f'<meta property="og:title" content="{t}">',
         f'<meta property="og:description" content="{d}">',
         f'<meta property="og:url" content="{url}">',
         f'<meta property="og:image" content="{OGIMG}">',
         '<meta name="twitter:card" content="summary_large_image">',
         f'<meta name="twitter:title" content="{t}">',
         f'<meta name="twitter:description" content="{d}">',
         f'<meta name="twitter:image" content="{OGIMG}">']
    if is_home:
        person = {"@context": "https://schema.org", "@type": "Person", "name": AUTHOR,
                  "url": BASE + "/", "image": OGIMG, "jobTitle": "Research Scientist",
                  "worksFor": {"@type": "Organization", "name": "Ethereum Foundation"},
                  "sameAs": SAMEAS,
                  "knowsAbout": ["Artificial Intelligence", "Machine Learning", "Ethereum",
                                 "Decentralized AI", "Blockchain"]}
        L.append('<script type="application/ld+json">' + json.dumps(person, ensure_ascii=False) + '</script>')
    L.append(E)
    return "\n".join(L)

def inject(path):
    t = open(path, encoding='utf-8').read()
    fn = os.path.basename(path)
    is_home = (fn == 'index.html')
    url = BASE + '/' if is_home else f'{BASE}/{fn}'
    m = re.search(r'<title>(.*?)</title>', t, re.S)
    title = (m.group(1).replace(' — Marcello Politi', '').strip() if m else AUTHOR) or AUTHOR
    blk = block(url, title, description(t, title, is_home), is_home)
    if S in t and E in t:
        t = re.sub(re.escape(S) + '.*?' + re.escape(E), lambda _: blk, t, flags=re.S)
    elif '</head>' in t:
        t = t.replace('</head>', blk + '\n</head>', 1)
    else:
        return
    open(path, 'w', encoding='utf-8').write(t)

def sitemap(files):
    rows = []
    for f in files:
        fn = os.path.basename(f)
        loc = BASE + '/' if fn == 'index.html' else f'{BASE}/{fn}'
        lastmod = __import__('datetime').date.fromtimestamp(os.path.getmtime(f)).isoformat()
        rows.append(f'  <url><loc>{loc}</loc><lastmod>{lastmod}</lastmod></url>')
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + '\n'.join(rows) + '\n</urlset>\n')
    open(os.path.join(SITE, 'sitemap.xml'), 'w', encoding='utf-8').write(xml)
    open(os.path.join(SITE, 'robots.txt'), 'w', encoding='utf-8').write(
        f'User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n')

def main():
    files = sorted(glob.glob(os.path.join(SITE, '*.html')))
    for f in files:
        inject(f)
    sitemap(files)
    print(f'SEO: {len(files)} pages + sitemap.xml + robots.txt')

if __name__ == '__main__':
    main()
