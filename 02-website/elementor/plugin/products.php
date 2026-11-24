<?php

namespace Cups1\ElementorSite;

defined( 'ABSPATH' ) || exit;

function catalog_is_active(): bool {
	return function_exists( 'wc_get_products' ) && (bool) get_option( 'cups1_catalog_imported' );
}

function legacy_product( string $slug ): ?\WC_Product {
	if ( ! catalog_is_active() ) {
		return null;
	}
	$id = get_option( 'cups1_catalog_imported' )[ $slug ] ?? 0;
	$product = $id ? wc_get_product( $id ) : false;
	return $product && 'publish' === $product->get_status() ? $product : null;
}

function product_catalog(): array {
	static $products;
	return $products ??= array_filter( wc_get_products( [
		'status' => 'publish',
		'limit' => -1,
		'orderby' => 'menu_order',
		'order' => 'ASC',
	] ), static fn( $product ) => in_array( $product->get_catalog_visibility(), [ 'visible', 'catalog' ], true ) );
}

function product_inquiry_key( \WC_Product $product ): string {
	return (string) ( $product->get_meta( '_cups1_packaging_key' ) ?: 'wc-' . $product->get_id() );
}

function inquiry_products(): array {
	$names = design()['products'];
	if ( catalog_is_active() ) {
		foreach ( product_catalog() as $product ) {
			$names[ product_inquiry_key( $product ) ] = $product->get_name();
		}
	}
	return $names;
}

function product_options( string $markup ): string {
	if ( ! str_contains( $markup, '<select name="product"' ) || ! catalog_is_active() ) {
		return $markup;
	}
	return preg_replace_callback( '/(<select name="product"[^>]*>).*?(<\/select>)/s', static function ( array $match ): string {
		$options = '<option value="">Select a product</option>';
		foreach ( inquiry_products() as $key => $name ) {
			$options .= '<option value="' . esc_attr( $key ) . '">' . esc_html( $name ) . '</option>';
		}
		return $match[1] . $options . '<option value="other">Other packaging</option>' . $match[2];
	}, $markup );
}

function product_request_url( \WC_Product $product, string $page ): string {
	return resolve_link( '@page/' . $page . '?packaging_product=' . product_inquiry_key( $product ) . '#quote' );
}

function catalog_collections(): array {
	return [ 'cups' => 'Cups', 'lids' => 'Lids', 'containers' => 'Containers', 'ware' => 'Ware' ];
}

function selected_catalog_collection(): string {
	$collection = $_GET['collection'] ?? '';
	return is_string( $collection ) && isset( catalog_collections()[ $collection ] ) ? $collection : '';
}

function product_in_collection( \WC_Product $product, string $collection ): bool {
	$terms = 'containers' === $collection ? [ 'containers', 'food' ] : $collection;
	return has_term( $terms, 'product_cat', $product->get_id() );
}

function catalog_collection_nav(): string {
	$selected = selected_catalog_collection();
	$catalog = resolve_link( '@page/products' );
	ob_start();
	?>
	<nav class="catalog-collections" aria-label="Product collections">
		<?php foreach ( [ '' => 'All Products' ] + catalog_collections() as $slug => $label ) : ?>
			<a class="button outline" href="<?php echo esc_url( $slug ? add_query_arg( 'collection', $slug, $catalog ) : $catalog ); ?>"<?php if ( $slug === $selected ) echo ' aria-current="page"'; ?>><?php echo esc_html( $label ); ?></a>
		<?php endforeach; ?>
		<a class="button outline" href="<?php echo esc_url( resolve_link( '@page/customize' ) ); ?>">Custom Products</a>
		<?php if ( 'yes' !== get_option( 'woocommerce_coming_soon' ) ) : ?>
			<a class="button outline" href="<?php echo esc_url( wc_get_cart_url() ); ?>">View cart</a>
		<?php endif; ?>
	</nav>
	<?php
	return ob_get_clean();
}

