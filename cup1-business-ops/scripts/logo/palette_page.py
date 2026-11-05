import json, os
D = os.path.dirname(os.path.abspath(__file__))
data = json.load(open(os.path.join(D, "palette_data.json")))

FONTS = [
    dict(id="f1", font="Fredoka", w=700, name="F1 · Fredoka", feel="Rounded, friendly",
         why="Soft round strokes echo cup rims and lids. Feels at home with bubble tea, desserts and family cafés.",
         watch="Less “serious supplier” for distributor and procurement buyers."),
    dict(id="f2", font="Nunito", w=900, name="F2 · Nunito Black", feel="Rounded but tidy",
         why="Rounded ends keep it warm, while the shapes stay plain and businesslike. A safe middle ground.",
         watch="Widely used, so a little less distinctive."),
    dict(id="f3", font="Bricolage Grotesque", w=800, name="F3 · Bricolage Grotesque", feel="Crafted, modern",
         why="Ink-trap details look like printed packaging. Modern and a bit hand-made, good for specialty coffee.",
         watch="Quirky details soften below 24px; check the navbar."),
    dict(id="f4", font="Fraunces", w=900, name="F4 · Fraunces", feel="Café-menu serif",
         why="A soft, chunky serif with the warmth of coffee-shop menus and bakery labels.",
         watch="Further from the “compliance and documents” tone; serif needs care at 16px."),
    dict(id="f5", font="Archivo Black", w=400, name="F5 · Archivo Black", feel="Industrial, stamped",
         why="Heavy and compact, like a shipping-carton stamp. Signals bulk supply and reliability to B2B buyers.",
         watch="Least warm option; leans warehouse more than café."),
    dict(id="f6", font="Baloo 2", w=800, name="F6 · Baloo 2", feel="Bubbly, playful",
         why="Plump letters with a hand-lettered feel; matches takeaway, snacks and bubble-tea packaging.",
         watch="Most playful; may read as consumer brand rather than supplier."),
]
data["fonts"] = FONTS
gf = "&".join(f"family={f['font'].replace(' ', '+')}:wght@{f['w']}" for f in FONTS if f["font"] != "Archivo Black")
gf += "&family=Archivo+Black&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@500"

