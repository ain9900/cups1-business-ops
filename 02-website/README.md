# Cups1 WordPress redesign

## Design review

The [visual reference board](design-review/reference-board.html) compares EarthStore’s homepage, customization catalog, and sales inquiry with the corresponding Cups1 layouts. The current design follows EarthStore’s full-width photo montage, white navigation, compact product grid, and split sales inquiry using Cups1’s brand and original packaging concepts.

## Elementor site on cups1.com

The [live Cups1 site](https://cups1.com/) uses Elementor Canvas for 21 WordPress pages. Each section is an Elementor widget with separate controls for its copy, images, and links. Rearrange sections in Elementor’s Structure panel.

The [product catalog](https://cups1.com/products/) supports keyword search, use filters, and name sorting. The [customization catalog](https://cups1.com/customize/) starts a quote with the selected packaging format. Quotes can include dimensions, print preference, quantity, delivery country and postal code, and whether the request is for recurring or multi-location supply.

In WordPress, open **Tools → Cups1 Site Setup** for direct editing links to the pages and the shared header and footer templates. View submitted quotes, sample requests, and contact messages under **Cups1 Inquiries**. Artwork is stored with the private inquiry and downloaded from its WordPress admin screen.

The addon source is in `elementor/plugin`. To build the installable ZIP, install Python's `beautifulsoup4` package and run `python 02-website/elementor/build.py path/to/cups1-elementor.zip`. The builder packages the preview assets and produces initial widget settings.

## v2.cups1.com audit and fixes

The v2 installation runs Hello Elementor and Cups1 Elementor Design 1.2.0. The update preserves the original 1.0.0 control IDs and saved page settings. **Tools → Cups1 Site Setup** includes the new editable Customize page and editing links for the existing pages.

The audit covered all 21 public Elementor pages and 33 internal destinations. It verified catalog search, the responsive menu, the homepage at a 345px editor viewport, and product selection on quote and sample links. It also verified an invalid quantity response and a synthetic quote with artwork, dimensions, postal code, print preference, and ordering pattern in the private WordPress inbox.

Version 1.2.0 adds catalog search, use filters and sorting, a Customize page, expanded quote fields, inline form feedback, and default search descriptions and a favicon. Legacy quote and sample links redirect to the current product selection URLs. The audit and addon deployment were scoped to v2.

## Local design source

Open [the homepage](design-review/index.html) and [the double-wall cup page](design-review/double-wall-paper-cups.html) in a browser. Both files work locally from this checkout and adapt to desktop and mobile. Try opening the product from the homepage catalog, switching the gallery image, and following the quote and sample buttons. The form shows the selected product and uses sample data locally for the interaction preview.

Review the header and hero, the six-category catalog, the delivered-quote breakdown, the request-information state for documentation, and the way the flagship product moves buyers from specifications to inquiry. The approved Cups1 logo, warm paper backgrounds, navy typography, and orange quote buttons carry across both pages. Photography is represented by labeled concept images. Product details awaiting verification are described as items to confirm during quotation.

The [preview stylesheet](design-review/styles.css) defines the palette, typography, spacing, and component styles for review. Orange buttons use navy labels. Leaf green is limited to the logo. Verified green is reserved for records that have been reviewed against the applicable product and destination.

## Remaining WordPress launch work

| Area | Remaining work |
| --- | --- |
| Product content | Add approved product photos and verified sizes, lid fit, print options, minimum orders, and lead times. Material and size filters require verified product data. |
| Documentation and legal copy | Publish approved product documentation and legal pages after the owner supplies the files and copy. |
| Inquiry operations | Forms show a confirmation reference and save privately in WordPress. Configure SMTP and CRM notifications when the destination is approved. |
| Commerce | WooCommerce is active in coming-soon mode, with Shop, Cart, Checkout and My Account assigned. Configure approved SKUs, case pricing, stock, payments, shipping, and tax before taking orders. |
| SEO and analytics | Configure page metadata, eligible structured data, and consent-gated analytics as part of launch operations. |

Later phases can add account management, quote approval, order tracking, reorders, contracts, and sample payments if required.

## Concept imagery

The `design-review/assets/` WebP files were prepared with built-in ImageGen. The generation prompts specified:

- A warm, directional-light product hero with three graduated paper cups on a limestone plinth, using abstract navy, cream, and restrained orange print.
- A consistent studio grid of cup, tub, bowl, and carton formats, plus paper print detail and a kraft sample mailer.
- Editorial scenes of a café counter, a restaurant takeaway order, and a wholesale buyer comparing packaging samples.

The visuals omit customer names and logos. Replace them with approved sample photography when available.
