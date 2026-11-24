<?php

namespace Cups1\ElementorSite;

defined( 'ABSPATH' ) || exit;

add_action( 'admin_menu', function () {
	add_management_page( 'Cups1 Site Setup', 'Cups1 Site Setup', 'manage_options', 'cups1-site-setup', __NAMESPACE__ . '\setup_screen' );
} );

function setup_screen(): void {
	$pages = page_ids();
	$message = get_transient( 'cups1_setup_' . get_current_user_id() );
	delete_transient( 'cups1_setup_' . get_current_user_id() );
	?>
	<div class="wrap">
		<h1>Cups1 Site Setup</h1>
		<?php if ( $message ) : ?>
			<div class="notice <?php echo $message['error'] ? 'notice-error' : 'notice-success'; ?>"><p><?php echo esc_html( $message['text'] ); ?></p></div>
		<?php endif; ?>
		<?php if ( ! did_action( 'elementor/loaded' ) ) : ?>
			<p>Activate Elementor to create and edit Cups1 pages.</p>
		<?php elseif ( empty( $pages ) ) : ?>
			<p>Create editable draft pages and shared Elementor header and footer templates.</p>
			<?php setup_button( 'import', 'Create Elementor Drafts' ); ?>
		<?php else : ?>
			<p>Use Edit with Elementor to change the design content or reorder sections.</p>
			<?php if ( function_exists( 'wc_get_product' ) && ! get_option( 'cups1_catalog_imported' ) ) : ?>
				<?php setup_button( 'catalog', 'Import Existing Packaging into WooCommerce' ); ?>
			<?php endif; ?>
			<?php if ( ! get_post_meta( $pages['home'] ?? 0, '_cups1_reference_sections_added', true ) ) : ?>
				<?php setup_button( 'home-sections', 'Add Homepage Reference Sections' ); ?>
			<?php endif; ?>
			<?php if ( array_diff_key( design()['pages'], $pages ) ) : ?>
				<?php setup_button( 'import', 'Create Missing Elementor Pages' ); ?>
			<?php endif; ?>
			<ul>
				<?php foreach ( $pages as $slug => $id ) : ?>
					<?php if ( retired_product_page( $slug, $id ) ) continue; ?>
					<li><?php echo esc_html( get_the_title( $id ) ); ?>
						<a href="<?php echo esc_url( add_query_arg( [ 'post' => $id, 'action' => 'elementor' ], admin_url( 'post.php' ) ) ); ?>">Edit with Elementor</a>
						<?php if ( get_post_type( $id ) === 'page' ) : ?>
							· <a href="<?php echo esc_url( get_post_status( $id ) === 'publish' ? get_permalink( $id ) : get_preview_post_link( $id ) ); ?>">View page</a>
						<?php endif; ?>
					</li>
				<?php endforeach; ?>
			</ul>
			<?php if ( array_filter( $pages, fn( $id, $slug ) => 'publish' !== get_post_status( $id ) && ! retired_product_page( $slug, $id ), ARRAY_FILTER_USE_BOTH ) || (int) get_option( 'page_on_front' ) !== (int) $pages['home'] || 'page' !== get_option( 'show_on_front' ) ) : ?>
				<?php setup_button( 'publish', 'Publish Pages and Set Homepage' ); ?>
			<?php else : ?>
				<p>Cups1 Home is the current front page.</p>
			<?php endif; ?>
		<?php endif; ?>
	</div>
	<?php
}

function setup_button( string $mode, string $label ): void {
	?>
	<form action="<?php echo esc_url( admin_url( 'admin-post.php' ) ); ?>" method="post">
		<input type="hidden" name="action" value="cups1_site_setup">
		<input type="hidden" name="mode" value="<?php echo esc_attr( $mode ); ?>">
		<?php wp_nonce_field( 'cups1_site_setup' ); ?>
		<?php submit_button( $label ); ?>
	</form>
	<?php
}