html = r"""<title>Cup1 Logo Palette</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?__GF__&display=swap">
<style>
/* Layout: a swatch-book of logo cards, each tested on the three places Cup1 actually uses it: navbar, kraft sample-kit label, favicon. */
:root{
  --bg:#EFEAE1; --panel:#FBF9F5; --fg:#1C2B2E; --muted:#5D6866; --line:#D9D1C3; --accent:#1F4E5A; --accent-ink:#F7F3EC;
  --star:#C77A1E; --chip:#E6DFD2;
  /* preview surfaces stay fixed in both themes: they show the logo on real materials */
  --s-white:#FFFFFF; --s-kraft:#C99F6E; --s-kraft-ink:#1C2B2E; --s-browser:#E8EAED; --s-teal:#1F4E5A; --s-ink:#1C2B2E;
  --display:"Bricolage Grotesque", "Arial Black", system-ui, sans-serif;
  --body:"IBM Plex Sans", system-ui, -apple-system, "Segoe UI", sans-serif;
  --mono:"IBM Plex Mono", ui-monospace, Menlo, Consolas, monospace;
}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){
  --bg:#141B1C; --panel:#1D2627; --fg:#ECE7DE; --muted:#A3ADAA; --line:#334042; --accent:#7DB7C4; --accent-ink:#0F1718; --star:#F0A24A; --chip:#2A3536; color-scheme:dark}}
:root[data-theme="dark"]{--bg:#141B1C; --panel:#1D2627; --fg:#ECE7DE; --muted:#A3ADAA; --line:#334042; --accent:#7DB7C4; --accent-ink:#0F1718; --star:#F0A24A; --chip:#2A3536; color-scheme:dark}
*{box-sizing:border-box}
body{background:var(--bg); color:var(--fg); font:15px/1.5 var(--body); padding-left:max(16px, env(safe-area-inset-left,0px)); padding-right:max(16px, env(safe-area-inset-right,0px)); padding-block:28px 64px}
.wrap{max-width:1240px; margin:0 auto; display:flex; flex-direction:column; gap:28px}
header{display:grid; gap:10px; max-width:760px}
.eyebrow{font:500 12px/1 var(--mono); letter-spacing:.08em; text-transform:uppercase; color:var(--muted)}
h1{font:800 clamp(30px,5vw,46px)/1.05 var(--display); margin:0; text-wrap:balance; letter-spacing:-.01em}
h2{font:800 24px/1.15 var(--display); margin:0; text-wrap:balance}
.lede{color:var(--muted); margin:0; max-width:65ch}
.bar{position:sticky; top:env(safe-area-inset-top,0px); z-index:5; background:var(--bg); padding-block:10px; display:flex; flex-wrap:wrap; gap:8px; align-items:center; border-bottom:1px solid var(--line)}
body::before{content:""; position:fixed; inset:0 0 auto; height:env(safe-area-inset-top,0px); z-index:10; background:var(--bg)}
.tab{font:500 13px var(--body); border:1px solid var(--line); background:var(--panel); color:var(--fg); border-radius:999px; padding:7px 14px; cursor:pointer}
.tab[aria-pressed="true"]{background:var(--fg); color:var(--bg); border-color:var(--fg)}
.tab .n{font-family:var(--mono); opacity:.7; margin-left:4px}
.spacer{flex:1}
.btn{font:600 13px var(--body); background:var(--accent); color:var(--accent-ink); border:0; border-radius:8px; padding:9px 14px; cursor:pointer}
.btn.ghost{background:transparent; color:var(--fg); border:1px solid var(--line)}
:focus-visible{outline:2px solid var(--star); outline-offset:2px}
section{display:grid; gap:14px}
.sechead{display:flex; flex-wrap:wrap; gap:6px 16px; align-items:baseline}
.sechead p{margin:0; color:var(--muted); max-width:70ch}
.grid{display:grid; grid-template-columns:repeat(auto-fill,minmax(min(100%,340px),1fr)); gap:16px}
.card{background:var(--panel); border:1px solid var(--line); border-radius:14px; overflow:hidden; display:flex; flex-direction:column; min-width:0}
.card.picked{border-color:var(--star); box-shadow:0 0 0 2px var(--star) inset}
.hero{background:var(--s-white); height:170px; display:flex; align-items:center; justify-content:center; padding:38px 18px 16px; position:relative}
.hero svg{max-height:96px; max-width:88%; width:auto; height:auto}
.hero img{max-height:100%; width:auto; object-fit:contain; border-radius:6px}
.badge{position:absolute; top:10px; left:10px; font:500 11px/1 var(--mono); letter-spacing:.04em; text-transform:uppercase; padding:5px 8px; border-radius:6px; background:#F1ECE3; color:#1C2B2E}
.badge.cur{background:#1F4E5A; color:#F7F3EC}
.badge.rej{background:#F3E1DC; color:#8A2E1C}
.badge.rec{background:#FCEBD3; color:#7A4310}
.tests{display:grid; gap:8px; padding:12px; border-top:1px solid var(--line)}
.nav{background:var(--s-white); border:1px solid #E2E2E2; border-radius:8px; height:48px; display:flex; align-items:center; gap:12px; padding:0 12px; overflow:hidden}
.nav svg{height:30px; width:auto; flex:none}
.nav .links{margin-left:auto; display:flex; gap:10px; font:500 11px var(--body); color:#55605F; white-space:nowrap}
.nav .links b{background:#1F4E5A; color:#fff; padding:5px 8px; border-radius:5px; font-weight:600}
.row2{display:grid; grid-template-columns:1.4fr 1fr; gap:8px}
.kraft{background:var(--s-kraft); border-radius:8px; min-height:96px; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:4px; padding:10px; color:var(--s-kraft-ink)}
.kraft svg{height:40px; width:auto; max-width:90%}
.kraft .kit{font:600 11px var(--body); letter-spacing:.02em}
.favs{background:var(--s-browser); border-radius:8px; padding:8px; display:flex; flex-direction:column; gap:8px; justify-content:center}
.tabmock{background:#fff; border-radius:7px 7px 0 0; display:flex; align-items:center; gap:6px; padding:6px 8px; font:12px var(--body); color:#333}
.tabmock svg,.tabmock .fi{width:16px; height:16px; flex:none}
.sizes{display:flex; align-items:flex-end; gap:8px}
.sizes figure{margin:0; display:grid; justify-items:center; gap:2px; font:500 9px var(--mono); color:#5f6368}
.lab{font:500 10px/1 var(--mono); letter-spacing:.06em; text-transform:uppercase; color:var(--muted)}
.info{padding:12px 14px 14px; display:grid; gap:8px; border-top:1px solid var(--line); flex:1; align-content:start}
.title{display:flex; align-items:flex-start; gap:10px}
.title h3{font:700 16px/1.25 var(--body); margin:0; flex:1; min-width:0}
.title .tag{font:500 11px var(--mono); color:var(--muted)}
.pick{flex:none; display:inline-flex; align-items:center; gap:6px; font:600 12px var(--body); border:1px solid var(--line); background:transparent; color:var(--fg); border-radius:999px; padding:6px 10px; cursor:pointer}
.pick svg{width:14px; height:14px}
.pick[aria-pressed="true"]{background:var(--star); border-color:var(--star); color:#fff}
dl{margin:0; display:grid; grid-template-columns:auto 1fr; gap:4px 10px; font-size:13.5px}
dt{font:500 10px/1.9 var(--mono); text-transform:uppercase; letter-spacing:.06em; color:var(--muted)}
dd{margin:0; min-width:0}
/* live-font wordmark */
.wm{display:inline-flex; align-items:baseline; white-space:nowrap; line-height:1; color:#1C2B2E}
.wm .cup{display:inline-block; height:.9em; height:1.24cap; width:auto; margin-left:.04em; color:#1F4E5A; align-self:baseline; vertical-align:baseline; transform:translateY(0)}
.hero .wm{font-size:78px}
.nav .wm{font-size:26px}
.kraft .wm{font-size:40px}
.kraft .wm .cup{color:#1F4E5A}
.samplecard .hero{height:auto; min-height:150px; padding:0; background:#fff}
.samplecard .hero img{display:block; width:100%; height:auto; border-radius:0; max-height:none}
.note{font-size:13.5px; background:var(--chip); border-radius:8px; padding:8px 10px}
.rec{background:var(--panel); border:1px solid var(--line); border-radius:14px; padding:16px 18px; display:grid; gap:8px; max-width:900px}
.rec ol{margin:0; padding-left:20px; display:grid; gap:4px}
.out{display:grid; gap:8px}
textarea{width:100%; min-height:120px; font:13px/1.5 var(--mono); background:var(--panel); color:var(--fg); border:1px solid var(--line); border-radius:8px; padding:10px}
.toast{font:500 12px var(--mono); color:var(--muted)}
footer{color:var(--muted); font-size:13px; max-width:80ch}
@media (max-width:480px){ .row2{grid-template-columns:1fr} .hero .wm{font-size:60px} .nav .links span{display:none} }
@media (prefers-reduced-motion:no-preference){ .card{transition:box-shadow .15s, border-color .15s} }
</style>

<div class="wrap">
  <header>
    <div class="eyebrow">Cup1 · Phase 3 Branding · Logo review · 5 Nov 2026</div>
    <h1>Every Cup1 logo direction, side by side</h1>
    <p class="lede">All our concepts, six font options for the current logo, five new suggestions based on your samples, and your samples themselves. Each logo is tested where it will really live: a 30px website navbar, a kraft Sample Kit label and a 16px browser favicon. Star the ones you like, then copy your shortlist and send it back.</p>
  </header>

  <div class="bar" role="toolbar" aria-label="Filter logos">
    <button class="tab" data-f="all" id="tab-all">All</button>
    <button class="tab" data-f="fonts" id="tab-fonts">Font options</button>
    <button class="tab" data-f="new" id="tab-new">New suggestions</button>
    <button class="tab" data-f="ours" id="tab-ours">Our concepts</button>
    <button class="tab" data-f="samples" id="tab-samples">Your samples</button>
    <button class="tab" data-f="picked" id="tab-picked">Shortlist</button>
    <span class="spacer"></span>
    <button class="btn" id="copy">Copy my shortlist</button>
  </div>

  <div class="rec">
    <h2>Our recommendation</h2>
    <ol>
      <li><b>Keep the v1.2 idea</b> (“Cup” + a cup holding the 1). It is the only structure that stays readable in the navbar and as a 16px favicon.</li>
      <li><b>Font:</b> F2 Nunito Black or F3 Bricolage Grotesque if you want the name warmer than today's Inter. Both keep the B2B tone.</li>
      <li><b>Colour:</b> stay teal (v1.2) or move to S1 navy + orange if you prefer your samples' colours. Avoid the green directions unless we can document eco claims.</li>
      <li><b>Taglines and illustrations</b> from your samples work on packaging, banners and decks (S5), never in the navbar or favicon.</li>
    </ol>
  </div>

  <section data-sec="fonts">
    <div class="sechead"><h2>Font options</h2><p>Same cup, same colours as v1.2. Only the “Cup” lettering changes, using faces that suit cafés and food packaging. These are live previews; once you pick one we outline it into final SVG files.</p></div>
    <div class="grid" id="g-fonts"></div>
  </section>
  <section data-sec="new">
    <div class="sechead"><h2>New suggestions</h2><p>Ideas taken from your samples and simplified so they still work at small sizes: no steam, leaves or extra objects inside the mark.</p></div>
    <div class="grid" id="g-new"></div>
  </section>
  <section data-sec="ours">
    <div class="sechead"><h2>Our concepts so far</h2><p>Every direction from Round 1, v1.1, Round 2 and the current v1.2, kept for comparison.</p></div>
    <div class="grid" id="g-ours"></div>
  </section>
  <section data-sec="samples">
    <div class="sechead"><h2>Your samples</h2><p>The references you shared, saved in the project for later design work. Notes say what to keep and what to watch.</p></div>
    <div class="grid" id="g-samples"></div>
  </section>

  <section class="out" id="outsec" data-sec="out">
    <h2>Your shortlist</h2>
    <p class="lede">Your stars are saved in this browser only. Copy this text and paste it into the chat, or send it to your boss.</p>
    <textarea id="out" readonly aria-label="Shortlist text"></textarea>
    <span class="toast" id="toast" aria-live="polite"></span>
  </section>

  <footer>Font previews load from Google Fonts (all free for commercial use under the SIL Open Font License). Samples are shown for internal reference only. ® may only be used once the mark is registered; until then use ™ or nothing.</footer>
</div>

<script>
const DATA = __DATA__;
const STAR = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 2.5l2.9 6.1 6.6.8-4.9 4.5 1.3 6.6L12 17.3l-5.9 3.2 1.3-6.6L2.5 9.4l6.6-.8z"/></svg>';
let picks = {};
try { picks = JSON.parse(localStorage.getItem("cup1-picks") || "{}") || {}; } catch (e) { picks = {}; }
const save = () => { try { localStorage.setItem("cup1-picks", JSON.stringify(picks)); } catch (e) {} };
const esc = s => String(s).replace(/[&<>"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const sized = (svg, cls="") => svg.replace("<svg ", `<svg ${cls ? `class="${cls}" ` : ""}aria-hidden="true" focusable="false" `);
const badge = s => {
  const c = /Current/.test(s) ? "cur" : /Rejected|Superseded/.test(s) ? "rej" : /Suggested|Option|Font/.test(s) ? "rec" : "";
  return `<span class="badge ${c}">${esc(s)}</span>`;
};
const navLinks = '<span class="links"><span>Products</span><span>Samples</span><b>Get a quote</b></span>';
function favRow(icon) {
  if (!icon) return '<div class="favs"><span class="lab">No icon</span><span style="font-size:12px;color:#5f6368">This wordmark has no stand-alone favicon.</span></div>';
  return `<div class="favs"><div class="tabmock">${sized(icon)}<span>Cup1 · Custom cups</span></div>
    <div class="sizes">${[16,32,48].map(s => `<figure>${sized(icon).replace("<svg ", `<svg width="${s}" height="${s}" `)}<figcaption>${s}</figcaption></figure>`).join("")}</div></div>`;
}
function pickBtn(id) {
  return `<button class="pick" data-id="${id}" id="pick-${id}" aria-pressed="${picks[id] ? "true" : "false"}">${STAR}<span>${picks[id] ? "Shortlisted" : "Shortlist"}</span></button>`;
}
function info(id, name, tag, rows) {
  return `<div class="info"><div class="title"><h3>${esc(name)}<br><span class="tag">${esc(tag)}</span></h3>${pickBtn(id)}</div>
    <dl>${rows.map(([k,v]) => `<dt>${k}</dt><dd>${esc(v)}</dd>`).join("")}</dl></div>`;
}
function wm(f) { return `<span class="wm" style="font-family:'${f.font}', var(--display); font-weight:${f.w}"><span>Cup</span>${sized(DATA.cupmark, "cup")}</span>`; }
const favIcon = DATA.variants.find(v => v.id === "v12").icon;

const g = id => document.getElementById(id);
g("g-fonts").innerHTML = DATA.fonts.map(f => `<article class="card" data-id="${f.id}">
  <div class="hero">${badge("Font option")}${wm(f)}</div>
  <div class="tests"><span class="lab">Navbar · 30px</span><div class="nav">${wm(f)}${navLinks}</div>
    <div class="row2"><div class="kraft">${wm(f)}<span class="kit" style="font-family:'${f.font}', var(--body)">Sample Kit</span></div>${favRow(favIcon)}</div></div>
  ${info(f.id, f.name, f.feel, [["Why", f.why], ["Watch", f.watch]])}</article>`).join("");

function variantCard(v) {
  return `<article class="card" data-id="${v.id}">
  <div class="hero">${badge(v.status)}${sized(v.logo)}</div>
  <div class="tests"><span class="lab">Navbar · 30px</span><div class="nav">${sized(v.logo)}${navLinks}</div>
    <div class="row2"><div class="kraft">${sized(v.logo)}<span class="kit">Sample Kit</span></div>${favRow(v.icon)}</div></div>
  ${info(v.id, v.name, v.round, [["Good", v.pros], ["Watch", v.cons]])}</article>`;
}
g("g-new").innerHTML = DATA.variants.filter(v => v.group === "new").map(variantCard).join("");
g("g-ours").innerHTML = DATA.variants.filter(v => v.group === "ours").reverse().map(variantCard).join("");
g("g-samples").innerHTML = DATA.samples.map(s => `<article class="card samplecard" data-id="${s.id}">
  <div class="hero"><img src="${s.img}" alt="${esc(s.name)}" loading="lazy"></div>
  ${info(s.id, s.name, "Reference · " + s.file, [["What", s.desc]])}
  <div style="padding:0 14px 14px"><div class="note"><b>Our note:</b> ${esc(s.note)}</div></div></article>`).join("");

const NAMES = {};
DATA.fonts.forEach(f => NAMES[f.id] = f.name + " (font option, " + f.feel.toLowerCase() + ")");
DATA.variants.forEach(v => NAMES[v.id] = v.name + " (" + v.round + ")");
DATA.samples.forEach(s => NAMES[s.id] = s.name + " (your sample)");
const ORDER = [...DATA.fonts.map(f=>f.id), ...DATA.variants.map(v=>v.id), ...DATA.samples.map(s=>s.id)];

function refresh() {
  document.querySelectorAll(".card").forEach(c => c.classList.toggle("picked", !!picks[c.dataset.id]));
  const ids = ORDER.filter(id => picks[id]);
  g("out").value = ids.length ? "Cup1 logo shortlist (" + new Date().toLocaleDateString() + "):\n" + ids.map((id, i) => `${i+1}. ${NAMES[id]}`).join("\n")
    : "No logos shortlisted yet. Tap “Shortlist” on the cards you like.";
  g("tab-picked").innerHTML = `Shortlist <span class="n">${ids.length}</span>`;
  applyFilter();
}
document.addEventListener("click", e => {
  const b = e.target.closest(".pick");
  if (b) { const id = b.dataset.id; picks[id] = !picks[id]; if (!picks[id]) delete picks[id]; save();
    document.querySelectorAll(`.pick[data-id="${id}"]`).forEach(x => { x.setAttribute("aria-pressed", picks[id] ? "true" : "false"); x.querySelector("span").textContent = picks[id] ? "Shortlisted" : "Shortlist"; });
    refresh(); }
  const t = e.target.closest(".tab");
  if (t) { filter = t.dataset.f; try { localStorage.setItem("cup1-filter", filter); } catch (e) {} applyFilter(); }
});
let filter = "all";
try { filter = localStorage.getItem("cup1-filter") || "all"; } catch (e) {}
function applyFilter() {
  document.querySelectorAll(".tab").forEach(t => t.setAttribute("aria-pressed", t.dataset.f === filter ? "true" : "false"));
  document.querySelectorAll("section[data-sec]").forEach(s => {
    const sec = s.dataset.sec;
    s.hidden = !(filter === "all" || filter === "picked" || sec === filter || sec === "out");
    if (filter === "picked" && sec !== "out") {
      const any = [...s.querySelectorAll(".card")].some(c => picks[c.dataset.id]);
      s.hidden = !any;
    }
  });
  document.querySelectorAll(".card").forEach(c => { c.hidden = filter === "picked" && !picks[c.dataset.id]; });
}
g("copy").addEventListener("click", async () => {
  const ta = g("out");
  try { await navigator.clipboard.writeText(ta.value); g("toast").textContent = "Copied. Paste it into the chat."; }
  catch (e) { ta.focus(); ta.select(); g("toast").textContent = "Copy was blocked here. The text is selected; press Ctrl+C."; }
  ta.scrollIntoView({behavior: "smooth", block: "center"});
});
refresh();
</script>
"""
html = html.replace("__GF__", gf).replace("__DATA__", json.dumps(data, ensure_ascii=False).replace("</", "<\\/"))
open(os.path.join(D, "Cup1_Logo_Palette.html"), "w").write(html)
print(len(html) // 1024, "KB")
