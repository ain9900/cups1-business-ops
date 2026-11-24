<?php

namespace Cups1\ElementorSite;

defined( 'ABSPATH' ) || exit;

$product = wc_get_product( get_queried_object_id() );
$name = $product->get_name();
$images = array_filter( array_unique( array_merge( [ $product->get_image_id() ], $product->get_gallery_image_ids() ) ) );
$first_image = reset( $images );
$specifications = [];
foreach ( $product->get_attributes() as $attribute ) {
	if ( $attribute->get_visible() ) {
		$label = wc_attribute_label( $attribute->get_name(), $product );
		$value = $product->get_attribute( $attribute->get_name() );
		if ( $value && ( ! $attribute->get_variation() || ! in_array( sanitize_title( $label ), [ 'size', 'pack' ], true ) ) ) {
			$specifications[ $label ] = $value;
		}
	}
}
$specifications = [ 'Format' => $name ] + $specifications;
if ( $product->get_attribute( 'format' ) ) {
	$specifications['Format'] = $product->get_attribute( 'format' );
}
$specifications += [ 'Delivery' => 'Quotation for eligible USA & Canada destinations' ];
$price = $product->get_price_html();
$variable = $product->is_type( 'variable' );
$can_buy = $price && $product->is_purchasable() && $product->is_in_stock();
$sizes = $price ? [] : catalog_quote_sizes( $product );
$collection = '';
foreach ( catalog_collections() as $slug => $label ) {
	if ( product_in_collection( $product, $slug ) ) {
		$collection = $slug;
		break;
	}
}
$linked_ids = array_merge( $product->get_upsell_ids(), $product->get_cross_sell_ids() );
$related = $linked_ids ? array_filter( product_catalog(), static fn( $item ) =>
	$item->get_id() !== $product->get_id() && in_array( $item->get_id(), $linked_ids, true )
) : [];
?><!doctype html>
<html <?php language_attributes(); ?>>
<head>
	<meta charset="<?php bloginfo( 'charset' ); ?>">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<?php wp_head(); ?>
	<?php print_product_schema( $product ); ?>
