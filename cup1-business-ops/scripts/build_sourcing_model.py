from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.comments import Comment
from openpyxl.utils import get_column_letter

import os
OUT = os.path.join(os.path.dirname(__file__), "..", "deliverables", "phase2", "Cup1_Phase2_Sourcing_Model.xlsx")
F = "Arial"
BLUE = Font(name=F, color="0000FF", size=10)
BLK = Font(name=F, size=10)
BOLD = Font(name=F, size=10, bold=True)
HDR = Font(name=F, size=10, bold=True, color="FFFFFF")
TITLE = Font(name=F, size=14, bold=True)
SUB = Font(name=F, size=10, italic=True, color="555555")
HFILL = PatternFill("solid", fgColor="1F4E5A")
SFILL = PatternFill("solid", fgColor="DCE9EC")
YEL = PatternFill("solid", fgColor="FFFF00")
RED = PatternFill("solid", fgColor="F8D7DA")
GRN = PatternFill("solid", fgColor="D4EDDA")
thin = Side(style="thin", color="BBBBBB")
BOX = Border(left=thin, right=thin, top=thin, bottom=thin)
WRAP = Alignment(wrap_text=True, vertical="top")
USD = '$#,##0;($#,##0);"-"'
USD4 = '$0.0000;($0.0000);"-"'
PCT = '0.0%;(0.0%);"-"'
NUM = '#,##0;(#,##0);"-"'

wb = Workbook()

def header(ws, row, vals, widths=None):
    for i, v in enumerate(vals, 1):
        c = ws.cell(row=row, column=i, value=v)
        c.font = HDR; c.fill = HFILL; c.alignment = Alignment(wrap_text=True, vertical="center"); c.border = BOX
    if widths:
        for i, w in enumerate(widths, 1):
            ws.column_dimensions[get_column_letter(i)].width = w

# ---------------- README ----------------
ws = wb.active; ws.title = "Read Me"
ws.column_dimensions["A"].width = 120
lines = [
    ("Cup1 – Phase 2 Supplier Sourcing Model (Paper Cups & Food Packaging)", TITLE),
    ("Prepared 5 Nov 2026 · Target markets: USA, Canada (+ Mexico/region) · Lead product: 12oz double-wall custom-printed hot cup", SUB),
    ("", BLK),
    ("HOW TO USE", BOLD),
    ("• Blue text = inputs you can change. Yellow fill = assumptions that MUST be replaced with real supplier / forwarder quotes.", BLK),
    ("• Black text = formulas. Do not overwrite.", BLK),
    ("• 'Landed Cost Model' compares 4 sourcing routes side-by-side. Replace the FOB price with real RFQ answers as they arrive (log them in 'RFQ Tracker').", BLK),
    ("", BLK),
    ("KEY FINDINGS (verified 4–5 Nov 2026 – see 'Tariffs & Compliance' and 'Sources')", BOLD),
    ("1. USA: paper cups (HTS 4823.69.00) from CHINA currently pay ~37.5% extra duty (25% Section 301 + 12.5% base tariff). From VIETNAM ~12.5%. Vietnam-made cups land ~25 points cheaper in duty.", BLK),
    ("2. CANADA: CBSA opened anti-dumping + anti-subsidy investigations on Chinese paperboard cups & containers (17 Aug 2026). Estimated margins at initiation: 75.8% dumping + 49.6% subsidy. Preliminary decision (and possible provisional duties) due by 16 Nov 2026. Do NOT quote Canadian clients China-made cups until this is resolved.", BLK),
    ("3. Sowinpak (our first supplier) states it runs factories in BOTH China and Vietnam – this is its biggest advantage for North America. Must confirm cups can be produced in Vietnam with Vietnamese origin (not just transshipped).", BLK),
    ("4. US clients increasingly require: FDA food-contact compliance, PFAS-free declarations (state bans: CA, NY, WA, VT, MN, CO, CT, MD and others), and BPI certification for 'compostable' claims. Sowinpak holds BPI, BRC, FSC – the strongest certificate set on the shortlist.", BLK),
    ("5. Market headroom: US online sellers list custom-printed 12oz double-wall cups at ~$0.38/cup (10k qty) and 12oz custom cups at ~$0.13/cup (30k qty). Estimated landed cost is far below these – room for Cup1 margin.", BLK),
    ("", BLK),
    ("IMPORTANT", BOLD),
    ("• Tariffs are changing frequently in 2026. Re-check rates with a licensed US customs broker / Canadian customs broker before quoting any client.", BLK),
    ("• Supplier data was taken from their Alibaba storefronts (self-reported unless Alibaba marks it verified). No supplier has been contacted yet.", BLK),
]
for i, (t, f) in enumerate(lines, 1):
    c = ws.cell(row=i, column=1, value=t); c.font = f; c.alignment = Alignment(wrap_text=True, vertical="top")

