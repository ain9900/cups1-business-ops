# Cup1 – Master Phase Tracker & Project Memory

**Last updated:** 5 Nov 2026 · **Owner:** Cup1 team · **How to use:** read this first in any new chat. Update the status, decisions and next actions whenever a phase moves. Phases run one at a time, and each needs user APPROVAL before the next starts.

---

## 1. Business model (summary)

- **What:** B2B sourcing + custom-printed food-service packaging (cups, lids, bowls, takeaway boxes) with the client's logo.
- **Who:** café groups, bubble-tea and dessert chains, and regional distributors in the **USA & Canada** (Mexico and nearby markets secondary). Sweet spot: **30,000–100,000 cups per order**.
- **Made where:** certified Asian factories via Alibaba. Primary supplier is **Zhejiang Sowinpak** (China + **Vietnam** + Indonesia plants); Vietnam production is used for North America.
- **Positioning:** "Your brand. Every cup. Fully documented." Factory-direct price, delivered (duties and freight included), with FDA and PFAS-free paperwork.
- **Revenue:**
  1. Product margin (main): buy FOB, sell delivered (DDP). Placeholder estimate ≈ 31% net per order.
  2. Sourcing commission: 3–10% of FOB (market range), minimum fee ≈ $1,000 per order, for clients who import themselves.
  3. Service fees: design, Sample Kit, QC inspection, monthly retainers ($500–3,000/month market range).
- **Asset-light:** no factory or warehouse. Protect against clients going direct with service value, client contracts and supplier non-circumvention agreements.

---

## 2. Phase status overview

| # | Phase | Status | Approved? |
|---|---|---|---|
| 1 | Product Research | ✅ Done: product chosen (custom paper cups & food packaging; lead SKU 12oz double-wall hot cup) | Yes (implicitly by user, 5 Nov 2026) |
| 2 | Supplier Sourcing | 🟡 Desk work done; **RFQs not yet sent**, no quotes or samples | Partly (user moved on) |
| 3 | Branding | ✅ Revision 1 done (new logo + favicon, 5 Nov 2026): **awaiting user APPROVE / REVISE** | **No – pending** |
| 4 | Website Development | ⏳ Not started (blueprint ready from design teardown) | – |
| 5 | Client Acquisition | ⏳ Not started (segments defined) | – |
| 6 | Client Onboarding | ⏳ Not started | – |
| 7 | Procurement & Fulfillment | ⏳ Not started | – |
| 8 | Financial Management | ⏳ Not started (cost & margin model exists) | – |
| + | Research: Competitor Intelligence & Website Design Teardown | ✅ Done (supports Phases 3–5) | n/a |

---

## 3. Phase details

### Phase 1 – Product Research ✅
- **Decision:** custom-printed paper cups and food packaging for North American food service. Lead product: 12oz double-wall hot cup; launch range of 6 (DW cup, single-wall cup, ripple cup, ice-cream cups, kraft bowls, takeaway boxes).
- **Source:** Sowinpak Alibaba store (project doc "Suppliers Sourcing Link").

### Phase 2 – Supplier Sourcing 🟡
- **Done:** shortlist of 5 suppliers scored; US/Canada tariff research; landed-cost and margin model; RFQ, verification checklist and sample request written.
- **Shortlist (score /5):** Sowinpak 4.6 (primary) · Haining Xinhua 2.9 (China price benchmark) · Wenzhou Liping 2.6 (small orders, MOQ 5,000) · Dongyuan Haoyuan 2.3 · Thuan Loi (Vietnam) 2.2.
- **Key facts:**
  - US duty: China ≈ 37.5% (25% Sec.301 + 12.5% base), Vietnam ≈ 12.5%.
  - Canada: anti-dumping/subsidy case on Chinese paper cups, preliminary decision due by 16 Nov 2026 (estimated 75.8% + 49.6%).
  - Freight: Drewry WCI Shanghai–LA $7,514 per 40ft (30 Oct 2026).
- **Placeholder economics:** FOB $0.06; 100k cups landed USA ≈ $0.11 (VN) – $0.12 (CN) per cup; client price at 35% GM ≈ $0.17–0.19 per cup.
- **Open items:**
  - [ ] Send RFQ to all 5 suppliers (target 7 Nov 2026)
  - [ ] Ask Sowinpak: 12oz DW at the Vietnam plant + price
  - [ ] Check the CBSA decision on 17 Nov 2026 and update the Canada column
  - [ ] Forwarder quote (LCL to LA and Vancouver); US customs broker to confirm duty rates
  - [ ] Order samples from the top 2 (target 20 Nov 2026)
  - [ ] Find a second Vietnam paper-cup factory
- **Deliverables:** `Cup1_Phase2_Sourcing_Model.xlsx`, `Cup1_Phase2_Supplier_Sourcing_Pack.pdf/.docx` (folder); doc https://claude.ai/artifact/XzLCMWbwm8tUBrUW4ACq6U; `docs/phases/phase2-sourcing-findings.md`, `docs/phases/phase2-supplier-sourcing-pack.md`.

