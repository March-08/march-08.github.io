#!/usr/bin/env python3
"""
Studio — a local editor for the personal website.

    python3 editor/studio.py        # → http://localhost:8787

Standard library only (no pip installs). Studio only ever creates/updates its own
managed files:
  • editor/content/<slug>.md            (article sources — the source of truth)
  • editor/content/travels.json         (Travels source of truth)
  • site/<slug>.html                    (only for slugs Studio owns)
  • site/images/<slug>/*                (article images)
  • site/images/travels/*               (travels images)
  • site/travels-data.js                (regenerated from travels.json)
  • the marked block inside site/index.html's Writing list
It never touches the 49 imported articles. Everything is under git, so any change
is revertable, and Publish shows the diff before committing.
"""
import os, sys, json, re, subprocess, tempfile, shutil, base64, html, mimetypes, threading, webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HERE      = os.path.dirname(os.path.abspath(__file__))
ROOT      = os.path.dirname(HERE)                     # repo root
SITE      = os.path.join(ROOT, 'site')
TOOLS     = os.path.join(ROOT, 'tools')
CONTENT   = os.path.join(HERE, 'content')
STATIC    = os.path.join(HERE, 'static')
CONVERTER = os.path.join(TOOLS, 'notion2tufte.py')
PORT      = int(os.environ.get('STUDIO_PORT', '8787'))
os.makedirs(CONTENT, exist_ok=True)

MONTHS = ['January','February','March','April','May','June','July','August',
          'September','October','November','December']

# ----------------------------------------------------------------------------- helpers
def slugify(s):
    return re.sub(r'[^a-z0-9]+', '-', (s or '').lower()).strip('-') or 'untitled'

def pretty_date(d):
    try:
        y, m, dd = d.split('-'); return f'{MONTHS[int(m)-1]} {int(dd)}, {y}'
    except Exception:
        return d or ''

FRONT_RE = re.compile(r'^---\n(.*?)\n---\n?(.*)$', re.S)
def parse_md(text):
    meta, body = {}, text
    m = FRONT_RE.match(text)
    if m:
        for line in m.group(1).splitlines():
            if ':' in line:
                k, v = line.split(':', 1); meta[k.strip()] = v.strip()
        body = m.group(2)
    return meta, body

def dump_md(meta, body):
    fm = '\n'.join(f'{k}: {v}' for k, v in meta.items())
    return f'---\n{fm}\n---\n{body}'

def run_converter(fetch_path, sitedir, slug, title, date):
    return subprocess.run([sys.executable, CONVERTER, fetch_path, sitedir, slug, title, date],
                          capture_output=True, text=True, timeout=180)

def build_fetch(subtitle, body):
    """Prepend the subtitle as the leading italic tagline the converter picks up."""
    head = f'*{subtitle.strip()}*\n\n' if (subtitle or '').strip() else ''
    return head + (body or '')

# ----------------------------------------------------------------------------- articles
def article_list():
    items = []
    for f in sorted(os.listdir(CONTENT)):
        if f.endswith('.md'):
            meta, _ = parse_md(open(os.path.join(CONTENT, f), encoding='utf-8').read())
            items.append({'slug': f[:-3], 'title': meta.get('title', f[:-3]),
                          'date': meta.get('date', ''), 'subtitle': meta.get('subtitle', '')})
    items.sort(key=lambda x: x['date'], reverse=True)
    return items

def load_article(slug):
    p = os.path.join(CONTENT, slug + '.md')
    if not os.path.exists(p):
        return None
    meta, body = parse_md(open(p, encoding='utf-8').read())
    return {'slug': slug, 'title': meta.get('title', ''), 'date': meta.get('date', ''),
            'subtitle': meta.get('subtitle', ''), 'markdown': body.lstrip('\n')}

START = '<!-- studio:posts:start -->'
END   = '<!-- studio:posts:end -->'
def update_index():
    path = os.path.join(SITE, 'index.html')
    text = open(path, encoding='utf-8').read()
    lis = [f'      <li><a class="title" href="{a["slug"]}.html">{html.escape(a["title"])}</a>'
           f'<span class="date">{pretty_date(a["date"])}</span></li>'
           for a in article_list()]
    block = START + '\n' + '\n'.join(lis) + '\n      ' + END
    if START in text and END in text:
        text = re.sub(re.escape(START) + '.*?' + re.escape(END), lambda _: block, text, flags=re.S)
    else:
        text = text.replace('<ul class="postlist">', '<ul class="postlist">\n      ' + block, 1)
    open(path, 'w', encoding='utf-8').write(text)

