<?php

namespace Cups1\ElementorSite;

defined( 'ABSPATH' ) || exit;

function has_seo_plugin(): bool {
	return defined( 'WPSEO_VERSION' ) || defined( 'RANK_MATH_VERSION' ) || defined( 'AIOSEO_VERSION' ) || defined( 'SEOPRESS_VERSION' );
}

function search_summary( string $text ): string {
	return wp_html_excerpt( trim( wp_strip_all_tags( strip_shortcodes( $text ), true ) ), 160, '…' );
}

function search_description( $product = null ): string {
	if ( $product ) {
		$summary = search_summary( $product->get_short_description() );
		return $summary ?: sprintf( 'Explore %s from Cups1. Check available sizes and ask about case quantities, custom printing, and delivery.', $product->get_name() );
	}

	if ( is_tax( 'product_cat' ) ) {
		$term = get_queried_object();
		$summary = search_summary( $term->description );
		return $summary ?: sprintf( 'Browse %s from Cups1. Compare packaging formats for your business and request pricing for US or Canadian delivery.', $term->name );
	}

	$slug = get_post_meta( get_queried_object_id(), '_cups1_component_page', true );
	if ( is_cups1_shop() ) {
		$slug = 'products';
	}
	$descriptions = [
		'home' => 'Source custom-printed paper cups, food bowls, and takeaway packaging for cafés, restaurants, and distributors. Request a delivered quote for the US or Canada.',
		'products' => 'Explore Cups1 packaging for beverages, desserts, and takeaway. Compare formats and request a quote for the product you need.',
		'customize' => 'Choose a packaging format and share your dimensions, branding, quantity, and artwork for a custom quote from Cups1.',
		'custom-printing' => 'See how Cups1 coordinates logo placement, brand colors, artwork preparation, and proof review for custom packaging.',
		'how-it-works' => 'Learn how to request a packaging quote, review your artwork proof, and coordinate production and delivery with Cups1.',
		'industries' => 'Explore custom packaging options for cafés, restaurant groups, and wholesale buyers in the US and Canada.',
		'documents' => 'Ask Cups1 about product specifications, available reports, and inspection records for your packaging and destination.',
		'about' => 'Learn how Cups1 coordinates supplier sourcing, artwork proofs, quality review, and cross-border delivery for custom packaging.',
		'faq' => 'Find answers about custom packaging, artwork, order minimums, samples, delivery, and product documentation.',
		'shipping-delivery' => 'See what goes into a Cups1 delivered quote, including setup, freight, applicable duties, and destination delivery.',
		'request-a-quote' => 'Request a delivered quote for custom paper cups or food packaging. Share the product, order quantity, destination, and artwork if available.',
		'request-a-sample' => 'Request a Cups1 sample kit to compare packaging formats, materials, and fit before placing a custom order.',
		'contact' => 'Contact Cups1 with questions about custom packaging, artwork, delivery, or product documentation.',
		'for-distributors' => 'Discuss custom packaging sourcing and delivery options for a wholesale project or a recurring supply program.',
		'resources' => 'Find buyer guides to Cups1 custom printing, delivered quote costs, and common packaging questions.',
	];
	if ( isset( $descriptions[ $slug ] ) ) {
		return $descriptions[ $slug ];
	}
	if ( isset( design()['pages'][ $slug ] ) ) {
		return sprintf( 'Explore %s from Cups1. Ask about size, custom printing, samples, and delivered quotes for the US and Canada.', get_the_title() );
	}
	return '';
}

// Site identity applies to every public template, including WooCommerce archives.
add_action( 'wp_head', function () {
	if ( ! has_site_icon() ) {
		echo '<link rel="icon" type="image/svg+xml" href="' . esc_url( asset_url( 'favicon.svg' ) ) . '">' . "\n";
	}
}, 5 );

function is_filtered_catalog(): bool {
	$catalog_id = (int) ( page_ids()['products'] ?? 0 );
	if ( ! is_cups1_shop() && ! is_tax( 'product_cat' ) && ! ( $catalog_id && is_page( $catalog_id ) ) ) {
		return false;
	}
	foreach ( [ 'packaging', 'collection', 'format', 'sort', 'orderby', 'min_price', 'max_price', 'rating_filter' ] as $key ) {
		if ( isset( $_GET[ $key ] ) && '' !== $_GET[ $key ] ) {
			return true;
		}
	}
	return false;
}

