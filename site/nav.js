// Mobile hamburger menu. On small screens the nav links are hidden behind a ☰
// button (styled in custom.css); on desktop this button is display:none and the
// nav is unchanged. Loaded on every page via the SEO injector (tools/seo.py).
(function () {
  var nav = document.querySelector("header > nav.group");
  if (!nav || nav.querySelector(".navtoggle")) return;

  var btn = document.createElement("button");
  btn.className = "navtoggle";
  btn.type = "button";
  btn.setAttribute("aria-label", "Menu");
  btn.setAttribute("aria-expanded", "false");
  btn.innerHTML = "<span></span><span></span><span></span>";
  nav.insertBefore(btn, nav.firstChild);

  function setOpen(open) {
    nav.classList.toggle("open", open);
    btn.setAttribute("aria-expanded", open ? "true" : "false");
  }
  btn.addEventListener("click", function () { setOpen(!nav.classList.contains("open")); });
  // tapping a link (or anywhere outside) closes the menu
  nav.addEventListener("click", function (e) { if (e.target.tagName === "A") setOpen(false); });
  document.addEventListener("click", function (e) { if (!nav.contains(e.target)) setOpen(false); });
})();
