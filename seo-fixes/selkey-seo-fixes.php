<?php
/**
 * Plugin Name: Selkey SEO Fixes
 * Description: Fixes index bloat, og:locale, and header exposure identified in the July 2026 SEO audit. Requires Yoast SEO.
 * Version:     1.0.0
 * Author:      Selkey Cyber Security
 *
 * INSTALL (pick one):
 *   A) Copy this file to wp-content/mu-plugins/selkey-seo-fixes.php  (auto-active, recommended)
 *   B) Zip it and install via Plugins → Add New → Upload, then activate.
 *
 * After activating: Yoast SEO → Tools → "Optimize SEO Data", then resubmit
 * sitemap_index.xml in Google Search Console.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/**
 * Post types that are theme internals and must never be indexed:
 *  - elementskit_content : ElementsKit mega-menu/widget content
 *  - th-mega-menu        : TechCo theme mega menus
 *  - techco_template     : TechCo header/footer templates (/header-footer/...)
 */
const SELKEY_JUNK_POST_TYPES = array( 'elementskit_content', 'th-mega-menu', 'techco_template' );

/** Taxonomies that only hold theme demo terms. */
const SELKEY_JUNK_TAXONOMIES = array( 'project_cat' );

/* 1. Drop junk post types from the Yoast XML sitemap. */
add_filter(
	'wpseo_sitemap_exclude_post_type',
	function ( $excluded, $post_type ) {
		return in_array( $post_type, SELKEY_JUNK_POST_TYPES, true ) ? true : $excluded;
	},
	10,
	2
);

/* 2. Drop junk taxonomies from the Yoast XML sitemap. */
add_filter(
	'wpseo_sitemap_exclude_taxonomy',
	function ( $excluded, $taxonomy ) {
		return in_array( $taxonomy, SELKEY_JUNK_TAXONOMIES, true ) ? true : $excluded;
	},
	10,
	2
);

/* 3. Force noindex,nofollow on junk pages if someone reaches them directly. */
add_filter(
	'wpseo_robots',
	function ( $robots ) {
		if (
			is_singular( SELKEY_JUNK_POST_TYPES )
			|| is_post_type_archive( SELKEY_JUNK_POST_TYPES )
			|| is_tax( SELKEY_JUNK_TAXONOMIES )
		) {
			return 'noindex, nofollow';
		}
		return $robots;
	}
);

/* 4. Belt-and-braces: also cover the core robots output for those pages. */
add_filter(
	'wp_robots',
	function ( $robots ) {
		if (
			is_singular( SELKEY_JUNK_POST_TYPES )
			|| is_post_type_archive( SELKEY_JUNK_POST_TYPES )
			|| is_tax( SELKEY_JUNK_TAXONOMIES )
		) {
			$robots['noindex']  = true;
			$robots['nofollow'] = true;
			unset( $robots['max-image-preview'], $robots['max-snippet'], $robots['max-video-preview'] );
		}
		return $robots;
	},
	20
);

/* 5. og:locale — business serves India, not the US. */
add_filter(
	'wpseo_og_locale',
	function () {
		return 'en_IN';
	}
);

/* 6. Stop advertising the PHP version. (Also set expose_php = Off in php.ini if possible.) */
add_action(
	'init',
	function () {
		if ( ! headers_sent() ) {
			header_remove( 'X-Powered-By' );
		}
	},
	0
);