### Phase 3 – Branding ✅ (revision 1 done, awaiting approval)
- **Revision 1 (5 Nov 2026):** user asked for a branding revision and for Claude to design the logo and favicon using the `logo-favicon-designer` skill. Result: **Rim Monogram logo v1.1** (C1 seal), full logo system, favicon/app-icon set, guidelines, mockups. Files: `brand/logo/`.
- **User decisions:** brand Cup1 itself as a B2B supplier; positioning **eco + compliant**.
- **Tagline (recommended):** "Your brand. Every cup. Fully documented."
- **Identity:**
  - Logo: Rim Monogram (C1) + "Cup1" wordmark (v1.1)
  - Colors: Harbor Teal #1F4E5A, Ink #1C2B2E, Kraft #B88A5A, Paper #F7F3EC, Kraft Tint #EDE5D8, Verified green #2E7D4F (compliance only)
  - Font: Inter (ExtraBold for headlines)
- **Claims rule:** if we can't attach the document, we don't make the claim. No unqualified eco or recyclable claims; "compostable" only for BPI-certified SKUs; no reviews or client logos until they are real.
- **Recommended additions (from research):** show "from 30,000 cups · ~35 days + shipping"; add a "Request a Sample Kit" call to action.
- **Open items:** [ ] User APPROVE/REVISE · [x] Wordmark outlined (done in v1.1) · [ ] Professional trademark search before registering.
- **Deliverables:**
  - `Cup1_Phase3_Brand_Strategy.pdf/.docx`, `Cup1_Brand_Sheet.png`, `Brand Assets/` (logos PNG/SVG) in the folder
  - Brand doc https://claude.ai/artifact/AowAYBzKhSdbusoSipzGak
  - Design System https://claude.ai/artifact/JrMk8352xRmnsqFWVvjf4Q (private; share before others can open it)
  - `docs/phases/phase3-brand-decisions.md`, `docs/phases/phase3-brand-strategy.md`; tokens in `brand/design-system/tokens.json`

### Research add-on – Competitors & Website Design ✅
- **Competitors studied (9):** YourBrandCafe, LogoCup, CupPrint USA, noissue, Good Start Packaging, KimEcopak, Karat Packaging (KRT), YOON, Sowinpak (also sells direct).
- **Findings:**
  - Free samples are standard.
  - Competitors run heavy tracking (GTM, GA4, ad pixels, Clarity/Hotjar, HubSpot/Klaviyo).
  - Every product page shows MOQ, lead time and price up front.
  - **Price alert:** noissue lists custom PE cups "from $0.10" (MOQ 1,000, 3 weeks), which pressures our ~$0.17–0.19 delivered price.
- **Deliverables:** `Cup1_Competitor_Intelligence_Report.pdf/.docx`, `Cup1_Website_Design_Teardown.pdf/.docx`, `Brand Assets/Cup1_Homepage_Blueprint.png`; docs https://claude.ai/artifact/RU2sFTyv3E19yNcRp26ZUc and https://claude.ai/artifact/3zFrmKpKpSscTAD3NPSgQ7; `docs/research/competitor-intelligence-report.md`, `docs/research/website-design-teardown.md`.

### Phase 4 – Website Development ⏳
- **Ready inputs:** 12-section homepage blueprint, product-page blueprint, design system, brand copy, 6 product descriptions.
- **To do:**
  - Choose a platform (e.g. Shopify or WordPress)
  - Domain
  - Quote form (product, size, quantity, city, logo upload, "how did you hear about us")
  - Sample Kit request
  - Compliance documents page
  - Tracking (GTM, GA4, Clarity, Meta/LinkedIn pixels) + cookie consent
  - CRM (HubSpot free)
  - SEO blog plan
- **Blocker:** real sample photos and confirmed prices (from Phase 2).

### Phase 5 – Client Acquisition ⏳
- **Segments (priority order):** 1) café group owners (3–30 stores), 2) operations/procurement managers (chains, universities, caterers), 3) regional packaging distributors.
- **To do:** prospect list (20–30 named businesses), cold email and LinkedIn sequences, Sample Kit program, Google Ads test, SEO content, coffee trade media and events.

### Phase 6 – Client Onboarding ⏳
- **To do:** client brief template, artwork and proof process, pricing confirmation, service agreement (fees, payment stages, minimum fee), order form.

### Phase 7 – Procurement & Fulfillment ⏳
- **To do:**
  - Purchase order template
  - Supplier non-circumvention agreement
  - Trade Assurance payment
  - Third-party pre-shipment inspection (~$300)
  - Freight booking
  - US customs (ISF, bond, broker) / Canada broker
  - Weekly client updates

### Phase 8 – Financial Management ⏳
- **To do:**
  - Per-order P&L (product cost, freight, duties, other costs, selling price, commission, gross profit, net profit)
  - Invoice and payment records
  - Cash-flow plan (client 50/50 vs factory 30/70)
  - Receiving USD in Bangladesh: check Bangladesh Bank rules with an accountant

---

## 4. Standing rules for this project
- One phase at a time; the user approves before moving on (commands: START, NEXT, APPROVE, REVISE, REPEAT, SKIP, STOP, STATUS).
- Never fabricate suppliers, prices, reviews or statistics; label facts, estimates and assumptions.
- Never claim an email was sent, an order placed or a site published unless it actually was.
- Keep this tracker updated at every phase change.

## 5. File locations (this repository)
- Markdown sources: `docs/` (phases in `docs/phases/`, research in `docs/research/`)
- Shareable files: `deliverables/phase2/`, `deliverables/phase3/`, `deliverables/research/`
- Brand: `brand/logos/`, `brand/design-system/tokens.json`, `brand/brand-sheet.png`, `brand/homepage-blueprint.png`
- Original working folder on the first PC: `D:\TechR Projects\Cup1 Business Operations\`
- claude.ai project "Cup1 Business Operations" holds copies under `claude/`