add_action( 'admin_post_cups1_site_setup', function () {
	if ( ! current_user_can( 'manage_options' ) || ! did_action( 'elementor/loaded' ) ) {
		wp_die( 'Elementor and administrator access are required.', '', [ 'response' => 403 ] );
	}
	check_admin_referer( 'cups1_site_setup' );
	$mode = sanitize_key( wp_unslash( $_POST['mode'] ?? '' ) );
	$result = match ( $mode ) {
		'import' => import_pages(),
		'publish' => publish_pages(),
		'home-sections' => add_home_reference_sections(),
		'catalog' => import_catalog(),
		default => new \WP_Error( 'cups1_invalid_mode', 'Unknown setup action.' ),
	};
	set_transient( 'cups1_setup_' . get_current_user_id(), [
		'error' => is_wp_error( $result ),
		'text'  => is_wp_error( $result ) ? $result->get_error_message() : $result,
	], MINUTE_IN_SECONDS );
	wp_safe_redirect( admin_url( 'tools.php?page=cups1-site-setup' ) );
	exit;
} );

function add_home_reference_sections() {
	$id = (int) ( page_ids()['home'] ?? 0 );
	if ( ! $id || 'home' !== get_post_meta( $id, '_cups1_component_page', true ) ) {
		return new \WP_Error( 'cups1_missing_home', 'The Cups1 homepage could not be found.' );
	}
	if ( get_post_meta( $id, '_cups1_reference_sections_added', true ) ) {
		return 'Homepage reference sections are already installed.';
	}
	$original = get_post_meta( $id, '_elementor_data', true );
	$elements = json_decode( $original, true );
	if ( ! is_array( $elements ) || ! $elements ) {
		return new \WP_Error( 'cups1_home_data', 'The homepage Elementor data could not be read.' );
	}
	$sections = array_map( __NAMESPACE__ . '\section_data', design()['home_reference_sections'] );
	$closing = array_pop( $sections );
	$existing_ids = array_column( $elements, 'id' );
	$sections = array_values( array_filter( $sections, fn( $section ) => ! in_array( $section['id'], $existing_ids, true ) ) );
	array_splice( $elements, 1, 0, $sections );
	if ( ! in_array( $closing['id'], $existing_ids, true ) ) {
		$elements[] = $closing;
	}
	add_post_meta( $id, '_cups1_home_before_reference_sections', wp_slash( $original ), true );
	$updated = wp_json_encode( $elements );
	if ( $updated !== $original && ! update_post_meta( $id, '_elementor_data', wp_slash( $updated ), $original ) ) {
		return new \WP_Error( 'cups1_home_update', 'The homepage changed during setup. Reload and try again.' );
	}
	update_post_meta( $id, '_cups1_reference_sections_added', 1 );
	\Elementor\Plugin::$instance->files_manager->clear_cache();
	clean_post_cache( $id );
	return 'Added six editable homepage reference sections.';
}

