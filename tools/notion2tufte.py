#!/usr/bin/env python3
"""Notion enhanced-markdown -> Tufte/nicola-style HTML page. Migration renderer.

Usage:
  python3 notion2tufte.py <fetchfile> <site_dir> <slug> "<title>" "<date>"
Writes <site_dir>/<slug>.html and images into <site_dir>/images/<slug>/.
Extracts subtitle + tags from the Notion source automatically.
"""
import sys, re, html, os, urllib.request, ssl, subprocess, urllib.parse

FETCH   = sys.argv[1]
SITEDIR = sys.argv[2]
SLUG    = sys.argv[3]
TITLE   = sys.argv[4] if len(sys.argv) > 4 else ''
DATE    = sys.argv[5] if len(sys.argv) > 5 else ''
IMGDIR  = os.path.join(SITEDIR, 'images', SLUG)
IMGREL  = f'images/{SLUG}'
os.makedirs(IMGDIR, exist_ok=True)
ctx = ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE

raw = open(FETCH, encoding='utf-8').read().replace('\\n','\n').replace('\\t','\t').replace('\\"','"')
m = re.search(r'<content>(.*?)</content>', raw, re.S); content = m.group(1) if m else raw
tm = re.search(r'"Tags":\[([^\]]*)\]', raw); tags = re.findall(r'"([^"]+)"', tm.group(1)) if tm else []

def dl(url, fn):
    dst=os.path.join(IMGDIR, fn)
    if os.path.exists(dst) and os.path.getsize(dst) > 70:
        return True                      # reuse an already-downloaded image (re-convert without re-fetch)
    try:
        pr=urllib.parse.urlparse(url); ref=f'{pr.scheme}://{pr.netloc}/'
        hdr={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122 Safari/537.36',
             'Referer':ref, 'Accept':'image/avif,image/webp,image/png,image/*,*/*;q=0.8'}
        req=urllib.request.Request(url, headers=hdr)
        data=urllib.request.urlopen(req,timeout=60,context=ctx).read()
        if not data: return False
        open(os.path.join(IMGDIR,fn),'wb').write(data)
        return True
    except Exception as e:
        print(f'  DL FAIL {fn}: {e}', file=sys.stderr); return False

def dims(fn):
    p=os.path.join(IMGDIR,fn)
    try:
        out=subprocess.run(['sips','-g','pixelWidth','-g','pixelHeight',p],capture_output=True,text=True,timeout=15).stdout
        return int(re.search(r'pixelWidth:\s*(\d+)',out).group(1)), int(re.search(r'pixelHeight:\s*(\d+)',out).group(1))
    except Exception: return None,None
def size_class(fn):
    w,h=dims(fn)
    if not w: return 'med'
    r=h/w
    return 'portrait' if r>=1.15 else ('wide' if r<0.72 else 'med')

SUP=str.maketrans("0123456789+-=()n","⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾ⁿ"); SUB=str.maketrans("0123456789+-=()","₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎")
def sup(x): return x.translate(SUP) if all(c in "0123456789+-=()n" for c in x) else "^"+x
def sub(x): return x.translate(SUB) if all(c in "0123456789+-=()" for c in x) else "_"+x
def demath(e):
    e=re.sub(r'\\mathrm\{([^}]*)\}',r'\1',e); e=re.sub(r'\\text(?:it|bf|rm)?\{([^}]*)\}',r'\1',e)
    e=re.sub(r'\\d?frac\{([^}]*)\}\{([^}]*)\}',r'(\1)/(\2)',e)
    for a,b in [('\\ln','ln'),('\\log','log'),('\\times','×'),('\\cdot','·'),('\\approx','≈'),
                ('\\geq','≥'),('\\leq','≤'),('\\neq','≠'),('\\pm','±'),('\\infty','∞'),
                ('\\,',' '),('\\;',' '),('\\!','')]: e=e.replace(a,b)
    e=re.sub(r'\^\{([^}]*)\}',lambda mm:sup(mm.group(1)),e); e=re.sub(r'\^(\w)',lambda mm:sup(mm.group(1)),e)
    e=re.sub(r'_\{([^}]*)\}',lambda mm:sub(mm.group(1)),e); e=re.sub(r'_(\w)',lambda mm:sub(mm.group(1)),e)
    return re.sub(r'\s+',' ',e.replace('{','').replace('}','').replace('\\','')).strip()
