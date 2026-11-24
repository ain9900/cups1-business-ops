"""Build the Cups1 Elementor addon from the approved design preview."""

import html
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

from bs4 import BeautifulSoup, Comment, NavigableString
from home_sections import SECTIONS as HOME_REFERENCE_SECTIONS


ROOT = Path(__file__).resolve().parent
PREVIEW = ROOT.parent / "design-review"
PRODUCTS = {
    "double-wall": ("double-wall-paper-cups", "Double-Wall Paper Cups"),
    "single-wall": ("single-wall-paper-cups", "Single-Wall Paper Cups"),
    "ripple-wall": ("ripple-wall-paper-cups", "Ripple-Wall Paper Cups"),
    "dessert": ("ice-cream-dessert-cups", "Ice Cream & Dessert Cups"),
    "bowls": ("kraft-food-salad-bowls", "Kraft Food & Salad Bowls"),
    "boxes": ("custom-takeaway-boxes", "Custom Takeaway Boxes"),
}
SECTIONS = {
    "branding": ("custom-printing", "Custom Printing"),
    "process": ("how-it-works", "How It Works"),
    "industries": ("industries", "Industries"),
    "documents": ("documents", "Documents & Quality"),
    "about": ("about", "About Cups1"),
    "faq": ("faq", "Frequently Asked Questions"),
    "delivered": ("shipping-delivery", "Shipping & Delivery"),
}


def soup(markup):
    return BeautifulSoup(markup, "html.parser")


def route(href, local=False):
    url = urlsplit(href)
    if url.scheme or url.netloc or href == "#main" or href.startswith("@page/"):
        return href
    if local and not url.path and not url.query and url.fragment not in ("quote", "contact"):
        return href
    query = parse_qs(url.query)
    product = query.get("product", [""])[0]
    fragment = url.fragment
    if query.get("intent") == ["sample"]:
        slug = "request-a-sample"
    elif fragment in ("quote", "artwork-field") or product:
        slug = "request-a-quote"
    elif fragment == "contact":
        slug = "contact"
    elif fragment in SECTIONS:
        slug = SECTIONS[fragment][0]
    elif fragment == "products":
        slug = "products"
    elif fragment in PRODUCTS:
        slug = PRODUCTS[fragment][0]
    elif url.path == "double-wall-paper-cups.html":
        slug = "double-wall-paper-cups"
    elif href.startswith("#"):
        return href
    else:
        slug = "home"
    return f"@page/{slug}" + (f"?product={product}" if product else "")


def asset_name(src):
    return src.rsplit("/", 1)[-1]


