"""Collect every Cup1 logo direction + new suggestions + owner samples into palette_data.json."""
import os, json, re, base64, io
from PIL import Image
from round2 import text_path, one_centered, f2, logo as r2logo, icon as r2icon, OPTIONS
from build_v12 import cup_path, horizontal, icon_svg
import concepts as C1
from glyphs import word

D = os.path.dirname(os.path.abspath(__file__))
TEAL, INK, PAPER, KRAFT = "#1F4E5A", "#1C2B2E", "#F7F3EC", "#B88A5A"
NAVY, ORANGE, FOREST, LIME = "#0E2340", "#EE6A11", "#1E3B2F", "#8CC63F"
ATT = "/mnt/user-data/attachments/a1d5cde3-3768-592d-9758-4f3c55baa1ab/"


def rd(p):
    return open(os.path.join(D, p)).read().strip()


def geom(x, base, cap, heavy=False):
    H = cap * 1.04
    top_w, bot_w = (cap * 0.86, cap * 0.66) if heavy else (cap * 0.80, cap * 0.60)
    cx = x + top_w / 2 + cap * 0.04
    yt, yb = base - H, base
    lid_h = cap * (0.17 if heavy else 0.14); lid_gap = cap * (0.06 if heavy else 0.05)
    lid_w = top_w + cap * 0.10
    return dict(H=H, top_w=top_w, bot_w=bot_w, cx=cx, yt=yt, yb=yb, lid_h=lid_h, lid_gap=lid_gap, lid_w=lid_w,
                ly=yt - lid_gap - lid_h, r=cap * 0.035)


def lid_d(g):
    L, R, lr, ly, h = g["cx"] - g["lid_w"] / 2, g["cx"] + g["lid_w"] / 2, g["lid_h"] / 2, g["ly"], g["lid_h"]
    return (f"M{f2(L + lr)} {f2(ly)}H{f2(R - lr)}A{f2(lr)} {f2(lr)} 0 0 1 {f2(R - lr)} {f2(ly + h)}"
            f"H{f2(L + lr)}A{f2(lr)} {f2(lr)} 0 0 1 {f2(L + lr)} {f2(ly)}Z")


def body_d(g, inset=0.0):
    cx, yt, yb, tw, bw, r = g["cx"], g["yt"] + inset, g["yb"] - inset, g["top_w"] - 2 * inset * 1.05, g["bot_w"] - 2 * inset * 1.05, g["r"]
    return (f"M{f2(cx - tw/2)} {f2(yt)}H{f2(cx + tw/2)}L{f2(cx + bw/2)} {f2(yb - r)}"
            f"Q{f2(cx + bw/2)} {f2(yb)} {f2(cx + bw/2 - r)} {f2(yb)}H{f2(cx - bw/2 + r)}"
            f"Q{f2(cx - bw/2)} {f2(yb)} {f2(cx - bw/2)} {f2(yb - r)}Z")


def cup_parts(x, base, cap, style, c_body, c_one, c_lid=None, heavy=False):
    """style: solid (1 knocked out), line (outline cup, coloured 1), lid (solid body, other-colour lid)."""
    g = geom(x, base, cap, heavy)
    c_lid = c_lid or c_body
    if style == "line":
        sw = cap * (0.13 if heavy else 0.10)
        ring = body_d(g) + body_d(g, sw)          # evenodd → outline ring
        one = one_centered(cap * (0.66 if heavy else 0.62), g["cx"], g["yt"] + g["H"] * 0.54)
        out = (f'<path d="{lid_d(g)}" fill="{c_lid}"/><path d="{ring}" fill="{c_body}" fill-rule="evenodd"/>'
               f'<path d="{one}" fill="{c_one}"/>')
    else:
        one = one_centered(cap * (0.92 if heavy else 0.86), g["cx"], g["yt"] + g["H"] * 0.55)
        if c_one is None:   # knock out
            out = f'<path d="{lid_d(g)}" fill="{c_lid}"/><path d="{body_d(g) + one}" fill="{c_body}" fill-rule="evenodd"/>'
        else:
            out = f'<path d="{lid_d(g)}" fill="{c_lid}"/><path d="{body_d(g)}" fill="{c_body}"/><path d="{one}" fill="{c_one}"/>'
    return out, g["cx"] + g["lid_w"] / 2, g["ly"]


