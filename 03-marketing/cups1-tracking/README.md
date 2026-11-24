# Cups1 measurement setup

24 November 2026 · Production host cups1.com

[Tag Manager container draft](cups1-gtm-draft.json) · [Cups1 Elementor update with site events](../../02-website/cups1-elementor-1.8.45.zip)

## Campaign audiences and storefront funnel

GA4 has four Cups1 audiences. [Cups1 Audiences](https://analytics.google.com/analytics/web/#/a417363282p565678418/admin/audiences/hub)

| Audience | Membership | Rule |
| --- | --- | --- |
| Product viewers | 30 days | Product detail path matches `^/product/[^/]+/?$`. |
| Cart intent | 30 days | `add_to_cart`, with a temporary `purchase` exclusion. |
| B2B leads | 90 days | `generate_lead`. |
| Sample requests | 60 days | `sample_request`. |

The Cups1 property is linked to Marketian Google Ads **993-633-5611** with personalized advertising and auto-tagging enabled. Embedded Google Ads access to edit Analytics is off. The `generate_lead` key event was imported as a **Secondary** Google Ads conversion.

| Campaign stage | Membership | Rule and use |
| --- | --- | --- |
| Google paid visitors | 30 days | Session source / medium `google / cpc`. Paid acquisition cohort. |
| Funnel 1 - Product interest | 30 days | Product-detail viewers. Excludes cart, checkout, and converted users. |
| Funnel 2 - Cart without checkout | 14 days | `add_to_cart`. Excludes users who started checkout or converted. |
| Funnel 3 - Checkout without conversion | 7 days | `begin_checkout`. Excludes converted users. |
| Funnel 4 - Converted | 90 days | Completed B2B inquiries, sample requests, contacts, or purchases. Suppression list for acquisition. |

Stage exclusions are temporary, so returning buyers can requalify after the audience window. All five campaign audiences appeared in Marketian Audience Manager with zero eligible members and the status **Too small to serve** at setup. Use high-intent Search keywords for prospecting and Observation for audience reporting while lists build. Use separate audience-targeted retargeting once lists qualify. Keep the converted audience excluded from acquisition and retargeting. Use a campaign-specific completed-inquiry goal when a Cups1 campaign is ready for conversion bidding.

[Storefront GTM configuration](cups1-gtm-storefront.json) adds `view_item`, `view_cart`, and `begin_checkout` in [GTM version 5](https://tagmanager.google.com/#/versions/accounts/6407569107/containers/288489610/versions/5). All three require Statistics consent. Product views use the WooCommerce variation ID when the page has selected a variation and the product ID otherwise. Cart and checkout extract only item IDs, names, quantities, prices, currency, and subtotal from WooCommerce. Chrome Tag Assistant verified all three GA4 hits. The checkout hit included one case of variation 182 at USD 150. The test cart was emptied. Cash on Delivery was subsequently enabled and verified at checkout.

## Accounts and installation

1. Production uses GTM **GTM-W4F8PCCM** and GA4 web stream **G-VCXTFZGR23**, with Search Console already linked. Tag Assistant confirmed a Page View and an `add_to_cart` hit after Statistics consent. The cart hit showed one case of variation 182 at USD 150. A denied cart action sent no hit. The test item was removed afterward. Both event names also appeared in GA4 Realtime.
2. WPConsent sends **wpconsent_consent_processed** after reading or saving consent. Statistics enables Analytics, and Marketing is the choice for Meta Pixel. The initial notice is in the bottom-left corner. The lower-left gear reopens Cookie Preferences.
3. The **Cups1 Website** Meta dataset under Arif TechR is **2584915388999993**. The six Meta tags went live in GTM version 6 after the owner approved the activation and the [Cookie Policy](https://cups1.com/cookie-policy/) was published. The Cookie Preferences panel links to this policy. Chrome Preview previously showed PageView and AddToCart requests under Marketing consent, and a withdrawal/reload showed zero Meta resources. Verify post-launch receipt in Events Manager.
4. The Meta base tag permits Cups1's public quote and collection URL parameters and excludes private reference URLs and account, checkout, and admin routes. It sends `ViewContent` for an individual product and `ViewCategory` for catalog browsing. The revoke tag calls the Pixel's revoke command only if this Pixel already loaded, and the base tag can restore permission on the same page.
5. GA4 uses accepted submissions and successful cart actions as its conversion sources. Stream-level automatic form interactions are off. Email redaction is on. Seven URL keys are configured for redaction, including the private inquiry `reference` and WooCommerce order `key`. A synthetic URL check confirmed both values were masked and `utm_source` was retained.

[Google container installation](https://support.google.com/tagmanager/answer/14847097) · [Container import](https://support.google.com/tagmanager/answer/6106997) · [Search Console link](https://support.google.com/analytics/answer/10737381) · [Tag Manager consent settings](https://support.google.com/tagmanager/answer/10718549)

## Events in the draft

| Website action | GA4 | Meta Pixel | Verification |
| --- | --- | --- | --- |
| Eligible page load | page_view from the Google tag | PageView | One event per page for the respective consent choice. |
| Product detail view | view_item | ViewContent | Use the selected WooCommerce variation ID when available. |
| Catalog collection view | page_view | ViewCategory | Public collection slug or `all`. |
| Accepted quote, pricing, or customization inquiry | generate_lead | Lead | Final successful submission only. Mark generate_lead as a GA4 key event and use Lead for the Meta B2B campaign goal. |
| Accepted sample request | sample_request | SampleRequest | Keep available for reporting. |
| Accepted general contact | contact_request | Contact | Keep available for reporting. |
| Successful cart addition | add_to_cart | AddToCart | Check the actual WooCommerce variation ID, increment in case quantity, value and USD. |

GA4 has **lead_type** and **form_type** registered as event-scoped dimensions and **generate_lead** marked as a key event. Use the order success state and transaction ID when adding purchase tracking after checkout has been tested. Add product views and checkout milestones after their website events exist, then verify them on the live page. Map Meta catalog item IDs to the same WooCommerce variation ID that the draft sends in AddToCart. Keep catalog data sync under a single source, such as CTX Feed. If adding Conversions API, pair browser and server versions with matching event names and IDs and validate deduplication before enabling it.

[GA4 event specification](https://developers.google.com/analytics/devguides/collection/ga4/reference/events) · [Meta Pixel events](https://developers.facebook.com/docs/facebook-business-extension/fbe/guides/pixel-events)

## Publish checks

- Confirm the WordPress page loads one container and the intended GA4 stream and Pixel. In Tag Assistant, check that the container rejects the staging hostname and blocks analytics and advertising tags before their respective grants.
- Test accepted inquiries, a popup first step, failed and retried submissions, and one accepted cart addition. Verify destination events in GA4 DebugView and Meta Test Events. Sample and contact should remain distinct from the B2B lead event.
- Inspect outbound requests and verify they omit form fields, contact details, customer addresses, uploaded files, and private inquiry references. Check that raw query parameters outside the event payload are also handled.
- After publication, recheck Realtime on a real consented visit and record the GTM version and account IDs. Keep the previous WordPress addon and GTM version available for rollback.

The GTM merge was completed from Google's native export schema. Live QA used synthetic details with the owner's approval. The empty quote was blocked by browser validation. Accepted QA quote, sample, and contact submissions were recorded in WordPress. GA4 Realtime showed `generate_lead`, `sample_request`, and `contact_request`. Chrome observed corresponding Meta `Lead`, `SampleRequest`, and `Contact` browser requests. The quote's Meta request omitted the synthetic name, email, and private inquiry reference. Two QA sample records were accepted, matching two GA4 hits and two Meta requests. The two-step inquiry and rejected submissions were also exercised by local fixtures.

Meta Chrome checks captured `PageView`, `ViewContent`, `ViewCategory` for the Cups collection, and `AddToCart` for WooCommerce variation 182. The first product view used the parent ID before WooCommerce finished resolving the default selection. [GTM version 7](https://tagmanager.google.com/#/versions/accounts/6407569107/containers/288489610/versions/7) matches the selected attributes against WooCommerce's variations and uses a Meta product-group event when the selection is ambiguous. Chrome Preview verified variation 182 in both Meta `ViewContent` and GA4 `view_item` before publication. Meta Events Manager receipt remained unconfirmed at the end of QA. Checkout and purchase URLs are excluded from Meta browser tracking.

## Cash on Delivery and paid purchases

WooCommerce Cash on Delivery is enabled and was selected by default on a live checkout with a test item. The test item was removed and checkout was left before placing an order. The [native purchase workspace archive](gtm-exports/GTM-W4F8PCCM_workspace7_paid-purchase_UNPUBLISHED.json) preserves all ten unpublished changes from former GTM workspace #7. The draft uses a paid WooCommerce order ID for GA4 deduplication and excludes the private order key from the event parameters. The COD-specific addon release 1.8.47 suppresses processing-stage COD orders and is staged locally. The GA4 purchase tag is unpublished. Meta Purchase awaits a separate design for paid confirmation without exposing order-received URL tokens.

## Container diagnostics

The account permissions table confirmed `arif.techr@gmail.com` is the sole administrator, per the owner's direction. A live Tag Assistant test verified denied defaults, Statistics-only consent with all advertising signals denied, full consent with all four signals granted, a persisted choice after reload, and a GA4 page view. The diagnostics page may still show the aggregate regional 0% warning and the recommendation to add a backup administrator.

## Catalog event enrichment and CTX Feed

[GTM version 8](https://tagmanager.google.com/#/versions/accounts/6407569107/containers/288489610/versions/8) is live. The public WooCommerce Store API supplies product metadata. GA4 captures item categories, SKU, variation, price and currency when available. Meta `ViewContent` and `AddToCart` use the same WooCommerce variation ID with category and the available case price and currency. GA4 registers `product_category`, `pricing_mode` and `price_band` as event-scoped custom dimensions. Mixed-category carts retain the category on each item.

Chrome Tag Assistant verified `view_item`, `add_to_cart`, `view_cart` and `begin_checkout` for Double-Wall Paper Cups, variation `182`, category `Cups`, secondary category `Beverages`, at `150 USD` per case. Meta browser requests contained the same ID, category, value and currency for `ViewContent` and `AddToCart`. The quote-only Kraft Food & Salad Bowls page sent product group `124`, category `Food and takeaway` and `quote_only` without a numeric price or value. The test cart was emptied before placing an order. Meta dashboard ingestion and catalog matching require verification after the feed is connected.

For a future CTX Feed catalog, use the exact WooCommerce variation ID as each variant's feed `id` and the WooCommerce parent ID as its `item_group_id`. Keep SKU separate. For a sellable simple product, use its WooCommerce product ID as feed `id`. Exclude quote-only items from the priced catalog feed and use their view events for category-level engagement. After enabling the feed, compare the exact feed IDs with `content_ids` in Meta Events Manager, including variation `182`, and verify catalog diagnostics and event matching before activating dynamic retargeting.

## Engagement tracking and Google Ads audiences

[GTM version 9](https://tagmanager.google.com/#/versions/accounts/6407569107/containers/288489610/versions/9) adds four analytics events after Statistics consent on public Cups1 pages. Chrome Tag Assistant showed all four hits sent to the Cups1 GA4 stream after a product-page scroll, quote CTA click and one interaction with the inquiry form.

| Event | Trigger |
| --- | --- |
| `cta_click` | A click on a defined Cups1 CTA, such as quote, sample, product, contact or add to cart. |
| `scroll_depth` | 25%, 50%, 75% and 90% of the page, with each threshold recorded once per page view. |
| `content_engaged` | 75% depth on a product, catalog, business or customization page. |
| `inquiry_start` | The first real edit to a popup or standalone inquiry form, once per form per page load. |

The new tags send a fixed action, scroll threshold, form type or public page type. They omit field values, URL query strings, URL fragments and the referrer's path. GA4 has event-scoped custom dimensions `cta_action` and `page_type`. Accepted submissions continue to send `generate_lead`, `sample_request` or `contact_request`. The Chrome form-start test stopped before submission.

Marketian Google Ads **993-633-5611** received both audience segments through the personalized GA4 link. **Engaged visitors** has a 30-day duration and uses a CTA click or commercial-page engagement, with temporary exclusions for inquiry starts, cart adds, checkout and conversions. **Inquiry started without completion** has a 14-day duration and temporarily excludes completed inquiries and purchases. Google Ads showed zero eligible users and **Too small to serve** for both at verification.

## Direct Google Ads remarketing for 104-616-6584

[GTM version 10](https://tagmanager.google.com/#/versions/accounts/6407569107/containers/288489610/versions/10) adds the native Google Ads destination and a website remarketing tag for **AW-660762155**, the destination verified in [Google Ads account 104-616-6584](https://ads.google.com/aw/datamanager?ocid=413659830). Both tags require Marketing consent and use the same public Cups1 URL and referrer rules. The remarketing tag has no conversion label or custom user ID. The rules exclude private account and checkout URLs and query parameters such as inquiry references and order keys.

Chrome Tag Assistant confirmed no requests to the destination with Marketing off and a remarketing hit to `/pagead/viewthroughconversion/660762155/` after Marketing opt-in on the Double-Wall Paper Cups page. The original browser preference was restored. The public GTM response confirmed version 10 and the Ads destination. This direct tag supplies website remarketing data independently of the approved GA4 link. To build a Cups1-only data segment in this shared Ads account, scope the website visitor rule to URLs beginning with `https://cups1.com/`.
