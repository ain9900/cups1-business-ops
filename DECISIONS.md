# Decisions Log

All experts read this before starting work. Start with **Current decisions** (what is true now),
then **Open decisions** (waiting for the owner). The full history is in the **Decision log** below.

## Current decisions (as of 2026-11-06)
| Topic | Decision |
|---|---|
| Project | **One project, one Git repo** (`ain9900/cup1-business-ops`), used from the home PC and the office PC. `CLAUDE.md` is the shared instruction file |
| Business type | **FINAL (2026-11-06): asset-light B2B sourcing & trading company.** Main = trading company/reseller (product margin, sells under Cup1 name, supplier hidden); side = sourcing agent for distributors who import (commission); plus service fees. Not a manufacturer, warehouse distributor, marketplace or dropshipper. `01-business/business-model.md` |
| Extra revenue | Sourcing commission for distributors who import themselves (3–10% of FOB, minimum ≈ US$1,000/order) + service fees (design, Sample Kit, QC, retainers) |
| Market | Worldwide B2B. **Launch market: USA & Canada** |
| Trade terms | USA & Canada: delivered (DDP) price. Other regions: FOB / CIF first |
| Brand | **Brand name: Cups1 – FINAL (owner, 2026-11-06)** for brand, website and company; "Cup1" is the old working name. Final logo = Cups1 artwork. Tagline in logo: "Custom Branded Packaging for Cafés & Food Businesses"; positioning line "Your brand. Every cup. Fully documented.". **Final logo (owner, 2026-11-06):** owner-supplied artwork (navy line cup with orange steam, green leaf, orange swoosh, italic navy "Cups" + orange "1", tagline). Master + derived files (transparent, reversed, navbar, avatars, favicon set): `brand/logo/final/`. Colours: Navy #00213C, Orange #FE7702, Leaf #67A42D (tokens updated). Teal v1.2 and vector v2.0 superseded |
| Positioning | Eco + compliant, proof-led: "if we can't attach the document, we don't make the claim" |
| Products | Disposable paper food packaging (cups, lids, bowls, boxes, plates), mostly custom-printed. Lead SKU: 12oz double-wall hot cup |
| Supplier visibility | Hidden: buyers deal only with Cup1 |
| Shipping | Factory-direct to buyer; no Cup1 warehouse at start |
| Factory payments | Only via Alibaba Trade Assurance (first orders); never pay factory before the buyer pays us |
| Supplier shortlist | **Sowinpak** (primary; Vietnam plant for USA/Canada). China-origin RFQ list: Xiamen Jeafer, Hefei Hengxin. Benchmarks/backups: Haining Xinhua, Wenzhou Liping, Dongyuan Haoyuan, Thuan Loi (VN). All need samples + trial before approval |
| Way of working | **Three experts** (Business, Web Developer, Marketing). The 6-role / 8-phase approval-gate system of the old repo is retired |
| Website core | "Submit your requirement" / delivered-quote form + Sample Kit request + compliance documents page + order tracking (not a big online shop) |

## Open decisions (owner)
- [ ] Leaf in the logo implies an eco benefit: back it with documents on site/packaging (claims rule)
- [ ] Vector (SVG/AI/EPS) trace of the final logo for large print: designer
- [ ] Target margin % (placeholder model uses 35% gross) · buyer deposit % (repo model: 50/50) · sample policy · minimum order value
- [ ] Company registration country and bank (notes assume Bangladesh base: confirm USD receipt rules with an accountant), budget
- [ ] Priority regions after USA & Canada (e.g. Middle East, Europe)
- [ ] Add Quanzhou Dayu + Shanghai Sunkea to the RFQ list? (`01-business/top5-alibaba-suppliers.md`)
- [ ] Show prices online? (suggested: "from" prices, e.g. "from 30,000 cups · ~35 days + shipping"; final price by quote)
- [ ] **Website colour rule** (orange = buttons/prices only, paper background, navy headings) and homepage structure: `02-website/website-design-direction-v2.md`
- [ ] **Website launch features** from the competitor website report (8 "Launch" ideas; delivered-price example; quote reply time): `02-website/competitor-website-report.md`
- [ ] Website platform / tech stack (Web Developer to propose) and domain
- [ ] Languages at launch (English first; Arabic later if Middle East is chosen)
- [ ] Professional trademark search before registering "Cup1" / "Cups1" (note: Chinese cup maker **CupsPak**, cupspak.com, has a similar name)