# ---------------- Supplier Comparison ----------------
ws = wb.create_sheet("Supplier Comparison")
ws["A1"] = "Supplier Comparison – Paper Cup Manufacturers (Alibaba, viewed 5 Nov 2026)"; ws["A1"].font = TITLE
ws["A2"] = "Facts copied from each Alibaba storefront. Scores (1–5) are Cup1's judgement – blue cells, adjust as RFQ answers arrive."; ws["A2"].font = SUB
cols = ["Supplier", "Alibaba store", "Location", "Business type", "Yrs on Alibaba", "Founded", "Factory size", "Staff",
        "Certifications shown on Alibaba", "Store rating (reviews)", "On-time dispatch", "Dispute rate", "Reorder rate",
        "Response time", "Listed cup price range (USD/pc)", "MOQ (pcs)", "Lead time", "Vietnam production?",
        "Strengths", "Risks / gaps",
        "Compliance (30%)", "Track record (25%)", "Capacity (15%)", "Tariff flexibility (20%)", "Price (10%)", "Weighted score (of 5)"]
header(ws, 4, cols, [26, 30, 18, 18, 9, 9, 13, 11, 40, 12, 10, 9, 9, 10, 16, 11, 11, 16, 40, 40, 11, 11, 11, 11, 10, 11])
ws.row_dimensions[4].height = 45
sup = [
    ["Zhejiang Sowinpak Technology Co., Ltd.", "https://sowinpak88.en.alibaba.com", "Wenzhou, Zhejiang, CN", "Custom Manufacturer (verified by Intertek)", 2, 2008, "55,225 m²", "~1,046",
     "ISO 9001, ISO 14001, ISO 22000, HACCP, BRC, BRCGS Packaging, FSC, PEFC, BPI, DIN CERTCO (home compost)", "5.0 (5)", 1.0, 0.0, 0.222, "≤2h",
     "0.0246–0.182 (double wall)", 30000, "~35 days", "Yes – claims China + Vietnam plants",
     "Strongest certificates incl. BPI & BRC; 100% on-time; 0 disputes; full range (cups, bowls, boxes, lids) = one-stop for clients; 10% of sales already to North America",
     "Only 2 yrs on Alibaba; listed prices are wide ranges; Vietnam plant capacity & product scope unconfirmed",
     5, 4, 5, 5, 3],
    ["Haining Xinhua Paper Cup Factory", "https://xhpapercup.en.alibaba.com", "Haining, Zhejiang, CN", "Manufacturer, Trading Co.", 6, 2006, "3,000–5,000 m²", "11–50",
     "None listed on Alibaba", "5.0 (1)", 1.0, 0.0, 0.143, "≤3h",
     "0.02–0.04", 30000, "~30 days", "No",
     "Cup specialist (60 cup machines, 3.5M pcs/day claimed); 53 Alibaba transactions, US$850k+; 100% on-time; infrared inspection of every cup",
     "No food-safety/FSC/BPI certificates shown – must request FDA/PFAS test reports; China origin = 37.5% US duty; Canada AD risk",
     2, 4, 4, 1, 5],
    ["Dongyuan (Dongyang) Haoyuan Paper Cup Factory", "https://hyzbc.en.alibaba.com", "Dongyang, Zhejiang, CN", "Manufacturer, Trading Co.", 20, 2003, "7,800 m²", "51–100",
     "None listed on Alibaba", "5.0 (3)", None, None, None, "≤3h",
     "0.042–0.092", 100000, "~15 days", "No",
     "20 yrs on Alibaba; 23 cup lines, 1.5M pcs/day claimed; double-wall & ripple specialist; near Yiwu/Ningbo",
     "Very little online trade history (3 transactions); no certificates shown; high MOQ on main listing; China origin tariff/AD exposure",
     2, 2, 4, 1, 4],
    ["Wenzhou Liping Paper Plastic Packaging Co., Ltd.", "https://chinaliping.en.alibaba.com", "Wenzhou, Zhejiang, CN", "Custom Manufacturer", 9, None, "5,750 m²", "50+",
     "ISO 9001, ISO 14001, ISO 45001, FSC, LFGB", "4.8 (4)", 0.667, 0.0, 0.25, "≤5h",
     "0.05–0.08", 5000, "~15 days dispatch", "No",
     "Low MOQ (5,000) – good for small café clients & samples; 17 yrs exporting; has US repeat buyers in reviews",
     "On-time dispatch only 66.7%; no BPI/BRC; China origin tariff/AD exposure",
     3, 3, 2, 1, 4],
    ["Thuan Loi Mfg. Trading Service Imp-Exp Co. (Long An Branch)", "Alibaba product ID 10000017466885", "Long An / HCMC, VN", "Manufacturer", 11, None, "n/a", "n/a",
     "None listed for paper cups (ISO 9001 mentioned on some plastic listings)", "No reviews", None, None, None, "n/a",
     "$20 per box (box qty not stated)", "100 boxes", "n/a", "Yes – Vietnam origin",
     "Vietnam origin (12.5% US duty, outside Canada China AD case); 3–20oz single & double wall",
     "No online performance data; mainly plastic cups; unclear printing capability & pricing – treat as benchmark only",
     1, 1, 2, 5, 3],
]
r0 = 5
for i, row in enumerate(sup):
    r = r0 + i
    for j, v in enumerate(row, 1):
        c = ws.cell(row=r, column=j, value=v)
        c.font = BLUE if j >= 21 else BLK
        c.alignment = WRAP; c.border = BOX
        if j in (11, 12, 13) and v is not None: c.number_format = '0.0%'
        if j == 16 and isinstance(v, int): c.number_format = NUM
        if j in (11, 12, 13) and v is None: c.value = "n/a"
    ws.cell(row=r, column=26, value=f"=ROUND(U{r}*0.3+V{r}*0.25+W{r}*0.15+X{r}*0.2+Y{r}*0.1,2)").font = BOLD
    ws.cell(row=r, column=26).border = BOX
    ws.row_dimensions[r].height = 95
