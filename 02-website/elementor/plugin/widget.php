<?php

namespace Cups1\ElementorSite;

use Elementor\Controls_Manager;
use Elementor\Widget_Base;

defined( 'ABSPATH' ) || exit;

class Design_Widget extends Widget_Base {
	private string $component;

	public function __construct( array $data = [], $args = null ) {
		$this->component = $args['cups1_component'] ?? substr( $data['widgetType'] ?? '', 6 );
		parent::__construct( $data, $args );
	}

	public function get_name(): string {
		return 'cups1-' . $this->component;
	}

	public function get_title(): string {
		return $this->definition()['title'];
	}

	public function get_icon(): string {
		return 'eicon-container';
	}

	public function get_categories(): array {
		return [ 'cups1' ];
	}

	protected function is_dynamic_content(): bool {
		return true;
	}

	protected function register_controls(): void {
		$this->start_controls_section( 'cups1_content', [ 'label' => 'Cups1 content' ] );
		foreach ( $this->definition()['fields'] as $id => $field ) {
			$control = [ 'label' => $field['label'] ];
			switch ( $field['type'] ) {
				case 'media':
					$control['type'] = Controls_Manager::MEDIA;
					$control['default'] = [ 'url' => asset_url( $field['value'] ), 'id' => '' ];
					break;
				case 'url':
					$control['type'] = Controls_Manager::TEXT;
					$control['description'] = 'Use a URL, an anchor such as #products, or a Cups1 page reference such as @page/products.';
					$control['default'] = $field['value'];
					break;
				default:
					$control['type'] = strlen( $field['value'] ) > 100 ? Controls_Manager::TEXTAREA : Controls_Manager::TEXT;
					$control['default'] = $field['value'];
			}
			$this->add_control( $id, $control );
		}
		$this->end_controls_section();
	}