def inline(t):
    # drop Notion color spans first (so adjacent italic runs merge before asterisk normalization)
    t=re.sub(r'<span[^>]*>', '', t); t=t.replace('</span>', '')
    # stash math so unescaping/escaping never corrupts LaTeX
    maths=[]
    def _stash(m): maths.append(m.group(1)); return f'\x01{len(maths)-1}\x02'
    t=re.sub(r'\$\$([^$]+?)\$\$', _stash, t)
    t=re.sub(r'\$([^$]+)\$', _stash, t)
    # unescape Notion backslash-escaped punctuation (\|  \[  \]  \(  etc.); leave * _ ` for markdown
    t=re.sub(r'\\+([|\[\]{}()#~.!>-])', r'\1', t)
    t=re.sub(r'\\+([$^])', r'\1', t)
    # Notion malformed "*NAME**: text*" (lone-italic open, stray bold before a label colon) -> drop the **.
    # The (?<!\*)\*(?!\*) guard requires a SINGLE opening asterisk so real **bold** is never touched.
    t=re.sub(r'(?<!\*)\*(?!\*)([^*\n]{1,80}?)\*\*(\s*:)', r'*\1\2', t)
    t=html.escape(t, quote=False)
    # allow the few inline HTML tags Notion emits; drop color spans (keep text)
    t=re.sub(r'&lt;(/?(?:br|sup|sub|u))\s*/?&gt;', r'<\1>', t)
    t=re.sub(r'&lt;span[^&]*&gt;', '', t); t=t.replace('&lt;/span&gt;','')
    # restore math
    t=re.sub(r'\x01(\d+)\x02', lambda mm: demath(maths[int(mm.group(1))]), t)
    t=re.sub(r'\[([^\]]+)\]\((https?://[^)]+)\)', lambda mm:f'<a href="{html.escape(mm.group(2),quote=True)}">{mm.group(1)}</a>', t)
    t=re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
    t=re.sub(r'(?<!\*)\*(?!\*)([^*]+?)\*(?!\*)', r'<em>\1</em>', t)
    t=re.sub(r'`([^`]+)`', r'<code>\1</code>', t)
    return t
def yt_id(u):
    m=re.search(r'(?:v=|youtu\.be/|embed/)([\w-]{6,})', u); return m.group(1) if m else None

content=re.sub(r'\n?\t*</?columns?>', '\n', content)
lines=content.split('\n')
out=[]; imgn=0; snid=0; subtitle=None; lead=False; i=0; N=len(lines)
listbuf=[]; quotebuf=[]; listord=False
def flush_list():
    global listbuf, listord
    if listbuf:
        tag='ol' if listord else 'ul'
        out.append(f'<{tag}>\n'+'\n'.join(f'  <li>{inline(x)}</li>' for x in listbuf)+f'\n</{tag}>')
        listbuf=[]; listord=False
def flush_quote():
    global quotebuf
    if not quotebuf: return
    if len(quotebuf)==1:
        text=quotebuf[0]; footer=''
        mm=re.search(r'\s[-–—]\s*([^-–—]{2,40})\s*$', text)
        if mm: footer=f'<footer>— {inline(mm.group(1).strip())}</footer>'; text=text[:mm.start()].rstrip()
        out.append(f'<blockquote><p>{inline(text)}</p>{footer}</blockquote>')
    else:
        out.append('<blockquote><p>'+'<br>'.join(inline(x) for x in quotebuf)+'</p></blockquote>')
    quotebuf=[]