function import_pages() {
	$plan = design()['pages'];
	foreach ( [ 'header', 'footer' ] as $key ) {
		$plan[ $key ] = [ 'title' => 'Cups1 ' . ucfirst( $key ), 'widgets' => [ $key ] ];
	}
	$ids = page_ids();
	$missing = array_diff_key( $plan, $ids );
	foreach ( $missing as $slug => $page ) {
		$type = in_array( $slug, [ 'header', 'footer' ], true ) ? 'elementor_library' : 'page';
		$name = $type === 'elementor_library' ? "cups1-$slug" : $slug;
		$existing = get_posts( [
			'post_type' => $type,
			'post_status' => [ 'draft', 'publish', 'pending', 'private', 'future' ],
			'numberposts' => 1,
			'meta_key' => '_cups1_component_page',
			'meta_value' => $slug,
			'fields' => 'ids',
		] );
		if ( $existing ) {
			$ids[ $slug ] = (int) $existing[0];
			continue;
		}
		if ( get_page_by_path( $name, OBJECT, $type ) ) {
			return new \WP_Error( 'cups1_slug_conflict', "The page or template slug $name already exists. Setup preserves existing content." );
		}
		$id = wp_insert_post( [
			'post_type' => $type,
			'post_title' => $page['title'],
			'post_name' => $name,
			'post_status' => $type === 'page' ? 'draft' : 'publish',
			'comment_status' => 'closed',
			'ping_status' => 'closed',
		], true );
		if ( is_wp_error( $id ) ) {
			return $id;
		}
		$elements = array_map( __NAMESPACE__ . '\section_data', $page['widgets'] );
		update_post_meta( $id, '_elementor_data', wp_slash( wp_json_encode( $elements ) ) );
		update_post_meta( $id, '_elementor_edit_mode', 'builder' );
		update_post_meta( $id, '_elementor_version', ELEMENTOR_VERSION );
		update_post_meta( $id, '_elementor_page_settings', [ 'hide_title' => 'yes' ] );
		update_post_meta( $id, '_wp_page_template', 'elementor_canvas' );
		if ( 'elementor_library' === $type ) {
			update_post_meta( $id, '_elementor_template_type', 'page' );
			wp_set_object_terms( $id, 'page', 'elementor_library_type' );
		}
		update_post_meta( $id, '_cups1_component_page', $slug );
		$ids[ $slug ] = $id;
	}
	update_option( 'cups1_elementor_pages', $ids, false );
	return sprintf( 'Added %d Elementor pages or shared templates to Cups1 Site Setup.', count( $missing ) );
}

function section_data( string $name ): array {
	$settings = [];
	foreach ( design()['components'][ $name ]['fields'] as $id => $field ) {
		$settings[ $id ] = $field['type'] === 'media' ? [ 'url' => asset_url( $field['value'] ), 'id' => '' ] : $field['value'];
	}
	return [
		'id' => substr( md5( "cups1-container-$name" ), 0, 7 ),
		'elType' => 'container',
		'isInner' => false,
		'settings' => [ 'content_width' => 'full', 'css_classes' => 'cups1-section', 'flex_direction' => 'column' ],
		'elements' => [ [
			'id' => substr( md5( "cups1-widget-$name" ), 0, 7 ),
			'elType' => 'widget',
			'widgetType' => "cups1-$name",
			'isInner' => false,
			'settings' => $settings,
			'elements' => [],
		] ],
	];
}

function retired_product_page( string $slug, int $id ): bool {
	return in_array( get_post_status( $id ), [ false, 'trash' ], true ) && (bool) legacy_product( $slug );
}

function publish_pages() {
	$pages = page_ids();
	if ( ! isset( $pages['home'] ) || count( $pages ) !== count( design()['pages'] ) + 2 ) {
		return new \WP_Error( 'cups1_missing_pages', 'Create all Elementor drafts before publishing.' );
	}
	foreach ( $pages as $slug => $id ) {
		if ( retired_product_page( $slug, $id ) ) {
			continue;
		}
		if ( $slug !== get_post_meta( $id, '_cups1_component_page', true ) || 'trash' === get_post_status( $id ) ) {
			return new \WP_Error( 'cups1_invalid_page', "Cups1 page $slug is missing or in the trash." );
		}
	}
	add_option( 'cups1_previous_front_page', [
		'show_on_front' => get_option( 'show_on_front' ),
		'page_on_front' => get_option( 'page_on_front' ),
	], '', false );
	foreach ( $pages as $slug => $id ) {
		if ( ! retired_product_page( $slug, $id ) && get_post_status( $id ) !== 'publish' ) {
			$result = wp_update_post( [ 'ID' => $id, 'post_status' => 'publish' ], true );
			if ( is_wp_error( $result ) ) {
				return $result;
			}
		}
	}
	update_option( 'page_on_front', $pages['home'] );
	update_option( 'show_on_front', 'page' );
	return 'Cups1 pages are published and Home is the front page.';
}