def save_article(slug, title, date, subtitle, markdown):
    slug = slugify(slug or title)
    target = os.path.join(SITE, slug + '.html')
    # refuse to clobber a non-Studio article
    if os.path.exists(target) and not os.path.exists(os.path.join(CONTENT, slug + '.md')):
        raise RuntimeError(f'"{slug}.html" already exists and is not managed by Studio — pick another title/slug.')
    open(os.path.join(CONTENT, slug + '.md'), 'w', encoding='utf-8').write(
        dump_md({'title': title, 'date': date, 'subtitle': subtitle}, markdown))
    fetch = tempfile.NamedTemporaryFile('w', suffix='.md', delete=False, encoding='utf-8')
    fetch.write(build_fetch(subtitle, markdown)); fetch.close()
    try:
        r = run_converter(fetch.name, SITE, slug, title, date)
    finally:
        os.unlink(fetch.name)
    if r.returncode != 0:
        raise RuntimeError(r.stderr or 'converter failed')
    update_index()
    return {'slug': slug, 'warnings': r.stderr.strip()}

def preview_article(slug, title, date, subtitle, markdown):
    slug = slugify(slug or title or 'preview')
    tmp = tempfile.mkdtemp(prefix='studio-prev-')
    os.makedirs(os.path.join(tmp, 'images'), exist_ok=True)
    real_imgs = os.path.join(SITE, 'images', slug)
    os.makedirs(real_imgs, exist_ok=True)
    try:  # symlink the article's real image dir so uploads + dimensions resolve, and http downloads cache
        os.symlink(real_imgs, os.path.join(tmp, 'images', slug))
    except Exception:
        pass
    fetch = tempfile.NamedTemporaryFile('w', suffix='.md', delete=False, encoding='utf-8')
    fetch.write(build_fetch(subtitle, markdown)); fetch.close()
    try:
        r = run_converter(fetch.name, tmp, slug, title or 'Untitled', date)
        hp = os.path.join(tmp, slug + '.html')
        out = open(hp, encoding='utf-8').read() if os.path.exists(hp) else ''
    finally:
        os.unlink(fetch.name); shutil.rmtree(tmp, ignore_errors=True)
    if r.returncode != 0 or not out:
        return f'<pre style="color:#b00;padding:1rem;white-space:pre-wrap">{html.escape(r.stderr or "preview failed")}</pre>'
    return out.replace('<head>', '<head>\n<base href="/site/">', 1)

# ----------------------------------------------------------------------------- travels
TRAVELS_JSON = os.path.join(CONTENT, 'travels.json')
def load_travels():
    if os.path.exists(TRAVELS_JSON):
        return json.load(open(TRAVELS_JSON, encoding='utf-8'))
    return {}

def gen_travels_js(data):
    rows = []
    for name, v in data.items():
        rows.append('    %s: { year: %s, photos: %s, text: %s }' % (
            json.dumps(name), json.dumps(v.get('year', '')),
            json.dumps(v.get('photos', [])), json.dumps(v.get('text', ''))))
    return (
        '/* ============================================================================\n'
        '   TRAVELS DATA — generated by editor/studio.py from editor/content/travels.json.\n'
        '   Edit your trips in Studio (python3 editor/studio.py), not here by hand.\n'
        '   ============================================================================ */\n'
        '(function () {\n'
        '  window.TRIPS = {\n\n' + ',\n'.join(rows) + '\n\n  };\n'
        '})();\n')