def flush(): flush_list(); flush_quote()

IMG=re.compile(r'^!\[(.*)\]\((https?://[^)\s]+|file://.*?%7D%7D)\)\s*$', re.S)
CAPRE=re.compile(r'^\s*(Image by|Photo by|Image from|Image source|Img|src\s*[:.]|Source|Figure|Credit|Fig\.)', re.I)
def emit_img(caption_raw, fn):
    cap=inline(caption_raw.strip()) if caption_raw.strip() else ''
    if not fn:
        # download failed / hotlink-blocked — omit the figure rather than show an empty box
        return
    img=f'<img class="{size_class(fn)}" src="{IMGREL}/{fn}" alt="{html.escape(re.sub(chr(60)+".*?"+chr(62),"",cap),quote=True)}">'
    out.append('<figure>\n  '+img+('\n  <figcaption>'+cap+'</figcaption>' if cap else '')+'\n</figure>')

# --- subtitle = the first heading/italic/bold "tagline" line before the body;
#     skip leading ---, hero image, photo caption, and a heading that duplicates the title ---
_nm=re.search(r'"Name":"([^"]*)"', raw)
_title=TITLE or (_nm.group(1) if _nm else '')
_tnorm=re.sub(r'[^a-z0-9]', '', re.sub(r'[*`]', '', _title).lower())
consumed=set(); _scan=0
while _scan < min(N, 16):
    _ss=lines[_scan].strip()
    if not _ss or _ss in ('<empty-block/>', '---') or _ss.startswith('!['): _scan+=1; continue
    if CAPRE.match(_ss): _scan+=1; continue
    _hm=re.match(r'^#{1,6}\s+(.*\S)\s*$', _ss)
    if _hm: _c=_hm.group(1)
    elif _ss.startswith('**') and _ss.endswith('**') and len(_ss) > 4: _c=_ss[2:-2]
    elif _ss.startswith('*') and _ss.endswith('*') and not _ss.startswith('**') and len(_ss) > 2: _c=_ss[1:-1]
    else: break                                   # hit body text -> no subtitle
    _ctxt=_c.strip().strip('*').strip()
    consumed.add(_scan)
    if re.sub(r'[^a-z0-9]', '', _ctxt.lower()) == _tnorm and _tnorm:
        _scan+=1; continue                        # this heading just repeats the title
    subtitle=inline(_ctxt); break