function search_canonical(): string {
	if ( is_singular() ) {
		return (string) wp_get_canonical_url( get_queried_object_id() );
	}
	if ( is_paged() ) {
		return '';
	}
	if ( is_cups1_shop() ) {
		return (string) get_permalink( page_ids()['products'] );
	}
	$link = is_tax( 'product_cat' ) ? get_term_link( get_queried_object() ) : '';
	return is_wp_error( $link ) ? '' : $link;
}

add_action( 'wp_head', function () {
	if ( has_seo_plugin() || is_preview() || is_cups1_commerce_page() || is_filtered_catalog() || is_paged() ) {
		return;
	}
	if ( ! uses_design() && ! is_tax( 'product_cat' ) ) {
		return;
	}
	$product = is_singular( 'product' ) && function_exists( 'wc_get_product' ) ? wc_get_product( get_queried_object_id() ) : null;
	$description = search_description( $product );
	$canonical = search_canonical();
	if ( ! $description || ! $canonical ) {
		return;
	}
	if ( ! is_singular() ) {
		echo '<link rel="canonical" href="' . esc_url( $canonical ) . '">' . "\n";
	}
	echo '<meta name="description" content="' . esc_attr( $description ) . '">' . "\n";
	$image_id = $product ? $product->get_image_id() : ( is_singular() ? get_post_thumbnail_id() : 0 );
	$image = $image_id ? wp_get_attachment_image_url( $image_id, 'large' ) : '';
	$social = [
		'og:title' => wp_get_document_title(),
		'og:description' => $description,
		'og:type' => $product ? 'product' : 'website',
		'og:url' => $canonical,
		'og:image' => $image ?: asset_url( 'hero.webp' ),
		'og:site_name' => get_bloginfo( 'name' ),
	];
	foreach ( $social as $property => $value ) {
		echo '<meta property="' . esc_attr( $property ) . '" content="' . esc_attr( $value ) . '">' . "\n";
	}
	echo '<meta name="twitter:card" content="summary_large_image">' . "\n";
}, 5 );

// The custom product template bypasses WooCommerce's native product and breadcrumb hooks.
function print_product_schema( \WC_Product $product ): void {
	if ( has_seo_plugin() || is_preview() || post_password_required( $product->get_id() ) ) {
		return;
	}
	$url = $product->get_permalink();
	$schema = array_filter( [
		'@type' => 'Product',
		'@id' => $url . '#product',
		'name' => $product->get_name(),
		'url' => $url,
		'description' => search_description( $product ),
		'image' => wp_get_attachment_image_url( $product->get_image_id(), 'full' ),
		'sku' => $product->get_sku(),
	], static fn( $value ) => false !== $value && '' !== $value );
	$crumbs = [];
	foreach ( [ [ 'Home', home_url( '/' ) ], [ 'Products', resolve_link( '@page/products' ) ], [ $product->get_name(), $url ] ] as [ $name, $link ] ) {
		$crumbs[] = [ '@type' => 'ListItem', 'position' => count( $crumbs ) + 1, 'name' => $name, 'item' => $link ];
	}
	$graph = [
		'@context' => 'https://schema.org',
		'@graph' => [ $schema, [ '@type' => 'BreadcrumbList', 'itemListElement' => $crumbs ] ],
	];
	// Offer markup stays disabled until pricing, stock, shipping and payments are approved.
	echo '<script type="application/ld+json">' . wp_json_encode( $graph, JSON_HEX_TAG | JSON_HEX_AMP | JSON_HEX_APOS | JSON_HEX_QUOT ) . '</script>' . "\n";
}

add_filter( 'document_title_parts', function ( array $parts ): array {
	if ( is_front_page() && uses_design() ) {
		$parts['tagline'] = 'Custom Branded Cups & Food Packaging';
	}
	return $parts;
} );

add_filter( 'wp_robots', function ( array $robots ): array {
	if ( is_filtered_catalog() || is_cups1_commerce_page() || ( uses_design() && isset( $_GET['inquiry'] ) ) ) {
		$robots['noindex'] = true;
	}
	return $robots;
} );

add_filter( 'wp_sitemaps_posts_query_args', function ( array $args, string $post_type ): array {
	if ( 'page' !== $post_type || empty( page_ids()['home'] ) || ! function_exists( 'wc_get_page_id' ) ) {
		return $args;
	}
	$excluded = $args['post__not_in'] ?? [];
	foreach ( [ 'cart', 'checkout', 'myaccount' ] as $page ) {
		$id = wc_get_page_id( $page );
		if ( $id > 0 ) {
			$excluded[] = (int) $id;
		}
	}
	$args['post__not_in'] = array_values( array_unique( $excluded ) );
	return $args;
}, 10, 2 );
