# Apply guide — fixing selkeycybersecurity.com step by step

Work top to bottom. Estimated total effort: ~1 day of dashboard work.
Files in this folder: `selkey-seo-fixes.php` (code), `redirects.htaccess` (redirect rules), `content-pack.md` (all copy/schema).

---

## Step 1 — Install the fix plugin (15 min) 🔴

1. Download `selkey-seo-fixes.php` from this folder.
2. Upload it to `wp-content/mu-plugins/` via your hosting file manager or FTP
   (create the `mu-plugins` folder if it doesn't exist — files there are always active, nothing to activate).
3. Verify: open `https://selkeycybersecurity.com/header-footer/footer-four/` → view source → the robots meta must now say `noindex, nofollow`.
4. Verify: `https://selkeycybersecurity.com/sitemap_index.xml` no longer lists `elementskit_content`, `th-mega-menu` or `techco_template` sitemaps.
   (If it still does: Yoast SEO → Tools → Optimize SEO data, and clear LiteSpeed cache.)

This fixes: index bloat (sitemap + noindex), og:locale, PHP version header.

## Step 2 — Belt and braces in Yoast settings (10 min) 🔴

Yoast SEO → Settings → Content types / Categories & tags:
- For **ElementsKit content**, **Mega Menus**, **Header/Footer templates**: set "Show in search results" → **No**.
- For the **Project categories** taxonomy: "Show in search results" → **No**.
- While you're there, decide on **Projects**: if you don't plan to publish real case studies, set it to No as well.

## Step 3 — Delete theme demo content (20 min) 🔴

WP admin → Projects: move to trash (they're TechCo demo posts, not your content):
- Mobile App Design, Dashboard Design, Technology Solution
- All "…IT Solutions / IT Portfolio…" posts (Driving Digital Transformation…, Explore Our IT Solutions Portfolio… **and its `-copy` duplicate**, Tech Triumphs…, Revolutionizing IT Strategies…, Cloud Migration and Integration…, Pioneering Progress…, Unlocking Potential…)

⚠️ **Do NOT delete** these — the theme uses them as homepage content blocks: Why Choose Us, Our Mission, Our Vision, Advanced Cybersecurity, Cybersecurity Solutions, SOC Compliance & Governance.

## Step 4 — Fix the misspelled slugs + redirects (20 min) 🔴

1. Edit each service → change the permalink slug:
   - `security-assesment-services-and-ot` → `security-assessment-services-and-ot` (also fix "Assesment" → "Assessment" in the page title and H1)
   - `gdpr-implementation-readness` → `gdpr-implementation-readiness`
   - `soc-as-a-services` → `soc-as-a-service` (fix title/H1 to "SOC as a Service")
2. Paste the rules from `redirects.htaccess` into your site's `.htaccess`, above `# BEGIN WordPress`.
3. Test all three old URLs → should 301 to the new ones.

## Step 5 — Build the /services/ hub page (1–2 h) 🔴

Follow the draft in `content-pack.md` §3. Then: Appearance → Menus → point the "Services" menu item at the new page (it currently redirects to a mega-menu template). While editing menus, fix the trailing-slash links: `/about-us` → `/about-us/`, `/contact-us` → `/contact-us/`.

## Step 6 — Replace the social share image (30 min) 🔴

Spec in `content-pack.md` §5. The current og:image is a 1.9 MB animated GIF — LinkedIn/WhatsApp previews are broken until this is replaced.

## Step 7 — Titles, meta descriptions, homepage copy (2–3 h) 🟠

All copy is ready to paste in `content-pack.md` §1–2:
- Meta descriptions for FAQ / Privacy / Terms
- Shortened & keyword-tuned service titles
- Homepage H2 rewrites + unique testimonial headings
- Unify the "144 vs 765 clients" numbers

## Step 8 — Schema fix (30 min) 🟠

Replace the ProfessionalService JSON-LD with `content-pack.md` §4 (drops the self-serving star rating, adds geo/hours/priceRange). Fill in real coordinates and opening hours. Validate at https://validator.schema.org.

## Step 9 — Alt text pass (2 h, can be spread out) 🟠

Media Library → grid view → work through images used on the homepage and service pages. Rule: describe the image for a blind visitor ("Selkey SOC analyst monitoring dashboards", "ISO 27001 certification badge"). Decorative shapes/blobs: leave alt empty.
Find offenders quickly with WP-CLI if you have shell access:
`wp db query "SELECT p.ID, p.guid FROM wp_posts p LEFT JOIN wp_postmeta m ON m.post_id=p.ID AND m.meta_key='_wp_attachment_image_alt' WHERE p.post_type='attachment' AND (m.meta_value IS NULL OR m.meta_value='')"`

## Step 10 — Tell Google (15 min) 🔴

Google Search Console:
1. Resubmit `sitemap_index.xml`.
2. Removals → request removal for `/header-footer/`, `/th-mega-menu/`, `/elementskit-content/`, `/project-category/` prefixes.
3. URL Inspection → request indexing for the new `/services/` page and the three renamed service URLs.

## Month 2+ (from the main audit)

- Launch the blog: SEBI CSCRF / DPDPA / RBI / VAPT content clusters.
- Move training courses to a `/training/` silo with Course schema.
- Google Business Profile (Ahmedabad) + review collection so the 4.8★ claim is verifiable.
- Performance: LiteSpeed Cache → Page Optimization → enable CSS/JS combine & critical CSS; target < 25 scripts.
