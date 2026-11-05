"""Outline text to SVG path data using an installed font (no <text> in final SVGs)."""
import math
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

FONT = "/usr/share/fonts/opentype/inter/InterDisplay-ExtraBold.otf"
_f = TTFont(FONT)
GS = _f.getGlyphSet()
CMAP = _f.getBestCmap()
UPEM = _f["head"].unitsPerEm


def word(text, size, x=0.0, baseline=0.0, tracking=0.0, kern=None):
    """Return (path_d, width, bounds) for text at font size `size` (px)."""
    s = size / UPEM
    pen = SVGPathPen(GS, ntos=lambda v: ("%.2f" % v).rstrip("0").rstrip("."))
    cx = x
    kern = kern or {}
    bp = BoundsPen(GS)
    for i, ch in enumerate(text):
        g = CMAP[ord(ch)]
        t = TransformPen(pen, (s, 0, 0, -s, cx, baseline))
        GS[g].draw(t)
        GS[g].draw(TransformPen(bp, (s, 0, 0, -s, cx, baseline)))
        cx += GS[g].width * s + tracking + kern.get(i, 0)
    return pen.getCommands(), cx - x, bp.bounds


def glyph(ch, size, x, baseline):
    return word(ch, size, x, baseline)


def arc_ring(cx, cy, ro, ri, a0, a1):
    """Annular sector from angle a0 to a1 (degrees, clockwise in screen coords, large sweep)."""
    def p(r, a):
        return cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))
    large = 1 if (a1 - a0) % 360 > 180 else 0
    x0, y0 = p(ro, a0); x1, y1 = p(ro, a1)
    x2, y2 = p(ri, a1); x3, y3 = p(ri, a0)
    f = lambda v: ("%.2f" % v).rstrip("0").rstrip(".")
    return (f"M{f(x0)} {f(y0)}A{ro} {ro} 0 {large} 1 {f(x1)} {f(y1)}"
            f"L{f(x2)} {f(y2)}A{ri} {ri} 0 {large} 0 {f(x3)} {f(y3)}Z")