function catalog_quote_sizes( \WC_Product $product ): array {
	if ( $product->is_type( 'variable' ) ) {
		$attributes = $product->get_variation_attributes();
		if ( ! empty( $attributes['size'] ) ) {
			return $attributes['size'];
		}
	}
	$size = $product->get_attribute( 'pa_size' ) ?: $product->get_attribute( 'size' );
	if ( $size ) {
		return preg_split( '/\s*(?:\||,)\s*/', trim( $size ), -1, PREG_SPLIT_NO_EMPTY );
	}
	$suggestions = [
		'double-wall' => [ '8 oz', '12 oz', '16 oz' ],
		'single-wall' => [ '4 oz', '8 oz', '12 oz', '16 oz' ],
		'ripple-wall' => [ '8 oz', '12 oz', '16 oz' ],
		'dessert' => [ '4 oz', '8 oz', '12 oz', '16 oz' ],
	];
	return $suggestions[ product_inquiry_key( $product ) ] ?? [];
}

function catalog_cards( ?array $products = null ): string {
	ob_start();
	foreach ( $products ?? product_catalog() as $product ) {
		$categories = wp_get_post_terms( $product->get_id(), 'product_cat', [ 'fields' => 'slugs' ] );
		$categories = is_array( $categories ) ? $categories : [];
		$price = '' !== $product->get_price();
		$can_buy = $price && $product->is_purchasable() && $product->is_in_stock();
		$show_options = $price && $product->is_type( 'variable' );
		$sizes = $price ? [] : catalog_quote_sizes( $product );
		?>
		<article class="card product catalog-product-card" data-catalog-category="<?php echo esc_attr( implode( ' ', $categories ) ); ?>">
			<a href="<?php echo esc_url( $product->get_permalink() ); ?>" data-catalog-product-link tabindex="-1" aria-hidden="true"><?php echo $product->get_image( 'woocommerce_single' ); ?></a>
			<div class="card-body">
				<h3><a href="<?php echo esc_url( $product->get_permalink() ); ?>" data-catalog-product-link><?php echo esc_html( $product->get_name() ); ?></a></h3>

				<?php if ( $sizes ) : ?>
					<label class="catalog-size-picker">
						<span>Size</span>
						<select data-catalog-quote-size>
							<option value="">Choose a size</option>
							<?php foreach ( $sizes as $size ) : ?>
								<option value="<?php echo esc_attr( $size ); ?>"><?php echo esc_html( $size ); ?></option>
							<?php endforeach; ?>
						</select>
					</label>
				<?php endif; ?>
				<?php if ( $show_options ) : ?>
					<?php catalog_purchase_form( $product ); ?>
				<?php elseif ( $price ) : ?>
					<?php catalog_purchase_summary( $product, ! $product->is_in_stock() ? wp_strip_all_tags( wc_get_stock_html( $product ) ) : '' ); ?>
				<?php endif; ?>
				<div class="catalog-tile-actions">
					<?php if ( $price ) : ?>
						<button type="button" class="button primary" data-catalog-cart-item="<?php echo esc_attr( $product->get_id() ); ?>"<?php if ( ! $can_buy ) echo ' data-catalog-unavailable'; ?><?php disabled( ! $can_buy || $show_options ); ?>>Add to cart</button>
					<?php else : ?>
						<a class="button primary" data-inquiry-reason="pricing" data-catalog-quote-link href="<?php echo esc_url( product_request_url( $product, 'request-a-quote' ) ); ?>">Request Pricing</a>
					<?php endif; ?>
					<a class="button outline" data-catalog-quote-link href="<?php echo esc_url( product_request_url( $product, 'configure-packaging' ) ); ?>">Customize</a>
				</div>
			</div>
		</article>
		<?php
	}
	return ob_get_clean();
}