def component(key, title, markup, local=False):
    doc = soup(markup)
    fields = {}
    # Allocate controls for additions after legacy controls so saved Elementor
    # settings retain their original meanings when the addon is updated.
    additions = {id(node) for group in doc.select("[data-cups1-new-fields]") for node in [group, *group.descendants]}
    appended = {id(node) for group in doc.select('[data-cups1-new-fields="append"], [data-cups1-new-fields="last"]') for node in [group, *group.descendants]}
    last = {id(node) for group in doc.select('[data-cups1-new-fields="last"]') for node in group.descendants}

    # Keep the remaining controls mapped to their saved settings.
    retired = {
        "cup-logo-preview": {16, 23, 24, 25, 26, 27, 28},
        "home-compare": {1, 2, 3, *range(14, 24), 39, 40},
    }.get(key, set())
    field_numbers = (number for number in range(1, sys.maxsize) if number not in retired)

    def field(label, value, kind="text"):
        identifier = f"field_{next(field_numbers)}"
        fields[identifier] = {"label": label, "type": kind, "value": value}
        return f"{{{{{identifier}}}}}"

    links = doc.select("a[href]")
    strings = list(doc.find_all(string=True))
    for link in links:
        if id(link) not in additions:
            link["href"] = field(f"Link · {link.get_text(' ', strip=True)}", route(link["href"], local), "url")
    def add_image_fields(image):
        file = asset_name(image["src"])
        image["src"] = field(f"Image · {Path(file).stem}", file, "media")
        image.attrs.pop("srcset", None)
        image.attrs.pop("sizes", None)
        if image.get("alt"):
            image["alt"] = field(f"Alt text · {Path(file).stem}", image["alt"])

    images = doc.select("img[src]")
    for image in images:
        if id(image) not in additions:
            add_image_fields(image)
    for element in doc.select("[data-alt], [data-caption]"):
        for attribute in ("data-alt", "data-caption"):
            if element.get(attribute):
                element[attribute] = field(attribute.removeprefix("data-").capitalize(), element[attribute])
    for option in doc.select("option:not([value])"):
        option["value"] = option.get_text(strip=True)
    def add_text_field(node):
        value = str(node).strip()
        if not value or isinstance(node, Comment) or node.parent.name in ("script", "style", "svg"):
            return
        if node.parent.get("aria-hidden") == "true":
            return
        label = "Heading" if re.fullmatch("h[1-6]", node.parent.name) else node.parent.name.capitalize()
        if node.parent.name in ("a", "button"):
            label = "Action label"
        elif node.parent.name == "p":
            label = "Eyebrow" if "eyebrow" in node.parent.get("class", []) else "Paragraph"
        snippet = value[:52] + ("…" if len(value) > 52 else "")
        node.replace_with(NavigableString(str(node).replace(value, field(f"{label} · {snippet}", value), 1)))
    for node in sorted(strings, key=lambda node: id(node) in additions):
        if id(node) not in appended:
            add_text_field(node)
    for link in links:
        if id(link) in additions:
            link["href"] = field(f"Link · {link.get_text(' ', strip=True)}", route(link["href"], local), "url")
    for image in images:
        if id(image) in additions and id(image) not in appended:
            add_image_fields(image)
    for node in strings:
        if id(node) in appended and id(node) not in last:
            add_text_field(node)
    for image in images:
        if id(image) in appended:
            add_image_fields(image)
    for node in strings:
        if id(node) in last:
            add_text_field(node)
    for group in doc.select("[data-cups1-new-fields]"):
        del group["data-cups1-new-fields"]
    if key == "home-compare":
        heading = doc.select_one(".comparison-heading")
        doc.select_one("[data-cups1-comparison]").insert_before(heading.parent.extract())
    if key == "header":
        navigation = doc.select_one(".main-nav")
        navigation.append(navigation.select_one(":scope > a.button.primary").extract())
    if key == "page-products":
        grid = doc.select_one(".catalog-grid")
        grid.insert(0, Comment("cups1-products-start"))
        grid.append(Comment("cups1-products-end"))
        grid.insert_after(Comment("cups1-catalog-business"))
    return key, {"title": title, "markup": str(doc), "fields": fields}


