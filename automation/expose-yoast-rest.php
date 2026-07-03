<?php
/**
 * Plugin Name: Expose Yoast Meta to REST
 * Description: Makes the Yoast SEO title and meta description writable through
 *              the WordPress REST API so the auto-blogger can set them.
 * Version:     1.0.0
 *
 * INSTALL: copy to wp-content/mu-plugins/expose-yoast-rest.php (auto-active).
 * Only needed if you want the generator to set the SEO title/description.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

add_action( 'init', function () {
	foreach ( array( '_yoast_wpseo_title', '_yoast_wpseo_metadesc' ) as $key ) {
		register_post_meta(
			'post',
			$key,
			array(
				'type'          => 'string',
				'single'        => true,
				'show_in_rest'  => true,
				// Only editors/admins (the app-password user) may write these.
				'auth_callback' => function () {
					return current_user_can( 'edit_posts' );
				},
			)
		);
	}
} );