// Reuse shop cards for the empty cart's existing latest-product selection.
add_filter( 'render_block_woocommerce/product-new', function ( string $content ): string {
	if ( ! function_exists( 'is_cart' ) || ! is_cart() || ! catalog_is_active() ) {
		return $content;
	}
	preg_match_all( '/data-product_id="(\d+)"/', $content, $matches );
	$products = [];
	foreach ( array_unique( array_map( 'absint', $matches[1] ) ) as $id ) {
		$product = wc_get_product( $id );
		if ( $product && $product->is_visible() ) {
			$products[] = $product;
		}
	}
	if ( ! $products ) {
		return $content;
	}
	return '<div class="grid catalog-grid cups1-cart-recommendations">' . catalog_cards( $products ) . '</div>';
} );

function catalog_variation_dropdown( array $args ): array {
	$args['selected'] = '';
	if ( in_array( sanitize_title( $args['attribute'] ), [ 'size', 'pa_size' ], true ) ) {
		$args['show_option_none'] = __( 'Choose a size', 'cups1' );
	}
	return $args;
}

function catalog_purchase_form( \WC_Product $item, ?bool $can_buy = null ): void {
	global $product;
	$previous = $product;
	$product = $item;
	$is_card = null === $can_buy;
	$cart_priority = has_action( 'woocommerce_single_variation', 'woocommerce_single_variation_add_to_cart_button' );
	if ( ! $can_buy && false !== $cart_priority ) {
		remove_action( 'woocommerce_single_variation', 'woocommerce_single_variation_add_to_cart_button', $cart_priority );
	}
	if ( $is_card ) {
		add_filter( 'woocommerce_dropdown_variation_attribute_options_args', __NAMESPACE__ . '\\catalog_variation_dropdown' );
	}
	ob_start();
	try {
		woocommerce_template_single_add_to_cart();
	} finally {
		remove_filter( 'woocommerce_dropdown_variation_attribute_options_args', __NAMESPACE__ . '\\catalog_variation_dropdown' );
		$form = ob_get_clean();
		$product = $previous;
		if ( ! $can_buy && false !== $cart_priority ) {
			add_action( 'woocommerce_single_variation', 'woocommerce_single_variation_add_to_cart_button', $cart_priority );
		}
	}
	$markup = new \WP_HTML_Tag_Processor( $form );
	$prefix = 'catalog-' . $item->get_id() . '-';
	while ( $markup->next_tag() ) {
		foreach ( [ 'id', 'for' ] as $attribute ) {
			$value = $markup->get_attribute( $attribute );
			if ( is_string( $value ) && '' !== $value ) {
				$markup->set_attribute( $attribute, $prefix . $value );
			}
		}
	}
	echo '<div class="' . ( $is_card ? 'catalog-card-purchase' : 'catalog-detail-purchase' ) . ( $item->is_type( 'variable' ) ? ' cups1-variation-purchase' : '' ) . '">';
	catalog_purchase_summary( $item );
	echo $markup->get_updated_html() . '</div>';
}

// Pilot the case count editor on Clear PET cold cups.
add_action( 'woocommerce_product_after_variable_attributes', function ( $index, $data, $variation ) {
	if ( 'clear-pet-cold-cups' !== get_post_field( 'post_name', $variation->post_parent ) ) {
		return;
	}
	woocommerce_wp_text_input( [
		'id' => 'cups1_case_quantity_' . $variation->ID,
		'name' => 'cups1_case_quantity[' . $variation->ID . ']',
		'label' => 'Units per case',
		'value' => get_post_meta( $variation->ID, '_cups1_units_per_case', true ),
		'type' => 'number',
		'custom_attributes' => [ 'min' => '1', 'step' => '1' ],
		'wrapper_class' => 'form-row form-row-full',
		'description' => 'Leave blank to use the main product’s case count, if set.',
		'desc_tip' => true,
	] );
}, 10, 3 );

