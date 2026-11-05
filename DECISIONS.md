# Decisions Log

All experts read this before starting work. Start with **Current decisions** (what is true now),
then **Open decisions** (waiting for the owner). The full history is in the **Decision log** below.

## Current decisions (as of 2026-11-05)
| Topic | Decision |
|---|---|
| Project | **One project, one Git repo** (`ain9900/cup1-business-ops`), used from the home PC and the office PC. `CLAUDE.md` is the shared instruction file |
| Business type | **B2B sourcing company, reseller model (Model B)**: buyers send requirements, Cup1 sources from checked Asian suppliers and sells under the Cup1 name, earning a margin |
| Extra revenue | Sourcing commission for distributors who import themselves (3–10% of FOB, minimum ≈ US$1,000/order) + service fees (design, Sample Kit, QC, retainers) |
| Market | Worldwide B2B. **Launch market: USA & Canada** |
| Trade terms | USA & Canada: delivered (DDP) price. Other regions: FOB / CIF first |
| Brand | **Cup1** is the brand. Tagline "Your brand. Every cup. Fully documented." Logo v1.2 chosen (teal "Cup" + cup-1); final font/colour pick from the Logo Palette pending |
| Positioning | Eco + compliant, proof-led: "if we can't attach the document, we don't make the claim" |
| Products | Disposable paper food packaging (cups, lids, bowls, boxes, plates), mostly custom-printed. Lead SKU: 12oz double-wall hot cup |
| Supplier visibility | Hidden: buyers deal only with Cup1 |
| Shipping | Factory-direct to buyer; no Cup1 warehouse at start |
| Factory payments | Only via Alibaba Trade Assurance (first orders); never pay factory before the buyer pays us |
| Supplier shortlist | **Sowinpak** (primary; Vietnam plant for USA/Canada). China-origin RFQ list: Xiamen Jeafer, Hefei Hengxin. Benchmarks/backups: Haining Xinhua, Wenzhou Liping, Dongyuan Haoyuan, Thuan Loi (VN). All need samples + trial before approval |
| Way of working | **Three experts** (Business, Web Developer, Marketing). The 6-role / 8-phase approval-gate system of the old repo is retired |
| Website core | "Submit your requirement" / delivered-quote form + Sample Kit request + compliance documents page + order tracking (not a big online shop) |

## Open decisions (owner)
- [ ] **Logo:** final pick from the Logo Palette (keep v1.2 font or F2/F3; teal or S1 navy+orange), then APPROVE
- [ ] Target margin % (placeholder model uses 35% gross) · buyer deposit % (repo model: 50/50) · sample policy · minimum order value
- [ ] Company registration country and bank (notes assume Bangladesh base: confirm USD receipt rules with an accountant), budget
- [ ] Priority regions after USA & Canada (e.g. Middle East, Europe)
- [ ] Add Quanzhou Dayu + Shanghai Sunkea to the RFQ list? (`01-business/top5-alibaba-suppliers.md`)
- [ ] Show prices online? (suggested: "from" prices, e.g. "from 30,000 cups · ~35 days + shipping"; final price by quote)
- [ ] Website platform / tech stack (Web Developer to propose) and domain
- [ ] Languages at launch (English first; Arabic later if Middle East is chosen)
- [ ] Professional trademark search before registering "Cup1"

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
