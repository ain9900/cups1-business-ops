# Cups1 – Tracking & Audience Snapshot (memory for next session)

**Captured:** 2026-11-24 (Asia/Dhaka), read-only, by Claude from the owner's signed-in Chrome.
**Nothing was changed** in GA4, GTM or Google Ads during this capture.
**Read with:** `CUPS1-STATUS-2026-11-24.md` (handoff) · Audience plan doc: https://claude.ai/artifact/4HDBEU5fJavbftEkkMADoD (proposal, not started)

## IDs at a glance
| Item | ID |
|---|---|
| Website | https://cups1.com (WordPress 7.1.5, Elementor 4.4.1, WooCommerce 11.3.1, Hostinger; plugin cups1-elementor 1.8.46 live) |
| GTM | GTM-W4F8PCCM · account 6407569107 (Marketian) · container 288489610 · **v10 live** |
| GA4 | account 417363282 · property 565678418 · stream "Cups1 Production Web" · G-VCXTFZGR23 |
| Google Ads (boss) | 104-616-6584 · tag AW-660762155 (remarketing) |
| Google Ads (Marketian) | 993-633-5611 |
| Meta Pixel | dataset 2584915388999993 (Arif TechR Business Portfolio) |
| Consent | WPConsent; GA4 on Statistics consent, Meta + Google Ads on Marketing consent; Google consent defaults all denied |
| GTM admin login | arif.techr@gmail.com |

## GA4 audiences (13) — all created Nov 24, 2026, all "< 10 users"
| Audience | Definition (GA4 description) |
|---|---|
| Cups1 \| Engaged visitors \| 30 days | Key CTA click or commercial-page engagement (excludes inquiry starts, cart, checkout, conversions) |
| Cups1 \| Inquiry started without completion \| 14 days | Began an inquiry; excludes completed inquiries and purchases |
| Cups1 \| Google paid visitors \| 30 days | Google paid traffic (google / cpc); campaign entry audience |
| Cups1 \| Funnel 1 - Product interest \| 30 days | Product viewers without cart, checkout, inquiry or purchase |
| Cups1 \| Funnel 2 - Cart without checkout \| 14 days | Cart additions without checkout, inquiry or purchase |
| Cups1 \| Funnel 3 - Checkout without conversion \| 7 days | Checkout starts without completed inquiry or purchase |
| Cups1 \| Funnel 4 - Converted \| 90 days | Completed quote, sample, contact, customization or purchase |
| Cups1 \| Product viewers \| 30 days | Viewed a product detail page |
| Cups1 \| Sample requests \| 60 days | Completed a sample request |
| Cups1 \| B2B leads \| 90 days | Submitted a quote, pricing or customization inquiry |
| Cups1 \| Cart intent \| 30 days | Successfully added packaging to cart |
| All Users | Google default |
| Purchasers | Google default (540 days) |

## GA4 key events
| Event | Stream data (last 28 days) |
|---|---|
| generate_lead | Active (Cups1 Production Web) |
| purchase | No data (purchase tracking staged, not published) |
| qualify_lead | No data |
| close_convert_lead | No data |

Note: `sample_request` and `contact_request` are sent to GA4 but are **not** key events.

## GTM v10 — container contents (21 tags · 16 triggers · 2 settings · 18 user variables)
Version history: 1 Empty → 2 GA4 foundation → 3 GA4 via WPConsent → 4 GA4 lead and cart measurement → 5 GA4 ecommerce funnel → 6 Meta Pixel consent-gated activation → 7 Product view variation IDs → 8 WooCommerce catalog event enrichment → 9 CTA scroll and inquiry engagement → **10 Google Ads website remarketing 104-616-6584** (published 2026-11-24 17:46). All by arif.techr@gmail.com.

