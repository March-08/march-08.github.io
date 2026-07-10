"use strict";
const $  = (s, el = document) => el.querySelector(s);
const $$ = (s, el = document) => [...el.querySelectorAll(s)];
const api  = (p, o) => fetch(p, o).then(r => r.json());
const post = (p, body) => api(p, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });
const esc  = s => (s || "").replace(/&/g, "&amp;").replace(/</g, "&lt;");
const slugify = s => (s || "").toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "") || "untitled";
const today = () => new Date().toISOString().slice(0, 10);
const readURL = f => new Promise(res => { const r = new FileReader(); r.onload = () => res(r.result); r.readAsDataURL(f); });
function toast(msg, err) {
  const t = $("#toast"); t.textContent = msg; t.className = "toast" + (err ? " err" : ""); t.hidden = false;
  clearTimeout(t._h); t._h = setTimeout(() => (t.hidden = true), 2800);
}

/* ---------------- tabs ---------------- */
$$(".tab").forEach(b => b.onclick = () => {
  $$(".tab").forEach(x => x.classList.toggle("active", x === b));
  $$(".view").forEach(v => v.classList.toggle("active", v.id === b.dataset.tab));
  if (b.dataset.tab === "travels") loadCountries();
});

/* ================= ARTICLES ================= */
const aTitle = $("#aTitle"), aDate = $("#aDate"), aSubtitle = $("#aSubtitle"),
      aBody = $("#aBody"), aSlug = $("#aSlug"), preview = $("#preview");
let curSlug = null;

const curArticleSlug = () => curSlug || slugify(aTitle.value);
const updateSlug = () => (aSlug.textContent = curArticleSlug() + ".html");

async function loadArticleList() {
  const items = await api("/api/articles");
  const list = $("#articleList"); list.innerHTML = "";
  if (!items.length) list.innerHTML = '<p class="muted" style="padding:.4rem">No articles yet. Click “New article”.</p>';
  items.forEach(a => {
    const el = document.createElement("div");
    el.className = "list-item" + (a.slug === curSlug ? " active" : "");
    el.innerHTML = `<span class="t">${esc(a.title)}</span><span class="d">${a.date || ""}</span>`;
    el.onclick = () => openArticle(a.slug);
    list.appendChild(el);
  });
}
function newArticle() {
  curSlug = null; aTitle.value = ""; aSubtitle.value = ""; aBody.value = ""; aDate.value = today();
  updateSlug(); loadArticleList(); doPreview(); aTitle.focus();
}
async function openArticle(slug) {
  const a = await api("/api/article?slug=" + encodeURIComponent(slug));
  if (a.error) return toast("Could not load article", true);
  curSlug = a.slug; aTitle.value = a.title; aDate.value = a.date || today();
  aSubtitle.value = a.subtitle || ""; aBody.value = a.markdown || "";
  updateSlug(); loadArticleList(); doPreview();
}

/* live preview (debounced) */
let pvTimer;
function schedulePreview() { updateSlug(); clearTimeout(pvTimer); pvTimer = setTimeout(doPreview, 450); }
async function doPreview() {
  const res = await post("/api/preview", {
    slug: curArticleSlug(), title: aTitle.value, date: aDate.value,
    subtitle: aSubtitle.value, markdown: aBody.value });
  preview.srcdoc = res.html || "";
}
[aTitle, aSubtitle, aBody].forEach(el => el.addEventListener("input", schedulePreview));
aDate.addEventListener("change", schedulePreview);

