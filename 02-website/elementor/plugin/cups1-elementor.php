<?php
/**
 * Plugin Name: Cups1 Elementor Design
 * Description: Editable Elementor components and site setup for Cups1.
 * Version: 1.8.47
 * Requires PHP: 8.0
 * Requires Plugins: elementor
 */

namespace Cups1\ElementorSite;

defined( 'ABSPATH' ) || exit;

const PLUGIN_FILE = __FILE__;
const VERSION = '1.8.47';

require_once __DIR__ . '/setup.php';
require_once __DIR__ . '/inquiries.php';
require_once __DIR__ . '/inquiry-admin.php';
require_once __DIR__ . '/inquiry-popup.php';
require_once __DIR__ . '/search-metadata.php';
require_once __DIR__ . '/products.php';
require_once __DIR__ . '/purchase-measurement.php';

function design(): array {
	static $design;
	if ( null === $design ) {
		$design = json_decode( file_get_contents( __DIR__ . '/design.json' ), true, 512, JSON_THROW_ON_ERROR );
	}
	return $design;
}

function page_ids(): array {
	return (array) get_option( 'cups1_elementor_pages', [] );
}

function asset_url( string $file ): string {
	return plugins_url( 'assets/' . rawurlencode( basename( $file ) ), PLUGIN_FILE );
}

function resolve_link( string $url ): string {
	if ( ! str_starts_with( $url, '@page/' ) ) {
		return $url;
	}
	[ $route, $fragment ] = array_pad( explode( '#', substr( $url, 6 ), 2 ), 2, '' );
	[ $slug, $query ] = array_pad( explode( '?', $route, 2 ), 2, '' );
	if ( 'woocommerce-account' === $slug && function_exists( 'wc_get_page_permalink' ) ) {
		return wc_get_page_permalink( 'myaccount' );
	}
	$id = page_ids()[ $slug ] ?? 0;
	$product = legacy_product( $slug );
	$permalink = $product ? $product->get_permalink() : ( $id ? get_permalink( $id ) : home_url( '/' ) );
	if ( $query ) {
		wp_parse_str( $query, $args );
		// WooCommerce reserves the public product query variable for product routes.
		if ( isset( $args['product'] ) && in_array( $slug, [ 'request-a-quote', 'request-a-sample' ], true ) ) {
			$args['packaging_product'] = $args['product'];
			unset( $args['product'] );
			$fragment = $fragment ?: 'quote';
		}
		$permalink = add_query_arg( array_map( 'sanitize_text_field', array_filter( $args, 'is_string' ) ), $permalink );
	}
	return $permalink . ( $fragment ? '#' . rawurlencode( $fragment ) : '' );
}

function is_cups1_shop(): bool {
	$catalog_id = (int) ( page_ids()['products'] ?? 0 );
	return $catalog_id && function_exists( 'is_shop' ) && is_shop() && (int) get_queried_object_id() === $catalog_id;
}

function uses_design(): bool {
	return is_cups1_commerce_page() || is_cups1_shop() || is_singular( 'product' ) || ( is_singular() && (bool) get_post_meta( get_queried_object_id(), '_cups1_component_page', true ) );
}

add_action( 'template_redirect', function () {
	$legacy = $_GET['product'] ?? '';
	if ( ! is_string( $legacy ) || ! isset( design()['products'][ $legacy ] ) ) {
		return;
	}
	$request_path = wp_parse_url( wp_unslash( $_SERVER['REQUEST_URI'] ?? '' ), PHP_URL_PATH );
	foreach ( [ 'request-a-quote', 'request-a-sample' ] as $slug ) {
		$id = page_ids()[ $slug ] ?? 0;
		$url = $id ? get_permalink( $id ) : '';
		if ( $url && untrailingslashit( (string) wp_parse_url( $url, PHP_URL_PATH ) ) === untrailingslashit( (string) $request_path ) ) {
			wp_safe_redirect( add_query_arg( 'packaging_product', $legacy, $url ) . '#quote', 301 );
			exit;
		}
	}
}, 0 );

add_action( 'elementor/elements/categories_registered', function ( $manager ) {
	$manager->add_category( 'cups1', [ 'title' => 'Cups1', 'icon' => 'eicon-folder' ] );
} );

add_action( 'elementor/widgets/register', function ( $manager ) {
	require_once __DIR__ . '/widget.php';
	foreach ( design()['components'] as $name => $component ) {
		$manager->register( new Design_Widget( [], [ 'cups1_component' => $name ] ) );
	}
} );

add_filter( 'body_class', function ( array $classes ): array {
	if ( uses_design() ) {
		$classes[] = 'cups1-site';
		$slug = get_post_meta( get_queried_object_id(), '_cups1_component_page', true );
		if ( is_singular( 'product' ) || ( in_array( $slug, array_keys( design()['pages'] ), true ) && str_contains( $slug, 'cups' ) ) ) {
			$classes[] = 'product-page';
		}
	}
	return $classes;
} );

