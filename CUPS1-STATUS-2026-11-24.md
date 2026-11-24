# Cups1 website and marketing handoff

**Status as of 2026-11-24, Asia/Dhaka**  
**Production** · [cups1.com](https://cups1.com/) · WordPress, Elementor and WooCommerce  
**Review scope** · The public site, checkout, SEO, consent, analytics, advertising and catalog work. This handoff records the latest verified state for these areas and distinguishes it from the 2026-11-23 audit baseline.

## Current state

| Area | Status | Evidence or next check |
| --- | --- | --- |
| Public site | Homepage, WordPress sitemap and cookie policy returned HTTP 200 during the handoff check. | [Homepage](https://cups1.com/) · [XML sitemap](https://cups1.com/wp-sitemap.xml) · [Cookie policy](https://cups1.com/cookie-policy/) |
| Tag Manager | Production container **GTM-W4F8PCCM**, account **6407569107**, container **288489610**. **Version 10** is live. Public GTM JavaScript returned version 10 with the GA4, Meta and Google Ads destination IDs present. | [Live GTM version](https://tagmanager.google.com/#/versions/accounts/6407569107/containers/288489610/versions/10) |
| Google Analytics | **Cups1 \| cups1.com**, property **565678418**, web measurement ID **G-VCXTFZGR23**. Search Console and both Google Ads accounts are linked. | [GA4](https://analytics.google.com/analytics/web/#/a417363282p565678418/reports/intelligenthome) · [Google Ads links](https://analytics.google.com/analytics/web/#/a417363282p565678418/admin/integrations/google-ads) |
| Boss’s Google Ads account | **104-616-6584**. Admin approval completed. GA4 shows personalized advertising enabled and Google Ads shows **Import Google Analytics audiences: On**. App and web metrics import was **Off** on the Ads side. | [GA4 connection in the Ads account](https://ads.google.com/aw/productlinks/analyticsappweb?ocid=413659830) |
| Marketian Google Ads | **993-633-5611**, linked with personalized advertising and auto-tagging. The GA4 `generate_lead` action was imported as **Secondary**. | [Marketian](https://ads.google.com/aw/overview?ocid=8675438802) |
| Direct Google Ads remarketing | **AW-660762155** routes eligible Cups1 visits directly to **104-616-6584**. Chrome Tag Assistant recorded a remarketing hit after Marketing consent and zero requests to this destination before consent. | [Google Ads Data Manager](https://ads.google.com/aw/datamanager?ocid=413659830) |
| Meta Pixel | **Cups1 Website**, dataset **2584915388999993**, in the **Arif TechR** Business Portfolio. Chrome confirmed browser events. Meta Events Manager showed no activity at the last dashboard check, so platform receipt still needs verification. | [Meta Test Events](https://eventsmanager.facebook.com/events_manager2/list/dataset/2584915388999993/test_events?business_id=1016134031528891) |
| Checkout and purchase | Cash on Delivery was enabled and selected in the tested checkout. Paid GA4 purchase tracking is staged. Meta Purchase and checkout-page browser events are pending. | [Staged GA4 purchase workspace](https://tagmanager.google.com/#/container/accounts/6407569107/containers/288489610/workspaces/7) |
| CTX Feed and catalog ads | Future work. Catalog ID mapping is defined and one priced variant was verified across GA4 and Meta browser events. | [Feed mapping below](#ctx-feed-and-catalog-ads) |

GTM is managed under **arif.techr@gmail.com**, the sole administrator confirmed during setup at the owner’s direction. The same login has **Standard** access to Ads account **104-616-6584**. For browser troubleshooting, use the correct Google account in each product. The tag routes by destination ID even when GTM and Google Ads use different logins.

## Consent, event tracking and QA

- WPConsent applies denied defaults. **Statistics** enables Analytics. **Marketing** enables the Meta Pixel and direct Google Ads remarketing. The notice and gear are at the lower left, and the gear reopens Cookie Preferences. Tag Assistant verified denied defaults, Statistics-only consent, all four Google consent signals granted after full consent, and persistence after reload.
- The Meta Ads Data Advisor warning was reproduced with Marketing disabled. The panel detected the correct Meta Pixel and an active `PageView` after Marketing was enabled. This verified browser firing. Meta’s separate Test Events and Overview checks still showed no activity for the tested date.
- The native Google Ads destination and remarketing tags fire on the WPConsent event after Marketing permission. Both require `ad_storage`, `ad_user_data` and `ad_personalization`. The trigger allows approved public Cups1 pages and safe referrers and excludes private routes and query keys. The tag uses no conversion label or custom user ID. Test cases checked that private inquiry references, checkout/order links and admin pages fail the public URL rule.
- GA4 automatic form interactions are off. Accepted submissions drive conversion events. The engagement tags send approved action labels, public page context and thresholds. Form values, full referrer paths, URL fragments and query strings are omitted from those engagement payloads. GA4 stream redaction also covers emails and specified URL keys, including inquiry `reference` and order `key`.

| Action | GA4 | Meta browser | Latest evidence |
| --- | --- | --- | --- |
| Eligible page visit | `page_view` | `PageView` | GA4 Tag Assistant and Meta Ads Data Advisor. |
| Catalog collection visit | Standard page view | `ViewCategory` | Chrome recorded the Cups collection event. |
| Product detail visit | `view_item` | `ViewContent` | Chrome verified variant, category and actual case price on the priced test product. |
| Successful cart addition | `add_to_cart` | `AddToCart` | Chrome verified the same variant, category, case quantity, currency and value in both destinations. |
| Cart page and checkout start | `view_cart`, `begin_checkout` | — | Tag Assistant verified GA4 payloads and a consistent cart and checkout total. |
| Accepted quote, pricing or customization inquiry | `generate_lead` | `Lead` | Private WordPress record, GA4 Realtime and Meta browser request. |
| Accepted sample or contact request | `sample_request`, `contact_request` | `SampleRequest`, `Contact` | Private WordPress records, GA4 Realtime and Meta browser requests. |
| Key button or link click | `cta_click` | — | Tag Assistant verified the quote CTA. Other allowlisted actions include sample, contact, catalog and cart links. |
| Scroll and commercial content engagement | `scroll_depth`, `content_engaged` | — | 25%, 50%, 75% and 90% once per page view. A 75% scroll on a product, catalog, business or customization page qualifies as content engagement. |
| First inquiry interaction | `inquiry_start` | — | Tag Assistant verified the first real edit, once per form per page load. QA stopped before submission in this test. |
| Paid order | `purchase` staged | `Purchase` pending | Production GTM v10 has no paid purchase trigger. |

The priced QA sample was **Double-Wall Paper Cups, 8 oz**, WooCommerce variation **182**, SKU **C1-DW-8-OZ**, category **Cups**, secondary category **Beverages**, at **USD 150 per case of 100**. The second sample was the quote-only **Kraft Food & Salad Bowls**, group **124**, category **Food and takeaway**, with `quote_only` and no numeric price. GA4 event-scoped dimensions include `lead_type`, `form_type`, `product_category`, `pricing_mode`, `price_band`, `cta_action` and `page_type`.

Approved live inquiry QA used synthetic details. WordPress accepted one quote, two separate sample submissions and one contact. All three GA4 event types appeared in Realtime, and Chrome captured the corresponding Meta requests. The quote’s Meta request omitted the synthetic name, email and private inquiry reference. Empty quote validation blocked submission. Local fixtures exercised the popup’s first step and rejected requests. The test cart was emptied and no order or payment was placed.

## Google Ads audiences

The latest check confirmed the following segments inside **104-616-6584**, after the GA4 link moved to **Completed**. **Engaged visitors** and **Inquiry started without completion** both showed **0 eligible users** and **Too small to serve**. Other checked Cups1 funnel lists had **0** and showed **Populating**. The segments are available in Audience Manager, and no campaign launch or audience assignment was part of this work. [Audience Manager for 104-616-6584](https://ads.google.com/aw/audiences/management?ocid=413659830)

| Audience | Membership | Inclusion or exclusion |
| --- | --- | --- |
| Engaged visitors | 30 days | Key CTA click or commercial-page engagement. Temporarily excludes inquiry starts, cart adds, checkout and conversions. |
| Inquiry started without completion | 14 days | Inquiry form start. Temporarily excludes completed inquiries and purchases. |
| Google paid visitors | 30 days | Session source and medium `google / cpc`. |
| Funnel 1 · Product interest | 30 days | Product detail interest with exclusions for cart, checkout and converters. |
| Funnel 2 · Cart without checkout | 14 days | Successful cart addition with checkout and converted-user exclusions. |
| Funnel 3 · Checkout without conversion | 7 days | Checkout start with converted-user exclusions. |
| Funnel 4 · Converted | 90 days | Completed quote, sample, contact, customization or purchase. Use for suppression when appropriate. |
| Additional Cups1 lists | 30–90 days | Product viewers, cart intent, B2B leads and sample requests. Google also creates All Users and Purchasers lists. |

Import and verify `generate_lead` separately if **104-616-6584** will optimize for Cups1 leads. That account’s campaign conversion configuration was outside the verified work. For any new site-specific list created from the direct Ads tag rather than GA4, use a Cups1 URL rule, for example `https://cups1.com/` as a prefix. This Ads account also contains another website’s data.

## SEO, checkout and site issues to review

- **Indexing and crawl.** The public sitemap responds and Search Console is linked to GA4. The 2026-11-23 audit counted 78 sitemap URLs and 18 extra URLs. A saved Search Console screenshot from a 2026-11-19 read showed zero discovered pages at that time. Check current **Pages**, **Sitemaps**, Live URL Inspection and Google-selected canonicals before treating any URL as indexed. Check the home page, catalog, Cups category and the Double-Wall product page first. [Audit and evidence](02-website/audit-2026-11-23/report.md)
- **Template SEO.** The prior audit found 42 product pages with base canonicals and missing descriptions and JSON-LD. The catalog and eight category pages lacked canonicals and descriptions. Twenty-five page-sitemap responses had duplicate title elements. Recheck filtered and sorted catalog URLs, transactional and author sitemap entries, and the duplicate crawlable `v2.cups1.com` site. Decide whether `v2` is staging or a retired site before planning changes. [URL inventory](02-website/audit-2026-11-23/url-inventory.md)
- **Checkout.** Cash on Delivery resolves the earlier missing-method symptom for the tested cart. Verify approved selling regions, shipping, tax, case units and order emails before relying on checkout for paid acquisition. Confirm the chosen definition of payment received for COD. WooCommerce’s initial COD `processing` state is insufficient proof of payment.
- **Buyer policies and inquiry delivery.** The tracking cookie policy is public. The usual privacy-policy URL returned 404 again during handoff. The previous audit also found missing public terms and returns paths. Verify owner-approved privacy, sales, returns and delivery content, policy links on forms and checkout, inquiry mailbox or CRM delivery, spam handling and file uploads. WordPress inquiry storage was verified.
- **Availability, mobile and performance.** Some repeated QA navigation encountered HTTP 429, and a generic scripted client received HTTP 403 during handoff while a normal HTTPS check returned 200 for the public homepage and sitemap. Reproduce from a standard signed-out browser and run Search Console Live URL Inspection before drawing conclusions about crawler access. The audit flagged duplicated logo payloads, informative image alternatives and mobile accessibility checks.
- **GTM diagnostics.** One-admin health advice can remain by owner choice. Earlier regional consent diagnostic figures were aggregate dashboard data. Live Tag Assistant verified consent behavior. Recheck the current diagnostics before assigning a severity.

## CTX Feed and catalog ads

Generate a review feed from owner-approved, sellable WooCommerce items. Use the exact WooCommerce **variation ID** for each feed `id`, the WooCommerce **parent ID** for `item_group_id`, and keep the SKU separate. For a sellable simple product, use its WooCommerce product ID as `id`. Confirm Meta `content_ids` matches the imported ID exactly, using **182** as a positive test. Exclude quote-only items such as group **124** from a priced feed.

Before activating catalog campaigns, match current case price, currency, case quantity, stock, image, variant deep link and shipping eligibility across WooCommerce, feed and destination. Verify Meta Events Manager receipt and the catalog match rate. CTX Feed, a verified Meta or Google catalog connection, and Meta Conversions API are still open. [Feed implementation notes](02-website/audit-2026-11-23/marketing-implementation.md#configure-ctx-feed)

## Versioned files for Claude

The native GTM exports belong to **GTM-W4F8PCCM**. Start with the v10 export for a production comparison. Historical exports are reference and rollback snapshots. The staged purchase files are separate from production.

| File or version | Role |
| --- | --- |
| [Native GTM exports v2–v10](03-marketing/cups1-tracking/gtm-exports/) | Google Tag Manager originals for the setup, from GA4 foundation through production remarketing. |
| [Native GTM v10](03-marketing/cups1-tracking/gtm-exports/GTM-W4F8PCCM_v10.json) | Current production snapshot. |
| [Native GTM v9](03-marketing/cups1-tracking/gtm-exports/GTM-W4F8PCCM_v9.json) | Prior production baseline with CTA, scroll and inquiry-start tracking. |
| [Native GTM v8](03-marketing/cups1-tracking/gtm-exports/GTM-W4F8PCCM_v8.json) | WooCommerce catalog enrichment and priced versus quote-only product behavior. |
| [Tracking implementation files](03-marketing/cups1-tracking/) | Local GTM import drafts and JavaScript sources. The older tracking README reflects earlier checkpoints. This handoff records the later approved Ads link. |
| [Cups1 Elementor 1.8.45](02-website/cups1-elementor-1.8.45.zip) | Earlier release with inquiry and cart events. |
| [Cups1 Elementor 1.8.46](02-website/cups1-elementor-1.8.46.zip) | Latest verified installed WordPress addon release for this work. |
| [Cups1 Elementor 1.8.47](02-website/cups1-elementor-1.8.47.zip) and [GTM purchase draft](03-marketing/cups1-tracking/cups1-gtm-purchase.json) | Staged COD-aware paid-purchase setup. The owner asked to keep this unpublished. |
| [Public-site audit](02-website/audit-2026-11-23/report.md) and [Claude audit checklist](CLAUDE-WEBSITE-AUDIT-CHECKLIST.md) | Audit baseline and read-only review scope. |

## Suggested first review pass

1. Compare the live GTM container with the native v10 export. Retest consent, a priced product, a quote-only product and the inquiry start. Use the approved read-only audit scope for any fresh live test. Review the staged purchase code separately.
2. Verify Meta Events Manager receipt and check the preferred Ads account’s segment eligibility. Confirm the campaign’s intended lead conversion before changing any bidding settings.
3. Recheck Search Console indexing, site access, buyer policies and approved case and shipping data. Use those results to prioritize SEO fixes and qualify the first CTX Feed test items.
