"""Round 2: 'Cup' wordmark + a takeaway cup holding the numeral 1 (user's idea). Paths only."""
import os, re
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

D = os.path.dirname(os.path.abspath(__file__))
BLACK = "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf"
f2 = lambda v: ("%.2f" % v).rstrip("0").rstrip(".")


def text_path(txt, size, x, base, font=BLACK, tracking=0.0):
    f = TTFont(font); gs = f.getGlyphSet(); cm = f.getBestCmap(); s = size / f["head"].unitsPerEm
    pen = SVGPathPen(gs, ntos=f2); bp = BoundsPen(gs); cx = x
    for ch in txt:
        g = cm[ord(ch)]
        gs[g].draw(TransformPen(pen, (s, 0, 0, -s, cx, base))); gs[g].draw(TransformPen(bp, (s, 0, 0, -s, cx, base)))
        cx += gs[g].width * s + tracking
    return pen.getCommands(), cx, bp.bounds


def one_centered(size, cx, cy):
    f = TTFont(BLACK); gs = f.getGlyphSet(); g = f.getBestCmap()[ord("1")]; s = size / f["head"].unitsPerEm
    bp = BoundsPen(gs); gs[g].draw(TransformPen(bp, (s, 0, 0, -s, 0, 0))); x0, y0, x1, y1 = bp.bounds
    tx, ty = cx - (x0 + x1) / 2 + size * 0.03, cy - (y0 + y1) / 2
    pen = SVGPathPen(gs, ntos=f2); gs[g].draw(TransformPen(pen, (s, 0, 0, -s, tx, ty)))
    return pen.getCommands()


def cup_glyph(x, base, cap, body, band, one, lid=None, band_on=True):
    """Takeaway cup sized to the wordmark: lid above cap line, body from cap line to baseline."""
    lid = lid or body
    H = cap * 1.04                       # body height
    top_w, bot_w = cap * 0.80, cap * 0.60
    cx = x + top_w / 2 + cap * 0.04
    yt, yb = base - H, base
    lid_h, lid_gap = cap * 0.14, cap * 0.05
    lid_w = top_w + cap * 0.10
    r = cap * 0.035
    body_d = (f"M{f2(cx - top_w/2)} {f2(yt)}H{f2(cx + top_w/2)}L{f2(cx + bot_w/2)} {f2(yb - r)}"
              f"Q{f2(cx + bot_w/2)} {f2(yb)} {f2(cx + bot_w/2 - r)} {f2(yb)}H{f2(cx - bot_w/2 + r)}"
              f"Q{f2(cx - bot_w/2)} {f2(yb)} {f2(cx - bot_w/2)} {f2(yb - r)}Z")
    lid_y = yt - lid_gap - lid_h
    out = [f'<rect x="{f2(cx - lid_w/2)}" y="{f2(lid_y)}" width="{f2(lid_w)}" height="{f2(lid_h)}" rx="{f2(lid_h/2)}" fill="{lid}"/>',
           f'<path d="{body_d}" fill="{body}"/>']
    if band_on:
        # sleeve band across the middle third, clipped to the cup's taper
        b0, b1 = yt + H * 0.30, yt + H * 0.80
        w = lambda y: top_w + (bot_w - top_w) * (y - yt) / H
        out.append(f'<path d="M{f2(cx - w(b0)/2)} {f2(b0)}H{f2(cx + w(b0)/2)}L{f2(cx + w(b1)/2)} {f2(b1)}H{f2(cx - w(b1)/2)}Z" fill="{band}"/>')
    out.append(f'<path d="{one_centered(cap * 0.86, cx, yt + H * 0.55)}" fill="{one}"/>')
    width = top_w + cap * 0.08 + cap * 0.10
    return "".join(out), width, lid_y


def logo(word_fill, body, band, one, lid=None, band_on=True, size=100):
    cap = size * 0.7275
    d, endx, b = text_path("Cup", size, 0, size * 1.05, tracking=-0.03 * size)
    cup, cw, lid_y = cup_glyph(endx + size * 0.02, size * 1.05, cap, body, band, one, lid, band_on)
    W = endx + size * 0.02 + cw + 2
    top = min(lid_y, b[1]) - 2
    H = (size * 1.05 + (b[3] - size * 1.05)) - top + 2
    vb = f"{f2(b[0] - 2)} {f2(top)} {f2(W - b[0] + 2)} {f2(H)}"
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" width="{f2(W - b[0] + 2)}" height="{f2(H)}"><path d="{d}" fill="{word_fill}"/>{cup}</svg>'