add_action( 'woocommerce_admin_process_variation_object', function ( $variation ) {
	$id = $variation->get_id();
	$value = $_POST['cups1_case_quantity'][ $id ] ?? null;
	if ( ! is_string( $value ) || 'clear-pet-cold-cups' !== get_post_field( 'post_name', $variation->get_parent_id() ) ) {
		return;
	}
	$value = trim( wp_unslash( $value ) );
	if ( '' === $value ) {
		$variation->delete_meta_data( '_cups1_units_per_case' );
	} elseif ( ctype_digit( $value ) && (int) $value > 0 ) {
		$variation->update_meta_data( '_cups1_units_per_case', (string) (int) $value );
	}
} );

function product_case_quantity( \WC_Product $product ): string {
	return (string) ( $product->get_meta( '_cups1_units_per_case' )
		?: $product->get_attribute( 'units-per-case' )
		?: $product->get_attribute( 'pa_units-per-case' ) );
}

function catalog_case_label( string $case ): string {
	if ( '' === $case ) {
		return '';
	}
	if ( ctype_digit( $case ) ) {
		return sprintf( _n( '%s unit per case', '%s units per case', (int) $case, 'cups1' ), number_format_i18n( (int) $case ) );
	}
	if ( preg_match( '/^\d+(?:\s*\|\s*\d+)+$/', $case ) ) {
		$counts = array_map( 'intval', explode( '|', $case ) );
		$case = sprintf( '%s–%s', number_format_i18n( min( $counts ) ), number_format_i18n( max( $counts ) ) );
	}
	return sprintf( __( '%s units per case', 'cups1' ), $case );
}

function catalog_purchase_summary( \WC_Product $product, string $stock = '' ): void {
	$price = $product->get_price_html();
	$case = catalog_case_label( product_case_quantity( $product ) );
	?>
	<div class="catalog-summary" aria-live="polite" aria-atomic="true">
		<p class="catalog-price" data-catalog-price><?php echo $price ? wp_kses_post( $price ) : esc_html( 'Request pricing' ); ?></p>
		<div class="catalog-meta">
			<p class="catalog-case" data-catalog-case<?php if ( '' === $case ) echo ' hidden'; ?>><?php echo esc_html( $case ); ?></p>
			<?php if ( $product->is_type( 'variable' ) || $stock ) : ?>
				<p class="catalog-case" data-catalog-stock<?php if ( '' === $stock ) echo ' hidden'; ?>><?php echo esc_html( $stock ); ?></p>
			<?php endif; ?>
		</div>
	</div>
	<?php
}

add_filter( 'woocommerce_available_variation', function ( array $data, \WC_Product $parent, \WC_Product_Variation $variation ): array {
	if ( catalog_is_active() ) {
		$data['cups1_price_html'] = wp_kses_post( $variation->get_price_html() );
		$data['cups1_case_label'] = catalog_case_label( product_case_quantity( $variation ) ?: product_case_quantity( $parent ) );
		$data['cups1_stock_label'] = '';
		if ( empty( $data['availability_html'] ) && $variation->is_in_stock() && $variation->is_purchasable() ) {
			$data['cups1_stock_label'] = $variation->is_on_backorder() ? __( 'Available on backorder', 'cups1' ) : __( 'In stock', 'cups1' );
		}
	}
	return $data;
}, 10, 3 );

function catalog_business_panel(): string {
	ob_start();
	?>
	<aside class="catalog-business" aria-label="Business orders">
		<div><h2>Ordering for a business?</h2><p>Talk to Cups1 about custom printing, volume orders, and multi-location supply.</p></div>
		<div class="actions">
			<a class="button primary" href="<?php echo esc_url( resolve_link( '@page/contact-sales' ) ); ?>">Contact Sales</a>
			<a class="button outline" href="<?php echo esc_url( resolve_link( '@page/for-business' ) ); ?>">For Business</a>
		</div>
	</aside>
	<?php
	return ob_get_clean();
}

function can_order_online( \WC_Product $product ): bool {
	return 'yes' !== get_option( 'woocommerce_coming_soon' ) && '' !== $product->get_price()
		&& $product->is_type( [ 'simple', 'variable' ] );
}

