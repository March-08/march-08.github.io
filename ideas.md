# Personal Website — Parked Ideas

Strong concepts explored but not chosen for the first version. Revisit later.

---

## Knowledge-graph navigation (d3-force) ⭐ parked 2026-06-23
- **Working prototype**: `drafts/idea-knowledge-graph.html` (open in a browser; loads d3 from CDN)
- **Concept**: the whole site IS an interactive force-directed graph. Hub = name; four section nodes (Writing / Work / Map / About) orbit it; papers/essays/places hang off as leaf nodes. Drag any node and the graph responds with real physics. Hover a section to light its links + reveal leaf labels; click a section to open a content panel; click a Writing leaf to open that article.
- **Two themes prototyped**: a light "knowledge graph" (paper bg, green accent — the preferred look) and a dark "neural field" variant (glowing nodes + drifting particle mesh), both built on `d3-force`.
- **Why parked**: distinctive and very researcher-coded, but more than v1 needs. Going simple first.
- **Why it's worth keeping**: spatial navigation-as-place, no scrolling, memorable — ties to the map ideas saved in [personal-website-inspirations.md](../wiki/personal-website-inspirations.md) (#04 Paolo Rollo, #05 Cecilia Baldoni).
- **If revived**: pre-compute a stable-ish layout so it doesn't jiggle on load; add reduced-motion fallback; make leaf labels legible on mobile; consider the light theme as default.