def lockup(word_fill, style, c_body, c_one, c_lid=None, swoosh=None, tagline=None, tag_fill=None, size=100):
    base, cap = size * 1.05, size * 0.7275
    d, endx, b = text_path("Cup", size, 0, base, tracking=-0.03 * size)
    cup, right, top = cup_parts(endx + size * 0.02, base, cap, style, c_body, c_one, c_lid)
    extra, bottom = "", b[3]
    if swoosh:
        y = base + size * 0.10
        sd = (f"M{f2(b[0] + 4)} {f2(y + 6)}Q{f2((b[0] + right) / 2)} {f2(y + 20)} {f2(right - 2)} {f2(y - 4)}"
              f"Q{f2((b[0] + right) / 2)} {f2(y + 6)} {f2(b[0] + 4)} {f2(y + 6)}Z")
        extra += f'<path d="{sd}" fill="{swoosh}"/>'; bottom = y + 16
    if tagline:
        ts = size * 0.115
        td, tend, tb = text_path(tagline, ts, 0, 0, font="/usr/share/fonts/opentype/inter/Inter-SemiBold.otf", tracking=ts * 0.02)
        scale_w = right - b[0]
        if tend > scale_w:
            ts = ts * scale_w / tend
            td, tend, tb = text_path(tagline, ts, 0, 0, font="/usr/share/fonts/opentype/inter/Inter-SemiBold.otf", tracking=ts * 0.02)
        ty = bottom + size * 0.12 + ts
        td, tend, tb = text_path(tagline, ts, b[0] + (scale_w - tend) / 2, ty, font="/usr/share/fonts/opentype/inter/Inter-SemiBold.otf", tracking=ts * 0.02)
        extra += f'<path d="{td}" fill="{tag_fill or word_fill}"/>'; bottom = tb[3]
    x0, y0 = b[0] - 2, min(top, b[1]) - 2
    W, H = right + 2 - x0, bottom + 3 - y0
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{f2(x0)} {f2(y0)} {f2(W)} {f2(H)}">'
            f'<path d="{d}" fill="{word_fill}"/>{cup}{extra}</svg>')


def tile(bg, style, c_body, c_one, c_lid=None):
    cap = 66
    _, right0, top0 = cup_parts(0, 0, cap, style, c_body, c_one, c_lid, heavy=True)
    left0 = -(cap * 0.05)
    x = 50 - (left0 + right0) / 2
    base = 50 - top0 / 2
    cup, _, _ = cup_parts(x, base, cap, style, c_body, c_one, c_lid, heavy=True)
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect width="100" height="100" rx="22" fill="{bg}"/>{cup}</svg>'


def clean(svg):
    head, rest = svg.split(">", 1)
    return re.sub(r'\s(width|height)="[^"]*"', "", head) + ">" + rest


def r1(body_fn, wm_fill=INK):
    """Round-1 lockups: mark (100x100 space) + 'Cup1' wordmark."""
    mark = body_fn
    wm, w, b = C1.wordmark(64, wm_fill)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {f2(118 + w)} 100">{mark}'
            f'<g transform="translate(112 {f2(50 + 64 * 0.7275 / 2 - 64)})">{wm.replace("<path", "<path")}</g></svg>')


def r1_wm(body):
    return body


V = []
def add(**k): V.append(k)

