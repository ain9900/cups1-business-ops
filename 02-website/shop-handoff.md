# Cups1 shop handoff

Open [shop.html](design-review/shop.html) to review the Cups1 shop design. Collection filters, size and pack selectors, and the sample cart work in the browser. The preview uses a snapshot of the CSV and six illustrative products with prices. It has no live checkout.

## Import and complete the catalog

1. In WordPress, go to **Products → All Products → Import** and choose [cups1-products.csv](cups1-products.csv). Check the column mapping, including the parent SKU and attributes. The 41 product parents are set to Draft. Keep the rows for each variation linked to its parent SKU.
2. Compare the proposed products with your approved Cups1 catalog. Replace provisional SKUs where needed and enter your descriptions, photos, supported sizes or fits, and product relationships. Check for existing Cups1 products before importing to avoid duplicates.
3. Set the store currency in WooCommerce. For each sellable variation, enter the regular price and stock status, and optionally the sale price and stock count. Add image URLs if importing photos by CSV. Set a default size or pack to show its price when a card loads. Enter **Units per case** as a product attribute for a fixed count, or use the CSV's `Meta: _cups1_units_per_case` field for a count that changes by variation.
4. Link confirmed matching lids and related items as WooCommerce upsells or cross-sells. Keep made-to-order products without a price so shoppers can select a requested size and start a quote or customization.
5. Install the updated [Cups1 Elementor addon](cups1-elementor.zip) and test a priced product with approved data. With WooCommerce ordering enabled, change the size or pack on the catalog card, open the product, and check that the selected price, case count, image, and stock status are correct. Add an available option to the cart and confirm the exact variation and quantity.

[WooCommerce product CSV documentation](https://woocommerce.com/document/product-csv-importer-exporter/)
