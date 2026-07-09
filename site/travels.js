(function () {
  // simple labelled placeholder image (data-URI) so the demo carousel has distinct slides
  const ph = (label, bg) => "data:image/svg+xml," + encodeURIComponent(
    `<svg xmlns='http://www.w3.org/2000/svg' width='640' height='430'><rect width='640' height='430' fill='${bg}'/>` +
    `<text x='320' y='228' font-family='Georgia' font-size='42' fill='#ffffff' text-anchor='middle'>${label}</text></svg>`);

  // --- DUMMY DATA (replace with real trips) — keyed by exact GeoJSON country name ---
  const VISITS = {
    "Italy": { year: "Home", photos: ["images/photo.jpeg"],
      text: "Where it all starts. Rome, the coast, and endless espresso. Dummy text — swap in a real note about home and travels across Italy." },
    "Netherlands": { year: "2024", photos: ["images/avatar.png", "images/photo.jpeg"],
      text: "Amsterdam canals and a conference or two. Placeholder text about the trip — the food, the bikes, the rain." },
    "Japan": { year: "2023", photos: [ph("Tokyo", "#2f8fd8"), ph("Kyoto", "#12659f"), ph("Osaka", "#4aa5e6")],
      text: "Tokyo neon and Kyoto temples. Dummy travel note: ramen counters, bullet trains, and getting cheerfully lost in Shinjuku. (Three demo photos — use the arrows.)" },
    "United States of America": { year: "2022", photos: ["images/avatar.png"],
      text: "From the Bay Area to the East Coast. Placeholder text — replace with a story from the trip." },
    "France": { year: "2023", photos: ["images/photo.jpeg"],
      text: "Paris and the south. Dummy note about museums, markets, and a very long walk along the Seine." },
    "Iceland": { year: "2021", photos: ["images/avatar.png"],
      text: "Waterfalls, black-sand beaches, and the northern lights. Placeholder travel text goes here." }
  };

  const geo = window.WORLD_GEOJSON;
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
    // full-bleed rectangular Mercator; scale slightly past full-width so the ±180° antimeridian
    // edges (and their stray vertical seam) crop off-screen
    const proj = d3.geoMercator().scale(w / (2 * Math.PI) * 1.08).translate([w / 2, h * 0.62]);
    const path = d3.geoPath(proj);
    const sel = svg.selectAll("path").data(geo.features);
    sel.join("path")
      .attr("d", path)
      .attr("class", d => "country" + (VISITS[d.properties.name] ? " visited" : ""))
      .on("click", function (e, d) { if (VISITS[d.properties.name]) openPanel(d.properties.name, this); });
  }

  draw();
  let t; window.addEventListener("resize", () => { clearTimeout(t); t = setTimeout(draw, 150); });
})();