/* toolbar */
function surround(before, after) {
  const t = aBody, s = t.selectionStart, e = t.selectionEnd, sel = t.value.slice(s, e);
  t.setRangeText(before + sel + after, s, e, "end");
  if (!sel) t.selectionStart = t.selectionEnd = s + before.length;
  t.focus(); schedulePreview();
}
function insertBlock(text) {
  const t = aBody, s = t.selectionStart, pre = t.value.slice(0, s);
  const lead = (pre === "" || pre.endsWith("\n")) ? "" : "\n";
  t.setRangeText(lead + text + "\n", s, s, "end"); t.focus(); schedulePreview();
}
async function pickArticleImage() {
  if (!aTitle.value.trim()) toast("Tip: set a title first so images group under this article");
  $("#fileArticle").click();
}
$("#fileArticle").onchange = async e => {
  const f = e.target.files[0]; e.target.value = ""; if (!f) return;
  const res = await post("/api/upload", { slug: curArticleSlug(), filename: f.name, data: await readURL(f) });
  if (res.ok) { insertBlock(`![](${res.path})`); toast("Image added"); } else toast("Upload failed", true);
};
const CMDS = {
  bold: () => surround("**", "**"),
  italic: () => surround("*", "*"),
  h2: () => insertBlock("## Heading"),
  h3: () => insertBlock("### Subheading"),
  link: () => { const u = prompt("Link URL:", "https://"); if (!u) return;
    const t = aBody, s = t.selectionStart, e = t.selectionEnd, sel = t.value.slice(s, e) || "link text";
    t.setRangeText(`[${sel}](${u})`, s, e, "end"); t.focus(); schedulePreview(); },
  sidenote: () => insertBlock("(your side note — shows in the margin)"),
  image: () => pickArticleImage(),
  video: () => { const u = prompt("YouTube URL:", "https://youtu.be/"); if (u) insertBlock(`<video src="${u}">caption</video>`); },
  embed: () => { const u = prompt("URL to embed (any site, or a Google Slides link):", "https://"); if (u) insertBlock(`<embed src="${u}">caption</embed>`); },
  quote: () => insertBlock("> A memorable quote"),
  code: () => insertBlock("```python\n# your code\n```"),
  mathi: () => surround("$", "$"),
  mathb: () => insertBlock("$$\n\\int_0^1 x^2\\,dx\n$$"),
  callout: () => insertBlock('<callout icon="💡" color="blue_bg">Something worth highlighting.</callout>'),
  toc: () => insertBlock("<table_of_contents>"),
};
$("#toolbar").addEventListener("click", e => {
  const b = e.target.closest("button"); if (b && CMDS[b.dataset.cmd]) CMDS[b.dataset.cmd]();
});

$("#newArticle").onclick = newArticle;
$("#saveArticle").onclick = async () => {
  if (!aTitle.value.trim()) return toast("Please add a title first", true);
  $("#aStatus").textContent = "Saving…";
  const res = await post("/api/save-article", {
    slug: curArticleSlug(), title: aTitle.value, date: aDate.value || today(),
    subtitle: aSubtitle.value, markdown: aBody.value });
  if (res.ok) { curSlug = res.slug; $("#aStatus").textContent = "Saved ✓"; toast("Saved to your site");
    updateSlug(); loadArticleList(); }
  else { $("#aStatus").textContent = ""; toast(res.error || "Save failed", true); }
};

/* ================= TRAVELS ================= */
let travels = {}, allCountries = [], curCountry = null;