add_action( 'admin_init', function () {
	if ( ! current_user_can( 'manage_woocommerce' ) || ! catalog_is_active() || get_option( 'cups1_cups_collection_ready' ) ) {
		return;
	}
	$term = term_exists( 'cups', 'product_cat' ) ?: wp_insert_term( 'Cups', 'product_cat', [ 'slug' => 'cups' ] );
	if ( is_wp_error( $term ) ) {
		return;
	}
	$ids = get_option( 'cups1_catalog_imported' );
	foreach ( [ 'double-wall-paper-cups', 'single-wall-paper-cups', 'ripple-wall-paper-cups', 'ice-cream-dessert-cups' ] as $slug ) {
		if ( isset( $ids[ $slug ] ) && 'product' === get_post_type( $ids[ $slug ] ) ) {
			$result = wp_set_object_terms( $ids[ $slug ], [ (int) $term['term_id'] ], 'product_cat', true );
			if ( is_wp_error( $result ) ) {
				return;
			}
		}
	}
	update_option( 'cups1_cups_collection_ready', true );
} );

function import_catalog() {
	if ( ! function_exists( 'wc_get_product' ) ) {
		return new \WP_Error( 'cups1_missing_woocommerce', 'Activate WooCommerce before importing packaging.' );
	}
	if ( catalog_is_active() ) {
		return 'The packaging catalog has already been imported.';
	}
	require_once ABSPATH . 'wp-admin/includes/file.php';
	require_once ABSPATH . 'wp-admin/includes/media.php';
	require_once ABSPATH . 'wp-admin/includes/image.php';

	$ids = [];
	$categories = [ 'beverage' => 'Beverages', 'dessert' => 'Desserts', 'food' => 'Food and takeaway' ];
	foreach ( design()['product_seed'] as $key => $record ) {
		$existing = get_page_by_path( $record['slug'], OBJECT, 'product' );
		$product = $existing ? wc_get_product( $existing->ID ) : false;
		if ( ! $product ) {
			$images = [];
			foreach ( $record['images'] as $image ) {
				$id = import_catalog_image( $image );
				if ( is_wp_error( $id ) ) {
					return $id;
				}
				$images[] = $id;
			}
			$category = term_exists( $record['category'], 'product_cat' ) ?: wp_insert_term(
				$categories[ $record['category'] ], 'product_cat', [ 'slug' => $record['category'] ]
			);
			if ( is_wp_error( $category ) ) {
				return $category;
			}
			$product = new \WC_Product_Simple();
			$product->set_name( $record['title'] );
			$product->set_slug( $record['slug'] );
			$product->set_short_description( $record['summary'] );
			$product->set_description( $record['description'] );
			$product->set_status( 'publish' );
			$product->set_menu_order( count( $ids ) );
			$product->set_image_id( array_shift( $images ) );
			$product->set_gallery_image_ids( $images );
			$product->set_category_ids( [ (int) $category['term_id'] ] );
			$attributes = [];
			foreach ( $record['specs'] as $label => $value ) {
				$attribute = new \WC_Product_Attribute();
				$attribute->set_name( $label );
				$attribute->set_options( [ $value ] );
				$attribute->set_position( count( $attributes ) );
				$attribute->set_visible( true );
				$attributes[] = $attribute;
			}
			$product->set_attributes( $attributes );
			$product->update_meta_data( '_cups1_packaging_key', $key );
			try {
				if ( ! $product->save() ) {
					return new \WP_Error( 'cups1_product_save', 'Could not save ' . $record['title'] . '.' );
				}
			} catch ( \Exception $error ) {
				return new \WP_Error( 'cups1_product_save', $error->getMessage() );
			}
		}
		$ids[ $record['slug'] ] = $product->get_id();
	}
	update_option( 'cups1_catalog_imported', $ids );
	return sprintf( 'The WooCommerce catalog is active with %d migrated product records.', count( $ids ) );
}