ws.cell(row=r0, column=1).fill = GRN
ws.cell(row=r0 + 6, column=1, value="Recommendation: Primary = Sowinpak (request Vietnam-plant quote for US/Canada). Backup China price benchmark = Haining Xinhua. Small-order / sample option = Wenzhou Liping. Keep looking for a 2nd verified Vietnam paper-cup factory.").font = BOLD
ws.cell(row=r0 + 7, column=1, value="Scoring: 5 = best. Weights in header. 'Tariff flexibility' = ability to ship non-China origin into US/Canada.").font = SUB
ws.freeze_panes = "B5"

# ---------------- Landed Cost Model ----------------
ws = wb.create_sheet("Landed Cost Model")
ws["A1"] = "Landed Cost & Margin Model – 12oz Double-Wall Custom-Printed Hot Cup"; ws["A1"].font = TITLE
ws["A2"] = "One column per sourcing route. Change blue inputs; yellow = placeholder until supplier/forwarder quotes arrive. All money in USD."; ws["A2"].font = SUB
header(ws, 4, ["Line item", "A: China → USA (LA)", "B: Vietnam → USA (LA)", "C: Vietnam → Canada (Vancouver)", "D: China → Canada (AD/CVD risk)", "Unit", "Notes / source"],
       [44, 18, 18, 20, 20, 10, 70])
ws.row_dimensions[4].height = 32
rows = []  # (label, [A,B,C,D] or formula template, unit, note, kind)
# kind: 'sec', 'in', 'yin', 'f'
R = {}
def add(key, label, vals, unit="", note="", kind="in", fmt=None):
    rows.append((key, label, vals, unit, note, kind, fmt))

