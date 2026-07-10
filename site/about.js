(function () {
  // Timeline content lives in about-data.js (window.TIMELINE) — edit that file.
  var DATA = window.TIMELINE || [];
  var timeline = document.getElementById("timeline");
  if (!timeline) return;

  var TAG = { work: "Experience", edu: "Education" };

  // --- build the DOM from the data ---
  DATA.forEach(function (d, i) {
    var side = i % 2 === 0 ? "right" : "left";   // alternate around the central spine
    var item = document.createElement("div");
    item.className = "tl-item reveal " + side;
    item.setAttribute("data-kind", d.kind || "work");
    item.innerHTML =
      '<div class="tl-badge"><img src="' + d.logo + '" alt="' + (d.org || "") + '"></div>' +
      '<div class="tl-card">' +
        '<span class="tl-tag">' + (TAG[d.kind] || TAG.work) + '</span>' +
        '<h3 class="tl-role">' + d.role + '</h3>' +
        '<div class="tl-org">' + d.org + '</div>' +
        '<div class="tl-meta">' + d.meta + '</div>' +
        '<p class="tl-text">' + d.text + '</p>' +
      '</div>';
    timeline.appendChild(item);
  });

  // --- extra sections below the timeline (skills / languages / honors) ---
  var A = window.ABOUT || {};
  var extra = document.getElementById("aboutExtra");

  function block(title, bodyHTML) {
    var b = document.createElement("section");
    b.className = "about-block reveal";
    b.innerHTML = '<h2 class="about-h">' + title + '</h2>' + bodyHTML;
    extra.appendChild(b);
  }
  function esc(s) { return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;"); }

  if (extra && A.skills && A.skills.length) {
    var sk = A.skills.map(function (g) {
      return '<div class="skillgroup"><h4>' + esc(g.group) + '</h4><div class="chips">' +
        g.items.map(function (it) { return '<span class="chip">' + esc(it) + '</span>'; }).join("") +
        '</div></div>';
    }).join("");
    block("Skills", '<div class="skillgroups">' + sk + '</div>');
  }
  if (extra && A.languages && A.languages.length) {
    var lg = A.languages.map(function (l) {
      return '<div class="lang"><span class="lang-name">' + esc(l.name) + '</span>' +
        '<span class="lang-level">' + esc(l.level) + '</span></div>';
    }).join("");
    block("Languages", '<div class="langs">' + lg + '</div>');
  }
  if (extra && A.honors && A.honors.length) {
    var hn = A.honors.map(function (h) {
      return '<div class="honor"><span class="honor-year">' + esc(h.year) + '</span>' +
        '<span class="honor-body"><span class="honor-title">' + esc(h.title) + '</span>' +
        '<span class="honor-org">' + esc(h.org) + '</span></span></div>';
    }).join("");
    block("Honors &amp; Certifications", '<div class="honors">' + hn + '</div>');
  }

  var spineFill = document.getElementById("spineFill");
  // everything that animates in on scroll: timeline entries + the extra blocks
  var items = [].slice.call(document.querySelectorAll(".tl-item, .about-block"));

  // --- reveal each entry as it scrolls into view ---
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); }
      });
    }, { threshold: 0.2, rootMargin: "0px 0px -8% 0px" });
    items.forEach(function (it) { io.observe(it); });
  } else {
    items.forEach(function (it) { it.classList.add("in"); });   // no-JS-observer fallback
  }

  // --- grow the coloured spine down to the middle of the screen as you scroll ---
  function updateSpine() {
    var r = timeline.getBoundingClientRect();
    var total = timeline.offsetHeight;
    var progress = window.innerHeight * 0.5 - r.top;             // how far we've scrolled through it
    spineFill.style.height = Math.max(0, Math.min(total, progress)) + "px";
  }
  // Reveal anything already at/above the fold too — covers jump-scrolls (End key,
  // anchor jumps) that an IntersectionObserver can skip over.
  function revealPass() {
    var trigger = window.innerHeight * 0.9;
    items.forEach(function (it) {
      if (!it.classList.contains("in") && it.getBoundingClientRect().top < trigger) it.classList.add("in");
    });
  }
  var ticking = false;
  window.addEventListener("scroll", function () {
    if (!ticking) { window.requestAnimationFrame(function () { updateSpine(); revealPass(); ticking = false; }); ticking = true; }
  }, { passive: true });
  window.addEventListener("resize", updateSpine);
  updateSpine();
})();
