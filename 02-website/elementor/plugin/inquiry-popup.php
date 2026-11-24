<?php

namespace Cups1\ElementorSite;

defined( 'ABSPATH' ) || exit;

const POPUP_REASONS = [
	'quote' => 'Request a quote',
	'pricing' => 'Request pricing',
	'sample' => 'Request samples',
	'contact' => 'Contact sales',
	'customize' => 'Customize packaging',
];

add_action( 'wp_footer', function () {
	if ( ! uses_design() ) {
		return;
	}
	$sizes = [];
	if ( catalog_is_active() ) {
		foreach ( product_catalog() as $product ) {
			$sizes[ product_inquiry_key( $product ) ] = catalog_quote_sizes( $product );
		}
	}
	?>
	<dialog class="cups1-inquiry-popup" data-inquiry-popup aria-labelledby="cups1-popup-title">
		<header class="cups1-popup-header">
			<button type="button" class="cups1-popup-close" aria-label="Close inquiry">×</button>
			<p class="cups1-popup-progress" data-popup-progress>Step 1 of 2</p>
			<h2 id="cups1-popup-title" tabindex="-1" autofocus>Your inquiry</h2>
			<p class="cups1-popup-context" data-popup-context hidden></p>
		</header>
		<form action="<?php echo esc_url( admin_url( 'admin-ajax.php' ) ); ?>" method="post">
			<div class="cups1-popup-scroll">
			<fieldset data-popup-step="contact">
				<legend class="screen-reader-text">Contact details</legend>
				<div class="cups1-popup-fields">
				<label>Full name<input name="name" autocomplete="name" maxlength="160" required></label>
				<label>Work email<input name="email" type="email" autocomplete="email" maxlength="254" required></label>
				<label>Company name<input name="company" autocomplete="organization" maxlength="200" required></label>
				<label>Reason for inquiry
					<select name="reason" required>
						<?php foreach ( POPUP_REASONS as $value => $label ) : ?>
							<option value="<?php echo esc_attr( $value ); ?>"><?php echo esc_html( $label ); ?></option>
						<?php endforeach; ?>
					</select>
				</label>
				</div>
			</fieldset>
			<fieldset data-popup-step="details" hidden disabled>
				<legend class="screen-reader-text">Request details</legend>
				<div class="cups1-popup-fields">
				<label data-reasons="quote pricing sample customize">Product
					<select name="product" required>
						<option value="">Choose a product</option>
						<?php foreach ( inquiry_products() + [ 'other' => 'Other packaging' ] as $value => $label ) : ?>
							<option value="<?php echo esc_attr( $value ); ?>" data-sizes="<?php echo esc_attr( wp_json_encode( $sizes[ $value ] ?? [] ) ); ?>"><?php echo esc_html( $label ); ?></option>
						<?php endforeach; ?>
					</select>
				</label>
				<label data-reasons="quote pricing sample customize">Size or dimensions <small>Optional</small><input name="dimensions" maxlength="120" list="cups1-popup-sizes" placeholder="e.g. 12 oz"><datalist id="cups1-popup-sizes"></datalist></label>
				<label data-reasons="quote pricing customize">Quantity<input name="quantity" type="number" min="1" step="1" required></label>
				<label data-reasons="quote pricing customize">Print preference
					<select name="print_preference"><option value="">Choose a preference</option><option value="single">Single color</option><option value="multi">Multiple colors</option><option value="plain">Unprinted</option><option value="help">I need help choosing</option></select>
				</label>
				<label data-reasons="quote pricing sample customize">Delivery country
					<select name="country" required><option value="">Choose a country</option><option>United States</option><option>Canada</option></select>
				</label>
				<label data-reasons="quote pricing sample customize"><span data-popup-postal>ZIP or postal code</span> <small>Optional</small><input name="postal_code" autocomplete="postal-code" maxlength="24"></label>
				<label class="cups1-popup-wide" data-reasons="sample">Shipping address <small>Optional</small><input name="shipping_address" autocomplete="street-address" maxlength="500"></label>
				<label class="cups1-popup-wide">Tell us what you need <small data-popup-notes-optional>Optional</small><textarea name="notes" maxlength="8000" rows="3"></textarea></label>
				<details class="cups1-popup-wide cups1-popup-artwork" data-reasons="quote pricing customize">
					<summary>Add artwork <small>Optional</small></summary>
					<input name="artwork" type="file" accept=".pdf,.png,.jpg,.jpeg" aria-label="Artwork file" aria-describedby="cups1-artwork-help">
					<span class="cups1-popup-help" id="cups1-artwork-help">PDF, PNG, or JPEG up to 5 MB.</span>
				</details>
				</div>
			</fieldset>
			</div>
			<div hidden><label>Leave blank<input name="website" tabindex="-1" autocomplete="off"></label></div>
			<footer class="cups1-popup-footer">
				<p data-popup-consent>By clicking Next, you agree that Cups1 may contact you about this request. <?php echo get_the_privacy_policy_link(); ?></p>
				<p data-popup-status role="status"></p>
				<button class="button primary" type="submit">Next</button>
			</footer>
		</form>
	</dialog>
	<?php
} );