# ---------- Our concepts ----------
cwm, cw = C1.wordmark_C(100)
add(id="r1-a", group="ours", round="Round 1", name="A · Cup & lid mark + Cup1",
    logo=r1(C1.mark_A()), icon=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect width="100" height="100" rx="22" fill="{TEAL}"/>{C1.mark_A(PAPER, TEAL)}</svg>',
    status="Earlier idea", pros="Clean, very readable cup icon.", cons="Mark and name sit apart; the cup does not spell anything.")
add(id="r1-c", group="ours", round="Round 1", name="C · Cup-shaped u",
    logo=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-2 -2 {f2(cw + 4)} 128">{cwm}</svg>', icon=None,
    status="Rejected", pros="Playful one-piece wordmark.", cons="Read as “CVp1” in testing. No usable favicon on its own.")
add(id="v11", group="ours", round="v1.1", name="Rim Monogram C1",
    logo=rd("out/svg/cup1-logo-horizontal-color.svg"), icon=rd("out/svg/cup1-icon-tile.svg"),
    status="Superseded", pros="Distinctive C-ring seen from above; strong favicon.", cons="Owner wanted “Cup” spelled out and a recognisable cup.")
for i, (nm, key) in enumerate([("A · Teal cup", "opt1"), ("B · Navy word + orange cup", "opt2"), ("C · Navy cup + orange 1", "opt3")], 1):
    add(id=f"r2-{'abc'[i-1]}", group="ours", round="Round 2", name=nm,
        logo=rd(f"r2/{key}-logo.svg"), icon=rd(f"r2/{key}-icon.svg"),
        status="Chosen → v1.2" if i == 1 else "Option",
        pros=["Calm, premium, matches the approved palette.", "High energy; orange is easy to spot on shelves and ads.", "Navy reads corporate and trusted; the orange 1 pops."][i-1],
        cons=["Less loud than orange directions.", "Orange cup + navy text is the look of many generic packaging sellers.", "The small orange 1 loses contrast at 16px."][i-1])
add(id="v12", group="ours", round="v1.2 · current", name="Cup + teal cup-1 (final)",
    logo=rd("v12/svg/cup1-logo-horizontal-color.svg"), icon=rd("v12/favicon/favicon.svg"),
    status="Current pick", pros="Owner's idea, tested at 30px navbar and 16px favicon. Full file set already built.", cons="Quieter than your new samples; no tagline lockup yet.")

# ---------- New suggestions (from the samples, simplified to survive small sizes) ----------
add(id="s1", group="new", round="Suggestion", name="S1 · Navy line cup + orange 1",
    logo=lockup(NAVY, "line", NAVY, ORANGE), icon=tile(NAVY, "line", "#FFFFFF", ORANGE, "#FFFFFF"),
    status="Suggested", pros="Keeps the line-art feel and navy/orange colours of your samples 1 and 4, without steam, leaf or swoosh.", cons="Outline cup is thinner than v1.2; check the 16px favicon before choosing.")
add(id="s2", group="new", round="Suggestion", name="S2 · Navy + orange cup with swoosh",
    logo=lockup(NAVY, "solid", ORANGE, None, swoosh=ORANGE), icon=tile(ORANGE, "solid", "#FFFFFF", None),
    status="Suggested", pros="Closest to sample 4's energy; solid cup stays readable at every size.", cons="Swoosh is decoration; drop it in the navbar (use the plain lockup there).")
add(id="s3", group="new", round="Suggestion", name="S3 · Forest + lime",
    logo=lockup(FOREST, "line", FOREST, "#5E9E1F"), icon=tile(FOREST, "line", PAPER, LIME, PAPER),
    status="Suggested", pros="Takes the dark green + lime of samples 2 and 3; feels fresh and food-friendly.", cons="Green reads “eco”. Our claims rule means the site must back that with documents.")
add(id="s4", group="new", round="Suggestion", name="S4 · Teal cup + kraft lid",
    logo=lockup(INK, "solid", TEAL, None, c_lid=KRAFT), icon=tile(TEAL, "solid", PAPER, None, KRAFT),
    status="Suggested", pros="v1.2 plus the kraft-paper warmth of sample 3's sleeve, in one extra colour.", cons="Kraft lid is low-contrast on a teal tile; fine at 32px+, subtle at 16px.")