add("s1", "1. ORDER & PRODUCT", None, kind="sec")
add("us", "Destination is USA? (1 = yes, 0 = no)", [1, 1, 0, 0], "flag", "Drives US fees (MPF/HMF)", "in", "0")
add("qty", "Order quantity", [100000] * 4, "cups", "Example order. Supplier MOQ is 30,000.", "in", NUM)
add("fob", "FOB unit price (12oz DW, 1–2 colour print, no lid)", [0.06] * 4, "$/cup",
    "PLACEHOLDER. Sowinpak lists DW cups at $0.0246–0.182; real price depends on paper GSM, colours, qty. Replace with RFQ answer. Vietnam price may differ.", "yin", USD4)
add("plate", "Printing plates / setup (one-off)", [300] * 4, "$", "Assumption – ask supplier; often waived on repeat orders.", "yin", USD)
add("s2", "2. FREIGHT", None, kind="sec")
add("cpc", "Cups per export carton", [500] * 4, "cups", "Assumption – typical for 12oz DW; confirm on quote.", "yin", NUM)
add("cbm", "Carton volume", [0.075] * 4, "CBM", "Assumption – confirm carton dimensions with supplier.", "yin", "0.000")
add("cartons", "Number of cartons", "=ROUNDUP({c}{qty}/{c}{cpc},0)", "cartons", "", "f", NUM)
add("vol", "Total shipment volume", "={c}{cartons}*{c}{cbm}", "CBM", "", "f", "0.0")
add("frate", "Ocean freight rate (LCL)", [160] * 4, "$/CBM",
    "Assumption. Reference: Drewry WCI Shanghai–Los Angeles FCL $7,514/40ft (30 Oct 2026) ≈ $125/CBM at 60 CBM; LCL priced higher. Get forwarder quote.", "yin", USD)
add("ffix", "Origin + destination LCL/CFS & documentation charges", [600] * 4, "$", "Assumption – get forwarder quote.", "yin", USD)
add("freight", "Total freight", "={c}{vol}*{c}{frate}+{c}{ffix}", "$", "", "f", USD)
add("insr", "Cargo insurance rate (on goods + freight)", [0.003] * 4, "%", "Assumption – typical 0.2–0.5%.", "in", PCT)
add("s3", "3. DUTIES & CUSTOMS", None, kind="sec")
add("mfn", "Base (MFN) duty – HS 4823.69", [0, 0, 0, 0], "%", "US: Free (HTSUS 4823.69.00). Canada: assumed Free – VERIFY with Canadian broker.", "in", PCT)
add("s301", "US Section 301 (China only)", [0.25, 0, 0, 0], "%", "25% on China-origin 4823 goods (tariffstool.com, wove tariff data).", "in", PCT)
add("base", "US base tariff layer (replaced Sec.122 on 24 Jul 2026)", [0.125, 0.125, 0, 0], "%", "12.5% on China and Vietnam origin per tariffstool.com (Nov 2026). Changes often – re-check.", "in", PCT)
add("ad", "Canada anti-dumping + countervailing (China only)", [0, 0, 0, 1.254], "%",
    "RISK SCENARIO: CBSA initiation estimates 75.8% dumping + 49.6% subsidy (PCC 2026 IN). Preliminary decision due by 16 Nov 2026 – replace with actual provisional rates.", "in", PCT)