add_action( 'wp_ajax_cups1_inquiry_step', __NAMESPACE__ . '\\submit_popup_inquiry' );
add_action( 'wp_ajax_nopriv_cups1_inquiry_step', __NAMESPACE__ . '\\submit_popup_inquiry' );

function submit_popup_inquiry(): void {
	$result = save_popup_inquiry();
	if ( is_wp_error( $result ) ) {
		wp_send_json_error( [ 'message' => inquiry_error_message( $result->get_error_code() ) ], 422 );
	}
	wp_send_json_success( [ 'reference' => $result ] );
}

function save_popup_inquiry() {
	global $wpdb;
	$token = posted_value( 'token' );
	$step = posted_value( 'step' );
	if ( 'POST' !== ( $_SERVER['REQUEST_METHOD'] ?? '' ) || ! wp_verify_nonce( posted_value( 'cups1_nonce' ), 'cups1_inquiry' ) ) {
		return new \WP_Error( 'expired' );
	}
	if ( posted_value( 'website' ) || ! preg_match( '/^[a-f0-9]{32}$/D', $token ) || ! in_array( $step, [ 'contact', 'details' ], true ) ) {
		return new \WP_Error( 'invalid' );
	}
	$key = hash_hmac( 'sha256', $token, wp_salt( 'nonce' ) );
	if ( '1' !== (string) $wpdb->get_var( $wpdb->prepare( 'SELECT GET_LOCK(%s, 3)', $key ) ) ) {
		return new \WP_Error( 'save_error' );
	}
	try {
		return persist_popup_step( $key, $step );
	} finally {
		$wpdb->get_var( $wpdb->prepare( 'SELECT RELEASE_LOCK(%s)', $key ) );
	}
}

