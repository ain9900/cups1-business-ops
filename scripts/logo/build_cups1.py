"""Cups1 logo v2.0 – vector rebuild of owner's shortlisted Sample 1 (navy line cup, orange steam, green leaf,
orange swoosh, navy 'Cups' + orange slab '1', tagline). Text is outlined to paths."""
import os, json
from round2 import text_path, f2

D = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(D, "cups1")
for s in ("svg", "png", "favicon"):
    os.makedirs(os.path.join(OUT, s), exist_ok=True)

NAVY, ORANGE, GREEN, WHITE = "#102A4C", "#F28A1B", "#5FA136", "#FFFFFF"
MED = "/usr/share/fonts/opentype/inter/Inter-Medium.otf"
SW = 6.2  # cup stroke


def cup(cx, base, c_line, c_leaf, c_vein, c_steam=None, steam=True, sw=SW):
    """Line cup centred on cx, bottom at base. Returns svg, (left, top, right)."""
    bt, bb = base - 60, base               # body top / bottom
    tw, bw = 64, 48
    rim_y, rim_h, rim_w = base - 72, 11, 76
    cap_y, cap_h, cap_w = base - 82, 10, 60
    r = 4
    body = (f'M{f2(cx - tw/2)} {f2(bt)}L{f2(cx - bw/2)} {f2(bb - r)}Q{f2(cx - bw/2 + .5)} {f2(bb)} {f2(cx - bw/2 + r)} {f2(bb)}'
            f'H{f2(cx + bw/2 - r)}Q{f2(cx + bw/2 - .5)} {f2(bb)} {f2(cx + bw/2)} {f2(bb - r)}L{f2(cx + tw/2)} {f2(bt)}')
    out = [f'<path d="{body}" fill="none" stroke="{c_line}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round"/>',
           f'<rect x="{f2(cx - rim_w/2)}" y="{f2(rim_y)}" width="{rim_w}" height="{rim_h}" rx="4.5" fill="none" stroke="{c_line}" stroke-width="{sw}"/>',
           f'<rect x="{f2(cx - cap_w/2)}" y="{f2(cap_y)}" width="{cap_w}" height="{cap_h}" rx="4" fill="none" stroke="{c_line}" stroke-width="{sw}"/>']
    # leaf (lower-left of the cup body, tip up-right) + vein
    lx, ly = cx - 12, base - 9
    leaf = (f'M{f2(lx)} {f2(ly)}C{f2(lx - 6)} {f2(ly - 24)} {f2(lx + 8)} {f2(ly - 36)} {f2(lx + 27)} {f2(ly - 40)}'
            f'C{f2(lx + 27)} {f2(ly - 20)} {f2(lx + 18)} {f2(ly - 4)} {f2(lx)} {f2(ly)}Z')
    out.append(f'<path d="{leaf}" fill="{c_leaf}"/>')
    out.append(f'<path d="M{f2(lx - 1.5)} {f2(ly + 4)}Q{f2(lx + 4)} {f2(ly - 16)} {f2(lx + 21)} {f2(ly - 30)}" fill="none" stroke="{c_vein}" stroke-width="2.6" stroke-linecap="round"/>')
    top = cap_y - sw / 2
    if steam:
        for dx in (-7, 7):
            x, y = cx + dx, cap_y - 7
            out.append(f'<path d="M{f2(x)} {f2(y)}c-6 -5 -6 -9 0 -14s6 -9 0 -14s-6 -9 0 -14" fill="none" stroke="{c_steam}" stroke-width="4.6" stroke-linecap="round"/>')
        top = cap_y - 7 - 42 - 3
    return "".join(out), (cx - rim_w / 2 - sw / 2, top, cx + rim_w / 2 + sw / 2)


def one(x, base, H, fill):
    s = H / 100
    pts = [(38, -100), (63, -100), (63, -17), (81, -17), (81, 0), (17, 0), (17, -17), (36, -17), (36, -71), (15, -63), (11, -82)]
    d = "M" + "L".join(f"{f2(x + px * s)} {f2(base + py * s)}" for px, py in pts) + "Z"
    return f'<path d="{d}" fill="{fill}"/>', x + 81 * s