add("dtot", "Total duty rate", "={c}{mfn}+{c}{s301}+{c}{base}+{c}{ad}", "%", "", "f", PCT)
add("cval", "Customs value (FOB value of goods)", "={c}{qty}*{c}{fob}", "$", "US & Canada assess duty on FOB-type transaction value.", "f", USD)
add("duty", "Duties payable", "={c}{cval}*{c}{dtot}", "$", "", "f", USD)
add("mpfr", "US Merchandise Processing Fee rate", [0.003464] * 4, "%", "CBP FY2027 (from 1 Oct 2026): 0.3464%, min $34.58, max $670.86.", "in", "0.0000%")
add("mpf", "US MPF payable", "={c}{us}*MIN(MAX({c}{cval}*{c}{mpfr},34.58),670.86)", "$", "", "f", USD)
add("hmf", "US Harbor Maintenance Fee (0.125%)", "={c}{us}*{c}{cval}*0.00125", "$", "Ocean shipments into US ports.", "f", USD)
add("broker", "Customs broker, ISF / e-manifest, bond", [350] * 4, "$", "Assumption – broker quote. US needs ISF filing + customs bond.", "yin", USD)
add("inland", "Delivery port → client warehouse", [500] * 4, "$", "Assumption – depends on client location.", "yin", USD)
add("s4", "4. LANDED COST", None, kind="sec")
add("goods", "Product cost", "={c}{cval}+{c}{plate}", "$", "Goods + printing plates", "f", USD)
add("ins", "Insurance", "=({c}{cval}+{c}{freight})*{c}{insr}", "$", "", "f", USD)
add("landed", "TOTAL LANDED COST", "={c}{goods}+{c}{freight}+{c}{ins}+{c}{duty}+{c}{mpf}+{c}{hmf}+{c}{broker}+{c}{inland}", "$", "Canada GST 5% excluded (recoverable by GST-registered importer).", "f", USD)
add("lpc", "Landed cost per cup", "=IFERROR({c}{landed}/{c}{qty},0)", "$/cup", "", "f", USD4)
add("s5", "5. MODEL 1 – CUP1 SELLS PRODUCT (product margin)", None, kind="sec")
add("gm", "Target gross margin on selling price", [0.35] * 4, "%", "Cup1 decision. Gross margin = (price – landed cost) / price.", "in", PCT)
add("ppc", "Client price per cup (DDP, delivered)", "=IFERROR({c}{lpc}/(1-{c}{gm}),0)", "$/cup", "", "f", USD4)
add("rev", "Revenue", "={c}{ppc}*{c}{qty}", "$", "", "f", USD)
add("gp", "Gross profit", "={c}{rev}-{c}{landed}", "$", "", "f", USD)
add("opex", "Cup1 order costs (samples, courier, 3rd-party QC inspection, bank fees)", [700] * 4, "$", "Assumption – pre-shipment inspection ~$300, samples/courier ~$250, payment fees ~$150.", "yin", USD)
add("np", "Net profit (before overheads & tax)", "={c}{gp}-{c}{opex}", "$", "", "f", USD)
add("npm", "Net margin", "=IFERROR({c}{np}/{c}{rev},0)", "%", "", "f", PCT)
add("bench", "US market benchmark – custom 12oz DW cup", [0.3768] * 4, "$/cup", "YourBrandCafe 12oz DW custom, 20+ cases (10,000+ cups), Nov 2026. RestaurantSupplyDrop lists 30k 12oz custom at ~$0.13/cup.", "in", USD4)
add("head", "Client price vs. benchmark", "=IFERROR({c}{ppc}/{c}{bench}-1,0)", "%", "Negative = Cup1 is cheaper than benchmark.", "f", PCT)
add("s6", "6. MODEL 2 – SOURCING COMMISSION (client imports directly)", None, kind="sec")
add("comm", "Sourcing commission rate (on FOB value)", [0.08] * 4, "%", "Cup1 decision – common range 5–10%.", "in", PCT)
add("commmin", "Minimum sourcing fee per order", [1000] * 4, "$", "Cup1 decision. Without a minimum, 8% of a small order does not cover Cup1's own order costs.", "in", USD)
add("commv", "Commission earned", "=MAX({c}{cval}*{c}{comm},{c}{commmin})", "$", "Revenue to Cup1; client pays supplier, freight & duties.", "f", USD)
add("commnp", "Net profit on commission (after order costs)", "={c}{commv}-{c}{opex}", "$", "", "f", USD)

r = 5
for key, label, vals, unit, note, kind, fmt in rows:
    R[key] = r
    r += 1
r = 5
for key, label, vals, unit, note, kind, fmt in rows:
    a = ws.cell(row=r, column=1, value=label); a.border = BOX; a.alignment = WRAP
    if kind == "sec":
        for cc in range(1, 8):
            ws.cell(row=r, column=cc).fill = SFILL; ws.cell(row=r, column=cc).border = BOX
        a.font = BOLD
    else:
        a.font = BOLD if key in ("landed", "lpc", "ppc", "np", "commv") else BLK
        for k, col in enumerate("BCDE"):
            if kind == "f":
                f = vals.replace("{c}", col)
                for kk, rr in R.items():
                    f = f.replace("{" + kk + "}", str(rr))
                c = ws.cell(row=r, column=k + 2, value=f); c.font = BOLD if key in ("landed", "lpc", "ppc", "np") else BLK
            else:
                c = ws.cell(row=r, column=k + 2, value=vals[k]); c.font = BLUE
                if kind == "yin": c.fill = YEL
            c.border = BOX
            if fmt: c.number_format = fmt
        ws.cell(row=r, column=6, value=unit).font = BLK
        n = ws.cell(row=r, column=7, value=note); n.font = Font(name=F, size=9, color="444444"); n.alignment = WRAP
        ws.cell(row=r, column=6).border = BOX; n.border = BOX
    r += 1