</head>
<body <?php body_class(); ?>>
<?php wp_body_open(); ?>
<?php do_action( 'elementor/page_templates/canvas/before_content' ); ?>
<div class="shell">
	<?php wc_print_notices(); ?>
	<nav class="breadcrumbs" aria-label="Breadcrumb">
		<a href="<?php echo esc_url( home_url( '/' ) ); ?>">Home</a>
		<span aria-hidden="true">/</span>
		<a href="<?php echo esc_url( resolve_link( '@page/products' ) ); ?>">Products</a>
		<?php if ( $collection ) : ?>
			<span aria-hidden="true">/</span><a href="<?php echo esc_url( add_query_arg( 'collection', $collection, resolve_link( '@page/products' ) ) ); ?>"><?php echo esc_html( catalog_collections()[ $collection ] ); ?></a>
		<?php endif; ?>
		<span aria-hidden="true">/</span>
		<span aria-current="page"><?php echo esc_html( $name ); ?></span>
	</nav>
	<section class="product-hero split product" data-product-detail aria-labelledby="product-title">
		<div class="product-heading">
			<p class="eyebrow"><?php echo esc_html( $collection ? catalog_collections()[ $collection ] : 'Packaging' ); ?></p>
			<h1 id="product-title"><?php echo esc_html( $name ); ?></h1>
		</div>
		<div class="gallery">
			<figure class="visual">
				<?php if ( $first_image ) : ?>
					<?php echo wp_get_attachment_image( $first_image, 'large', false, [ 'id' => 'gallery-image' ] ); ?>
					<figcaption id="gallery-caption" aria-live="polite"><?php echo esc_html( get_the_title( $first_image ) ); ?></figcaption>
				<?php else : ?>
					<?php echo wc_placeholder_img( 'woocommerce_single', [ 'id' => 'gallery-image' ] ); ?>
					<figcaption id="gallery-caption" aria-live="polite"></figcaption>
				<?php endif; ?>
			</figure>
			<?php if ( $images ) : ?>
				<div class="gallery-controls" role="group" aria-label="Product images">
					<?php foreach ( $images as $id ) : ?>
						<button type="button" aria-pressed="<?php echo $id === $first_image ? 'true' : 'false'; ?>"
							data-image="<?php echo esc_url( wp_get_attachment_image_url( $id, 'large' ) ); ?>"
							data-caption="<?php echo esc_attr( get_the_title( $id ) ); ?>"
							data-alt="<?php echo esc_attr( get_post_meta( $id, '_wp_attachment_image_alt', true ) ); ?>">
							<?php echo wp_get_attachment_image( $id, 'medium', false, [ 'alt' => '' ] ); ?>
							<?php echo esc_html( get_the_title( $id ) ); ?>
						</button>
					<?php endforeach; ?>
				</div>
			<?php endif; ?>
		</div>
		<div class="product-details">
			<?php if ( $product->get_short_description() ) : ?>
				<div class="lead"><?php echo wp_kses_post( wpautop( $product->get_short_description() ) ); ?></div>
			<?php endif; ?>
			<dl class="specs">
					<?php foreach ( $specifications as $label => $value ) : ?>
						<div>
							<dt><?php echo esc_html( $label ); ?></dt>
							<dd><?php echo esc_html( $value ); ?></dd>
						</div>
					<?php endforeach; ?>
				</dl>
			<?php if ( $price ) : ?>
				<div class="catalog-purchase">
					<?php if ( $variable ) : ?>
						<?php catalog_purchase_form( $product, false ); ?>
					<?php else : ?>
						<?php catalog_purchase_summary( $product ); ?>
						<?php if ( ! $product->is_in_stock() ) echo wp_kses_post( wc_get_stock_html( $product ) ); ?>
					<?php endif; ?>
				</div>
			<?php endif; ?>
			<?php if ( $sizes ) : ?>
				<label class="catalog-size-picker">
					<span>Requested size</span>
					<select data-catalog-quote-size>
						<option value="">Choose a size</option>
						<?php foreach ( $sizes as $size ) : ?>
							<option value="<?php echo esc_attr( $size ); ?>"><?php echo esc_html( $size ); ?></option>
						<?php endforeach; ?>
					</select>
				</label>
			<?php endif; ?>
			<div class="actions">
				<?php if ( $price ) : ?>
					<button type="button" class="button primary" data-catalog-cart-item="<?php echo esc_attr( $product->get_id() ); ?>"<?php if ( ! $can_buy ) echo ' data-catalog-unavailable'; ?><?php disabled( ! $can_buy || $variable ); ?>>Add to cart</button>
				<?php endif; ?>
				<a class="button <?php echo $price ? 'outline' : 'primary'; ?>" data-catalog-quote-link href="<?php echo esc_url( product_request_url( $product, 'request-a-quote' ) ); ?>">Get a Delivered Quote <span aria-hidden="true">↗</span></a>
				<a class="button product-customize" data-catalog-quote-link href="<?php echo esc_url( product_request_url( $product, 'configure-packaging' ) ); ?>">Customize <span aria-hidden="true">↗</span></a>
				<?php if ( ! $price ) : ?>
					<a class="button outline" data-catalog-quote-link href="<?php echo esc_url( product_request_url( $product, 'request-a-sample' ) ); ?>">Request a Sample Kit</a>
				<?php endif; ?>
			</div>
		</div>
	</section>
</div>
<?php if ( $product->get_description() ) : ?>
	<section class="section white"><div class="shell">
		<?php echo apply_filters( 'the_content', $product->get_description() ); ?>
	</div></section>
<?php endif; ?>
<?php if ( $related ) : ?>
	<section class="section white"><div class="shell">
		<h2>Matching Lids &amp; Related Products</h2>
		<div class="catalog-grid"><?php echo catalog_cards( $related ); ?></div>
	</div></section>
<?php endif; ?>
<div class="shell"><?php echo catalog_business_panel(); ?></div>
<?php do_action( 'elementor/page_templates/canvas/after_content' ); ?>
<?php wp_footer(); ?>
</body>
</html>