function import_catalog_image( array $image ) {
	$existing = get_posts( [
		'post_type' => 'attachment',
		'post_status' => 'inherit',
		'fields' => 'ids',
		'numberposts' => 1,
		'meta_key' => '_cups1_packaging_asset',
		'meta_value' => $image['file'],
	] );
	if ( $existing ) {
		return (int) $existing[0];
	}

	$temporary = wp_tempnam( $image['file'] );
	if ( ! $temporary ) {
		return new \WP_Error( 'cups1_product_image', 'Could not create a temporary product image.' );
	}
	if ( ! copy( __DIR__ . '/assets/' . basename( $image['file'] ), $temporary ) ) {
		unlink( $temporary );
		return new \WP_Error( 'cups1_product_image', 'Could not copy ' . $image['file'] . '.' );
	}
	$id = media_handle_sideload( [ 'name' => $image['file'], 'tmp_name' => $temporary ], 0, $image['title'] );
	if ( is_wp_error( $id ) ) {
		unlink( $temporary );
		return $id;
	}
	update_post_meta( $id, '_wp_attachment_image_alt', $image['alt'] );
	update_post_meta( $id, '_cups1_packaging_asset', $image['file'] );
	return $id;
}

add_filter( 'woocommerce_coming_soon_exclude', function ( $excluded ) {
	return $excluded || is_cups1_shop() || ( catalog_is_active() && is_singular( 'product' ) && 'publish' === get_post_status() );
} );

add_filter( 'template_include', function ( string $template ): string {
	if ( is_cups1_shop() && did_action( 'elementor/loaded' ) ) {
		return __DIR__ . '/shop.php';
	}
	return catalog_is_active() && is_singular( 'product' ) ? __DIR__ . '/single-product.php' : $template;
}, 99 );

add_action( 'template_redirect', function () {
	if ( is_preview() || isset( $_GET['elementor-preview'] ) || ! in_array( $_SERVER['REQUEST_METHOD'] ?? '', [ 'GET', 'HEAD' ], true ) ) {
		return;
	}
	$path = untrailingslashit( (string) wp_parse_url( wp_unslash( $_SERVER['REQUEST_URI'] ?? '' ), PHP_URL_PATH ) );
	$shop_path = untrailingslashit( (string) wp_parse_url( home_url( '/shop/' ), PHP_URL_PATH ) );
	$catalog = (int) ( page_ids()['products'] ?? 0 );
	if ( $path === $shop_path && $catalog && $catalog === (int) get_option( 'woocommerce_shop_page_id' ) ) {
		if ( wp_safe_redirect( add_query_arg( wp_unslash( $_GET ), get_permalink( $catalog ) ), 301 ) ) {
			exit;
		}
	}

	$slug = '';
	if ( is_page() ) {
		$slug = get_post_meta( get_queried_object_id(), '_cups1_component_page', true );
	} elseif ( is_404() && catalog_is_active() ) {
		// Keep the original page URLs working after their Elementor pages are retired.
		$candidate = basename( $path );
		$legacy_path = wp_parse_url( home_url( '/' . $candidate ), PHP_URL_PATH );
		if ( $path === $legacy_path && isset( design()['products'][ $candidate ] ) ) {
			$slug = $candidate;
		}
	}
	$product = $slug ? legacy_product( $slug ) : null;
	if ( $product && wp_safe_redirect( $product->get_permalink(), 301 ) ) {
		exit;
	}
}, 1 );

add_filter( 'elementor/frontend/widget/should_render', function ( bool $render, $widget ): bool {
	if ( (int) get_queried_object_id() !== (int) ( page_ids()['products'] ?? 0 ) || 'html' !== $widget->get_name() ) {
		return $render;
	}
	// The live catalog used an HTML widget for these controls before they moved into the addon.
	return $render && ! str_contains( (string) $widget->get_settings( 'html' ), 'id="cups1-tile-cart-script"' );
}, 10, 2 );
