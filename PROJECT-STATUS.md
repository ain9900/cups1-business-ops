# Cup1 – Project Status

**Last updated:** 2026-11-05 · **Read after** `DECISIONS.md`. Update this file whenever work moves, then commit and push.
Legend: ✅ done · 🟡 in progress · ⏳ not started · ⛔ blocked

## Overview
| Area | Expert | Status | Next step |
|---|---|---|---|
| Business model | Business | ✅ Reseller + commission model set; owner numbers (margin, deposit) open | Owner decides open points in `DECISIONS.md` |
| Product research | Business | ✅ Custom-printed paper food packaging; lead SKU 12oz DW hot cup; launch range of 6 | — |
| Supplier sourcing | Business | 🟡 Desk research done (2 rounds). **No RFQ sent, no quotes, no samples** | Send RFQs |
| Branding | Marketing | 🟡 Strategy done, logo v1.2 + favicon + design system done | Owner's final Logo Palette pick → APPROVE |
| Competitor research | Marketing | ✅ 9 competitors + website design teardown | Sourcing-agent competitor audit (optional) |
| Website | Web Developer | ⏳ Plan + 12-section homepage blueprint ready | Propose platform/stack (needs approval) |
| Client acquisition | Marketing | ⏳ Segments defined | Prospect list (20–30), email/LinkedIn sequences, Sample Kit program |
| Client onboarding | Business | ⏳ | Client brief template, artwork/proof process, service agreement |
| Procurement & fulfillment | Business | ⏳ | PO template, non-circumvention agreement, inspection, forwarder, US/CA customs broker |
| Finance | Business | ⏳ Cost & margin model exists (`deliverables/phase2/Cup1_Phase2_Sourcing_Model.xlsx`) | Per-order P&L, cash-flow plan, USD receipt rules (accountant) |
| Policies | Business | ⏳ `01-business/policies/` empty | Terms of sale, payment, shipping, claims (lawyer review) |

## Sourcing – details
- **Primary:** Zhejiang Sowinpak (China + Vietnam + Indonesia plants; BRC/BRCGS, BPI, FSC, PEFC, ISO 22000). Audit: `01-business/supplier-audit-sowinpak.md`.
- **USA/Canada pack:** `01-business/usa-canada-supplier-sourcing-pack.md` (tariffs, landed cost, RFQ, verification checklist, sample request).
  - US duty: China ≈ 37.5%, Vietnam ≈ 12.5%. Canada: CBSA AD/CVD case on Chinese cups, preliminary decision due **2026-11-16**.
  - Placeholder economics (FOB $0.06, 100k cups): landed USA ≈ $0.11 (VN) – $0.12 (CN)/cup; client price at 35% GM ≈ $0.17–0.19.
  - Freight reference: Drewry WCI Shanghai–LA $7,514 per 40ft (2026-10-30).
- **Other shortlists:** `01-business/supplier-comparison-paper-cups.md` (Jeafer, Hengxin + backups), `01-business/top5-alibaba-suppliers.md` (adds Dayu, Sunkea). Master list: `01-business/suppliers-sourcing-links.md`.
- **Open tasks:**
  - [ ] Send RFQ to Sowinpak (ask: 12oz DW at the **Vietnam** plant + price), Jeafer, Hengxin, Haining Xinhua, Wenzhou Liping (+ Dayu, Sunkea if approved)
  - [ ] Ask all for BRCGS, FSC, FDA 21 CFR 176.170, EU 10/2011, LFGB reports + PFAS-free declaration
  - [ ] Check the CBSA decision on 2026-11-17 and update the Canada numbers
  - [ ] Forwarder quote (LCL to LA and Vancouver); US customs broker to confirm duty rates
  - [ ] Find a second **Vietnam** paper-cup factory
  - [ ] Samples from the top 2, then a Trade Assurance trial order
  - [ ] Verify SGS / TÜV report numbers on Alibaba

## Branding – details
- Strategy: `03-marketing/brand-strategy.md` · decisions: `03-marketing/brand-decisions.md` · PDF: `deliverables/phase3/`.
- Logo v1.2 files: `brand/logo/` (svg, png, favicon set, guidelines PDF, mockups). Logo Palette (all variants, fonts F1–F6, suggestions S1–S5): `brand/logo/palette/Cup1_Logo_Palette.html`.
- Colours: Harbor Teal #1F4E5A, Ink #1C2B2E, Kraft #B88A5A, Paper #F7F3EC, Kraft Tint #EDE5D8, Verified #2E7D4F (compliance only). Font: Inter. Tokens: `brand/design-system/tokens.json`.
- **Open:** [ ] owner's Logo Palette pick · [ ] if a new font is chosen, outline the final SVGs · [ ] trademark search · [ ] ® only after registration.

## Website – inputs ready
`02-website/website-features-plan.md` (requirement/quote system, admin, tracking stages) + `02-website/website-design-teardown.md` (12-section homepage + product page blueprint, `brand/homepage-blueprint.png`).
To do: platform, domain, delivered-quote form (product, size, qty, city, logo upload), Sample Kit request, compliance documents page,
tracking (GTM, GA4, Clarity, Meta/LinkedIn pixels) + cookie consent, CRM (HubSpot free), SEO blog plan.
**Blocker:** real sample photos and confirmed prices (from sourcing).

## Marketing – inputs ready
Competitors: `03-marketing/competitor-intelligence-report.md` (YourBrandCafe, LogoCup, CupPrint USA, noissue, Good Start Packaging, KimEcopak, Karat, YOON, Sowinpak direct).
Findings: free samples are standard; MOQ, lead time and price shown up front; heavy tracking. **Price alert:** noissue "from $0.10" (MOQ 1,000).
Segments (priority): 1) café group owners (3–30 stores) 2) operations/procurement managers 3) regional distributors.

## claude.ai links (private to the owner's account unless shared)
- Phase 2 sourcing doc: https://claude.ai/artifact/XzLCMWbwm8tUBrUW4ACq6U
- Brand doc: https://claude.ai/artifact/AowAYBzKhSdbusoSipzGak · Design System: https://claude.ai/artifact/JrMk8352xRmnsqFWVvjf4Q
- Logo Palette: https://claude.ai/artifact/RpmU4DEYZAvoMoecMwDB2Q
- Competitor report: https://claude.ai/artifact/RU2sFTyv3E19yNcRp26ZUc · Website teardown: https://claude.ai/artifact/3zFrmKpKpSscTAD3NPSgQ7