### Tags
| Tag | Type | Firing trigger |
|---|---|---|
| GA4 - Cups1 Production Web | Google tag (GA4) | CE - Cups1 Analytics Consent Ready |
| GA4 - view_item | GA4 Event | CE - cups1_product_view |
| GA4 - add_to_cart | GA4 Event | CE - Successful cart addition |
| GA4 - view_cart | GA4 Event | CE - cups1_cart_view |
| GA4 - begin_checkout | GA4 Event | CE - cups1_checkout_start |
| GA4 - generate_lead | GA4 Event | CE - Completed quote, pricing or customization |
| GA4 - sample_request | GA4 Event | CE - Completed sample request |
| GA4 - contact_request | GA4 Event | CE - Completed general contact |
| GA4 - Cups1 engagement events | GA4 Event (cta_click, scroll_depth, content_engaged, inquiry_start) | CE - Cups1 engagement event |
| Cups1 - Engagement measurement | Custom HTML | CE - Statistics consent for Cups1 engagement |
| Cups1 - Enrich successful cart addition | Custom HTML | CE - Cups1 raw cart addition |
| Cups1 - Public WooCommerce catalog data | Custom HTML | CE - Cups1 catalog data initialization |
| Cups1 - WooCommerce funnel events | Custom HTML | CE - Statistics consent on WooCommerce funnel |
| Meta Pixel - PageView | Custom HTML | CE - WPConsent marketing granted |
| Meta Pixel - Revoke consent | Custom HTML | CE - WPConsent marketing denied |
| Meta Pixel - AddToCart | Custom HTML | CE - Successful cart addition |
| Meta Pixel - Lead | Custom HTML | CE - Completed quote, pricing or customization |
| Meta Pixel - SampleRequest | Custom HTML | CE - Completed sample request |
| Meta Pixel - Contact | Custom HTML | CE - Completed general contact |
| Google Ads AW-660762155 | Google Ads (destination) | CE - Cups1 public pages with Marketing consent |
| Google Ads - Cups1 website remarketing - 104-616-6584 | Google Ads Remarketing | CE - Cups1 public pages with Marketing consent |

(Meta ViewContent/ViewCategory are sent from the catalog/funnel Custom HTML tags, per the handoff.)

### Triggers (all Custom Event, Page Hostname = cups1.com unless noted)
| Trigger | Extra condition |
|---|---|
| CE - Completed quote, pricing or customization | lead_type matches ^(quote\|pricing\|customize)$ |
| CE - Completed sample request | lead_type = sample |
| CE - Completed general contact | lead_type = contact |
| CE - Cups1 Analytics Consent Ready | — |
| CE - Cups1 catalog data initialization | — |
| CE - Cups1 engagement event | — |
| CE - Cups1 raw cart addition | — |
| CE - Successful cart addition | — |
| CE - cups1_product_view / cups1_cart_view / cups1_checkout_start | — (3 triggers) |
| CE - Statistics consent for Cups1 engagement | — |
| CE - Statistics consent on WooCommerce funnel | Page Path matches ^/(?:product/[^/]+\|cart\|checkout)/?$ |
| CE - WPConsent marketing granted / denied | Marketing Consent = true / false |
| CE - Cups1 public pages with Marketing consent | Marketing Consent = true AND Page URL matches an allowlist of public cups1.com paths (products, for-business, industries, request-a-quote, request-a-sample, contact(-sales), configure-packaging, custom-printing, how-it-works, documents, faq, resources, help-center, about, for-distributors, cart, product/…, product-category/…) with only safe query keys (gclid, gbraid, wbraid, dclid, fbclid, gad_*, utm_*, collection, packaging_product, packaging_size, intent) AND Referrer is a public cups1 URL, empty, or a bare origin |

### Variables
CONST - Meta Pixel ID · DLV - currency, value, items, items.0.item_id, items.0.quantity, lead_type, form_type, Marketing Consent, price_band, pricing_mode, product_category, engagement_action, engagement_depth, engagement_form_type, engagement_page_location, engagement_page_referrer, engagement_page_type · Built-ins: Event, Page Hostname, Page Path, Page URL, Referrer.

### Settings
Manage automatic event detection · Allow user-provided data capabilities.

## Gaps seen in this capture (for next session — not acted on)
1. Every GA4 audience is < 10 users: they need traffic before Google Ads can use them (100 active users / 30 days).
2. `sample_request` and `contact_request` are not GA4 key events — decide whether to mark them before importing conversions to Ads 104-616-6584.
3. No Google Ads conversion tag in GTM (remarketing only); lead optimisation relies on GA4 `generate_lead` import.
4. Purchase tracking is still staged (plugin 1.8.47 + `cups1-gtm-purchase.json`), owner wants it unpublished.
5. Audience plan suggests adding "B2B page visitors, 60 days" — not created yet.
6. Meta Events Manager receipt still unverified; privacy policy and terms pages still 404.

## How to continue on another PC
1. `git pull` the repo (`ain9900/cup1-business-ops`) — this file lives in `03-marketing/cups1-tracking/`.
2. In the Claude project "Cups1 B2B", the same snapshot is at `03-marketing/tracking-audience-snapshot-2026-11-24.md`; status at `claude/PROJECT-STATUS.md`.
3. Start with the "Gaps" list above and the audience plan doc.