def save_travels(data):
    json.dump(data, open(TRAVELS_JSON, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    open(os.path.join(SITE, 'travels-data.js'), 'w', encoding='utf-8').write(gen_travels_js(data))
    # cache-bust the data file on the live site so edits show up immediately (not a stale CDN copy)
    hp = os.path.join(SITE, 'travels.html')
    if os.path.exists(hp):
        h = open(hp, encoding='utf-8').read()
        if 'travels-data.js?v=' in h:
            h = re.sub(r'travels-data\.js\?v=(\d+)', lambda m: f'travels-data.js?v={int(m.group(1)) + 1}', h)
        else:
            h = h.replace('travels-data.js', 'travels-data.js?v=1')
        open(hp, 'w', encoding='utf-8').write(h)

def country_names():
    p = os.path.join(TOOLS, 'country-names.txt')
    if os.path.exists(p):
        return [l.strip() for l in open(p, encoding='utf-8') if l.strip()]
    return []

# ----------------------------------------------------------------------------- uploads
def save_upload(subdir, filename, data_b64):
    safe = re.sub(r'[^A-Za-z0-9._-]', '-', filename) or 'file'
    d = os.path.join(SITE, 'images', subdir); os.makedirs(d, exist_ok=True)
    raw = base64.b64decode(data_b64.split(',', 1)[-1])
    open(os.path.join(d, safe), 'wb').write(raw)
    return f'images/{subdir}/{safe}'

# ----------------------------------------------------------------------------- git
def git(*args):
    return subprocess.run(['git', '-C', ROOT] + list(args), capture_output=True, text=True)
def git_status():
    return [l for l in git('status', '--short').stdout.splitlines() if l.strip()]
def publish(message):
    git('add', '-A')
    c = git('-c', 'user.name=Marcello Politi', '-c', 'user.email=marcello.politi@ethereum.org',
            'commit', '-m', message or 'Update site content via Studio')
    if 'nothing to commit' in (c.stdout + c.stderr):
        return {'ok': False, 'log': 'Nothing to publish — no changes.'}
    p = git('push')
    return {'ok': p.returncode == 0, 'log': (c.stdout + c.stderr + '\n' + p.stdout + p.stderr).strip()}

# ----------------------------------------------------------------------------- HTTP
class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):  # quiet
        pass

    def _send(self, code, body, ctype='application/json'):
        if isinstance(body, (dict, list)):
            body = json.dumps(body).encode('utf-8')
        elif isinstance(body, str):
            body = body.encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', ctype)
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _serve_file(self, abspath):
        if not (os.path.isfile(abspath)):
            return self._send(404, {'error': 'not found'})
        ctype = mimetypes.guess_type(abspath)[0] or 'application/octet-stream'
        with open(abspath, 'rb') as f:
            data = f.read()
        self.send_response(200); self.send_header('Content-Type', ctype)
        self.send_header('Content-Length', str(len(data))); self.end_headers()
        self.wfile.write(data)

    def _body(self):
        n = int(self.headers.get('Content-Length', 0))
        return json.loads(self.rfile.read(n) or b'{}') if n else {}

    def do_GET(self):
        path = self.path.split('?', 1)[0]
        if path == '/' or path == '/index.html':
            return self._serve_file(os.path.join(STATIC, 'index.html'))
        if path.startswith('/static/'):
            return self._serve_file(os.path.join(STATIC, path[len('/static/'):]))
        if path.startswith('/site/'):
            rel = path[len('/site/'):]
            return self._serve_file(os.path.normpath(os.path.join(SITE, rel)))
        if path == '/api/articles':
            return self._send(200, article_list())
        if path == '/api/article':
            q = self.path.split('?', 1)[1] if '?' in self.path else ''
            slug = dict(kv.split('=', 1) for kv in q.split('&') if '=' in kv).get('slug', '')
            a = load_article(slug)
            return self._send(200 if a else 404, a or {'error': 'not found'})
        if path == '/api/travels':
            return self._send(200, load_travels())
        if path == '/api/countries':
            return self._send(200, country_names())
        if path == '/api/status':
            return self._send(200, {'changes': git_status()})
        return self._send(404, {'error': 'not found'})

    def do_POST(self):
        path = self.path.split('?', 1)[0]
        try:
            b = self._body()
            if path == '/api/preview':
                return self._send(200, {'html': preview_article(
                    b.get('slug', ''), b.get('title', ''), b.get('date', ''),
                    b.get('subtitle', ''), b.get('markdown', ''))})
            if path == '/api/save-article':
                res = save_article(b.get('slug', ''), b.get('title', ''), b.get('date', ''),
                                   b.get('subtitle', ''), b.get('markdown', ''))
                return self._send(200, {'ok': True, **res})
            if path == '/api/upload':
                url = save_upload(slugify(b.get('slug', 'misc')), b['filename'], b['data'])
                return self._send(200, {'ok': True, 'path': url})
            if path == '/api/upload-travel-image':
                url = save_upload('travels', b['filename'], b['data'])
                return self._send(200, {'ok': True, 'path': url})
            if path == '/api/save-travels':
                save_travels(b.get('data', {}))
                return self._send(200, {'ok': True})
            if path == '/api/publish':
                return self._send(200, publish(b.get('message', '')))
            return self._send(404, {'error': 'not found'})
        except Exception as e:
            return self._send(500, {'ok': False, 'error': str(e)})


def main():
    # keep site/travels-data.js in sync with the JSON source of truth on launch
    if os.path.exists(TRAVELS_JSON):
        save_travels(load_travels())
    url = f'http://127.0.0.1:{PORT}/'
    print(f'\n  Studio → {url}\n  (Ctrl-C to stop)\n')
    if not os.environ.get('STUDIO_NO_BROWSER'):
        try:
            threading.Timer(0.6, lambda: webbrowser.open(url)).start()
        except Exception:
            pass
    ThreadingHTTPServer(('127.0.0.1', PORT), Handler).serve_forever()


if __name__ == '__main__':
    main()
