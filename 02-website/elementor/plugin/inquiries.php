<?php

namespace Cups1\ElementorSite;

defined( 'ABSPATH' ) || exit;

add_action( 'init', function () {
	register_post_type( 'cups1_inquiry', [
		'labels' => [ 'name' => 'Cups1 Inquiries', 'singular_name' => 'Cups1 Inquiry', 'edit_item' => 'Cups1 Inquiry' ],
		'public' => false,
		'show_ui' => true,
		'show_in_rest' => false,
		'menu_icon' => 'dashicons-email-alt',
		'supports' => [ 'title' ],
		'capability_type' => 'post',
		'capabilities' => array_fill_keys( [ 'edit_post', 'read_post', 'delete_post', 'edit_posts', 'edit_others_posts', 'delete_posts', 'publish_posts', 'read_private_posts' ], 'manage_options' ) + [ 'create_posts' => 'do_not_allow' ],
		'map_meta_cap' => false,
	] );
} );

add_action( 'add_meta_boxes_cups1_inquiry', function () {
	add_meta_box( 'cups1_inquiry_data', 'Inquiry details', __NAMESPACE__ . '\inquiry_details', 'cups1_inquiry' );
} );

function inquiry_details( \WP_Post $post ): void {
	$data = (array) get_post_meta( $post->ID, '_cups1_details', true );
	echo '<div class="cups1-inquiry-summary">';
	echo '<strong>' . esc_html( $data['Request type'] ?? 'Newsletter signup' ) . '</strong>';
	echo inquiry_admin_status( $data );
	echo '</div>';
	$groups = [
		'Contact' => array_intersect_key( $data, array_flip( [ 'Name', 'Business email', 'Email', 'Company' ] ) ),
		'Request' => array_diff_key( $data, array_flip( [ 'Status', 'Request type', 'Name', 'Business email', 'Email', 'Company', 'Notes', 'Contact consent recorded (UTC)', 'Signup recorded (UTC)' ] ) ),
		'Notes' => array_intersect_key( $data, [ 'Notes' => true ] ),
		'Activity' => array_intersect_key( $data, array_flip( [ 'Contact consent recorded (UTC)', 'Signup recorded (UTC)' ] ) ),
	];
	foreach ( $groups as $heading => $fields ) {
		if ( ! $fields ) {
			continue;
		}
		echo '<section class="cups1-inquiry-section"><h3>' . esc_html( $heading ) . '</h3><dl>';
		foreach ( $fields as $label => $value ) {
			$content = nl2br( esc_html( $value ) );
			if ( in_array( $label, [ 'Business email', 'Email' ], true ) && is_email( $value ) ) {
				$content = '<a href="' . esc_url( 'mailto:' . $value ) . '">' . $content . '</a>';
			}
			echo '<div><dt>' . esc_html( $label ) . '</dt><dd>' . $content . '</dd></div>';
		}
		echo '</dl></section>';
	}
	if ( get_post_meta( $post->ID, '_cups1_artwork_name', true ) ) {
		$url = add_query_arg( [ 'action' => 'cups1_download_artwork', 'id' => $post->ID ], admin_url( 'admin-post.php' ) );
		echo '<p><a class="button" href="' . esc_url( wp_nonce_url( $url, 'cups1_artwork_' . $post->ID ) ) . '">Download private artwork</a></p>';
	}
}

add_action( 'admin_post_cups1_download_artwork', function () {
	$id = absint( $_GET['id'] ?? 0 );
	if ( ! current_user_can( 'manage_options' ) || 'cups1_inquiry' !== get_post_type( $id ) ) {
		wp_die( 'Access denied.', '', [ 'response' => 403 ] );
	}
	check_admin_referer( 'cups1_artwork_' . $id );
	$contents = base64_decode( (string) get_post_meta( $id, '_cups1_artwork_data', true ), true );
	$name = sanitize_file_name( get_post_meta( $id, '_cups1_artwork_name', true ) );
	if ( ! $contents || ! $name ) {
		wp_die( 'Artwork not found.', '', [ 'response' => 404 ] );
	}
	nocache_headers();
	header( 'Content-Type: application/octet-stream' );
	header( 'X-Content-Type-Options: nosniff' );
	header( 'Content-Disposition: attachment; filename*=UTF-8\'\'' . rawurlencode( $name ) );
	echo $contents;
	exit;
} );

add_action( 'wp_ajax_cups1_form_token', __NAMESPACE__ . '\form_token' );
add_action( 'wp_ajax_nopriv_cups1_form_token', __NAMESPACE__ . '\form_token' );
function form_token(): void {
	wp_send_json_success( [ 'nonce' => wp_create_nonce( 'cups1_inquiry' ) ] );
}

