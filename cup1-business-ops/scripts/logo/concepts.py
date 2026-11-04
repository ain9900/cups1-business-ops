import os
from glyphs import word, arc_ring

TEAL, INK, PAPER, KRAFT = "#1F4E5A", "#1C2B2E", "#F7F3EC", "#B88A5A"
OUT = os.path.dirname(os.path.abspath(__file__))


def svg(vb, body, w=None, h=None):
    W, H = vb[2], vb[3]
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb[0]} {vb[1]} {W} {H}" '
            f'width="{w or W}" height="{h or H}">{body}</svg>')


# ---------- Concept A: Cup & Lid (side view, refined) ----------
def mark_A(fg=TEAL, knock=PAPER):
    one, _, _ = word("1", 46, 0, 0)
    # centre the 1: bbox x 0.81..16.28, cap 33.47 at size 46
    tx, ty = 50 - (0.81 + 16.28) / 2 + 0.8, 79
    body = (f'<rect x="16" y="9" width="68" height="11" rx="5.5" fill="{fg}"/>'
            f'<path d="M20 24H80L73.6 88.2Q73 93 68.2 93H31.8Q27 93 26.4 88.2Z" fill="{fg}"/>'
            f'<path transform="translate({tx} {ty})" d="{one}" fill="{knock}"/>')
    return body


# ---------- Concept B: Rim monogram "C1" (cup seen from above) ----------
def mark_B(fg=TEAL, one_fill=None):
    ring = arc_ring(50, 50, 46, 31, 40, 320)
    one, _, _ = word("1", 54, 0, 0)
    # bbox at 54: x 0.95..19.12, cap ~39.29
    tx, ty = 50 - (0.95 + 19.12) / 2 + 1.2, 50 + 39.29 / 2
    return f'<path d="{ring}" fill="{fg}"/><path transform="translate({tx:.2f} {ty:.2f})" d="{one}" fill="{one_fill or fg}"/>'


# ---------- Concept C: Cup-u wordmark ----------
def cup_u(x, base, size, fg):
    s = size / 100
    def P(px, py):
        return f"{x + px * s:.2f} {base + (py - 100) * s:.2f}"
    d = (f"M{P(4.7,48.4)}L{P(21.5,48.4)}L{P(25.6,84.2)}L{P(34.5,84.2)}L{P(38.6,48.4)}L{P(55.4,48.4)}"
         f"L{P(49.4,101)}L{P(10.7,101)}Z")
    lid = f'<rect x="{x + 1.5 * s:.2f}" y="{base - 61 * s:.2f}" width="{57 * s:.2f}" height="{7.5 * s:.2f}" rx="{3.75 * s:.2f}" fill="{fg}"/>'
    return f'<path d="{d}" fill="{fg}"/>' + lid, 60.1 * s


def wordmark_C(size=100, fg=INK, accent=TEAL):
    c, wc, _ = word("C", size, 0, size)
    u, wu = cup_u(wc - 1.5 * size / 100, size, size, accent)
    p1, wp, _ = word("p1", size, wc + wu - 3 * size / 100, size)
    return f'<path d="{c}" fill="{fg}"/>{u}<path d="{p1}" fill="{fg}"/>', wc + wu + wp - 4.5 * size / 100


def wordmark(size=100, fg=INK):
    d, w, b = word("Cup1", size, 0, size, tracking=-0.025 * size)
    return f'<path d="{d}" fill="{fg}"/>', w, b


def board():
    wm, wmw, _ = wordmark(64)
    rows = []
    def tile(inner, bg, w=220, h=180, vb="0 0 100 100"):
        return f'<div style="background:{bg};border-radius:10px;width:{w}px;height:{h}px;display:flex;align-items:center;justify-content:center">{inner}</div>'
    def small(m, bg):
        return "".join(f'<div style="background:{bg};width:{z+8}px;height:{z+8}px;display:flex;align-items:center;justify-content:center;border-radius:4px">{svg((0,0,100,100), m, z, z)}</div>' for z in (16, 32, 48))
    concepts = [
        ("A · Cup & Lid", "Side-view takeaway cup with the \"1\" cut out. Literal and friendly, but side-view cup icons are common in the category (CupPrint, LogoCup).", mark_A(), mark_A(PAPER, TEAL), None),
        ("B · Rim Monogram (recommended)", "A cup seen from above: the rim forms a \"C\" that holds the \"1\" (C1). Reads like a seal of approval, which fits \"fully documented\". Unique in the category and strongest at favicon size.", mark_B(), mark_B(PAPER), None),
        ("C · Cup-u Wordmark", "The \"u\" in Cup1 becomes a cup with its lid. Charming in the wordmark; the icon alone is weaker at small sizes.", None, None, "C"),
    ]
    html = ['<html><body style="margin:0;padding:32px;background:#E9E4DA;font-family:Inter,Arial;color:#1C2B2E"><div style="font-weight:800;font-size:26px;margin-bottom:4px">Cup1 logo concepts</div><div style="color:#55605F;margin-bottom:20px">Round 1 · 3 directions · light and dark backgrounds · 16 / 32 / 48 px tests</div><div style="display:flex;gap:22px">']
    for title, why, light, dark, kind in concepts:
        if kind == "C":
            wc, w = wordmark_C(60)
            wcd, _ = wordmark_C(60, PAPER, "#6FB3C2")
            u_icon, _ = cup_u(20, 85, 100, TEAL)
            icon = svg((0, -8, 100, 100), u_icon, 110, 110)
            l = f'<div style="display:flex;flex-direction:column;align-items:center;gap:10px">{icon}{svg((0,0,w,80), wc, w, 80)}</div>'
            d = svg((0, 0, w, 80), wcd, w, 80)
            sm = "".join(f'<div style="background:#fff;width:{z+8}px;height:{z+8}px;display:flex;align-items:center;justify-content:center;border-radius:4px">{svg((0,-8,100,100), u_icon.replace("x=\"21.5\"","x=\"21.5\""), z, z)}</div>' for z in (16, 32, 48))
        else:
            l = f'<div style="display:flex;align-items:center;gap:14px">{svg((0,0,100,100), light, 86, 86)}{svg((0,0,wmw,90), wm, wmw*0.9, 81)}</div>'
            d = f'<div style="display:flex;align-items:center;gap:14px">{svg((0,0,100,100), dark, 86, 86)}{svg((0,0,wmw,90), wordmark(64, PAPER)[0], wmw*0.9, 81)}</div>'
            sm = small(light, "#fff")
        html.append(f'<div style="flex:1;background:#F7F3EC;border-radius:12px;padding:18px;border:1px solid #D6CCBC"><div style="font-weight:800;font-size:17px">{title}</div><div style="font-size:12.5px;color:#55605F;height:58px;margin:6px 0 12px">{why}</div>'
                    f'{tile(l, "#FFFFFF", 340, 170)}<div style="height:10px"></div>{tile(d, TEAL, 340, 150)}<div style="display:flex;gap:10px;align-items:flex-end;margin-top:12px">{sm}<span style="font-size:11px;color:#55605F">favicon test</span></div></div>')
    html.append("</div></body></html>")
    open(os.path.join(OUT, "concepts.html"), "w").write("".join(html))


if __name__ == "__main__":
    board()