for col in "E":
    for rr in range(5, r):
        if ws[f"{col}{rr}"].fill != SFILL and rows[rr - 5][5] != "sec":
            pass
ws.cell(row=4, column=5).fill = PatternFill("solid", fgColor="8B1E2B")
ws.freeze_panes = "B5"
R_LC = R

# ---------------- Tariffs & Compliance ----------------
ws = wb.create_sheet("Tariffs & Compliance")
ws["A1"] = "Tariff & Compliance Snapshot – Paper Cups into North America (checked 4–5 Nov 2026)"; ws["A1"].font = TITLE
header(ws, 3, ["Market / origin", "Measure", "Rate / status", "Key dates", "What it means for Cup1", "Source"], [22, 34, 22, 26, 60, 50])
tar = [
    ["USA ← China", "MFN duty, HTSUS 4823.69.00", "Free", "Ongoing", "No base duty on paper cups.", "tariffstool.com/hts/other-paper-articles-4823"],
    ["USA ← China", "Section 301 (List 3)", "+25%", "In force", "Main extra cost on China-made cups.", "tariffs.wove.com (HTS 4823.69.00.20 from CN)"],
    ["USA ← China", "Base tariff layer (replaced Section 122 on 24 Jul 2026)", "+12.5%", "From 24 Jul 2026", "Total ≈ 37.5% on China-origin cups.", "tariffstool.com/guides/china-tariff-rate"],
    ["USA ← Vietnam", "Base tariff layer", "+12.5%", "From 24 Jul 2026", "Total ≈ 12.5% – about 25 points cheaper than China. Goods must genuinely be made in Vietnam (transshipment is penalised).", "tariffstool.com/guides/importing-from-vietnam-to-us"],
    ["USA (all)", "IEEPA tariffs", "Struck down by Supreme Court 20 Feb 2026", "Refunds via CBP for eligible past entries", "Not a current cost. Rules have changed 3+ times in 2026 – re-verify before every client quote.", "tariffstool.com/guides/china-tariff-rate"],
    ["USA (all)", "Merchandise Processing Fee / Harbor Maintenance Fee", "0.3464% (min $34.58, max $670.86) / 0.125%", "FY2027 from 1 Oct 2026", "Small fixed-ish customs fees per entry.", "junologistics.com FY2027 user fees"],
    ["Canada ← China", "SIMA anti-dumping + countervailing investigation (PCC 2026 IN) – paperboard cups & containers incl. single/double-wall hot cups and bowls", "Est. margins 75.8% dumping + 49.6% subsidy (initiation)", "Initiated 17 Aug 2026; CITT injury finding 16 Oct 2026; CBSA preliminary decision by 16 Nov 2026", "Provisional duties likely soon. Avoid China-origin cups for Canadian clients; use Vietnam production. Ice-cream (enhanced clay-coated) containers, folded pails & molded fiber are EXCLUDED.", "cbsa-asfc.gc.ca PCC 2026 IN; canada.ca CITT news 16 Oct 2026"],
    ["Canada ← Vietnam", "MFN duty 4823.69", "Assumed Free – verify", "—", "Vietnam origin is outside the China SIMA case. Vietnam is also a CPTPP member.", "Confirm with CBSA Customs Tariff / broker"],
    ["Mexico ← China", "Tariff increase on non-FTA countries (China named)", "Up to 35% (paper & cardboard listed among goods)", "From 1 Jan 2026", "China-origin is expensive for Mexico too; Vietnam (CPTPP member with Mexico) is likely better – verify line-level rate.", "mohawkglobal.com"],
]
for i, row in enumerate(tar, 4):
    for j, v in enumerate(row, 1):
        c = ws.cell(row=i, column=j, value=v); c.font = BLK; c.alignment = WRAP; c.border = BOX
    ws.row_dimensions[i].height = 60
