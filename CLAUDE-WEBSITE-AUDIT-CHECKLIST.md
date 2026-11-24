# Cups1 website audit checklist for Claude

Audit the live Cups1 website at https://cups1.com/. It’s a B2B packaging store built on WordPress and WooCommerce. Review the whole site, including the public pages, product catalog, quote and customization flows, cart, checkout, SEO, accessibility, and performance.

Use a browser to test actual behavior on desktop and mobile. Start with the homepage, header, footer, and XML sitemap to build a page inventory. Group pages by template, check every public URL you can discover for obvious issues, and test representative pages from each template in depth. List any areas you couldn’t access or test. Keep the audit read-only. You may add items to your own test cart and restore it afterward. Stop before submitting forms, placing orders, or making payments unless I provide a test environment and authorize those steps.

## 1. Site coverage and navigation

- [ ] Review the homepage, product catalog, product details, customization, quote/contact, business pages, resources, policies, cart, and checkout.
- [ ] Check header, footer, buttons, menus, and internal links for broken destinations, redirect loops, confusing labels, and pages that are hard to find.
- [ ] Flag duplicate, outdated, thin, or unnecessary pages. Recommend keep, improve, merge, redirect, or remove for each candidate. Check where a page is linked before recommending removal.
- [ ] Check that mobile has no horizontal overflow and the header controls are visible in this order: Search, Cart, Menu, with Menu on the far right.

## 2. Product catalog and B2B flows

- [ ] Check that /products/ works as the storefront. Test search for a product name, a partial match, and a term with no results. Confirm the search field expands below the header and returns relevant products.
- [ ] Test a priced product, a product that requires a quote, and an unavailable variation if one exists.
- [ ] Verify that variable products show a price range before selection and the correct price, units per case, and stock after selecting a size. Watch for flicker or a temporary return to the range.
- [ ] Check sale prices appear before the crossed-out regular price. Verify Add to cart, Customize, Request Pricing, and Get a Delivered Quote appear where appropriate and lead to the right destinations.
- [ ] Check catalog tiles for consistent alignment, full-width size dropdowns, and stable button positions. Confirm detail pages use size buttons and don’t show a separate Units Per Case selector.
- [ ] Check that quotes and customization carry through the selected product and size where expected. Test required-field validation without submitting an inquiry.
- [ ] Look for gaps that matter to wholesale buyers: case pack, minimum order, lid compatibility, branding options, and delivery information. Flag missing or inconsistent claims and cite the page.

## 3. Cart and checkout

- [ ] Add a selected variation to the cart. Verify product name, image, size, units per case, price per case, quantity, line total, and subtotal.
- [ ] Check that the cart badge shows the total case count and hides when empty. Verify it stays in sync across the drawer and full cart.
- [ ] Test the cart drawer’s close button, Escape, and clicking outside where there is a visible backdrop. Check that focus returns to the cart trigger.
- [ ] In each cart item, check the remove × at the top right and the − / + controls at the bottom right. Verify quantity and prices update without a flashing “Updating cart…” message or layout shift. Test the minimum quantity and watch for lost clicks or stale totals.
- [ ] Verify checkout shows the same products and totals as the cart. Review contact, billing, shipping, coupons, tax, payment availability, validation, and mobile layout where testable. Flag any blocker that would prevent a buyer from ordering.
- [ ] Record order confirmation and order emails as untested unless you can verify them with an authorized test order.

## 4. SEO

- [ ] Check HTTP status, HTTPS redirects, robots.txt, XML sitemap, canonical tags, and indexability. Compare sitemap URLs with the pages you can reach.
- [ ] Review unique page titles, meta descriptions, headings, image alt text, internal links, and descriptive URLs across major templates.
- [ ] Check whether search, filter, variation, cart, and checkout URLs create duplicate or low-value URLs for search engines. Verify what the site actually emits.
- [ ] Check product, offer, breadcrumb, and organization structured data where present. Compare schema prices and availability with what shoppers see. Flag missing, invalid, or misleading fields.
- [ ] Review whether product and category pages answer what wholesale buyers search for. Identify specific content gaps and useful internal links.
- [ ] Separate verified crawl and indexability findings from actual indexing, rankings, and traffic. Mark those as unverified unless Search Console or equivalent data is available.

## 5. Performance, accessibility, and trust

- [ ] Check mobile and desktop load speed on the homepage, catalog, and a product page. Report measured results and distinguish lab scores from real-user data.
- [ ] Look for oversized images, slow requests, layout shifts, broken assets, and browser console errors that affect shoppers.
- [ ] Test keyboard navigation, visible focus, accessible labels for icon buttons, form errors, contrast, text readability, and touch targets.
- [ ] Check contact information, privacy and terms links, and shipping and returns information for visibility and consistency.

## Deliverable

Start with the five highest-priority findings. Then give me a table with severity, affected URL or template, device, steps to reproduce, expected behavior, actual behavior, evidence, and recommended fix. Use Critical for blocked ordering or severe sitewide issues, High for major buyer or SEO problems, Medium for meaningful usability or content issues, and Low for polish.

Group repeated problems by template and include example URLs. List what passed, what you couldn’t verify, and a prioritized fix checklist with a retest step for each issue. Label suspected causes as hypotheses. Use screenshots where they help reproduce a finding.