function persist_popup_step( string $key, string $step ) {
	$id = (int) ( get_posts( [
		'post_type' => 'cups1_inquiry',
		'post_status' => 'private',
		'posts_per_page' => 1,
		'fields' => 'ids',
		'name' => 'popup-' . $key,
	] )[0] ?? 0 );
	$reference = strtoupper( substr( $key, 0, 12 ) );
	$products = inquiry_products() + [ 'other' => 'Other packaging' ];
	$product = sanitize_key( posted_value( 'product' ) );
	if ( 'contact' === $step ) {
		if ( $id ) {
			return $reference;
		}
		$name = sanitize_text_field( posted_value( 'name' ) );
		$email = sanitize_email( posted_value( 'email' ) );
		$company = sanitize_text_field( posted_value( 'company' ) );
		$reason = posted_value( 'reason' );
		$size = sanitize_text_field( posted_value( 'selected_size' ) );
		if ( ! $name || mb_strlen( $name ) > 160 || ! is_email( $email ) || strlen( $email ) > 254 || ! $company || mb_strlen( $company ) > 200 || ! isset( POPUP_REASONS[ $reason ] ) || mb_strlen( $size ) > 120 ) {
			return new \WP_Error( 'invalid' );
		}
		$rate_key = 'cups1_popup_' . substr( hash_hmac( 'sha256', $_SERVER['REMOTE_ADDR'] ?? '', wp_salt( 'nonce' ) ), 0, 32 );
		$attempts = (int) get_transient( $rate_key );
		if ( $attempts >= 10 ) {
			return new \WP_Error( 'limit' );
		}
		set_transient( $rate_key, $attempts + 1, 10 * MINUTE_IN_SECONDS );
		$details = array_filter( [
			'Status' => 'Incomplete',
			'Request type' => POPUP_REASONS[ $reason ],
			'Name' => $name,
			'Business email' => $email,
			'Company' => $company,
			'Product' => $products[ $product ] ?? '',
			'Size or dimensions' => $size,
			'Contact consent recorded (UTC)' => gmdate( 'Y-m-d H:i:s' ),
		] );
		$id = wp_insert_post( [
			'post_type' => 'cups1_inquiry',
			'post_status' => 'private',
			'post_name' => 'popup-' . $key,
			'post_title' => $reference . ' · ' . POPUP_REASONS[ $reason ] . ' · Incomplete',
			'meta_input' => wp_slash( [ '_cups1_details' => $details ] ),
		], true );
		if ( ! $id || is_wp_error( $id ) ) {
			return new \WP_Error( 'save_error' );
		}
		if ( get_post_meta( $id, '_cups1_details', true ) !== $details ) {
			wp_delete_post( $id, true );
			return new \WP_Error( 'save_error' );
		}
		return $reference;
	}

	$details = $id ? get_post_meta( $id, '_cups1_details', true ) : [];
	$reason = array_search( $details['Request type'] ?? '', POPUP_REASONS, true );
	if ( false === $reason ) {
		return new \WP_Error( 'invalid' );
	}
	if ( 'Complete' !== $details['Status'] ) {
		$specification = quote_specification();
		$country = posted_value( 'country' );
		$quantity = filter_var( posted_value( 'quantity' ), FILTER_VALIDATE_INT, [ 'options' => [ 'min_range' => 1 ] ] );
		$notes = sanitize_textarea_field( posted_value( 'notes' ) );
		$address = sanitize_textarea_field( posted_value( 'shipping_address' ) );
		if ( is_wp_error( $specification ) || mb_strlen( $notes ) > 8000 || mb_strlen( $address ) > 500
			|| ( 'contact' === $reason && ! $notes )
			|| ( 'contact' !== $reason && ( ! isset( $products[ $product ] ) || ! in_array( $country, [ 'United States', 'Canada' ], true ) ) )
			|| ( in_array( $reason, [ 'quote', 'pricing', 'customize' ], true ) && ! $quantity ) ) {
			return new \WP_Error( 'invalid' );
		}
		$artwork = validate_artwork( $_FILES['artwork'] ?? [] );
		if ( is_wp_error( $artwork ) ) {
			return $artwork;
		}
		if ( $artwork ) {
			foreach ( $artwork as $field => $value ) {
				$meta_key = '_cups1_artwork_' . $field;
				update_post_meta( $id, $meta_key, wp_slash( $value ) );
				if ( get_post_meta( $id, $meta_key, true ) !== $value ) {
					return new \WP_Error( 'save_error' );
				}
			}
		}
		$details = array_replace( $details, array_filter( [
			'Product' => $products[ $product ] ?? '',
			'Delivery country' => $country,
			'Quantity' => $quantity ? (string) $quantity : '',
			'Shipping address' => $address,
			'Notes' => $notes,
		] + $specification ), [ 'Status' => 'Complete' ] );
		update_post_meta( $id, '_cups1_details', wp_slash( $details ) );
		if ( get_post_meta( $id, '_cups1_details', true ) !== $details ) {
			return new \WP_Error( 'save_error' );
		}
	}
	$title = $reference . ' · ' . POPUP_REASONS[ $reason ] . ' · Complete';
	if ( get_post_field( 'post_title', $id ) !== $title && is_wp_error( wp_update_post( [ 'ID' => $id, 'post_title' => $title ], true ) ) ) {
		return new \WP_Error( 'save_error' );
	}
	return $reference;
}