while i<N:
    ln=lines[i]; s=ln.strip()
    if i in consumed: i+=1; continue
    if not s or s=='<empty-block/>': i+=1; continue
    # fenced code block ``` ... ``` — preserve raw text, no markdown, escape only
    if s.startswith('```'):
        lang=re.sub(r'[^a-z0-9+#-]', '', s[3:].strip().lower())
        cls='' if lang in ('','plaintext','text','none') else f' class="language-{lang}"'
        flush(); i+=1; code=[]
        while i<N and lines[i].strip()!='```': code.append(lines[i]); i+=1
        i+=1
        out.append('<pre><code'+cls+'>'+html.escape('\n'.join(code), quote=False)+'</code></pre>')
        continue
    # display math block $$ ... $$ (single- or multi-line)
    if s.startswith('$$'):
        flush()
        if s.rstrip().endswith('$$') and s.count('$') >= 4 and s.strip().strip('$').strip():
            expr=s.strip().strip('$').strip(); i+=1
        else:
            i+=1; mb=[]
            while i<N and lines[i].strip()!='$$':
                if lines[i].strip(): mb.append(lines[i].strip())
                i+=1
            i+=1
            expr=' '.join(mb)
        if expr: out.append(f'<p class="mathblock">{html.escape(demath(expr), quote=False)}</p>')
        continue
    vm=re.match(r'<video src="([^"]+)">(.*?)</video>', s, re.S)
    if vm:
        flush(); vid=yt_id(vm.group(1)); cap=inline(vm.group(2).strip())
        if vid:
            imgn+=1; fn=f'video-{imgn:02d}.jpg'
            ok=dl(f'https://img.youtube.com/vi/{vid}/maxresdefault.jpg', fn) or dl(f'https://img.youtube.com/vi/{vid}/hqdefault.jpg', fn)
            poster=(f'<img src="{IMGREL}/{fn}" alt="{html.escape(re.sub(chr(60)+".*?"+chr(62),"",cap),quote=True)}">' if ok else '<div class="figph">video</div>')
            out.append(f'<figure>\n  <div class="videowrap" data-yt="{vid}">\n    {poster}\n    <span class="pbtn"></span>\n  </div>'
                       +(f'\n  <figcaption>{cap} · click to play</figcaption>' if cap else '')+'\n</figure>')
        else:
            out.append(f'<p><a href="{vm.group(1)}">▶ {cap or "Video"}</a></p>')
        i+=1; continue
    em=re.match(r'<embed src="([^"]+)">(.*?)</embed>', s, re.S)
    if em:
        flush(); cap=inline(em.group(2).strip()); esrc=em.group(1)
        # normalize Google Slides / Docs share links to their embeddable form
        esrc=re.sub(r'(docs\.google\.com/presentation/d/[\w-]+)/(?:edit|pub|view)[^"]*', r'\1/embed?start=false&loop=false', esrc)
        out.append(f'<figure>\n  <div class="embed"><iframe src="{esrc}" loading="lazy" allowfullscreen></iframe></div>'
                   f'\n  <figcaption>{cap} · <a href="{esrc}">open ↗</a></figcaption>\n</figure>')
        i+=1; continue
    if s.startswith('<unknown'): i+=1; continue
    if s.startswith('!['):
        mm=IMG.match(s)
        if not mm: i+=1; continue
        flush(); imgn+=1; alt=mm.group(1); url=mm.group(2); fn=None
        if url.startswith('file://'):
            namem=re.search(r'attachment%3A[0-9a-f-]+%3A([^%]+)', url)
            fname=urllib.parse.unquote(namem.group(1)) if namem else ''
            ext=(os.path.splitext(fname)[1] or '.jpg').lower().replace('.jpeg','.jpg')
            fn=f'img-{imgn:02d}{ext}'
            fn=fn if dl(f'https://commons.wikimedia.org/wiki/Special:FilePath/{urllib.parse.quote(fname)}', fn) else None
        else:
            em=re.search(r'\.(png|jpe?g|webp|gif|svg)(?:[?#]|$)', url, re.I)
            ext='.'+em.group(1).lower().replace('jpeg','jpg') if em else '.jpg'
            fn=f'img-{imgn:02d}{ext}'
            fn=fn if dl(url, fn) else None
        if not alt.strip():
            j=i+1
            while j<N and lines[j].strip() in ('','<empty-block/>'): j+=1
            if j<N and CAPRE.match(lines[j]): alt=lines[j].strip(); i=j
        emit_img(alt, fn); i+=1; continue
    cm=re.match(r'<callout icon="([^"]*)" color="([^"]*)">(.*)', s)
    if cm:
        color=cm.group(2); buf=[]; tail=cm.group(3)
        if '</callout>' in tail: buf=[tail.replace('</callout>','')]; i+=1
        else:
            if tail.strip(): buf.append(tail)
            i+=1
            while i<N and lines[i].strip()!='</callout>': buf.append(lines[i]); i+=1
            i+=1
        buf=[b.strip() for b in buf if b.strip() and b.strip()!='<empty-block/>']
        flush()
        icon=cm.group(1)
        titled=bool(buf) and buf[0].startswith('**') and buf[0].endswith('**')
        if 'yellow' in color:
            out.append('<div class="note">\n'+'\n'.join(f'<p>{inline(b.strip("*"))}</p>' for b in buf)+'\n</div>')
        elif not titled:
            # simple callout (icon + tinted background), e.g. info/warning notes
            cls='cw-red' if 'red' in color else ('cw-green' if 'green' in color else ('cw-blue' if 'blue' in color else 'cw-gray'))
            body='<br>'.join(inline(b) for b in buf)
            out.append(f'<div class="callout-note {cls}"><span class="cw-icon">{html.escape(icon)}</span><span class="cw-body">{body}</span></div>')
        else:
            c=['<div class="deepdive">','  <span class="callout-label">Deep dive</span>']; first=True; cul=[]
            def cflush():
                if cul: c.append('  <ul>\n'+'\n'.join(f'    <li>{inline(x)}</li>' for x in cul)+'\n  </ul>'); cul.clear()
            for b in buf:
                if b.startswith('- '): cul.append(b[2:]); continue
                cflush()
                if first and b.startswith('**') and b.endswith('**'): c.append(f'  <span class="callout-title">{inline(b.strip("*"))}</span>')
                elif re.match(r'^(E\s*[≥=]|f_sim)', b) and len(b)<60: c.append(f'  <span class="formula">{inline(b)}</span>')
                else: c.append(f'  <p>{inline(b)}</p>')
                first=False
            cflush(); c.append('</div>'); out.append('\n'.join(c))
        continue
    if s.startswith('<table_of_contents'):
        flush(); out.append('<!--TOC-->'); i+=1; continue
    if s.startswith('<table'):
        flush(); blk=[ln]; i+=1
        while i<N and '</table>' not in lines[i]: blk.append(lines[i]); i+=1
        if i<N: blk.append(lines[i]); i+=1
        tbl='\n'.join(blk); hdr='header-row="true"' in blk[0]
        rows=re.findall(r'<tr>(.*?)</tr>', tbl, re.S); hrows=[]
        for ri,row in enumerate(rows):
            cells=re.findall(r'<td>(.*?)</td>', row, re.S)
            if not cells or all(not c.strip() for c in cells): continue
            tag='th' if (hdr and ri==0) else 'td'
            hrows.append('<tr>'+''.join(f'<{tag}>{inline(c.strip())}</{tag}>' for c in cells)+'</tr>')
        if hrows:
            if hdr:
                out.append('<div class="tablewrap"><table class="ntable"><thead>'+hrows[0]+'</thead><tbody>'+''.join(hrows[1:])+'</tbody></table></div>')
            else:
                out.append('<div class="tablewrap"><table class="ntable"><tbody>'+''.join(hrows)+'</tbody></table></div>')
        continue
    if s.startswith('### '): flush(); out.append(f'<h3>{inline(re.sub(chr(94)+"[*]{2}|[*]{2}$","",s[4:]).strip())}</h3>'); i+=1; continue
    if s.startswith('## '):  flush(); out.append(f'<h2>{inline(s[3:].strip())}</h2>'); i+=1; continue
    if s.startswith('# '):   flush(); out.append(f'<h2>{inline(s[2:].strip())}</h2>'); i+=1; continue
    if s.startswith('> '):
        flush_list(); quotebuf.append(s[2:]); j=i+1
        while j<N and lines[j][:1]=='\t' and lines[j].strip():   # absorb tab-indented lines into the quote
            quotebuf.append(lines[j].strip()); j+=1
        i=j; continue
    _om=re.match(r'^\d+[.)]\s+(.*)', s)
    if re.match(r'^[-*] ', s) or _om:
        flush_quote()
        if not listbuf: listord=bool(_om)                          # list type set by its first item
        item=_om.group(1) if _om else s[2:]; j=i+1
        while j<N and lines[j][:1] in ('\t',' ') and lines[j].strip() and not (re.match(r'^[-*>#]', lines[j].strip()) or re.match(r'^\d+[.)]\s', lines[j].strip())):
            item+=' '+lines[j].strip(); j+=1                       # absorb tab-indented continuation into the item
        item=re.sub(r'\s+([,.;:!?])', r'\1', item)
        listbuf.append(item); i=j; continue
    if re.fullmatch(r'-{2,}', s): i+=1; continue
    _pg=re.match(r'^<page url="([^"]+)">(.*?)</page>\s*$', s)
    if _pg:
        flush(); out.append(f'<p><a href="{_pg.group(1)}">{inline(_pg.group(2).strip())} →</a></p>'); i+=1; continue
    pm2=re.match(r'^\((.+)\)[.,;:]?\s*$', s)
    if pm2 and 6 < len(s) < 400:
        flush(); snid+=1; inner=inline(pm2.group(1).strip())
        sn=(f'<label for="sn-{snid}" class="margin-toggle sidenote-number"></label>'
            f'<input type="checkbox" id="sn-{snid}" class="margin-toggle"/>'
            f'<span class="sidenote">{inner}</span>')
        if out and out[-1].endswith('</p>'): out[-1]=out[-1][:-4]+' '+sn+'</p>'
        else: out.append(f'<p>{sn}</p>')
        i+=1; continue
    flush()
    if not lead and s.startswith('Right now, your phone'):
        out.append(f'<p><span class="newthought">Right now, your phone</span>{inline(s[len("Right now, your phone"):])}</p>'); lead=True
    else:
        out.append(f'<p>{inline(s)}</p>')
    i+=1