def main():
    home = soup((PREVIEW / "index.html").read_text(encoding="utf-8"))
    product = soup((PREVIEW / "double-wall-paper-cups.html").read_text(encoding="utf-8"))
    definitions = {}
    pages = {}

    def add(key, title, markup, local=False):
        name, definition = component(key, title, str(markup), local)
        definitions[name] = definition
        return name

    header = str(home.select_one(".skip")) + str(home.select_one(".announcement")) + str(home.header)
    header = soup(header)
    header.select_one('.main-nav > a[href="#about"]').insert_before(
        soup('<a href="@page/customize" data-cups1-nav-fallback data-cups1-new-fields>Customize</a>')
    )
    def nav_icon(path):
        return f'<svg aria-hidden="true" focusable="false" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="{path}"/></svg>'

    def nav_card(slug, label, description, icon):
        return f'''<a class="nav-card" href="@page/{slug}">
            <span class="nav-card-icon" aria-hidden="true">{nav_icon(icon)}</span>
            <span data-cups1-new-fields="append"><strong>{label}</strong><small>{description}</small></span></a>'''

    products_dropdown = header.select_one(".main-nav > .dropdown")
    products_dropdown["class"].append("mega-dropdown")
    products_panel = products_dropdown.select_one(".dropdown-panel")
    products_panel["class"].extend(("mega-panel", "mega-products"))
    catalog_link, *product_links = products_panel.select("a")
    product_grid = header.new_tag("div", attrs={"class": "mega-card-grid"})
    products_panel.append(product_grid)
    product_details = (
        ("Insulated cups for hot drinks", "M5 7h14l-2 14H7zm-1 0h16M8 4h8M7 12h10"),
        ("Lightweight paper cups", "M5 5h14l-2 16H7zM5 8h14"),
        ("Textured grip for hot drinks", "M5 6h14l-2 15H7zM8 9l1 9m3-9v9m4-9-1 9"),
        ("For ice cream and desserts", "M4 11h16l-3 9H7zM6 11a6 6 0 0 1 12 0"),
        ("For salads, meals, and sides", "M3 10h18c-1 6-4 9-9 9s-8-3-9-9zm0 0h18"),
        ("Folded cartons for takeaway meals", "m3 7 9-4 9 4v10l-9 4-9-4zm0 0 9 4 9-4m-9 4v10"),
    )
    for link, (description, icon) in zip(product_links, product_details, strict=True):
        card = soup(nav_card("products", "", description, icon)).a
        card.strong.append(link.string.extract())
        del card.strong.parent["data-cups1-new-fields"]
        card.small["data-cups1-new-fields"] = "last"
        link["class"] = ["nav-card"]
        for child in list(card.contents):
            link.append(child)
        product_grid.append(link)
    catalog_link["class"] = ["mega-view-all"]

    business_cards = (
        ("for-business", "Business overview", "Packaging programs for your team", "M3 21V7l9-4 9 4v14zM9 21v-6h6v6"),
        ("custom-printing", "Custom printing", "Packaging printed with your brand", "M6 8h12l-2 13H8L6 8zm-2 0h16M9 5h6"),
        ("products", "Product offerings", "Cups, bowls, and takeaway boxes", "m3 7 9-4 9 4v10l-9 4-9-4zm0 0 9 4 9-4M12 11v10"),
        ("warehousing", "Warehousing", "Storage and fulfillment", "M3 21V8l9-5 9 5v13zM7 21V11h10v10M7 15h10m-10 3h10"),
        ("business-account", "Business account", "Account details and order history", "M3 3h7v7H3zm11 0h7v7h-7zM3 14h7v7H3zm11 0h7v7h-7z"),
        ("location-management", "Location management", "Coordinate packaging across locations", "M20 10c0 5-8 11-8 11s-8-6-8-11a8 8 0 0 1 16 0zM15 10a3 3 0 1 1-6 0 3 3 0 0 1 6 0z"),
    )
    resource_cards = (
        ("about", "About Cups1", "Meet the company", "M12 6c-3-2-6-2-9-1v14c3-1 6-1 9 1 3-2 6-2 9-1V5c-3-1-6-1-9 1zm0 0v14"),
        ("documents", "Documents &amp; quality", "Packaging specifications and records", "M5 3h10l4 4v14H5zm9 0v5h5M8 12h8m-8 4h8"),
        ("resources", "Buyer resources", "Artwork and ordering guides", "M4 6h4v15H4zm4-3h6v18H8zm7 3 4-1 4 14-4 1z"),
    )
    support_cards = (
        ("help-center", "Help Center", "Answers to common questions", "M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0zM9 9a3 3 0 1 1 4 3c-1 .5-1 1-1 2m0 3h.01"),
        ("contact", "Contact us", "Talk to the Cups1 team", "M3 5h18v14H3zm0 1 9 7 9-7"),
    )
    header.select_one('.main-nav').append(soup(f'''
        <details class="dropdown mega-dropdown" data-cups1-new-fields>
          <summary>For Business</summary>
          <div class="dropdown-panel mega-panel mega-business">
            <div class="mega-card-grid">{"".join(nav_card(*card) for card in business_cards)}</div>
            <div class="mega-sidebar" data-cups1-new-fields="append"><p>By industry</p>
              <a href="@page/industries#coffee-shops">Coffee shops</a>
              <a href="@page/industries#restaurants">Restaurants</a>
              <a href="@page/industries#distributors">Distributors</a>
              <a class="mega-view-all" href="@page/industries">View all industries →</a>
            </div>
          </div>
        </details>
        <details class="dropdown mega-dropdown" data-cups1-new-fields="append">
          <summary>Resources</summary>
          <div class="dropdown-panel mega-panel mega-resources">
            <div><p>Company</p>{"".join(nav_card(*card) for card in resource_cards)}</div>
            <div><p>Connect</p>{"".join(nav_card(*card) for card in support_cards)}</div>
          </div>
        </details>
    '''))
    for card, anchor in zip(home.select("#industries .industry"), ("coffee-shops", "restaurants", "distributors")):
        card["id"] = anchor
    footer = soup(str(home.footer))
    footer.select_one(".footer-base").find_all("span")[-1].extract()
    for label, slug in (("For distributors", "for-distributors"), ("Resources", "resources")):
        footer.select(".footer-grid > div")[-1].append(soup(f'<a href="@page/{slug}">{label}</a>'))
    footer.select_one(".footer-grid").append(soup("""
        <div data-cups1-new-fields><h2>For Business</h2>
          <a href="@page/for-business">Overview</a><a href="@page/warehousing">Warehousing</a>
          <a href="@page/business-account">Business account</a><a href="@page/location-management">Location management</a>
          <a href="@page/help-center">Help Center</a>
        </div>
    """))
    add("header", "Site header", header)
    add("footer", "Site footer", footer)

    for key, (slug, title) in list(PRODUCTS.items())[1:]:
        card = home.select_one(f".product#{key}")
        card.h3.string = ""
        card.h3.append(soup(f'<a href="@page/{slug}">{html.escape(title)}</a>'))

    inquiry = home.select_one("#quote")
    form = inquiry.form
    form["action"] = "@inquiry"
    form["method"] = "post"
    form["enctype"] = "multipart/form-data"
    form.insert(0, soup('<input type="hidden" name="action" value="cups1_inquiry"><input type="hidden" name="cups1_nonce" value="@nonce"><input type="hidden" name="intent" value="@intent"><input type="hidden" name="return_page" value="@current"><div hidden aria-hidden="true"><label>Leave blank<input name="website" tabindex="-1" autocomplete="off"></label></div>'))
    inquiry.select_one("#contact .footnote").extract()
    form.select_one("#inquiry-submit").attrs.pop("disabled", None)
    form.select_one(".form-status").insert(0, soup('<span data-inquiry-result></span>'))
    form.select_one("#artwork-field small").string = "(optional)"
    form.select_one("#file-help").string = "PDF, PNG, or JPEG, up to 5 MB."

    home_widgets = []
    for index, section in enumerate(home.main.find_all("section", recursive=False)):
        key = section.get("id", f"home-{index}")
        title = section.find(["h1", "h2"]).get_text(" ", strip=True)
        home_widgets.append(add(key, title, section))
    pages["home"] = {"title": "Home", "widgets": home_widgets}
    for key, (title, markup) in HOME_REFERENCE_SECTIONS.items():
        if key == "home-compare":
            markup = soup(markup)
            for link, (_, icon) in zip(markup.select(".reference-category a"), product_details, strict=True):
                link.append(soup(nav_icon(icon)).svg)
        add(key, title, markup)

    def standalone(key, title, section):
        section = soup(str(section))
        heading = section.find("h2")
        if heading and not section.find("h1"):
            heading.name = "h1"
        pages[key] = {"title": title, "widgets": [add(f"page-{key}", title, section)]}

    catalog = soup(str(home.select_one("#products")))
    grid = catalog.select_one(".catalog-grid")
    product_categories = dict(zip(PRODUCTS, ("beverage", "beverage", "beverage", "dessert", "food", "food"), strict=True))
    for card, category in zip(grid.select(".product"), product_categories.values(), strict=True):
        card["data-catalog-category"] = category
    grid.insert_before(soup('''
        <form class="catalog-filters" method="get" aria-label="Filter packaging" hidden data-cups1-new-fields>
          <label>Search products<input type="search" name="packaging" placeholder="Try paper cups"></label>
          <label>Use<select name="format"><option value="">All uses</option><option value="beverage">Beverages</option><option value="dessert">Desserts</option><option value="food">Food and takeaway</option></select></label>
          <label>Sort by<select name="sort"><option value="">Featured</option><option value="az">Name A–Z</option><option value="za">Name Z–A</option></select></label>
          <button class="button primary" type="submit">Apply filters</button>
        </form>
        <p class="catalog-status" aria-live="polite"></p>
        <p class="catalog-empty" hidden data-cups1-new-fields>Try a different search or select All uses.</p>
    '''))
    for card, product_key in zip(grid.select(".product"), PRODUCTS):
        for link in card.select('a[href*="#quote"]'):
            link["href"] = f"@page/request-a-quote?product={product_key}#quote"
    standalone("products", "Products", catalog)

    custom = soup(str(catalog))
    custom.section["id"] = "customize"
    custom.select_one(".catalog-filters").decompose()
    custom.select_one(".catalog-status").decompose()
    custom.select_one(".catalog-empty").decompose()
    custom.find("h2").string = "Choose packaging to customize"
    custom.select_one(".catalog-heading > p:not(.eyebrow)").string = "Pick a format, then share your dimensions, branding, quantity, and artwork for a delivered quote."
    for card, product_key in zip(custom.select(".product"), PRODUCTS):
        body = card.select_one(".card-body")
        for action in body.select(".card-actions, .text-link"):
            if action.parent is not None:
                action.decompose()
        body.append(soup(f'<a class="button outline" href="@page/request-a-quote?product={product_key}#quote">Customize</a>'))
    for section_id, (slug, title) in SECTIONS.items():
        standalone(slug, title, home.select_one(f"#{section_id}"))
    quote = soup(str(inquiry))
    quote.select_one("#quantity-field").insert_before(soup('''
        <label data-cups1-new-fields>Size or dimensions <small>(optional)</small><input name="dimensions" maxlength="120" placeholder="e.g. 12 oz or 180 × 120 mm"></label>
        <label data-cups1-new-fields>Print preference <small>(optional)</small><select name="print_preference"><option value="">Choose a preference</option><option value="single">Single color</option><option value="multi">Multiple colors</option><option value="plain">Unprinted</option><option value="help">I need help choosing</option></select></label>
        <label data-cups1-new-fields>Delivery ZIP or postal code <small>(optional)</small><input name="postal_code" autocomplete="postal-code" maxlength="24"></label>
        <label data-cups1-new-fields>Ordering pattern <small>(optional)</small><select name="order_pattern"><option value="">Choose an option</option><option value="one-off">One-time order</option><option value="recurring">Recurring supply</option><option value="multi-location">Multiple locations</option></select></label>
    '''))
    standalone("request-a-quote", "Request a Quote", quote)

    wizard = soup(str(quote))
    wizard.select_one("#inquiry-kicker").string = "Custom packaging"
    wizard.select_one("#inquiry-title").string = "Configure your packaging"
    wizard.select_one("#inquiry-title").name = "h1"
    wizard.select_one("#form-heading").string = "Your packaging specification"
    wizard.select_one("#inquiry-copy").string = "Choose a format, specify the size and print, then review your request before sending it."
    wizard.form["data-packaging-wizard"] = ""
    wizard.form.insert(0, soup('<div data-packaging-steps hidden><p class="eyebrow" data-packaging-step aria-live="polite"></p></div>'))
    for label in wizard.form.select("label"):
        field = label.select_one("input, select, textarea")
        if not field or not field.get("name") or field["name"] == "website":
            continue
        name = field["name"]
        label["data-packaging-panel"] = (
            "specification" if name in ("product", "quantity", "dimensions", "print_preference")
            else "artwork" if name == "artwork" else "contact"
        )
    wizard.form.select_one("#inquiry-submit").insert_before(soup("""
        <div data-packaging-review hidden><h3>Review your specification</h3><dl></dl></div>
        <div class="actions" data-packaging-controls hidden>
          <button class="button outline" type="button" data-packaging-back>Back</button>
          <button class="button primary" type="button" data-packaging-next>Continue</button>
        </div>
    """))
    pages["configure-packaging"] = {
        "title": "Configure Packaging",
        "widgets": [add("page-configure-packaging", "Packaging configurator", wizard)],
    }
    for card, product_key in zip(custom.select(".product"), PRODUCTS):
        card.select_one(".card-body > a.button")["href"] = (
            f"@page/configure-packaging?packaging_product={product_key}"
        )
    custom.select_one(".catalog-heading").append(soup(
        '<a class="button primary" href="@page/logo-preview" data-cups1-new-fields>Preview your logo on a cup</a>'
    ))
    standalone("customize", "Customize Packaging", custom)
    logo_preview = """
    <section class="reference-band" data-cups1-logo-preview>
      <div class="shell">
        <div class="section-heading"><h1>Preview your logo on packaging</h1>
          <p>Choose a product and add your logo to see how it could look in print.</p></div>
        <div class="logo-preview-layout">
          <div class="logo-preview-controls">
            <label>Logo file <input type="file" accept="image/png,image/jpeg,image/webp" data-logo-file></label>
            <p>PNG, JPEG, or WebP, up to 10 MB. A transparent PNG gives the clearest preview.</p>
            <label>Product <select data-logo-model>
              <option value="double-wall">Double-wall paper cup</option>
              <option value="single-wall">Single-wall paper cup</option>
              <option value="ripple-wall">Ripple-wall paper cup</option>
              <option value="dessert" data-cups1-new-fields="append">Dessert cup</option>
              <option value="bowls" data-cups1-new-fields="append">Kraft food bowl</option>
              <option value="boxes" data-cups1-new-fields="append">Takeaway box</option>
            </select></label>
            <button class="button outline" type="button" data-logo-remove hidden>Remove logo</button>
            <label data-cups1-new-fields>Logo position <input type="range" min="0" max="100" value="50" data-print-position disabled></label>
            <div class="logo-position-labels" aria-hidden="true" data-cups1-new-fields><span>Higher</span><span>Lower</span></div>
            <p role="status" data-logo-status></p>
            <a class="button primary" href="@page/configure-packaging?packaging_product=double-wall" data-logo-quote>Request a quote</a>
          </div>
          <figure class="logo-preview-stage">
            <div class="logo-preview-photo">
              <img src="assets/comparison-cup.png" alt="Blank double-wall paper cup" data-preview-cup="double-wall">
              <img src="assets/preview-single-wall.png" alt="Blank single-wall paper cup" data-preview-cup="single-wall" hidden>
              <img src="assets/preview-ripple-wall.png" alt="Blank ripple-wall paper cup" data-preview-cup="ripple-wall" hidden>
              <img src="assets/preview-dessert.png" alt="Blank paper dessert cup" data-preview-cup="dessert" data-cups1-new-fields="append" hidden>
              <img src="assets/preview-bowls.png" alt="Blank kraft food bowl" data-preview-cup="bowls" data-cups1-new-fields="append" hidden>
              <img src="assets/preview-boxes.png" alt="Blank kraft takeaway box" data-preview-cup="boxes" data-cups1-new-fields="append" hidden>
              <canvas width="1536" height="1024" role="img" aria-label="Your custom print on the product" data-logo-overlay hidden></canvas>
            </div>
            <figcaption>Digital mockup. Final print size and color are confirmed separately.</figcaption>
          </figure>
        </div>
      </div>
    </section>"""
    pages["logo-preview"] = {
        "title": "Cup Logo Preview",
        "widgets": [add("cup-logo-preview", "Cup logo preview", logo_preview)],
    }

    business_pages = (
        ("for-business", "Packaging for your business", "Find custom packaging for one location or a recurring order across your team.", [
            ("Custom printing", "custom-printing", "Choose a packaging format and share your artwork."),
            ("Warehousing and fulfillment", "warehousing", "Discuss inventory and scheduled deliveries."),
            ("Multi-location supply", "location-management", "Plan orders and delivery for multiple locations."),
            ("Business account", "business-account", "Access your orders and account details."),
        ]),
        ("warehousing", "Warehousing and fulfillment", "Share your order volume, delivery destinations, and replenishment schedule so we can review a supply plan.", [
            ("Shipping and delivery", "shipping-delivery", "See what goes into a delivered quote."),
            ("Talk to sales", "contact-sales", "Discuss recurring production and delivery."),
        ]),
        ("location-management", "Packaging for multiple locations", "Tell us which products and delivery destinations your locations need.", [
            ("Browse packaging", "products", "Compare product formats."),
            ("Request a supply quote", "request-a-quote", "Include your locations and expected volumes."),
        ]),
        ("business-account", "Your Cups1 account", "Sign in to manage account details and see your WooCommerce orders.", [
            ("Open my account", "woocommerce-account", "Sign in to your customer account."),
            ("Talk to sales", "contact-sales", "Discuss a business supply program."),
        ]),
        ("help-center", "How can we help?", "Find answers about packaging, artwork, delivery, and ordering.", [
            ("Ordering questions", "faq", "Review common questions about custom packaging."),
            ("Artwork and printing", "custom-printing", "Prepare your design for a custom order."),
            ("Shipping and delivery", "shipping-delivery", "Review delivery details."),
            ("Contact support", "contact", "Send a question to Cups1."),
        ]),
    )
    for slug, title, intro, cards in business_pages:
        items = "".join(
            f'<article class="card"><div class="card-body"><h2>{html.escape(label)}</h2>'
            f'<p>{html.escape(description)}</p><a class="text-link" href="@page/{target}">'
            f'{html.escape(label)} <span aria-hidden="true">↗</span></a></div></article>'
            for label, target, description in cards
        )
        markup = f'<section class="section white"><div class="shell"><div class="section-heading"><h1>{html.escape(title)}</h1><p>{html.escape(intro)}</p></div><div class="catalog-grid">{items}</div></div></section>'
        standalone(slug, title, soup(markup).section)

    sales = soup(str(quote))
    sales.select_one("#inquiry-kicker").string = "Contact sales"
    sales.select_one("#inquiry-title").string = "Put your brand on every order"
    sales.select_one("#inquiry-copy").string = "Tell us what you need printed, how many units you use, and where you need delivery."
    standalone("contact-sales", "Contact Sales", sales)

    sample = soup(str(inquiry))
    sample.select_one("#inquiry-kicker").string = "Sample kit"
    sample.select_one("#inquiry-title").string = "See the packaging before you order."
    sample.select_one("#inquiry-copy").string = "Tell us which formats you’d like to compare. We’ll confirm sample availability and applicable terms."
    sample.select_one("#form-heading").string = "Request a sample kit"
    sample.select_one(".inquiry-highlights").extract()
    for selector in ("#quantity-field", "#artwork-field"):
        sample.select_one(selector).extract()
    sample.select_one("#inquiry-submit").string = "Request a Sample Kit"
    standalone("request-a-sample", "Request a Sample Kit", sample)

    contact = soup(str(inquiry))
    contact.select_one("#inquiry-kicker").string = "Contact Cups1"
    contact.select_one("#inquiry-title").string = "How can we help?"
    contact.select_one("#inquiry-copy").string = "Ask about packaging, artwork, delivery, or documentation."
    contact.select_one("#form-heading").string = "Send an inquiry"
    contact.select_one(".inquiry-highlights").extract()
    for selector in ("#quantity-field", "#artwork-field", "select[name=product]", "select[name=country]"):
        field = contact.select_one(selector)
        (field if field.name == "label" else field.parent).extract()
    contact.textarea["required"] = ""
    contact.textarea.parent.find("small").extract()
    contact.select_one("#inquiry-submit").string = "Send Inquiry"
    standalone("contact", "Contact", contact)

    flagship = []
    product_seed = {}
    for index, element in enumerate(product.main.find_all(recursive=False)):
        heading = element.find(["h1", "h2"])
        title = heading.get_text(" ", strip=True) if heading else "Product section navigation"
        flagship.append(add(f"flagship-{index}", title, element, local=True))
    pages["double-wall-paper-cups"] = {"title": PRODUCTS["double-wall"][1], "widgets": flagship}
    for key, (slug, title) in PRODUCTS.items():
        card = home.select_one(f".product#{key}")
        flagship_hero = product.select_one(".product-hero") if key == "double-wall" else None
        description = ""
        if flagship_hero:
            for section in product.select("#overview, #artwork, #product-documents, #product-faq"):
                copy = soup(str(section))
                for element in copy.select("figure, .eyebrow, a"):
                    element.decompose()
                content = copy.select("h2, h3, p, ol, details")
                description += "".join(str(node) for node in content if not node.find_parent("details"))
        product_seed[key] = {
            "slug": slug,
            "title": title,
            "category": product_categories[key],
            "summary": (flagship_hero.select_one(".lead") if flagship_hero else card.select_one(".card-body > p:not(.eyebrow)")).get_text(" ", strip=True),
            "description": description,
            "images": [
                {"file": asset_name(button.img["src"]), "title": button["data-caption"], "alt": button["data-alt"]}
                for button in flagship_hero.select(".gallery-controls button")
            ] if flagship_hero else [
                {"file": asset_name(card.img["src"]), "title": title, "alt": card.img["alt"]}
            ],
            "specs": {
                row.dt.get_text(strip=True): row.dd.get_text(" ", strip=True)
                for row in flagship_hero.select(".specs > div")
            } if flagship_hero else {
                "Size & fit": "Share your preferred dimensions and lid requirements.",
                "Branding": "Ask about artwork and proof options for your specification.",
                "Order minimum": "Confirmed with your quote.",
            },
        }

    for product_key, (slug, title) in list(PRODUCTS.items())[1:]:
        card = home.select_one(f".product#{product_key}")
        description = card.select_one(".card-body > p:not(.eyebrow)").get_text(strip=True)
        markup = f'''<div class="shell"><nav class="breadcrumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><span aria-hidden="true">/</span><a href="index.html#products">Products</a><span aria-hidden="true">/</span><span aria-current="page">{html.escape(title)}</span></nav>
        <section class="product-hero split"><div class="product-heading"><p class="eyebrow">Custom packaging</p><h1>{html.escape(title)}</h1></div>
        <figure class="visual gallery">{card.img}<figcaption>Concept rendering</figcaption></figure>
        <div class="product-details"><p class="lead">{html.escape(description)}</p>
        <dl class="specs"><div><dt>Sizes and fit</dt><dd>Share your preferred dimensions and lid requirements.</dd></div><div><dt>Custom printing</dt><dd>Ask about artwork and proof options for your specification.</dd></div><div><dt>Order minimum and timing</dt><dd>Confirmed with your quote.</dd></div><div><dt>Documentation</dt><dd>Available records depend on product and destination.</dd></div></dl>
        <div class="actions"><a class="button primary" href="?product={product_key}#quote">Get a Delivered Quote</a><a class="button outline" href="?product={product_key}&amp;intent=sample#quote">Request a Sample Kit</a></div></div></section></div>'''
        pages[slug] = {"title": title, "widgets": [add(f"product-{product_key}", title, markup)]}

    for slug, title, eyebrow, body, action, link in (
        ("for-distributors", "Packaging sourcing for distributors", "Wholesale and distributors", "Share your target format, dimensions, branding, estimated volumes, and destination. We can review sourcing and delivery options for a single project or a recurring packaging program.", "Discuss your requirements", "index.html#quote"),
        ("resources", "Custom packaging resources", "Buyer resources", "Start with artwork requirements, the delivery quote breakdown, and answers to common purchasing questions.", "Read the packaging FAQ", "index.html#faq"),
    ):
        extra = '<a class="text-link" href="index.html#branding">Custom printing</a> <a class="text-link" href="index.html#delivered">Shipping and delivery</a>' if slug == "resources" else ""
        markup = f'<section class="section white"><div class="shell"><div class="section-heading"><p class="eyebrow">{eyebrow}</p><h1>{title}</h1><p>{body}</p><a class="button primary" href="{link}">{action}</a></div>{extra}</div></section>'
        pages[slug] = {"title": title, "widgets": [add(f"page-{slug}", title, markup)]}

    output = Path(sys.argv[1]).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="cups1-elementor-") as work:
        plugin = Path(work) / "cups1-elementor"
        shutil.copytree(ROOT / "plugin", plugin)
        shutil.copytree(PREVIEW / "assets", plugin / "assets")
        logo = ROOT.parents[1] / "brand/logo/final"
        for name in ("cups1-logo-final-nav.png", "cups1-logo-final-nav-reversed.png"):
            shutil.copy2(logo / name, plugin / "assets" / name)
        shutil.copy2(logo / "favicon/favicon.svg", plugin / "assets/favicon.svg")
        css = (PREVIEW / "styles.css").read_text(encoding="utf-8").replace('url("assets/', 'url("../assets/')
        (plugin / "public/design.css").write_text(css, encoding="utf-8")
        design = {"components": definitions, "pages": pages, "home_reference_sections": list(HOME_REFERENCE_SECTIONS), "products": {key: title for key, (_, title) in PRODUCTS.items()}, "product_seed": product_seed}
        (plugin / "design.json").write_text(json.dumps(design, ensure_ascii=False), encoding="utf-8")
        shutil.make_archive(str(output.with_suffix("")), "zip", work)
    print(f"Built {len(pages)} pages and {len(definitions)} editable widgets: {output}")


if __name__ == "__main__":
    main()
