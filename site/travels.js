(function () {
  // --- DUMMY DATA (replace with real trips) — keyed by exact GeoJSON country name ---
  const VISITS = {
    "Italy": { year: "Home", photos: ["images/photo.jpeg"],
      text: "Where it all starts. Rome, the coast, and endless espresso. Dummy text — swap in a real note about home and travels across Italy." },
    "Netherlands": { year: "2024", photos: ["images/avatar.png", "images/photo.jpeg"],
      text: "Amsterdam canals and a conference or two. Placeholder text about the trip — the food, the bikes, the rain." },
    "Japan": { year: "2023", photos: ["images/photo.jpeg"],
      text: "Tokyo neon and Kyoto temples. Dummy travel note: ramen counters, bullet trains, and getting cheerfully lost in Shinjuku." },
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
    pbody.innerHTML =
      `<h2>${name}</h2><div class="yr">${v.year || ""}</div>` +
      v.photos.map(src => `<img src="${src}" alt="${name}">`).join("") +
      `<p>${v.text}</p>`;
    panel.classList.add("open");
  }
  function closePanel() {
    panel.classList.remove("open");
    if (active) { active.classList.remove("active"); active = null; }
  }
  panel.querySelector(".close").addEventListener("click", closePanel);
  document.addEventListener("keydown", e => { if (e.key === "Escape") closePanel(); });

  function draw() {
    const w = container.clientWidth, h = container.clientHeight;
    svg.attr("viewBox", `0 0 ${w} ${h}`).attr("preserveAspectRatio", "xMidYMid slice");
    // full-bleed rectangular Mercator: span the whole width, crop the poles vertically
    const proj = d3.geoMercator().scale(w / (2 * Math.PI)).translate([w / 2, h * 0.62]);
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
