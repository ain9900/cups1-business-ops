# Cup1 Website: Features & Page Plan

**Prepared by:** Web Developer · **Date:** 2026-10-31 (updated for the reseller sourcing model) · **Status:** DRAFT for owner approval
**Based on:** `01-business/business-model.md`, `03-marketing/competitor-website-audit.md`, `DECISIONS.md`
**Not decided yet:** tech stack, hosting, payment gateways. I will propose these separately and wait for your approval.

---

## Summary
Cup1 is a **sourcing reseller**, so the website's main job is to **collect buyer requirements and turn them into
orders**, not to run a big online shop. The core journey:

**Submit your requirement → Cup1 sends a quote → buyer approves & pays deposit → production updates →
inspection report → balance → shipping & documents → reorder.**

Product pages exist to show **what we can source** (with examples and "from" prices), and every page leads to
the requirement form. Supplier names are **never** shown.

---

## 1. Sitemap (MVP)

| Page | Purpose |
|---|---|
| **Home** | Hero: "We source it, check it and ship it" · how it works (4 steps) · product categories · why Cup1 (checked factories, inspection, one contact, worldwide) · proof (certificates, photos, testimonials when real) · big **Submit your requirement** button |
| **How It Works** | The order process in simple steps, timelines, payment terms (deposit/balance), what the buyer gets |
| **What We Source** (categories) | Paper cups, lids, bowls & soup cups, food boxes, plates & trays, eco options. Each page: examples, specs, MOQ guide, "from" price, **Request a quote** |
| **Custom Printing** | Print options, design templates, free artwork help, proof approval |
| **Quality & Inspection** | How we check factories, certificates available (BRCGS, FSC, food-contact tests), sample inspection report |
| **Shipping & Trade Terms** | Countries served, FOB / CIF / DDP explained, lead times, documents provided |
| **For Distributors** | Container-load sourcing, private label, regular supply |
| **Samples** | Request a sample pack (paid, credited on first order: TBD) |
| **Submit Requirement** | The main form (see section 2) |
| **Resources / Blog** | Buying guides (cup sizes, single vs double wall, compostable vs recyclable), import tips by region |
| **About · Contact · FAQ** | Who we are, real address, WhatsApp, email, business hours + time zone |
| **Policies** | Terms of Sale, Payment Terms, Shipping, Claims & Returns, Privacy (from `01-business/policies/`) |

## 2. Core feature: Requirement & Quote system

### Requirement form (buyer)
- Company name, contact, country, website/registration no. (for verification)
- **What do you need?** product type (dropdown) or "something else" (free text, so we can source other products later)
- Size / specs, quantity, plain or printed, **artwork upload**, reference photos/links
- Destination country & port/city, preferred trade term (FOB / CIF / DDP / not sure)
- Target date, target price (optional), "I use them / I resell them"
- Add several products in one request (**Requirement basket**)

### Admin (Cup1 team)
- Requirement inbox with statuses: New → Sourcing → Quoted → Accepted → Lost
- Per requirement: attach **supplier quotes (internal only)** → cost calculator (factory price + inspection +
  freight + fees + margin) → generate **Cup1 quote PDF** (no supplier name)
- Convert accepted quote to order → generate Proforma Invoice
- Sanctions/country screen before quoting

### Buyer account
- My requests, quotes (accept online), orders, invoices & documents (PI, CI, packing list, inspection report, B/L)
- **Reorder** button

### Order tracking stages (buyer view)
Quote accepted → Deposit received → Artwork approved → In production → Inspection passed →
Balance received → Shipped (B/L no., ETA) → Delivered

Email notification at each stage (WhatsApp later).

## 3. Other must-haves (MVP)
- [ ] Mobile-first, fast (Lighthouse 90+ mobile), HTTPS, security basics (validation, CSRF/XSS protection, role-based admin)
- [ ] File uploads stored safely (artwork, documents); no supplier info visible to buyers
- [ ] WhatsApp button + contact form on every page
- [ ] Catalogue / capability PDF download (lead capture)
- [ ] USD prices; always show currency + Incoterm
- [ ] English first; structure ready for Arabic (RTL)
- [ ] SEO: clean URLs, meta tags, sitemap, Organization + Product schema; cookie consent (GDPR)
- [ ] Analytics events: requirement submitted, sample requested, catalogue downloaded, WhatsApp click, quote accepted

## 4. Payments
- Orders: bank transfer (T/T) with proof upload; Wise/multi-currency account details on PI. **TBD with owner.**
- Samples & small payments: card/PayPal via a hosted gateway (no card data stored by us).
- Large buyers: L/C (offline process).

## 5. Later (phase 2+)
- Instant "from" price calculator for common items
- Live chat; multi-language; multi-currency
- Buyer credit terms; distributor portal
- Online cup design editor (start with templates + free design help instead)

## 6. Decisions needed from you
| # | Question | My suggestion |
|---|---|---|
| 1 | Show prices online? | "From" prices on common items; final price by quote |
| 2 | Tech stack | I will propose 2–3 options with monthly costs |
| 3 | Languages at launch | English, then Arabic |
| 4 | Payment methods for orders | T/T + Wise; card/PayPal for samples only |

## Notes for Marketing
- Pages that need copy: Home, How It Works, Quality & Inspection, Shipping & Trade Terms, For Distributors, buying guides.
- Tracking events above feed the KPI plan (cost per requirement submitted).