async function loadCountries() {
  travels = await api("/api/travels");
  if (!allCountries.length) allCountries = await api("/api/countries");
  renderCountryList();
}
function isEmpty(v) { return (!v.photos || !v.photos.length) && (!v.text || /coming soon/i.test(v.text)); }
function renderCountryList() {
  const list = $("#countryList"); list.innerHTML = "";
  Object.keys(travels).sort().forEach(name => {
    const el = document.createElement("div");
    el.className = "list-item" + (name === curCountry ? " active" : "");
    el.innerHTML = `<span class="t">${esc(name)} ${isEmpty(travels[name]) ? "" : '<span class="dot">●</span>'}</span>`;
    el.onclick = () => openCountry(name);
    list.appendChild(el);
  });
}
function openCountry(name) {
  curCountry = name; $("#travelEmpty").hidden = true; $("#travelForm").hidden = false;
  const v = travels[name] || {}; $("#tName").textContent = name;
  $("#tYear").value = v.year || ""; $("#tText").value = /coming soon/i.test(v.text || "") ? "" : (v.text || "");
  renderPhotos(); renderCountryList();
}
function renderPhotos() {
  const box = $("#tPhotos"); box.innerHTML = ""; const arr = travels[curCountry].photos || (travels[curCountry].photos = []);
  arr.forEach((p, i) => {
    const d = document.createElement("div"); d.className = "photo";
    d.innerHTML = `<img src="/site/${p}" alt=""><button class="del" title="Remove">×</button>
      <div class="ctrl"><button data-l title="Move left">◀</button><button data-r title="Move right">▶</button></div>`;
    d.querySelector(".del").onclick = () => { arr.splice(i, 1); renderPhotos(); };
    d.querySelector("[data-l]").onclick = () => { if (i) { [arr[i - 1], arr[i]] = [arr[i], arr[i - 1]]; renderPhotos(); } };
    d.querySelector("[data-r]").onclick = () => { if (i < arr.length - 1) { [arr[i + 1], arr[i]] = [arr[i], arr[i + 1]]; renderPhotos(); } };
    box.appendChild(d);
  });
}
$("#tYear").oninput = () => { if (curCountry) travels[curCountry].year = $("#tYear").value; };
$("#tText").oninput = () => { if (curCountry) travels[curCountry].text = $("#tText").value; };
$("#addPhotos").onclick = () => $("#fileTravel").click();
$("#fileTravel").onchange = async e => {
  const files = [...e.target.files]; e.target.value = ""; if (!files.length || !curCountry) return;
  for (const f of files) {
    const res = await post("/api/upload-travel-image", { filename: `${slugify(curCountry)}-${f.name}`, data: await readURL(f) });
    if (res.ok) travels[curCountry].photos.push(res.path);
  }
  renderPhotos(); toast("Photos added — remember to Save travels");
};
$("#removeCountry").onclick = () => {
  if (!curCountry || !confirm(`Remove ${curCountry} from the map?`)) return;
  delete travels[curCountry]; curCountry = null;
  $("#travelForm").hidden = true; $("#travelEmpty").hidden = false; renderCountryList();
  toast("Removed — click Save travels to apply");
};
$("#saveTravels").onclick = async () => {
  const res = await post("/api/save-travels", { data: travels });
  toast(res.ok ? "Travels saved to your site" : "Save failed", !res.ok);
};
$("#addCountry").onclick = async () => {
  const name = await pickCountry(); if (!name) return;
  if (!allCountries.includes(name)) return toast("That name isn't a country on the map", true);
  if (!(name in travels)) travels[name] = { year: "", photos: [], text: "" };
  openCountry(name);
};
function pickCountry() {
  return new Promise(resolve => {
    const ov = document.createElement("div"); ov.className = "modal";
    const opts = allCountries.filter(c => !(c in travels)).map(c => `<option value="${esc(c)}">`).join("");
    ov.innerHTML = `<div class="modal-box"><h3>Add a country</h3>
      <p class="muted">Pick a country as it appears on the map.</p>
      <input id="cpick" list="cdl" placeholder="Start typing…" autocomplete="off"
             style="width:100%;padding:.6rem;border:1px solid var(--line);border-radius:6px;font:inherit">
      <datalist id="cdl">${opts}</datalist>
      <div class="modal-actions" style="margin-top:1rem">
        <button class="btn btn-ghost" data-x>Cancel</button><button class="btn btn-primary" data-ok>Add</button></div></div>`;
    document.body.appendChild(ov);
    const inp = $("#cpick", ov); setTimeout(() => inp.focus(), 30);
    const done = v => { ov.remove(); resolve(v); };
    $("[data-x]", ov).onclick = () => done(null);
    $("[data-ok]", ov).onclick = () => done(inp.value.trim());
    inp.onkeydown = e => { if (e.key === "Enter") done(inp.value.trim()); if (e.key === "Escape") done(null); };
  });
}

/* ================= PUBLISH ================= */
$("#publishBtn").onclick = async () => {
  const s = await api("/api/status");
  $("#changeList").textContent = (s.changes && s.changes.length) ? s.changes.join("\n") : "No changes since last publish.";
  $("#publishLog").hidden = true; $("#commitMsg").value = "";
  $("#publishModal").hidden = false;
};
$("#cancelPublish").onclick = () => ($("#publishModal").hidden = true);
$("#doPublish").onclick = async () => {
  const btn = $("#doPublish"); btn.disabled = true; btn.textContent = "Publishing…";
  const res = await post("/api/publish", { message: $("#commitMsg").value });
  const log = $("#publishLog"); log.hidden = false; log.textContent = res.log || "";
  btn.disabled = false; btn.textContent = "Commit & push";
  if (res.ok) toast("Published ✓");
  else toast(/nothing/i.test(res.log || "") ? "Nothing to publish" : "Publish failed", true);
};

/* ---------------- init ---------------- */
newArticle();