add_action( 'admin_post_cups1_inquiry', __NAMESPACE__ . '\submit_inquiry' );
add_action( 'admin_post_nopriv_cups1_inquiry', __NAMESPACE__ . '\submit_inquiry' );
function submit_inquiry(): void {
	$target = absint( $_POST['return_page'] ?? 0 );
	if ( ! in_array( $target, array_map( 'intval', page_ids() ), true ) || 'publish' !== get_post_status( $target ) ) {
		$target = page_ids()['request-a-quote'] ?? 0;
	}
	$result = process_inquiry();
	$newsletter = 'newsletter' === posted_value( 'intent' );
	if ( str_contains( $_SERVER['HTTP_ACCEPT'] ?? '', 'application/json' ) ) {
		nocache_headers();
		if ( is_wp_error( $result ) ) {
			wp_send_json_error( [ 'message' => inquiry_error_message( $result->get_error_code() ) ], 422 );
		}
		$message = $newsletter ? 'Your signup was recorded.' : 'Your inquiry was received. Reference: ' . $result . '.';
		wp_send_json_success( [ 'message' => $message ], 201 );
	}
	$params = is_wp_error( $result ) ? [ 'inquiry' => $result->get_error_code() ] : [ 'inquiry' => 'received', 'reference' => $result ];
	$url = $target ? get_permalink( $target ) : home_url( '/' );
	if ( $newsletter && ! is_wp_error( $result ) ) {
		$params = [ 'inquiry' => 'subscribed' ];
	}
	wp_safe_redirect( add_query_arg( $params, $url ) . ( $newsletter ? '#cups1-newsletter' : '#quote' ), 303 );
	exit;
}

function posted_value( string $key ): string {
	$value = $_POST[ $key ] ?? '';
	return is_string( $value ) ? wp_unslash( $value ) : '';
}

function process_inquiry() {
	if ( 'POST' !== ( $_SERVER['REQUEST_METHOD'] ?? '' ) || ! wp_verify_nonce( posted_value( 'cups1_nonce' ), 'cups1_inquiry' ) ) {
		return new \WP_Error( 'expired' );
	}
	if ( '' !== posted_value( 'website' ) ) {
		return new \WP_Error( 'invalid' );
	}
	$rate_key = 'cups1_inq_' . substr( hash_hmac( 'sha256', $_SERVER['REMOTE_ADDR'] ?? '', wp_salt( 'nonce' ) ), 0, 32 );
	$attempts = (int) get_transient( $rate_key );
	if ( $attempts >= 10 ) {
		return new \WP_Error( 'limit' );
	}
	set_transient( $rate_key, $attempts + 1, 10 * MINUTE_IN_SECONDS );

	$intent = sanitize_key( posted_value( 'intent' ) );
	if ( 'newsletter' === $intent ) {
		$email = sanitize_email( posted_value( 'email' ) );
		if ( ! is_email( $email ) || strlen( $email ) > 254 ) {
			return new \WP_Error( 'invalid' );
		}
		$signup = wp_insert_post( [
			'post_type' => 'cups1_inquiry',
			'post_title' => 'Newsletter signup',
			'post_status' => 'private',
			'meta_input' => [ '_cups1_details' => [
				'Email' => $email,
				'Signup recorded (UTC)' => gmdate( 'Y-m-d H:i:s' ),
			] ],
		], true );
		return $signup && ! is_wp_error( $signup ) ? 'subscribed' : new \WP_Error( 'save_error' );
	}
	$name = sanitize_text_field( posted_value( 'name' ) );
	$email = sanitize_email( posted_value( 'email' ) );
	$company = sanitize_text_field( posted_value( 'company' ) );
	$product = sanitize_key( posted_value( 'product' ) );
	$country = sanitize_text_field( posted_value( 'country' ) );
	$quantity = filter_var( posted_value( 'quantity' ), FILTER_VALIDATE_INT, [ 'options' => [ 'min_range' => 1 ] ] );
	$notes = sanitize_textarea_field( posted_value( 'notes' ) );
	$specification = 'quote' === $intent ? quote_specification() : [];
	if ( is_wp_error( $specification ) ) {
		return $specification;
	}
	$products = inquiry_products() + [ 'other' => 'Other packaging' ];
	if ( ! in_array( $intent, [ 'quote', 'sample', 'contact' ], true ) || ! $name || ! is_email( $email ) || ! $company || 'on' !== posted_value( 'consent' ) ) {
		return new \WP_Error( 'invalid' );
	}
	if ( 'contact' !== $intent && ( ! isset( $products[ $product ] ) || ! in_array( $country, [ 'United States', 'Canada' ], true ) ) ) {
		return new \WP_Error( 'invalid' );
	}
	if ( ( 'quote' === $intent && ! $quantity ) || ( 'contact' === $intent && ! $notes ) || strlen( $name ) > 160 || strlen( $company ) > 200 || strlen( $notes ) > 8000 ) {
		return new \WP_Error( 'invalid' );
	}

	$artwork = validate_artwork( $_FILES['artwork'] ?? [] );
	if ( is_wp_error( $artwork ) ) {
		return $artwork;
	}

	$reference = strtoupper( wp_generate_password( 12, false, false ) );
	$details = array_filter( [
		'Request type' => ucfirst( $intent ),
		'Name' => $name,
		'Business email' => $email,
		'Company' => $company,
		'Product' => $products[ $product ] ?? '',
		'Delivery country' => $country,
		'Quantity' => $quantity ? (string) $quantity : '',
		'Notes' => $notes,
		'Contact consent recorded (UTC)' => gmdate( 'Y-m-d H:i:s' ),
	] + $specification );
	$meta = [ '_cups1_details' => $details ];
	if ( $artwork ) {
		$meta['_cups1_artwork_name'] = $artwork['name'];
		$meta['_cups1_artwork_data'] = $artwork['data'];
	}
	$id = wp_insert_post( [
		'post_type' => 'cups1_inquiry',
		'post_title' => "$reference · " . ucfirst( $intent ),
		'post_status' => 'private',
		'meta_input' => wp_slash( $meta ),
	], true );
	if ( is_wp_error( $id ) || ! $id || ! get_post_meta( $id, '_cups1_details', true ) || ( $artwork && ! get_post_meta( $id, '_cups1_artwork_data', true ) ) ) {
		if ( $id && ! is_wp_error( $id ) ) {
			wp_delete_post( $id, true );
		}
		return new \WP_Error( 'save_error' );
	}
	return $reference;
}

