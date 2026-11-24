<?php

namespace Cups1\ElementorSite;

defined( 'ABSPATH' ) || exit;

function inquiry_admin_status( array $data ): string {
	$status = ( $data['Status'] ?? '' ) === 'Incomplete' ? 'Incomplete' : 'Complete';
	return '<span class="cups1-inquiry-status cups1-inquiry-' . strtolower( $status ) . '">' . esc_html( $status ) . '</span>';
}

add_filter( 'manage_cups1_inquiry_posts_columns', function ( array $columns ): array {
	return [ 'cb' => $columns['cb'], 'cups1_contact' => 'Contact', 'cups1_request' => 'Request', 'cups1_status' => 'Status', 'cups1_reference' => 'Reference', 'date' => 'Received' ];
} );

add_filter( 'list_table_primary_column', function ( string $column, string $screen ): string {
	return 'edit-cups1_inquiry' === $screen ? 'cups1_contact' : $column;
}, 10, 2 );

add_action( 'manage_cups1_inquiry_posts_custom_column', function ( string $column, int $id ): void {
	$data = (array) get_post_meta( $id, '_cups1_details', true );
	switch ( $column ) {
		case 'cups1_contact':
			$email = $data['Business email'] ?? $data['Email'] ?? '';
			$name = $data['Name'] ?? $email;
			echo '<strong><a href="' . esc_url( get_edit_post_link( $id ) ) . '">' . esc_html( $name ?: 'View inquiry' ) . '</a></strong>';
			if ( $data['Company'] ?? '' ) {
				echo '<span class="cups1-inquiry-secondary">' . esc_html( $data['Company'] ) . '</span>';
			}
			if ( $email && $email !== $name ) {
				echo '<span class="cups1-inquiry-secondary">' . esc_html( $email ) . '</span>';
			}
			break;
		case 'cups1_request':
			echo '<strong>' . esc_html( $data['Request type'] ?? 'Newsletter signup' ) . '</strong>';
			if ( $data['Product'] ?? '' ) {
				echo '<span class="cups1-inquiry-secondary">' . esc_html( $data['Product'] ) . '</span>';
			}
			break;
		case 'cups1_status':
			echo inquiry_admin_status( $data );
			break;
		case 'cups1_reference':
			$title = get_post_field( 'post_title', $id );
			echo preg_match( '/^[A-Z0-9]{12}(?= · )/u', $title, $reference ) ? esc_html( $reference[0] ) : '—';
			break;
	}
}, 10, 2 );

add_filter( 'post_date_column_time', function ( string $time, \WP_Post $post ): string {
	return 'cups1_inquiry' === $post->post_type ? esc_html( get_the_date( '', $post ) . ' · ' . get_the_time( '', $post ) ) : $time;
}, 10, 2 );

add_filter( 'post_date_column_status', function ( string $status, \WP_Post $post ): string {
	return 'cups1_inquiry' === $post->post_type ? 'Received' : $status;
}, 10, 2 );

add_action( 'admin_enqueue_scripts', function (): void {
	$screen = get_current_screen();
	if ( $screen && 'cups1_inquiry' === $screen->post_type ) {
		wp_enqueue_style( 'cups1-inquiry-admin', plugins_url( 'public/inquiry-admin.css', PLUGIN_FILE ), [], VERSION );
	}
} );