ws.cell(row=7 + 3, column=1).fill = RED
rr = 4 + len(tar) + 2
ws.cell(row=rr, column=1, value="COMPLIANCE CHECKLIST – documents to collect from every supplier before quoting US/Canada clients").font = BOLD
header(ws, rr + 1, ["Requirement", "Why", "Document to request", "Sowinpak", "Others", ""])
comp = [
    ["FDA food-contact compliance (21 CFR 176.170 for PE-coated paperboard)", "US legal requirement for food packaging", "FDA compliance statement + migration test report from accredited lab (SGS/Intertek)", "Claims FDA (website) – request report", "Request"],
    ["PFAS-free (no intentionally added PFAS)", "State bans: CA, NY, WA, VT, MN, CO, CT, MD, RI, HI and more", "PFAS test report (total organic fluorine) + declaration", "Request", "Request"],
    ["BPI certification (only if selling as 'compostable')", "Required by many US cities/states for compostable claims", "BPI certificate number, product listing", "BPI listed on Alibaba", "None shown"],
    ["FSC / PEFC chain of custody", "Many café chains require certified fibre", "FSC CoC certificate", "FSC + PEFC", "Liping FSC"],
    ["BRC / BRCGS Packaging", "Retail & large chain buyers ask for it", "BRCGS certificate + audit grade", "Yes", "None shown"],
    ["Country of origin proof", "Tariff & Canada SIMA exposure", "Certificate of origin + factory address of production", "Ask: which plant (CN or VN)?", "China"],
    ["Social compliance", "Corporate buyers", "BSCI / SMETA audit", "Claims BSCI (website)", "Request"],
]
for i, row in enumerate(comp, rr + 2):
    for j, v in enumerate(row, 1):
        c = ws.cell(row=i, column=j, value=v); c.font = BLK; c.alignment = WRAP; c.border = BOX
    ws.row_dimensions[i].height = 42

# ---------------- RFQ Tracker ----------------
ws = wb.create_sheet("RFQ Tracker")
ws["A1"] = "RFQ Tracker – fill in as supplier quotes arrive"; ws["A1"].font = TITLE
ws["A2"] = "Blue cells = enter data. Row 5 is an EXAMPLE showing the format (fictional numbers) – delete it after the first real quote."; ws["A2"].font = SUB
cols = ["Supplier", "Date RFQ sent", "Contact person", "Production plant (CN/VN)", "12oz DW price @30k ($/pc)", "@50k", "@100k",
        "Lid price ($/pc)", "Plate/setup fee ($)", "Sample cost ($)", "Lead time (days)", "Payment terms", "Incoterm & port",
        "FDA report?", "PFAS report?", "BPI cert?", "Carton qty & size", "Notes", "Best price ($/pc)"]
header(ws, 4, cols, [30, 12, 16, 12, 12, 10, 10, 10, 11, 10, 10, 16, 16, 9, 9, 9, 18, 30, 11])
ws.row_dimensions[4].height = 45
ex = ["EXAMPLE – Supplier X", "2026-11-06", "Ms. Lee", "VN", 0.065, 0.058, 0.052, 0.018, 250, 80, 35, "30% deposit / 70% before shipment", "FOB Haiphong", "Yes", "Yes", "No", "500 pcs, 0.075 CBM", "Fictional example row"]
for j, v in enumerate(ex, 1):
    c = ws.cell(row=5, column=j, value=v); c.font = Font(name=F, size=10, color="0000FF", italic=True); c.border = BOX
    if j in (5, 6, 7, 8): c.number_format = USD4
names = ["Zhejiang Sowinpak (China plant)", "Zhejiang Sowinpak (Vietnam plant)", "Haining Xinhua Paper Cup Factory", "Dongyuan Haoyuan Paper Cup Factory", "Wenzhou Liping Paper Plastic Packaging", "Thuan Loi (Vietnam)"]
for i in range(6, 14):
    for j in range(1, 19):
        c = ws.cell(row=i, column=j); c.font = BLUE; c.border = BOX
        if j in (5, 6, 7, 8): c.number_format = USD4
    if i - 6 < len(names):
        ws.cell(row=i, column=1, value=names[i - 6])
