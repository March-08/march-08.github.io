// Click-to-play YouTube facade: swaps the poster for an inline player on click.
// Plays inside the page (no redirect). Requires an http(s) origin — works on the
// hosted site and via a local server; not over file://.
document.addEventListener('click', function (e) {
  var el = e.target.closest && e.target.closest('.videowrap[data-yt]');
  if (!el) return;
  var id = el.getAttribute('data-yt');
  var wrap = document.createElement('div');
  wrap.className = 'embed';
  var f = document.createElement('iframe');
  f.src = 'https://www.youtube-nocookie.com/embed/' + id + '?autoplay=1&rel=0';
  f.setAttribute('allow', 'autoplay; encrypted-media; picture-in-picture; fullscreen');
  f.setAttribute('allowfullscreen', '');
  wrap.appendChild(f);
  el.parentNode.replaceChild(wrap, el);
});

// Syntax-highlight all code blocks (IDE-style colors) via highlight.js.
if (window.hljs) { try { hljs.highlightAll(); } catch (e) {} }

// Embedded X / Twitter posts: load the widget script only if a tweet is on the page.
// (Requires an http(s) origin — works on the hosted site and the local Studio server.)
if (document.querySelector('.twitter-tweet')) {
  var tw = document.createElement('script');
  tw.async = true; tw.charset = 'utf-8'; tw.src = 'https://platform.twitter.com/widgets.js';
  document.body.appendChild(tw);
}