def icon(bg, body, band, one, lid=None, band_on=True, tile=True):
    cap = 70
    cup, cw, lid_y = cup_glyph(0, 0, cap, body, band, one, lid, band_on)
    # cup spans x ~[ -3.5, cw ] and y [lid_y, 0]; centre in 100x100
    h = -lid_y; w = cap * 0.90
    tx, ty = 50 - (cap * 0.04 + cap * 0.40), 50 + h / 2 - 1
    rect = f'<rect width="100" height="100" rx="22" fill="{bg}"/>' if tile else ""
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">{rect}<g transform="translate({f2(tx)} {f2(ty)})">{cup}</g></svg>'


OPTIONS = {
    "A · Teal cup (current palette)": dict(word="#1C2B2E", body="#1F4E5A", band="#1F4E5A", one="#F7F3EC", tile="#1F4E5A", tbody="#F7F3EC", tband="#F7F3EC", tone="#1F4E5A", band_on=False),
    "B · Navy word + Orange cup": dict(word="#0E2340", body="#EE6A11", band="#EE6A11", one="#FFFFFF", tile="#EE6A11", tbody="#FFFFFF", tband="#FFFFFF", tone="#EE6A11", band_on=False),
    "C · Navy cup + Orange 1": dict(word="#0E2340", body="#0E2340", band="#0E2340", one="#F47A20", tile="#0E2340", tbody="#FFFFFF", tband="#FFFFFF", tone="#0E2340", band_on=False),
}

if __name__ == "__main__":
    os.makedirs(os.path.join(D, "r2"), exist_ok=True)
    cards = []
    def sz(svg, w=None, h=None):
        st = f"width:{w}px;height:auto" if w else f"height:{h}px;width:auto"
        return re.sub(r'width="[^"]*" height="[^"]*"', f'style="{st}"', svg, count=1)
    for i, (name, o) in enumerate(OPTIONS.items(), 1):
        bo = o.get("band_on", True)
        L = logo(o["word"], o["body"], o["band"], o["one"], band_on=bo)
        Lr = logo("#FFFFFF", "#FFFFFF", o["band"], o["tile"], band_on=bo)
        I = icon(o["tile"], o["tbody"], o["tband"], o["tone"], band_on=bo)
        open(os.path.join(D, "r2", f"opt{i}-logo.svg"), "w").write(L)
        open(os.path.join(D, "r2", f"opt{i}-icon.svg"), "w").write(I)
        nav = f'<div style="background:#fff;border:1px solid #ddd;border-radius:6px;display:flex;align-items:center;justify-content:space-between;padding:10px 14px;width:330px">{sz(L, h=30)}<span style="font-size:10px;color:#555">Products · Pricing · Contact</span></div>'
        favs = "".join(f'<div style="text-align:center;font-size:9px;color:#666">{sz(I, w=z)}<br>{z}px</div>' for z in (16, 24, 32, 48))
        cards.append(f'<div style="flex:1;background:#F7F3EC;border:1px solid #D6CCBC;border-radius:12px;padding:16px"><div style="font-weight:800;font-size:16px;margin-bottom:10px">{name}</div>'
                     f'<div style="background:#fff;border-radius:8px;height:150px;display:flex;align-items:center;justify-content:center">{sz(L, w=230)}</div>'
                     f'<div style="background:{o["tile"]};border-radius:8px;height:110px;display:flex;align-items:center;justify-content:center;margin-top:8px">{sz(Lr, w=190)}</div>'
                     f'<div style="margin-top:10px;font-size:11px;color:#555">Navbar (30px tall):</div>{nav}'
                     f'<div style="margin-top:10px;font-size:11px;color:#555">Favicon / app icon:</div><div style="display:flex;gap:14px;align-items:flex-end;margin-top:4px">{favs}</div></div>')
    html = ('<html><body style="margin:0;padding:28px;background:#E9E4DA;font-family:Inter,Arial;color:#1C2B2E;width:1160px">'
            '<div style="font-weight:800;font-size:24px">Cup1 logo – Round 2: "Cup" + a cup holding the 1</div>'
            '<div style="color:#55605F;margin:4px 0 18px">Your idea, built to stay readable in a 30px navbar and a 16px favicon · three color directions</div>'
            f'<div style="display:flex;gap:16px">{"".join(cards)}</div></body></html>')
    open(os.path.join(D, "round2.html"), "w").write(html)
    print("ok")