def lockup(c_word, c_one, c_line, c_leaf, c_vein, c_steam, c_swoosh, c_tag=None, steam=True, swoosh=True, tagline=True):
    base = 0
    csvg, (cl, ct, cr) = cup(40, base, c_line, c_leaf, c_vein, c_steam, steam)
    wx = cr + 9
    wd, wend, wb = text_path("Cups", 100, wx, base, tracking=-2.2)
    osvg, oend = one(wend - 7, base, 86, c_one)
    parts = [csvg, f'<path d="{wd}" fill="{c_word}"/>', osvg]
    bottom = wb[3]
    left = cl
    if swoosh:
        # thick under the cup's left side, tapering to the right under the 'C'
        sd = ("M6 -22C-14 -6 0 9 44 9C80 9 118 3 150 -3"
              "C116 1 82 4 50 3C16 2 -1 -6 6 -22Z")
        parts.insert(0, f'<path d="{sd}" fill="{c_swoosh}"/>')
        left = min(left, -6); bottom = max(bottom, 11)
    if tagline:
        txt = "Custom Branded Packaging for Cafés & Food Businesses"
        width = oend - left
        ts = 20
        _, e, _ = text_path(txt, ts, 0, 0, font=MED)
        ts = ts * width * 0.98 / e
        _, e, _ = text_path(txt, ts, 0, 0, font=MED)
        ty = bottom + 10 + ts * 0.73
        td, _, tb = text_path(txt, ts, left + (width - e) / 2, ty, font=MED)
        parts.append(f'<path d="{td}" fill="{c_tag or c_word}"/>')
        bottom = tb[3]
    x0, y0 = left - 3, min(ct, wb[1], base - 86) - 3
    W, H = oend + 3 - x0, bottom + 4 - y0
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{f2(x0)} {f2(y0)} {f2(W)} {f2(H)}" width="{f2(W)}" height="{f2(H)}">{"".join(parts)}</svg>\n'


def icon(bg, c_line, c_leaf, c_vein, c_steam, steam=True, square=False, sw=SW, pad_scale=1.0):
    csvg, (l, t, r) = cup(0, 0, c_line, c_leaf, c_vein, c_steam, steam, sw)
    w, h = r - l, -t + sw / 2
    s = (84 if steam else 88) / max(w, h) * pad_scale
    tx = 50 - (l + r) / 2 * s
    ty = 50 - (t + (0 + sw / 2)) / 2 * s
    rect = "" if bg is None else (f'<rect width="100" height="100" fill="{bg}"/>' if square else f'<rect width="100" height="100" rx="22" fill="{bg}"/>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">{rect}'
            f'<g transform="translate({f2(tx)} {f2(ty)}) scale({s:.4f})">{csvg}</g></svg>\n')


C = dict(c_word=NAVY, c_one=ORANGE, c_line=NAVY, c_leaf=GREEN, c_vein=WHITE, c_steam=ORANGE, c_swoosh=ORANGE)
R = dict(c_word=WHITE, c_one=ORANGE, c_line=WHITE, c_leaf=GREEN, c_vein=NAVY, c_steam=ORANGE, c_swoosh=ORANGE)
K = dict(c_word="#000", c_one="#000", c_line="#000", c_leaf="#000", c_vein="#fff", c_steam="#000", c_swoosh="#000")
files = {
    "cups1-logo-full-color.svg": lockup(**C),
    "cups1-logo-full-reversed.svg": lockup(**R),
    "cups1-logo-full-black.svg": lockup(**K),
    "cups1-logo-color.svg": lockup(**C, tagline=False),
    "cups1-logo-reversed.svg": lockup(**R, tagline=False),
    "cups1-logo-nav-color.svg": lockup(**C, tagline=False, swoosh=False, steam=False),
    "cups1-logo-nav-reversed.svg": lockup(**R, tagline=False, swoosh=False, steam=False),
    "cups1-icon-color.svg": icon(None, NAVY, GREEN, WHITE, ORANGE),
    "cups1-icon-tile.svg": icon(NAVY, WHITE, GREEN, NAVY, ORANGE),
}
for n, c in files.items():
    open(os.path.join(OUT, "svg", n), "w").write(c)
fav = icon(NAVY, WHITE, GREEN, NAVY, ORANGE, steam=False, sw=8.5)
open(os.path.join(OUT, "favicon", "favicon.svg"), "w").write(fav)
open(os.path.join(OUT, "fav_small.svg"), "w").write(fav)
open(os.path.join(OUT, "apple_square.svg"), "w").write(icon(NAVY, WHITE, GREEN, NAVY, ORANGE, square=True))
open(os.path.join(OUT, "maskable.svg"), "w").write(icon(NAVY, WHITE, GREEN, NAVY, ORANGE, square=True, pad_scale=0.78))
json.dump({"name": "Cups1", "short_name": "Cups1", "icons": [
    {"src": "/icon-192.png", "sizes": "192x192", "type": "image/png"},
    {"src": "/icon-512.png", "sizes": "512x512", "type": "image/png"},
    {"src": "/icon-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}],
    "theme_color": NAVY, "background_color": WHITE, "display": "standalone"},
    open(os.path.join(OUT, "favicon", "site.webmanifest"), "w"), indent=2)
open(os.path.join(OUT, "favicon", "favicon-snippet.html"), "w").write(
    '<link rel="icon" href="/favicon.ico" sizes="any">\n<link rel="icon" href="/favicon.svg" type="image/svg+xml">\n'
    '<link rel="apple-touch-icon" href="/apple-touch-icon.png">\n<link rel="manifest" href="/site.webmanifest">\n'
    f'<meta name="theme-color" content="{NAVY}">\n')
print("ok")
