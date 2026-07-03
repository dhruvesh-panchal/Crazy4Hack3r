# Auto-blogging for selkeycybersecurity.com with Claude

This automates: **pick a topic → Claude writes an SEO-optimised post → publish to
WordPress as a draft for review.** It reuses the same content strategy from the
SEO audit (SEBI / DPDPA / RBI / VAPT clusters, internal links to your service
pages, Yoast SEO title + meta description).

## ⚠️ Read this first — auto-publishing AI content is an SEO risk

Google's spam policies target **scaled content abuse** — mass-publishing
unreviewed AI articles can get a site demoted. This setup therefore defaults to
`POST_STATUS=draft`: Claude writes the post, you review and publish it in
`wp-admin → Posts`. Keep a human in the loop, at least until you trust the
output. Publishing 2 well-reviewed posts a week beats 20 auto-published ones.

---

## What's in this folder

| File | Purpose |
|---|---|
| `generate_post.py` | The generator: Claude → WordPress REST API |
| `topics.txt` | Your topic queue (one per line; script consumes the top line) |
| `expose-yoast-rest.php` | mu-plugin so the script can set the Yoast SEO title/description |
| `requirements.txt` | Python dependencies |
| `../.github/workflows/auto-blog.yml` | Scheduled GitHub Action (twice a week) |

---

## Setup

### 1. Prerequisite: enable REST authentication (one-time)

Your LiteSpeed/Hostinger server strips the `Authorization` header, so Application
Password auth over REST fails with `rest_not_logged_in`. Add the fix from
`../seo-fixes/enable-rest-auth.htaccess` to your site's `.htaccess`, then clear
the LiteSpeed cache. (Same fix needed for me to edit the site directly.)

### 2. Create a WordPress Application Password

`wp-admin → Users → Profile → Application Passwords` → name it "auto-blog" → copy
the generated password. You can revoke it anytime.

### 3. (Optional) Install the Yoast-meta mu-plugin

Copy `expose-yoast-rest.php` to `wp-content/mu-plugins/`. Without it, posts still
publish fine — they just won't have the SEO title/description pre-filled.

### 4. Get a Claude API key

From the Anthropic Console (console.anthropic.com) → API keys.

---

## Run it — two ways

### Option A: GitHub Actions (recommended — no server needed)

1. In this repo: `Settings → Secrets and variables → Actions → New repository secret`.
   Add four secrets:
   - `ANTHROPIC_API_KEY`
   - `WP_URL` = `https://selkeycybersecurity.com`
   - `WP_USER` = your WordPress username (or account email)
   - `WP_APP_PASSWORD` = the application password from step 2
2. The workflow (`.github/workflows/auto-blog.yml`) runs Mon & Thu at 09:00 UTC.
   Test it now: `Actions → Auto blog post → Run workflow`.
3. Each run creates one **draft** and advances the topic queue.

### Option B: Your own machine or Hostinger cron

```bash
pip install -r automation/requirements.txt

export ANTHROPIC_API_KEY="sk-ant-..."
export WP_URL="https://selkeycybersecurity.com"
export WP_USER="your-wp-username"
export WP_APP_PASSWORD="xxxx xxxx xxxx xxxx xxxx xxxx"
export POST_STATUS="draft"          # change to "publish" only once you trust it
export POST_CATEGORY="Insights"

python automation/generate_post.py
```

Schedule with cron (e.g. Mon & Thu at 09:00):

```
0 9 * * 1,4  cd /path/to/repo && /usr/bin/python3 automation/generate_post.py >> automation/run.log 2>&1
```

Hostinger has a **Cron Jobs** panel (hPanel → Advanced → Cron Jobs) that runs the
same command on a schedule if you host the script there.

---

## Configuration (environment variables)

| Variable | Default | Notes |
|---|---|---|
| `ANTHROPIC_API_KEY` | — | Required |
| `WP_URL` | — | Required, no trailing slash |
| `WP_USER` | — | Required |
| `WP_APP_PASSWORD` | — | Required |
| `POST_STATUS` | `draft` | Set to `publish` to skip review (not recommended at first) |
| `CLAUDE_MODEL` | `claude-opus-4-8` | For higher volume at lower cost, use `claude-sonnet-5` |
| `POST_CATEGORY` | (none) | Category name; created if it doesn't exist |

## Adding topics

Edit `topics.txt` — one topic per line. Consumed topics are logged to
`topics.done.txt`. When the queue empties, the script just reports "no topics".

## Cost

Roughly one 1,000–1,400 word post per run. On `claude-opus-4-8` that's a few
cents of output tokens per post; `claude-sonnet-5` is cheaper for high volume.

## Quality guardrails baked in

- Publishes as **draft** by default (human review).
- System prompt forbids invented stats, fake clients, and marketing fluff.
- Enforces structured output (title, slug, meta, tags, HTML) via schema.
- Internal links to your real service pages, CTA to `/contact-us/`.
- One topic per run — no bulk dumping.
