#!/usr/bin/env python3
"""Add a site favicon/logo to each .linkcard preview. Downloads each domain's
favicon once into site/images/favicons/ and restructures the card as
[icon] [title / domain]. Idempotent."""
import glob, re, os, sys, ssl, urllib.request
from urllib.parse import urlparse

site = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), '..', 'site')
FAV = os.path.join(site, 'images', 'favicons')
os.makedirs(FAV, exist_ok=True)
ctx = ssl.create_default_context(); ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122 Safari/537.36'
cache = {}

def favicon(domain):
    if domain in cache: return cache[domain]
    fn = domain + '.png'
    path = os.path.join(FAV, fn)
    if os.path.exists(path) and os.path.getsize(path) > 70:
        cache[domain] = fn; return fn
    for url in (f'https://www.google.com/s2/favicons?sz=64&domain={domain}',
                f'https://icons.duckduckgo.com/ip3/{domain}.ico'):
        try:
            data = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': UA}), timeout=30, context=ctx).read()
            if data and len(data) > 70:
                open(path, 'wb').write(data); cache[domain] = fn; return fn
        except Exception:
            continue
    cache[domain] = None; return None

def rewrite(m):
    href, body = m.group(1), m.group(2)
    if 'lc-icon' in body or 'lc-body' in body:      # already processed
        return m.group(0)
    dom = re.sub(r'^www\.', '', urlparse(href).netloc)
    fn = favicon(dom)
    icon = f'<img class="lc-icon" src="images/favicons/{fn}" alt="">' if fn else '<span class="lc-icon lc-icon-blank"></span>'
    return f'<a class="linkcard" href="{href}">{icon}<span class="lc-body">{body}</span></a>'

changed = 0
for f in glob.glob(os.path.join(site, '*.html')):
    t = open(f, encoding='utf-8').read()
    t2 = re.sub(r'<a class="linkcard" href="([^"]+)">(.*?)</a>', rewrite, t, flags=re.S)
    if t2 != t:
        open(f, 'w', encoding='utf-8').write(t2); changed += 1
print(f'linkicons: updated {changed} files; favicons cached: {sum(1 for v in cache.values() if v)}/{len(cache)}')
print('domains:', {d: bool(v) for d, v in cache.items()})