for i in range(5, 14):
    c = ws.cell(row=i, column=19, value=f'=IF(COUNT(E{i}:G{i})=0,"",MIN(E{i}:G{i}))'); c.number_format = USD4; c.border = BOX; c.font = BLK

# ---------------- Sources ----------------
ws = wb.create_sheet("Sources")
ws.column_dimensions["A"].width = 60; ws.column_dimensions["B"].width = 90
header(ws, 1, ["Source", "URL"])
src = [
    ("Sowinpak Alibaba storefront & company profile", "https://sowinpak88.en.alibaba.com/company_profile.html"),
    ("Sowinpak website – paper cups (China + Vietnam plants, certifications)", "https://www.sowinpak.com/paper-cup/"),
    ("Haining Xinhua Paper Cup Factory – Alibaba profile", "https://xhpapercup.en.alibaba.com/company_profile.html"),
    ("Dongyuan Haoyuan Paper Cup Factory – Alibaba profile", "https://hyzbc.en.alibaba.com/company_profile.html"),
    ("Wenzhou Liping Paper Plastic Packaging – Alibaba profile", "https://chinaliping.en.alibaba.com/company_profile.html"),
    ("Thuan Loi (Vietnam) paper cup listing", "https://www.alibaba.com/product-detail/DISPOSABLE-PAPER-CUPS-3oz-5oz-9oz_10000017466885.html"),
    ("US tariff, HTS 4823 (MFN Free, +25% China)", "https://www.tariffstool.com/hts/other-paper-articles-4823"),
    ("US tariff layers on China 2026 (Sec.301, base 12.5%, IEEPA struck down)", "https://www.tariffstool.com/guides/china-tariff-rate"),
    ("US paper hot coffee cups from China – 37.5% total", "https://tariffs.wove.com/us/tariff/4823.69.00.20/paper-hot-coffee-cups/from/CN"),
    ("US tariff on Vietnam – 12.5%", "https://www.tariffstool.com/guides/importing-from-vietnam-to-us"),
    ("CBP user fees FY2027 (MPF)", "https://www.junologistics.com/customs-updates/us-customs-user-fees-to-increase-for-fiscal-year-2027"),
    ("CBSA – Notice of initiation, paperboard cups & containers from China", "https://www.cbsa-asfc.gc.ca/sima-lmsi/i-e/pcc2026/pcc2026-ni-eng.html"),
    ("CBSA – Statement of Reasons (scope, estimated margins)", "https://www.cbsa-asfc.gc.ca/sima-lmsi/i-e/pcc2026/pcc2026-in-eng.html"),
    ("CITT – reasonable indication of injury, 16 Oct 2026", "https://www.canada.ca/en/international-trade-tribunal/news/2026/10/tribunal-issues-determination-of-reasonable-indication-of-injurypaperboard-cups-and-containers-from-china.html"),
    ("Mexico tariff increases on non-FTA countries (2026)", "https://mohawkglobal.com/trade-translation/mexico-approves-tariff-increases-on-imports-from-non-fta-countries/"),
    ("Drewry WCI week 44-2026 (Shanghai–LA $7,514/40ft)", "https://shippingtelegraph.com/freight-news/drewry-the-world-container-index-decreased-3-this-week-44-2026/"),
    ("US price benchmark – YourBrandCafe custom 12oz DW", "https://www.yourbrandcafe.com/products/custom-12oz-double-wall-coffee-cups/"),
    ("US price benchmark – RestaurantSupplyDrop 30k custom 12oz", "https://www.restaurantsupplydrop.com/products/custom-paper-coffee-cups-wholesale"),
    ("State PFAS food packaging bans overview", "https://www.steptoe.com/en/news-publications/state-of-the-states-pfas-food-packaging-bans-and-restrictions.html"),
]
for i, (a, b) in enumerate(src, 2):
    ws.cell(row=i, column=1, value=a).font = BLK
    c = ws.cell(row=i, column=2, value=b); c.font = Font(name=F, size=10, color="0563C1", underline="single"); c.hyperlink = b

wb.save(OUT)
print(OUT, R_LC)