## Decision log
| Date | Expert | Decision | Reason | Status |
|---|---|---|---|---|
| 2026-10-31 | — | Project set up with three experts (Business, Web Developer, Marketing) | Work in phases so each builds on the previous | Active |
| 2026-10-31 | Business Expert | Product focus: disposable paper food packaging; Sowinpak is the main supplier candidate (not yet approved) | Owner chose this supplier; large factory, short Alibaba history | Active |
| 2026-10-31 | Business Expert | Recommended a hybrid model (plain stock plus custom-print pre-orders), sea freight, and a Trade Assurance trial order first | Bulky, low-value goods; high MOQs | **Superseded** by reseller sourcing model. Trade Assurance trial still applies |
| 2026-10-31 | Owner | Market is worldwide B2B, not a single country | Owner's decision | Active (USA & Canada first, see 2026-11-05) |
| 2026-10-31 | Owner | Website/site name is "Cup1". Brand name will be decided later | Owner's decision | **Updated** 2026-11-05: Cup1 is also the brand |
| 2026-10-31 | Business Expert | Sowinpak desk audit: real factory, Intertek-verified, BRCGS + FSC; risk LOW–MEDIUM. Samples + Trade Assurance trial only. Contract and payment only with "Zhejiang Sowinpak Technology Co., Ltd." | `01-business/supplier-audit-sowinpak.md` | Active |
| 2026-10-31 | Business Expert | Shortlist Xiamen Jeafer and Hefei Hengxin to quote alongside Sowinpak; backups Anhui Chuangxin, Fujian Nanwang, Anqing Eternal | `01-business/supplier-comparison-paper-cups.md` | Active |
| 2026-10-31 | Marketing Expert | Competitor website audit of packaging sellers | `03-marketing/competitor-website-audit.md` | Reference only (see 2026-11-05 competitor intelligence) |
| 2026-10-31 | Web Developer | Draft site plan: requirement form + quote system, order tracking | `02-website/website-features-plan.md` | Waiting for approval |
| 2026-10-31 | Owner | **Business model: reseller under Cup1 name (Model B)**, supplier hidden | `01-business/business-model.md` | Active |
| 2026-10-31 | Owner | Expert instruction files updated for the worldwide reseller model | Project re-arrangement | Active |
| 2026-11-05 | Business Expert | Launch market USA & Canada; lead SKU 12oz DW custom-printed hot cup; launch range of 6 | Product research (former repo Phase 1) | Active |
| 2026-11-05 | Business Expert | Use Sowinpak's **Vietnam** plant for USA/Canada. US duty: China ≈ 37.5%, Vietnam ≈ 12.5%. Canada AD/CVD case on Chinese paper cups (preliminary decision due 2026-11-16): no China-origin cups for Canada until resolved | `01-business/usa-canada-supplier-sourcing-pack.md` | Active (re-verify rates before quoting) |
| 2026-11-05 | Business Expert | Revenue adds sourcing commission (minimum ≈ US$1,000/order) and service fees | `01-business/business-model.md` | Active |
| 2026-11-05 | Marketing Expert | Brand Cup1 itself as a B2B supplier; positioning eco + compliant; tagline "Your brand. Every cup. Fully documented."; claims rule | `03-marketing/brand-strategy.md`, `03-marketing/brand-decisions.md` | Active |
| 2026-11-05 | Owner | Logo v1.2 chosen (teal "Cup" + cup-1); Logo Palette built for the final font/colour pick | `brand/logo/`, `brand/logo/palette/` | Final pick pending |
| 2026-11-05 | Marketing Expert | Competitor intelligence (9 competitors) + website design teardown; price alert: noissue "from $0.10" | `03-marketing/competitor-intelligence-report.md`, `02-website/website-design-teardown.md` | Active |
| 2026-11-05 | Business Expert | Top 5 Alibaba suppliers for the full range: Sowinpak, Jeafer, Quanzhou Dayu (new), Hefei Hengxin, Shanghai Sunkea (new). Note: all except Sowinpak-Vietnam are China-origin, so mainly for non-US/Canada orders | `01-business/top5-alibaba-suppliers.md` | **Proposed**, owner to approve |
| 2026-11-05 | Owner | **Merged "Cup1 B2B" and "cup1-business-ops" into one project / one Git repo.** Worldwide with USA & Canada first; reseller + commission; three-expert system kept, phase gates retired; duplicates removed, superseded files in `archive/` | Use the same project and the same Claude instructions at home and at the office | Active |
| 2026-11-06 | Owner | **Logo pick: Sample 1 (navy cup, steam & leaf), spelled "Cups1".** Rebuilt as vector logo v2.0 with full, no-tagline, navbar and icon versions + favicon set | Owner's shortlist from the Logo Palette | Active (name scope to confirm) |
| 2026-11-06 | Owner | **Final logo = owner-supplied Cups1 artwork** (2 images). Owner also supplied the no-tagline master; Claude derived transparent/reversed/navbar versions, social avatars and the favicon set; design tokens switched to navy #00213C + orange #FE7702 | Owner: "These 2 are the final logo" | Active |
| 2026-11-06 | Web Developer + Marketing | Design direction v2: 4 closest-model sites added (PakFactory, Arka, Leeline, JingSourcing). Navy + orange is shared with Leeline, LogoCup and KimEcopak, so differentiate with paper ground, orange for action only, and a "see the paperwork" block. 12-section homepage proposed | `02-website/website-design-direction-v2.md` | **Proposed**, owner to approve |
| 2026-11-06 | Owner | **Business model finalized:** B2B sourcing & trading company = reseller (product margin, main) + sourcing agent (commission, distributors) + service fees | Owner: "finalize the business model" | Active (numbers still open) |
| 2026-11-06 | Marketing Expert | 15 professional competitors matched to the final model; closest: Kings Cups, Custom Disposables, SupplyCaddy, KimEcopak. New entrant Earth Brands ($10M from Cimpress). Name risk: CupsPak | `03-marketing/competitor-list-15.md` | Active |
| 2026-11-06 | Web Developer + Marketing | Competitor website report: 14 of 15 sites measured live + screenshots; scorecard; 4 gaps (documents, delivered-price breakdown, inspection report, tariffs/origin); 14 design ideas (8 for launch) | `02-website/competitor-website-report.md` | **Proposed**, owner to approve |
| 2026-11-06 | All experts | **Project briefing for owner/management**: everything researched and decided to date + 12 prioritized owner decisions + 30-day plan | `deliverables/Cups1_Project_Briefing.html` (offline) / `.md`; online: https://claude.ai/artifact/3UJnALKFoN6NH3tftGUuSB | Active |
| 2026-11-06 | Owner | **Brand name FINAL: Cups1** (with the owner-supplied Cups1 logo); replaces the working name "Cup1". Trademark search (USA/Canada) still needed before registering company/domain (CupsPak similar) | Owner: "Cups1 version is the final logo and brand model" | Active |
