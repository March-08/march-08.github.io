// Mobile hamburger menu. On small screens a fixed ☰ button stays on screen while
// you scroll, and opens the links as a dropdown panel; on desktop the button is
// hidden and the nav is unchanged. Loaded on every page via tools/seo.py.
(function () {
  var nav = document.querySelector("header > nav.group");
  if (!nav || nav.querySelector(".navtoggle")) return;

  // wrap the existing links so they can be positioned as a panel independently of
  // the button (`.navlinks` is display:contents on desktop, so layout is unchanged)
  var links = document.createElement("div");
  links.className = "navlinks";
  while (nav.firstChild) links.appendChild(nav.firstChild);
  nav.appendChild(links);

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
  btn.addEventListener("click", function (e) { e.stopPropagation(); setOpen(!nav.classList.contains("open")); });
  links.addEventListener("click", function (e) { if (e.target.tagName === "A") setOpen(false); });
  document.addEventListener("click", function (e) { if (!nav.contains(e.target)) setOpen(false); });
})();
