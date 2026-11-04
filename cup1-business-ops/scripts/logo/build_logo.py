"""Cup1 logo system – Rim Monogram (concept B, refined). Paths only, no <text>."""
import os, json
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen
from glyphs import word, arc_ring

TEAL, INK, PAPER, TEAL_L = "#1F4E5A", "#1C2B2E", "#F7F3EC", "#6FB3C2"
D = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(D, "out")
for sub in ("svg", "png", "favicon"):
    os.makedirs(os.path.join(OUT, sub), exist_ok=True)

f2 = lambda v: ("%.2f" % v).rstrip("0").rstrip(".")


def one_path(size, font, opt=0.0):
    """'1' glyph centred on (50,50) + optical shift, coordinates baked in (no transform)."""
    f = TTFont(font); gs = f.getGlyphSet(); g = f.getBestCmap()[ord("1")]; s = size / f["head"].unitsPerEm
    bp = BoundsPen(gs); gs[g].draw(TransformPen(bp, (s, 0, 0, -s, 0, 0)))
    x0, y0, x1, y1 = bp.bounds
    tx, ty = 50 - (x0 + x1) / 2 + opt, 50 - (y0 + y1) / 2
    pen = SVGPathPen(gs, ntos=f2); gs[g].draw(TransformPen(pen, (s, 0, 0, -s, tx, ty)))
    return pen.getCommands()


def mark(fg, small=False):
    """Rim monogram in a 100x100 box. small=True: heavier version for <=32px."""
    if small:
        ring = arc_ring(50, 50, 48, 31.5, 38, 322)
        d = one_path(50, "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf", 1.4)
    else:
        ring = arc_ring(50, 50, 46, 31, 36, 324)
        d = one_path(50, "/usr/share/fonts/opentype/inter/InterDisplay-ExtraBold.otf", 1.8)
    return f'<path d="{ring}" fill="{fg}"/><path d="{d}" fill="{fg}"/>'


def wordmark(size, fg, x=0, base=0):
    d, w, b = word("Cup1", size, x, base, tracking=-0.025 * size)
    return f'<path d="{d}" fill="{fg}"/>', w, b


def svgdoc(w, h, body, bg=None, vb=None):
    vb = vb or f"0 0 {f2(w)} {f2(h)}"
    rect = f'<rect width="100%" height="100%" fill="{bg}"/>' if bg else ""
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" width="{f2(w)}" height="{f2(h)}">{rect}{body}</svg>\n'


def horizontal(mfg, wfg):
    size = 63
    _, w, b = wordmark(size, wfg, 0, 0)
    gap = 18
    cap = -b[1]
    base = 50 + cap / 2
    x = 100 + gap - b[0]
    wm, _, _ = wordmark(size, wfg, x, base)
    body = mark(mfg) + wm
    return svgdoc(100 + gap + (b[2] - b[0]) + 3, 100, body)


def stacked(mfg, wfg):
    size = 56
    wm, w, b = wordmark(size, wfg)
    W = max(100, b[2] - b[0]) + 8
    cap = -b[1]
    mx = (W - 100) / 2
    base = 100 + 22 + cap
    H = base + b[3] + 2
    wm2, _, _ = wordmark(size, wfg, (W - (b[2]-b[0]))/2 - b[0], base)
    body = f'<g transform="translate({f2(mx)} 0)">{mark(mfg)}</g>{wm2}'
    return svgdoc(W, H, body)


def tile(bg=TEAL, fg=PAPER, small=False, pad=14, radius=22):
    inner = 100 - 2 * pad
    s = inner / 100
    return svgdoc(100, 100, f'<rect width="100" height="100" rx="{radius}" fill="{bg}"/><g transform="translate({pad} {pad}) scale({f2(s)})">{mark(fg, small)}</g>')


files = {
    "cup1-logo-horizontal-color.svg": horizontal(TEAL, INK),
    "cup1-logo-horizontal-reversed.svg": horizontal(PAPER, PAPER),
    "cup1-logo-horizontal-black.svg": horizontal("#000000", "#000000"),
    "cup1-logo-horizontal-white.svg": horizontal("#FFFFFF", "#FFFFFF"),
    "cup1-logo-stacked-color.svg": stacked(TEAL, INK),
    "cup1-logo-stacked-reversed.svg": stacked(PAPER, PAPER),
    "cup1-icon-color.svg": svgdoc(100, 100, mark(TEAL)),
    "cup1-icon-reversed.svg": svgdoc(100, 100, mark(PAPER)),
    "cup1-icon-black.svg": svgdoc(100, 100, mark("#000000")),
    "cup1-icon-tile.svg": tile(),
}
wm, w, b = wordmark(100, INK)
files["cup1-wordmark-ink.svg"] = svgdoc(b[2] - b[0] + 4, -b[1] + b[3] + 4, f'<g transform="translate({f2(2 - b[0])} {f2(2 - b[1])})">{wm}</g>')
for n, c in files.items():
    open(os.path.join(OUT, "svg", n), "w").write(c)

# favicon sources
fav_svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect width="100" height="100" rx="22" fill="{TEAL}"/>'
           f'<g transform="translate(10 10) scale(0.8)">{mark(PAPER, small=True)}</g></svg>\n')
open(os.path.join(OUT, "favicon", "favicon.svg"), "w").write(fav_svg)
open(os.path.join(OUT, "favicon_small_tile.svg"), "w").write(tile(small=True, pad=10, radius=22))
open(os.path.join(OUT, "favicon_full_tile_square.svg"), "w").write(svgdoc(100, 100, f'<rect width="100" height="100" fill="{TEAL}"/><g transform="translate(14 14) scale(0.72)">{mark(PAPER)}</g>'))
open(os.path.join(OUT, "maskable.svg"), "w").write(svgdoc(100, 100, f'<rect width="100" height="100" fill="{TEAL}"/><g transform="translate(25 25) scale(0.5)">{mark(PAPER)}</g>'))
manifest = {"name": "Cup1", "short_name": "Cup1", "icons": [
    {"src": "/icon-192.png", "sizes": "192x192", "type": "image/png"},
    {"src": "/icon-512.png", "sizes": "512x512", "type": "image/png"},
    {"src": "/icon-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}],
    "theme_color": TEAL, "background_color": PAPER, "display": "standalone"}
open(os.path.join(OUT, "favicon", "site.webmanifest"), "w").write(json.dumps(manifest, indent=2) + "\n")
open(os.path.join(OUT, "favicon", "favicon-snippet.html"), "w").write(
    '<link rel="icon" href="/favicon.ico" sizes="any">\n<link rel="icon" href="/favicon.svg" type="image/svg+xml">\n'
    '<link rel="apple-touch-icon" href="/apple-touch-icon.png">\n<link rel="manifest" href="/site.webmanifest">\n'
    f'<meta name="theme-color" content="{TEAL}">\n')
print("ok", len(files))