	protected function render(): void {
		$definition = $this->definition();
		$settings = $this->get_settings_for_display();
		if ( 'home-compare' === $this->component ) {
			// Replace the original seeded comparison values while preserving editor overrides.
			$previous_defaults = [
				'field_10' => [ 'url' => asset_url( 'double-wall.webp' ), 'id' => '' ],
				'field_11' => 'Custom double-wall cup concept',
				'field_12' => [ 'url' => asset_url( 'single-wall.webp' ), 'id' => '' ],
				'field_13' => 'Single-wall cup concept',
				'field_25' => 'Drag to compare cup concepts',
				'field_32' => 'Cup model',
				'field_39' => 'Try your logo on this cup →',
			];
			foreach ( $previous_defaults as $id => $previous ) {
				$saved = $settings[ $id ] ?? null;
				if ( $saved === $previous || ( is_array( $previous ) && is_array( $saved ) && ( $saved['url'] ?? '' ) === $previous['url'] && empty( $saved['id'] ) ) ) {
					unset( $settings[ $id ] );
				}
			}
		}
		$previous_labels = match ( $this->component ) {
			'home-compare' => [ 'field_54' => 'Drop your logo here or browse' ],
			'cup-logo-preview' => [
				'field_8' => 'Preview your logo on a cup',
				'field_9' => 'Choose a cup model and add your logo to see how it could look in print.',
				'field_12' => 'Cup model',
			],
			'page-products' => [
				'field_56' => 'Ice Cream & Dessert Cups',
				'field_57' => 'Short paper tubs for scoops, toppings, and dessert portions.',
				'field_58' => 'Request quote',
				'field_59' => '05 / Food service',
				'field_60' => 'Kraft Food & Salad Bowls',
				'field_61' => 'Round formats for salads, grain bowls, and takeaway meals.',
				'field_62' => 'Request quote',
				'field_63' => '06 / Takeaway',
				'field_64' => 'Custom Takeaway Boxes',
				'field_65' => 'Explore branded carton formats for takeaway menus.',
				'field_66' => 'Request quote',
				'field_67' => 'Catalog imagery shows concept renderings.',
			],
			default => [],
		};
		foreach ( $previous_labels as $id => $previous ) {
			if ( ( $settings[ $id ] ?? null ) === $previous ) {
				unset( $settings[ $id ] );
			}
		}
		$output = preg_replace_callback( '/\{\{(field_\d+)\}\}/', function ( array $match ) use ( $definition, $settings ): string {
			$id = $match[1];
			$field = $definition['fields'][ $id ];
			$value = $settings[ $id ] ?? $field['value'];
			if ( 'media' === $field['type'] ) {
				return esc_url( is_array( $value ) ? ( $value['url'] ?? '' ) : asset_url( $value ) );
			}
			if ( 'url' === $field['type'] ) {
				if ( 'page-customize' === $this->component && str_starts_with( $field['value'], '@page/configure-packaging?' )
					&& $value === str_replace( [ 'configure-packaging', 'packaging_product=' ], [ 'request-a-quote', 'product=' ], $field['value'] ) . '#quote' ) {
					$value = $field['value'];
				}
				return esc_url( resolve_link( (string) $value ) );
			}
			return esc_html( (string) $value );
		}, $definition['markup'] );

		if ( 'page-products' === $this->component && catalog_is_active() ) {
			$products = product_catalog();
			$collection = selected_catalog_collection();
			if ( $collection ) {
				$products = array_filter( $products, static fn( $product ) => product_in_collection( $product, $collection ) );
				$heading = '<h1>' . esc_html( catalog_collections()[ $collection ] ) . '</h1>';
				$output = preg_replace( '/<h1>.*?<\/h1>/s', $heading, $output, 1 );
				if ( ! $products ) {
					$output = preg_replace( '/<p class="catalog-empty" hidden="">.*?<\/p>/s', '<p class="catalog-empty">No products in this collection yet.</p>', $output, 1 );
				}
			}
			$output = preg_replace_callback( '/<!--cups1-products-start-->.*?<!--cups1-products-end-->/s', static fn() => catalog_cards( $products ), $output );
			$output = str_replace( '<form aria-label="Filter packaging"', catalog_collection_nav() . '<form aria-label="Filter packaging"', $output );
			$output = str_replace( '<p aria-live="polite" class="catalog-status"></p>', '<p aria-live="polite" class="catalog-status">' . esc_html( sprintf( _n( '%d product', '%d products', count( $products ), 'cups1' ), count( $products ) ) ) . '</p>', $output );
			$output = str_replace( '<!--cups1-catalog-business-->', catalog_business_panel(), $output );
		}
		$output = product_options( $output );

		if ( 'header' === $this->component ) {
			$output = preg_replace_callback( '/<a data-cups1-nav-fallback="" (href="[^"]*")>([^<]*)<\/a>/', static function ( array $match ) use ( $output ): string {
				$link = '<a ' . $match[1] . '>' . $match[2] . '</a>';
				return str_contains( $output, $link ) ? '' : $link;
			}, $output );
		}

		$mode = match ( $this->component ) {
			'page-request-a-sample' => 'sample',
			'page-contact' => 'contact',
			default => 'quote',
		};
		$selected = $_GET['packaging_product'] ?? '';
		if ( is_string( $selected ) && isset( inquiry_products()[ $selected ] ) ) {
			$option = 'value="' . esc_attr( $selected ) . '"';
			$output = str_replace( $option, $option . ' selected', $output );
		}
		$inquiry = inquiry_status_markup();
		if ( str_contains( $output, '<span data-inquiry-result=""></span>' ) ) {
			$privacy = get_the_privacy_policy_link( '<p>', '</p>' );
			$output = str_replace( '<p class="form-status" role="status">', $privacy . '<p class="form-status" role="status">', $output );
		}
		echo strtr( $output, [
			'@inquiry' => esc_url( admin_url( 'admin-post.php' ) ),
			'@nonce' => esc_attr( wp_create_nonce( 'cups1_inquiry' ) ),
			'@intent' => $mode,
			'@current' => (string) get_queried_object_id(),
			'<span data-inquiry-result=""></span>' => $inquiry,
		] );
	}

	private function definition(): array {
		return design()['components'][ $this->component ];
	}
}