flush()
body='\n'.join(out)

# ---- table of contents: add ids to headings, build nav, replace marker ----
if '<!--TOC-->' in body:
    cnt=[0]
    def _addid(m):
        cnt[0]+=1; return f'<{m.group(1)} id="sec-{cnt[0]}">{m.group(2)}</{m.group(1)}>'
    body=re.sub(r'<(h2|h3)>(.*?)</\1>', _addid, body, flags=re.S)
    items=[]; k=0
    for tag,txt in re.findall(r'<(h2|h3) id="sec-\d+">(.*?)</\1>', body, re.S):
        k+=1; plain=re.sub(r'<.*?>','',txt)
        items.append(f'<li class="toc-{tag}"><a href="#sec-{k}">{plain}</a></li>')
    toc='<nav class="toc"><span class="toc-title">Contents</span><ul>'+''.join(items)+'</ul></nav>'
    body=body.replace('<!--TOC-->', toc, 1).replace('<!--TOC-->','')

# ---- assemble full page ----
nm=re.search(r'"Name":"([^"]*)"', raw)
title=TITLE or (nm.group(1) if nm else 'Untitled')
esc_title=html.escape(title, quote=False)
subt=(f'<p class="subtitle">{subtitle}.</p>' if subtitle else '')
tagstr=(' · '+', '.join(tags)) if tags else ''
datestr=(DATE+tagstr) if (DATE or tagstr) else ''
HEAD='''<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="tufte.css">
<link rel="stylesheet" href="custom.css">
<link href="https://fonts.googleapis.com/css?family=Lato:400,400italic" rel="stylesheet">
<link rel="stylesheet" href="hljs.css">
<link rel="icon" href="images/avatar.png">'''
NAV='''  <header>
    <nav class="group">
      <a href="index.html">Home</a>
      <a href="#">About me</a>
      <a href="notebooks.html">Notebooks</a>
      <a href="lectures.html">Lectures</a>
    </nav>
  </header>'''
page=f'''<!doctype html>
<html lang="en">
<head>
<title>{esc_title} — Marcello Politi</title>
{HEAD}
</head>
<body class="layout-post">
{NAV}
  <article>
    <h1>{esc_title}</h1>
    {subt}
    {f'<p class="postdate">{datestr}</p>' if datestr else ''}
{body}
  </article>
<script src="highlight.min.js"></script>
<script src="site.js"></script>
</body>
</html>
'''
open(os.path.join(SITEDIR, f'{SLUG}.html'), 'w', encoding='utf-8').write(page)
print(f'{SLUG}: images={imgn} nodes={len(out)} tags={tags} sub={bool(subtitle)} title={title!r}')
