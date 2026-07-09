/* ============================================================================
   TRAVELS DATA  —  edit THIS file to add or change your trips.
   (No code here — just data. Reload travels.html to see changes.)

   Each entry is:   "Country Name": { year, photos, text }

   • Country Name  — must EXACTLY match the map's country name.
                     The full list of valid names is in  tools/country-names.txt
                     (e.g. "Italy", "Japan", "United States of America").
                     Any country you add here is automatically highlighted +
                     becomes clickable on the map.
   • year          — any short label shown under the title ("2023", "Summer 2022"…).
   • photos        — an array of image paths. Put your images in
                     site/images/travels/  and reference them like
                     "images/travels/japan-1.jpg".
                     0 photos → no image; 1 → single image; 2+ → arrows + counter.
   • text          — your write-up (plain text; basic HTML is allowed).
   ============================================================================ */
(function () {
  // demo-only helper that draws coloured placeholder slides — delete once you use real photos
  const ph = (label, bg) => "data:image/svg+xml," + encodeURIComponent(
    `<svg xmlns='http://www.w3.org/2000/svg' width='640' height='430'><rect width='640' height='430' fill='${bg}'/>` +
    `<text x='320' y='228' font-family='Georgia' font-size='42' fill='#ffffff' text-anchor='middle'>${label}</text></svg>`);

  window.TRIPS = {

    "Italy": {
      year: "Home",
      photos: ["images/photo.jpeg"],
      text: "Where it all starts. Rome, the coast, and endless espresso. Replace this with a real note about home."
    },

    "Japan": {
      year: "2023",
      photos: [ph("Tokyo", "#2f8fd8"), ph("Kyoto", "#12659f"), ph("Osaka", "#4aa5e6")],
      text: "Tokyo neon and Kyoto temples. This entry has three demo photos — use the arrows to scroll them."
    },

    "Netherlands": {
      year: "2024",
      photos: ["images/avatar.png", "images/photo.jpeg"],
      text: "Amsterdam canals and a conference or two. Placeholder text — the food, the bikes, the rain."
    },

    "United States of America": {
      year: "2022",
      photos: ["images/avatar.png"],
      text: "From the Bay Area to the East Coast. Placeholder text — replace with a story from the trip."
    },

    "France": {
      year: "2023",
      photos: ["images/photo.jpeg"],
      text: "Paris and the south. Dummy note about museums, markets, and a long walk along the Seine."
    },

    "Iceland": {
      year: "2021",
      photos: ["images/avatar.png"],
      text: "Waterfalls, black-sand beaches, and the northern lights. Placeholder travel text goes here."
    }

  };
})();
