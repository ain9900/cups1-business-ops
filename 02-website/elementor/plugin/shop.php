<?php

namespace Cups1\ElementorSite;

defined( 'ABSPATH' ) || exit;

$frontend = \Elementor\Plugin::$instance->frontend;
$catalog = $frontend->get_builder_content_for_display( get_queried_object_id(), true );
?><!doctype html>
<html <?php language_attributes(); ?>>
<head>
	<meta charset="<?php bloginfo( 'charset' ); ?>">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<?php wp_head(); ?>
</head>
<body <?php body_class(); ?>>
<?php wp_body_open(); ?>
<?php do_action( 'elementor/page_templates/canvas/before_content' ); ?>
<?php echo $catalog; ?>
<?php do_action( 'elementor/page_templates/canvas/after_content' ); ?>
<?php wp_footer(); ?>
</body>
</html>
