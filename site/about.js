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

  var items = [].slice.call(timeline.querySelectorAll(".tl-item"));
  var spineFill = document.getElementById("spineFill");

  // --- reveal each entry as it scrolls into view ---
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); }
      });
    }, { threshold: 0.25, rootMargin: "0px 0px -8% 0px" });
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
