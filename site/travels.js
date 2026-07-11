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
    const w = container.clientWidth;
    // Full-width Mercator, but the HEIGHT is sized to the latitude band I've actually
    // visited (≈ lat 74°N Alaska/Finland down to 58°S below Argentina) plus a margin, so
    // nothing is ever cropped at the top or bottom.
    const s = w / (2 * Math.PI) * 0.94;
    const shift = w * 0.03;                        // nudge the whole map slightly to the left
    const latN = 74, latS = -58, pad = 22;         // band to show + top/bottom ocean margin
    const base = d3.geoMercator().scale(s).translate([w / 2 - shift, 0]);
    const yN = base([0, latN])[1], yS = base([0, latS])[1];
    const h = Math.round(yS - yN + pad * 2);
    const proj = d3.geoMercator().scale(s).translate([w / 2 - shift, pad - yN]);
    const path = d3.geoPath(proj);

    container.style.height = h + "px";
    svg.attr("viewBox", `0 0 ${w} ${h}`).attr("preserveAspectRatio", "xMidYMid meet");

    // Clip to just inside the ±180° meridians. A country that wraps the date line
    // otherwise paints a full-height vertical seam at -180°; this trims it off.
    const xL = proj([-180, 0])[0], xR = proj([180, 0])[0];
    const defs = svg.selectAll("defs").data([0]).join("defs");
    defs.selectAll("clipPath").data([0]).join("clipPath").attr("id", "map-clip")
      .selectAll("rect").data([0]).join("rect")
      .attr("x", xL + 1.2).attr("y", 0).attr("width", (xR - xL) - 2.4).attr("height", h);
    const g = svg.selectAll("g.lands").data([0]).join("g")
      .attr("class", "lands").attr("clip-path", "url(#map-clip)");

    const sel = g.selectAll("path").data(feats);
    sel.join("path")
      .attr("d", path)
      .attr("class", d => "country" + (VISITS[d.properties.name] ? " visited" : ""))
      .on("click", function (e, d) { if (VISITS[d.properties.name]) openPanel(d.properties.name, this); });
    // raise visited countries above their neighbours so nothing overlaps their click target
    g.selectAll(".visited").raise();
  }

  draw();
  let t; window.addEventListener("resize", () => { clearTimeout(t); t = setTimeout(draw, 150); });
})();