function quote_specification() {
	$dimensions = sanitize_text_field( posted_value( 'dimensions' ) );
	$postal_code = sanitize_text_field( posted_value( 'postal_code' ) );
	$print = posted_value( 'print_preference' );
	$pattern = posted_value( 'order_pattern' );
	$print_options = [ '' => '', 'single' => 'Single color', 'multi' => 'Multiple colors', 'plain' => 'Unprinted', 'help' => 'Needs guidance' ];
	$patterns = [ '' => '', 'one-off' => 'One-time order', 'recurring' => 'Recurring supply', 'multi-location' => 'Multiple locations' ];
	if ( mb_strlen( $dimensions ) > 120 || mb_strlen( $postal_code ) > 24 || ! isset( $print_options[ $print ], $patterns[ $pattern ] ) ) {
		return new \WP_Error( 'invalid' );
	}
	return [
		'Size or dimensions' => $dimensions,
		'Print preference' => $print_options[ $print ],
		'Delivery ZIP or postal code' => $postal_code,
		'Ordering pattern' => $patterns[ $pattern ],
	];
}

function validate_artwork( array $upload ) {
	if ( ! $upload || UPLOAD_ERR_NO_FILE === ( $upload['error'] ?? null ) ) {
		return [];
	}
	if ( UPLOAD_ERR_OK !== ( $upload['error'] ?? null ) || ! is_int( $upload['size'] ?? null ) || $upload['size'] > 5 * MB_IN_BYTES
		|| ! is_string( $upload['tmp_name'] ?? null ) || ! is_uploaded_file( $upload['tmp_name'] ) || ! is_string( $upload['name'] ?? null ) ) {
		return new \WP_Error( 'artwork' );
	}
	$name = sanitize_file_name( $upload['name'] );
	$mimes = [ 'pdf' => 'application/pdf', 'png' => 'image/png', 'jpg|jpeg' => 'image/jpeg' ];
	$type = wp_check_filetype_and_ext( $upload['tmp_name'], $name, $mimes );
	$data = file_get_contents( $upload['tmp_name'] );
	if ( ! $type['ext'] || ! $data || ( $type['type'] === 'application/pdf' && ! str_starts_with( $data, '%PDF-' ) ) ) {
		return new \WP_Error( 'artwork' );
	}
	return [ 'name' => $name, 'data' => base64_encode( $data ) ];
}

function inquiry_status_markup(): string {
	$status = isset( $_GET['inquiry'] ) && is_string( $_GET['inquiry'] ) ? sanitize_key( wp_unslash( $_GET['inquiry'] ) ) : '';
	$reference = isset( $_GET['reference'] ) && is_string( $_GET['reference'] ) ? sanitize_text_field( wp_unslash( $_GET['reference'] ) ) : '';
	if ( 'subscribed' === $status ) {
		return '<span data-status="success">Your signup was recorded.</span>';
	}
	if ( 'received' === $status && preg_match( '/^[A-Z0-9]{12}$/D', $reference ) ) {
		return '<span data-status="success">Your inquiry was received. Reference: ' . esc_html( $reference ) . '.</span>';
	}
	$message = inquiry_error_message( $status );
	return $message ? '<span data-status="error">' . esc_html( $message ) . '</span>' : '';
}

function inquiry_error_message( string $status ): string {
	$messages = [
		'expired' => 'The form session expired. Please reload and try again.',
		'invalid' => 'Please check the required fields and try again.',
		'artwork' => 'Please choose a PDF, PNG, or JPEG file of 5 MB or less.',
		'limit' => 'Too many attempts. Please wait a few minutes and try again.',
		'save_error' => 'The inquiry could not be saved. Please try again.',
	];
	return $messages[ $status ] ?? '';
}