add_action( 'wp_enqueue_scripts', function () {
	if ( ! uses_design() ) {
		return;
	}
	wp_enqueue_style( 'cups1-design', plugins_url( 'public/design.css', PLUGIN_FILE ), [], VERSION );
	wp_enqueue_style( 'cups1-elementor-layout', plugins_url( 'public/elementor.css', PLUGIN_FILE ), [ 'cups1-design' ], VERSION );
	wp_enqueue_script( 'cups1-design', plugins_url( 'public/site.js', PLUGIN_FILE ), [], VERSION, true );
	wp_localize_script( 'cups1-design', 'cups1Navigation', [
		'shop' => resolve_link( '@page/products' ),
		'cart' => function_exists( 'wc_get_cart_url' ) ? wc_get_cart_url() : '',
	] );
	wp_enqueue_script( 'cups1-inquiry-popup', plugins_url( 'public/inquiry-popup.js', PLUGIN_FILE ), [ 'cups1-design' ], VERSION, true );
	$cart_dependencies = [ 'cups1-design' ];
	if ( catalog_is_active() && ( is_cart() || is_singular( 'product' ) || get_queried_object_id() === (int) ( page_ids()['products'] ?? 0 ) ) ) {
		wp_enqueue_script( 'cups1-catalog', plugins_url( 'public/catalog.js', PLUGIN_FILE ), [ 'wc-add-to-cart-variation' ], VERSION, true );
		$cart_dependencies[] = 'cups1-catalog';
	}
	if ( function_exists( 'wc_get_cart_url' ) ) {
		wp_enqueue_script( 'cups1-catalog-cart', plugins_url( 'public/catalog-cart.js', PLUGIN_FILE ), $cart_dependencies, VERSION, true );
		wp_localize_script( 'cups1-catalog-cart', 'cups1CatalogCart', [ 'endpoint' => rest_url( 'wc/store/v1/cart' ), 'cartUrl' => wc_get_cart_url() ] );
	}
}, 30 );

add_action( 'elementor/page_templates/canvas/before_content', function () {
	if ( ! uses_design() || ! ( is_cups1_shop() || is_singular( [ 'page', 'product' ] ) ) ) {
		return;
	}
	$id = page_ids()['header'] ?? 0;
	if ( $id ) {
		echo '<div class="cups1-global-header">' . \Elementor\Plugin::$instance->frontend->get_builder_content_for_display( $id ) . '</div>';
	}
	echo '<main id="main" tabindex="-1">';
} );

add_action( 'elementor/page_templates/canvas/after_content', function () {
	if ( ! uses_design() || ! ( is_cups1_shop() || is_singular( [ 'page', 'product' ] ) ) ) {
		return;
	}
	echo '</main>';
	$id = page_ids()['footer'] ?? 0;
	if ( $id ) {
		echo \Elementor\Plugin::$instance->frontend->get_builder_content_for_display( $id );
		echo get_the_privacy_policy_link( '<div class="shell cups1-privacy-link">', '</div>' );
	}
} );


function is_cups1_commerce_page(): bool {
	return function_exists( 'is_cart' ) && ( is_cart() || is_checkout() || is_account_page() );
}


add_action( 'template_redirect', function () {
	if ( ! is_cups1_commerce_page() || ! did_action( 'elementor/loaded' ) || is_preview() || ! is_page() ) {
		return;
	}
	add_filter( 'template_include', __NAMESPACE__ . '\\render_commerce_page', 100 );
}, 20 );

function render_commerce_page( string $template ): string {
	if ( ! current_user_can( 'manage_woocommerce' ) && 'yes' === get_option( 'woocommerce_coming_soon' ) ) {
		return $template;
	}
	$title = is_order_received_page() ? 'Order confirmation' : ( is_cart() ? 'Your cart' : get_the_title() );
	?>
	<!doctype html>
	<html <?php language_attributes(); ?>>
	<head>
		<meta charset="<?php bloginfo( 'charset' ); ?>">
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<?php if ( ! current_theme_supports( 'title-tag' ) ) : ?><title><?php echo esc_html( wp_get_document_title() ); ?></title><?php endif; ?>
		<?php wp_head(); ?>
	</head>
	<body <?php body_class(); ?>>
	<?php wp_body_open(); ?>
	<?php do_action( 'elementor/page_templates/canvas/before_content' ); ?>
	<section class="shell cups1-commerce" aria-labelledby="cups1-commerce-title">
		<?php if ( is_cart() ) : ?>
			<a class="text-link" href="<?php echo esc_url( wc_get_page_permalink( 'shop' ) ); ?>">Continue shopping</a>
		<?php endif; ?>
		<h1 id="cups1-commerce-title"><?php echo esc_html( $title ); ?></h1>
		<?php while ( have_posts() ) : the_post(); the_content(); endwhile; ?>
	</section>
	<?php do_action( 'elementor/page_templates/canvas/after_content' ); ?>
	<?php wp_footer(); ?>
	</body>
	</html>
	<?php
	exit;
}

add_filter( 'option_woocommerce_checkout_company_field', static fn( $value ) => 'hidden' === $value ? 'optional' : $value );
add_filter( 'default_option_woocommerce_checkout_company_field', static fn() => 'optional' );
