<?php

namespace Cups1\ElementorSite;

defined( 'ABSPATH' ) || exit;

add_action( 'template_redirect', function () {
	if ( ! function_exists( 'is_order_received_page' ) || ! is_order_received_page() ) {
		return;
	}
	$endpoint = get_option( 'woocommerce_checkout_order_received_endpoint', 'order-received' );
	$order_id = $endpoint ? absint( get_query_var( $endpoint ) ) : 0;
	$order_key = $_GET['key'] ?? '';
	if ( ! $order_id || ! is_string( $order_key ) || '' === $order_key ) {
		return;
	}
	$order = wc_get_order( $order_id );
	if ( ! $order instanceof \WC_Order || ! hash_equals( $order->get_order_key(), wp_unslash( $order_key ) ) ) {
		return;
	}
	if ( $order->get_customer_id() && $order->get_customer_id() !== get_current_user_id() ) {
		return;
	}
	$payload = paid_purchase_payload( $order );
	if ( ! $payload ) {
		return;
	}
	nocache_headers();
	add_action( 'wp_footer', static function () use ( $payload ) {
		$json = wp_json_encode( $payload, JSON_HEX_TAG | JSON_HEX_AMP | JSON_HEX_APOS | JSON_HEX_QUOT );
		if ( $json ) {
			wp_print_inline_script_tag( 'window.dataLayer = window.dataLayer || []; window.dataLayer.push(' . $json . ');' );
		}
	}, 30 );
}, 20 );

function paid_purchase_payload( \WC_Order $order ): array {
	$currency = $order->get_currency();
	if ( ! $order->is_paid() || ! $order->get_date_paid() || (float) $order->get_total() <= 0 || ! preg_match( '/^[A-Z]{3}$/', $currency ) ) {
		return [];
	}
	// The COD gateway can move an order to processing before cash is collected.
	if ( 'cod' === $order->get_payment_method() && ! $order->has_status( 'completed' ) ) {
		return [];
	}
	$items = [];
	$value = 0.0;
	foreach ( $order->get_items() as $item ) {
		$id = $item->get_variation_id() ?: $item->get_product_id();
		$quantity = $item->get_quantity();
		$line_total = (float) $item->get_total();
		if ( ! $id || $quantity <= 0 || $line_total < 0 ) {
			continue;
		}
		$items[] = [
			'item_id'   => (string) $id,
			'item_name' => $item->get_name(),
			'quantity'  => $quantity,
			'price'     => $line_total / $quantity,
		];
		$value += $line_total;
	}
	if ( ! $items ) {
		return [];
	}
	return [
		'event'          => 'cups1_paid_order_ready',
		'cups1_purchase' => [
			'transaction_id' => (string) $order->get_id(),
			'currency'       => $currency,
			'value'          => round( $value, wc_get_price_decimals() ),
			'tax'            => (float) $order->get_total_tax(),
			'shipping'       => (float) $order->get_shipping_total(),
			'items'          => $items,
			'page_location'  => strtok( wc_get_checkout_url(), '?#' ),
		],
	];
}