add(id="s5", group="new", round="Suggestion", name="S5 · v1.2 with tagline lockup",
    logo=lockup(INK, "solid", TEAL, None, tagline="CUSTOM PACKAGING FOR CAFÉS & FOOD BRANDS", tag_fill=TEAL), icon=rd("v12/favicon/favicon.svg"),
    status="Suggested", pros="Every sample has a tagline; this adds one for print, decks and email signatures.", cons="Tagline version is for large uses only; navbar keeps the plain logo.")

for v in V:
    v["logo"] = clean(v["logo"])
    if v.get("icon"): v["icon"] = clean(v["icon"])


# ---------- Owner samples ----------
def jpg(path, w=1100):
    im = Image.open(path).convert("RGB")
    if im.width > w: im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf, "JPEG", quality=82, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()

SAMPLES = [
    ("4b69e895-image.png", "Sample 1 · Navy cup, steam & leaf", "Navy outline cup with orange steam and a green leaf; navy “Cup”, orange 1, orange swoosh; tagline “Custom Branded Packaging for Cafés & Food Businesses”.",
     "Steam, leaf and swoosh vanish below ~40px. The leaf implies an eco claim we can't document yet."),
    ("595c0cd5-image.png", "Sample 2 · Dark green, sprout", "White “Cup” and lime 1 inside a cup outline with a sprout, on dark green; ® mark; “Custom-Branded Sustainable Food Packaging”.",
     "Remove ® until the mark is registered. “Sustainable” needs proof under our claims rule."),
    ("3b764e5d-image.png", "Sample 3 · Green cup, kraft sleeve", "Green line cup with kraft sleeve and a clamshell; dark green “Cup”, lime 1; ™; “Custom Packaging & Takeaway Supplies”.",
     "Two objects in the mark make it busy at icon size. ™ is fine to use before registration."),
    ("fd2b9c8a-image.png", "Sample 4 · Navy/orange product trio", "Box + cup + clamshell line art, orange swoosh, navy/orange type; “Custom Packaging & Takeaway Supplies”.",
     "Shows the full product range, but three objects can't shrink into a favicon."),
    ("304cc8de-image.png", "Sample 5 · Earlier reference", "The first reference you shared, same family as sample 4.",
     "Prompted the “Cup + cup holding 1” idea behind v1.2."),
]
samples = [dict(id=f"x{i+1}", file=f, name=n, desc=d, note=nt, img=jpg(ATT + f)) for i, (f, n, d, nt) in enumerate(SAMPLES)]
json.dump(dict(variants=V, samples=samples), open(os.path.join(D, "palette_data.json"), "w"))
os.makedirs(os.path.join(D, "palette_svg"), exist_ok=True)
for v in V:
    open(os.path.join(D, "palette_svg", f"{v['id']}-logo.svg"), "w").write(v["logo"] + "\n")
    if v.get("icon"): open(os.path.join(D, "palette_svg", f"{v['id']}-icon.svg"), "w").write(v["icon"] + "\n")
print(len(V), "variants;", sum(len(s["img"]) for s in samples) // 1024, "KB samples")

# tight cup mark (v1.2 geometry) for font-swap variants rendered with live web fonts
cap = 100
d, right, top = cup_path(0, 0, cap)
left = -(cap * 0.05)
cupmark = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{f2(left)} {f2(top)} {f2(right-left)} {f2(-top)}">'
           f'<path d="{d}" fill="currentColor" fill-rule="evenodd"/></svg>')
data = json.load(open(os.path.join(D, "palette_data.json")))
data["cupmark"] = cupmark
data["cupratio"] = round((right - left) / -top, 4)
json.dump(data, open(os.path.join(D, "palette_data.json"), "w"))
print("cup ratio", data["cupratio"])
