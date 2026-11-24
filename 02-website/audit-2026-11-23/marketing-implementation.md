# Cups1 marketing implementation plan

23 November 2026 · Production site cups1.com

## Set the campaign goals

- **Custom packaging.** Optimize for completed, qualified quote and pricing inquiries. Count samples and general contacts separately. Record campaign attribution and lead outcome in the CRM.
- **Case sales.** Add purchase optimization and shopping feeds once approved variations, case prices, inventory, shipping coverage, and payment flow pass testing. One product can have both a case purchase path and a custom-printing inquiry path.

## Set up tracking

The [Cups1 Elementor 1.8.45 update](../cups1-elementor-1.8.45.zip) adds two local data layer events for Tag Manager. Configure consent checks before connecting them to any destination.

| Data layer event | Fields | Tag Manager mapping |
| --- | --- | --- |
| cups1_inquiry_complete | lead_type, form_type | Send GA4 generate_lead after accepted submissions. Send Meta Lead for quote, pricing and customization, and use separate reporting for sample and contact. |
| cups1_cart_add | currency, value, items | Map to GA4 add_to_cart and Meta AddToCart. Use items[].item_id as the WooCommerce variation ID when checking CTX Feed and Meta item matches. |

Test the update on staging as a replacement for 1.8.44. Check the search and catalog markup, the sitemap, and both inquiry paths. Select the approved WordPress Privacy Policy page to enable its links. Keep the 1.8.44 package available for rollback.

| Setup | Implementation | Acceptance check |
| --- | --- | --- |
| Privacy and consent | Publish the approved privacy notice and link it beside the standalone forms and two-step popup. Set up a consent manager, initialize consent before tags execute, and apply decisions to browser and server tracking. | Verify initial state, analytics-only consent, advertising consent, rejection, persistence, and withdrawal. Check that forms and checkout work when optional tracking is declined. |
| GTM and GA4 | Use the Cups1 Tag Manager container and GA4 web stream. Send ecommerce and lead events through one event layer. Add Google Ads conversion reporting when the account and primary action are confirmed. | Use GTM Preview and GA4 DebugView. Verify each event once with the correct type, currency, value, and consent state. Use one primary Ads conversion per intended optimization action. |
| Meta Pixel and Conversions API | Connect the Cups1 dataset and ad account. Use an integration that supports consent and the custom cart and inquiry paths. Assign one owner per event and reuse the event name and event ID for corresponding browser and server copies. | In Meta Events Manager Test Events, verify browser and server sources, deduplication, and catalog matches. Reload confirmation and retry a request to check for duplicates. |
| CRM and email | Confirm accepted inquiries appear in the private WordPress inbox and reach the approved mailbox or CRM. Preserve approved campaign attribution through qualification. | In staging, send labeled quote, sample, and contact requests. Check storage, email delivery, routing, permitted artwork upload, spam handling, and qualification reporting. |

[Google consent setup](https://developers.google.com/tag-platform/security/guides/consent) · [GA4 recommended events](https://support.google.com/analytics/answer/9267735) · [Meta Pixel and Conversions API](https://developers.facebook.com/docs/facebook-business-extension/fbe/get-started/pixel-capi-onboarding) · [Meta for WooCommerce](https://woocommerce.com/document/facebook-for-woocommerce/)

### Event mapping

| Action | GA4 | Meta | When to fire |
| --- | --- | --- | --- |
| View catalog or product | view_item_list or view_item | ViewContent on product | On the actual view. For sellable items, use the selected or default variation ID when available. If recording an unselected parent as a group, match its group ID and content type in Meta. |
| Add product | add_to_cart | AddToCart | After WooCommerce accepts the cart change. Include variation ID, number of cases added, case price, and currency. Verify the custom drawer and any standard WooCommerce add action. |
| Start checkout | begin_checkout | InitiateCheckout | Once usable checkout loads with a non-empty cart. |
| Confirm purchase | purchase | Purchase | On the verified order state for the selected payment flow. Use one transaction ID per order. Test reloads and delayed gateway confirmations. |
| Complete quote, pricing, or customization inquiry | generate_lead with lead_type | Lead | After an accepted standalone submission or final popup success. Record the initial popup contact step separately if needed. |
| Complete a sample request or general contact | generate_lead with distinct lead_type | Dedicated custom event or Contact for general contact | After accepted submission. Keep these events separate from the primary quote conversion. |

The custom drawer uses the WooCommerce Store API in [catalog-cart.js](../elementor/plugin/public/catalog-cart.js). The two-step popup and standalone forms handle success separately in [inquiry-popup.js](../elementor/plugin/public/inquiry-popup.js) and [site.js](../elementor/plugin/public/site.js). Test native integration coverage across all three paths before adding handlers. Use an opaque deduplication key. Keep names, email addresses, phone numbers, notes, addresses, and uploaded artwork out of analytics payloads and event URLs. Review Meta advanced matching separately before enabling it.

## Configure CTX Feed

1. Review existing WooCommerce plugins and destination catalog data sources. Assign CTX Feed as the source for the chosen catalog. Disable overlapping product sync to that catalog after confirming who owns it and how the switch affects existing items.
2. Generate a private review feed with one row per approved sellable variation. Map a stable item ID that matches the pixel's content ID, a shared parent item_group_id, a title with size, a variant landing link, an accessible product image, brand, condition, stock status, case price, and currency. Use valid product identifiers where available. Exclude drafts, quote-only products, and items with unapproved prices or unsupported shipping. Set US and Canada targets according to approved coverage and pricing.
3. Check that the variant URL selects the intended size and case pack. Compare price, currency, and stock across landing page, cart, checkout, feed, and structured data. Sample a priced variation, a second variation in the same group, and an excluded quote-only product.
4. Add the approved feed to the intended Meta catalog and attach the corresponding dataset. Set up CTX refresh and scheduled fetch. Check image access, item diagnostics, grouping, and event ID match. Use the Google template for Merchant Center and verify site ownership, shipping, returns, and item diagnostics. Check that an approved test update reaches each platform.

[CTX Feed for Meta](https://webappick.com/docs/ctx-feed/merchants/how-to-make-and-upload-product-feed-to-facebook-business-manager/) · [CTX Feed setup and refresh](https://webappick.com/docs/ctx-feed/basic/make-woocommerce-product-feed/) · [Google Merchant Center product specification](https://support.google.com/merchants/answer/7052112?hl=en)

## Account access and launch checks

| Access | Needed for |
| --- | --- |
| WordPress administrator and a staging or approved test environment | Review plugins, WooCommerce settings, email, consent, checkout, and feed generation. |
| Meta Business Portfolio, dataset, ad account, and Commerce Manager catalog | Identify asset ownership and validate Pixel, CAPI, and catalog data sources. |
| Search Console, Tag Manager, and GA4 | Check live indexing and sitemap processing, then test and publish the measurement setup. |
| Merchant Center and Google Ads, where applicable | Check feed diagnostics, product listings, and conversions. |

Use delegated access and store server tokens in approved configuration. Start with lead tracking after inquiry delivery and consent checks pass. Launch shopping and dynamic catalog ads after approved variations pass checkout, diagnostics, and event matching. Record the GTM version, connected accounts, feed template, and rollout date for troubleshooting and rollback.
