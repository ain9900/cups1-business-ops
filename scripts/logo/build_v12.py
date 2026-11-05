"""Cup1 logo v1.2 – 'Cup' wordmark + teal takeaway cup with the '1' knocked out. Paths only, no transforms."""
import os, json
from round2 import text_path, one_centered, f2

TEAL, INK, PAPER = "#1F4E5A", "#1C2B2E", "#F7F3EC"
D = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(D, "v12")
for sub in ("svg", "png", "favicon"):
    os.makedirs(os.path.join(OUT, sub), exist_ok=True)


def cup_path(x, base, cap, heavy=False):
    """Cup glyph as one evenodd path (lid + body with '1' knocked out). Returns d, right edge, top."""
    H = cap * 1.04
    top_w, bot_w = cap * 0.80, cap * 0.60
    if heavy:                      # favicon: chunkier lid, bigger 1
        top_w, bot_w = cap * 0.86, cap * 0.66
    cx = x + top_w / 2 + cap * 0.04
    yt, yb = base - H, base
    lid_h = cap * (0.17 if heavy else 0.14)
    lid_gap = cap * (0.06 if heavy else 0.05)
    lid_w = top_w + cap * 0.10
    r, lr = cap * 0.035, lid_h / 2
    ly = yt - lid_gap - lid_h
    L, R = cx - lid_w / 2, cx + lid_w / 2
    lid = (f"M{f2(L + lr)} {f2(ly)}H{f2(R - lr)}A{f2(lr)} {f2(lr)} 0 0 1 {f2(R - lr)} {f2(ly + lid_h)}"
           f"H{f2(L + lr)}A{f2(lr)} {f2(lr)} 0 0 1 {f2(L + lr)} {f2(ly)}Z")
    body = (f"M{f2(cx - top_w/2)} {f2(yt)}H{f2(cx + top_w/2)}L{f2(cx + bot_w/2)} {f2(yb - r)}"
            f"Q{f2(cx + bot_w/2)} {f2(yb)} {f2(cx + bot_w/2 - r)} {f2(yb)}H{f2(cx - bot_w/2 + r)}"
            f"Q{f2(cx - bot_w/2)} {f2(yb)} {f2(cx - bot_w/2)} {f2(yb - r)}Z")
    one = one_centered(cap * (0.92 if heavy else 0.86), cx, yt + H * 0.55)
    return lid + body + one, cx + lid_w / 2, ly


def horizontal(word_fill, cup_fill, size=100):
    base = size * 1.05
    cap = size * 0.7275
    d, endx, b = text_path("Cup", size, 0, base, tracking=-0.03 * size)
    cd, right, top = cup_path(endx + size * 0.02, base, cap)
    x0, y0 = b[0] - 2, min(top, b[1]) - 2
    W, H = right + 2 - x0, b[3] + 2 - y0
    body = f'<path d="{d}" fill="{word_fill}"/><path d="{cd}" fill="{cup_fill}" fill-rule="evenodd"/>'
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{f2(x0)} {f2(y0)} {f2(W)} {f2(H)}" width="{f2(W)}" height="{f2(H)}">{body}</svg>\n'


def icon_svg(cup_fill, bg=None, heavy=False, pad=None, square=False):
    cap = 66 if not heavy else 66
    # measure at origin then centre in 100x100
    d0, right0, top0 = cup_path(0, 0, cap, heavy)
    left0 = -(cap * 0.05)  # lid overhang left of x=0
    w, h = right0 - left0, -top0
    s = 1.0
    x = 50 - (left0 + right0) / 2
    base = 50 + h / 2
    d, _, _ = cup_path(x, base, cap, heavy)
    rect = ""
    if bg:
        rect = f'<rect width="100" height="100" fill="{bg}"/>' if square else f'<rect width="100" height="100" rx="22" fill="{bg}"/>'
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">{rect}<path d="{d}" fill="{cup_fill}" fill-rule="evenodd"/></svg>\n'


files = {
    "cup1-logo-horizontal-color.svg": horizontal(INK, TEAL),
    "cup1-logo-horizontal-reversed.svg": horizontal(PAPER, PAPER),
    "cup1-logo-horizontal-black.svg": horizontal("#000000", "#000000"),
    "cup1-logo-horizontal-white.svg": horizontal("#FFFFFF", "#FFFFFF"),
    "cup1-icon-color.svg": icon_svg(TEAL),
    "cup1-icon-reversed.svg": icon_svg(PAPER),
    "cup1-icon-black.svg": icon_svg("#000000"),
    "cup1-icon-tile.svg": icon_svg(PAPER, TEAL),
}
for n, c in files.items():
    open(os.path.join(OUT, "svg", n), "w").write(c)

open(os.path.join(OUT, "favicon", "favicon.svg"), "w").write(icon_svg(PAPER, TEAL, heavy=True))
open(os.path.join(OUT, "fav_tile_heavy.svg"), "w").write(icon_svg(PAPER, TEAL, heavy=True))
open(os.path.join(OUT, "apple_square.svg"), "w").write(icon_svg(PAPER, TEAL, square=True))
# maskable: artwork inside central 80% safe zone -> scale via smaller cap
mask = icon_svg(PAPER, TEAL, square=True).replace('viewBox="0 0 100 100"', 'viewBox="-14 -14 128 128"').replace('<rect width="100" height="100" fill="#1F4E5A"/>', '<rect x="-14" y="-14" width="128" height="128" fill="#1F4E5A"/>')
open(os.path.join(OUT, "maskable.svg"), "w").write(mask)
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
print("ok")
