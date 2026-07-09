/* ============================================================================
   TRAVELS DATA  —  edit THIS file to add or change your trips.
   (No code here — just data. Reload travels.html to see changes.)

   Each entry is:   "Country Name": { year, photos, text }

   • Country Name  — must EXACTLY match the map's country name.
                     Full list of valid names:  tools/country-names.txt
                     Any country listed here is highlighted + clickable on the map.
   • year          — short label under the title ("2023", "Summer 2022", "Home"…). Optional.
   • photos        — array of image paths. Put images in  site/images/travels/  and
                     reference them like "images/travels/japan-1.jpg".
                     0 → no image · 1 → single image · 2+ → arrows + counter (carousel).
   • text          — your write-up (plain text; basic HTML allowed).

   NOTE: most countries below are placeholders — add your own photos + text.
         Italy (single photo) and Japan (3-photo carousel) are kept as examples.
   ============================================================================ */
(function () {
  // demo-only helper that draws coloured placeholder slides — delete once you use real photos
  const ph = (label, bg) => "data:image/svg+xml," + encodeURIComponent(
    `<svg xmlns='http://www.w3.org/2000/svg' width='640' height='430'><rect width='640' height='430' fill='${bg}'/>` +
    `<text x='320' y='228' font-family='Georgia' font-size='42' fill='#ffffff' text-anchor='middle'>${label}</text></svg>`);

  const soon = "Notes and photos coming soon.";

  window.TRIPS = {

    // --- examples (replace with real content) ---
    "Italy": {
      year: "Home",
      photos: ["images/photo.jpeg"],
      text: "Where it all starts. Example single-photo entry — replace with a real note."
    },
    "Japan": {
      year: "2023",
      photos: [ph("Tokyo", "#2f8fd8"), ph("Kyoto", "#12659f"), ph("Osaka", "#4aa5e6")],
      text: "Example multi-photo entry — use the arrows to scroll. Replace the placeholder slides with real photos."
    },

    // --- your countries (add photos + text later) ---
    "Argentina":                { year: "", photos: [], text: soon },
    "Hungary":                  { year: "", photos: [], text: soon },
    "United Kingdom":           { year: "", photos: [], text: soon },
    "Spain":                    { year: "", photos: [], text: soon },
    "France":                   { year: "", photos: [], text: soon },
    "Albania":                  { year: "", photos: [], text: soon },
    "Cyprus":                   { year: "", photos: [], text: soon },
    "Namibia":                  { year: "", photos: [], text: soon },
    "United States of America": { year: "", photos: [], text: soon },
    "Egypt":                    { year: "", photos: [], text: soon },
    "Turkey":                   { year: "", photos: [], text: soon },
    "Vietnam":                  { year: "", photos: [], text: soon },
    "Thailand":                 { year: "", photos: [], text: soon },
    "Switzerland":              { year: "", photos: [], text: soon },
    "Finland":                  { year: "", photos: [], text: soon },
    "Germany":                  { year: "", photos: [], text: soon },
    "Portugal":                 { year: "", photos: [], text: soon },
    "China":                    { year: "", photos: [], text: soon }

  };
})();
