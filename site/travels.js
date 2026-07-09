(function () {
  // Trip content lives in travels-data.js (window.TRIPS) — edit that file to add trips.
  const VISITS = window.TRIPS || {};

  const geo = window.WORLD_GEOJSON;
  const feats = geo.features.filter(f => !f.properties || f.properties.name !== "Antarctica");
  const container = document.getElementById("map");
  const panel = document.getElementById("panel");
  const pbody = panel.querySelector(".pbody");
  const svg = d3.select("#map").append("svg");
  let active = null;

  function openPanel(name, node) {
    const v = VISITS[name];
    if (!v) return;
    if (active) active.classList.remove("active");
    active = node; node.classList.add("active");
    const photos = v.photos || [];
    let gallery = "";
    if (photos.length > 1) {
      gallery =
        `<div class="gallery">` +
        `<img class="slide" src="${photos[0]}" alt="${name}">` +
        `<button class="gnav prev" aria-label="Previous photo">&#8249;</button>` +
        `<button class="gnav next" aria-label="Next photo">&#8250;</button>` +
        `<div class="counter"><span class="cur">1</span>&thinsp;/&thinsp;${photos.length}</div>` +
        `</div>`;
    } else if (photos.length === 1) {
      gallery = `<img src="${photos[0]}" alt="${name}">`;
    }
    pbody.innerHTML = `<h2>${name}</h2><div class="yr">${v.year || ""}</div>${gallery}<p>${v.text}</p>`;

    if (photos.length > 1) {
      let idx = 0;
      const img = pbody.querySelector(".slide");
      const cur = pbody.querySelector(".counter .cur");
      const show = () => { img.src = photos[idx]; cur.textContent = idx + 1; };
      pbody.querySelector(".prev").addEventListener("click", () => { idx = (idx - 1 + photos.length) % photos.length; show(); });
      pbody.querySelector(".next").addEventListener("click", () => { idx = (idx + 1) % photos.length; show(); });
    }
    panel.classList.add("open");
  }
  function closePanel() {
    panel.classList.remove("open");
    if (active) { active.classList.remove("active"); active = null; }
  }
  panel.querySelector(".close").addEventListener("click", closePanel);
  document.addEventListener("keydown", e => { if (e.key === "Escape") closePanel(); });

  // --- drag the left edge to resize the panel (content reflows automatically) ---
  const resizer = panel.querySelector(".resizer");
  let resizing = false;
  const setWidth = clientX => {
    let w = window.innerWidth - clientX;                 // panel is anchored to the right edge
    w = Math.max(300, Math.min(window.innerWidth * 0.95, w));
    panel.style.width = w + "px";
  };
  const startResize = () => { resizing = true; panel.classList.add("resizing"); document.body.classList.add("resizing"); };
  const endResize = () => { resizing = false; panel.classList.remove("resizing"); document.body.classList.remove("resizing"); };
  resizer.addEventListener("mousedown", e => { startResize(); e.preventDefault(); });
  window.addEventListener("mousemove", e => { if (resizing) setWidth(e.clientX); });
  window.addEventListener("mouseup", endResize);
  resizer.addEventListener("touchstart", e => { startResize(); }, { passive: true });
  window.addEventListener("touchmove", e => { if (resizing && e.touches[0]) setWidth(e.touches[0].clientX); }, { passive: true });
  window.addEventListener("touchend", endResize);

  function draw() {
    const w = container.clientWidth, h = container.clientHeight;
    svg.attr("viewBox", `0 0 ${w} ${h}`).attr("preserveAspectRatio", "xMidYMid slice");
    // Big full-bleed Mercator (fills the width; slight overscale crops the ±180° seam), and the
    // vertical position is pinned so the bottom edge sits near lat -58 → Argentina is always in view.
    const s = w / (2 * Math.PI) * 1.04;
    const ty = h - s * 1.25;                     // bottom edge ≈ lat -58°
    const proj = d3.geoMercator().scale(s).translate([w / 2, ty]);
    const path = d3.geoPath(proj);
    const sel = svg.selectAll("path").data(feats);
    sel.join("path")
      .attr("d", path)
      .attr("class", d => "country" + (VISITS[d.properties.name] ? " visited" : ""))
      .on("click", function (e, d) { if (VISITS[d.properties.name]) openPanel(d.properties.name, this); });
  }

  draw();
  let t; window.addEventListener("resize", () => { clearTimeout(t); t = setTimeout(draw, 150); });
})();
