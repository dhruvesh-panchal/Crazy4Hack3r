#!/usr/bin/env python3
"""
Auto-blog generator for selkeycybersecurity.com.

Pipeline: pick a topic -> Claude writes an SEO-optimised post (title, slug,
meta description, tags, HTML body with internal links) -> publish to WordPress
as a DRAFT for human review via the REST API.

Run once per invocation. Schedule it with cron or GitHub Actions (see README).

Environment variables (required):
  ANTHROPIC_API_KEY   - your Claude API key
  WP_URL              - https://selkeycybersecurity.com
  WP_USER             - WordPress username (or the account's login email)
  WP_APP_PASSWORD     - a WordPress Application Password (Users -> Profile)

Optional:
  POST_STATUS         - "draft" (default, recommended) or "publish"
  CLAUDE_MODEL        - defaults to claude-opus-4-8
  POST_CATEGORY       - category name to file posts under (e.g. "Insights")
"""

import os
import sys
import json
import datetime
import requests
from typing import List
from pydantic import BaseModel, Field
import anthropic

# --- config -----------------------------------------------------------------

WP_URL = os.environ["WP_URL"].rstrip("/")
WP_USER = os.environ["WP_USER"]
WP_APP_PASSWORD = os.environ["WP_APP_PASSWORD"].replace(" ", "")  # spaces are cosmetic
POST_STATUS = os.environ.get("POST_STATUS", "draft")
CLAUDE_MODEL = os.environ.get("CLAUDE_MODEL", "claude-opus-4-8")
POST_CATEGORY = os.environ.get("POST_CATEGORY", "")

TOPICS_FILE = os.path.join(os.path.dirname(__file__), "topics.txt")
DONE_FILE = os.path.join(os.path.dirname(__file__), "topics.done.txt")

# Map of themes -> the service page a post should internally link to.
# Claude is told to weave the most relevant one or two links into the body.
SERVICE_LINKS = {
    "vapt": f"{WP_URL}/service/vulnerability-assessment-and-penetration-testing/",
    "web pentest": f"{WP_URL}/service/web-vulnerability-assessment-and-penetration-testing/",
    "soc": f"{WP_URL}/service/soc-as-a-service/",
    "iso 27001": f"{WP_URL}/service/iso-27001-2022/",
    "sebi": f"{WP_URL}/service/sebi-cyber-security-compliance/",
    "rbi": f"{WP_URL}/service/rbi-cyber-security-compliance/",
    "dpdpa": f"{WP_URL}/service/dpdpa-cyber-security-compliance/",
    "incident response": f"{WP_URL}/service/incident-response-malware-analysis/",
    "red team": f"{WP_URL}/service/red-teaming/",
    "contact": f"{WP_URL}/contact-us/",
}


# --- structured output schema -----------------------------------------------

class BlogPost(BaseModel):
    title: str = Field(description="SEO title, 50-60 characters, India-focused where natural")
    slug: str = Field(description="URL slug, lowercase, hyphenated, no stop words")
    meta_description: str = Field(description="Meta description, 140-155 characters, with a call to value")
    excerpt: str = Field(description="1-2 sentence summary for listing pages")
    tags: List[str] = Field(description="4-7 lowercase topical tags")
    content_html: str = Field(
        description=(
            "Full article body as clean HTML using <h2>/<h3>/<p>/<ul>/<li>/<a>. "
            "900-1400 words. No <h1> (WordPress adds the title). Include 1-2 "
            "internal links from the provided service-link list where relevant, "
            "and end with a short call-to-action linking to the contact page."
        )
    )


# --- Claude generation -------------------------------------------------------

def generate(topic: str) -> BlogPost:
    client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY

    links = "\n".join(f"- {k}: {v}" for k, v in SERVICE_LINKS.items())
    system = (
        "You are the content lead at Selkey Cyber Security, an India-based "
        "cybersecurity firm (VAPT, managed SOC, digital forensics, and "
        "compliance for ISO 27001, SEBI, RBI, DPDPA). Write accurate, "
        "practical, E-E-A-T-strong articles for a business audience of CISOs, "
        "IT managers, and compliance officers in India. Be specific and "
        "concrete; avoid generic filler and marketing fluff. British/Indian "
        "English. Never invent statistics, client names, or fake case studies."
    )
    user = (
        f"Write a blog post on: {topic}\n\n"
        f"Weave in one or two of these internal links where they genuinely fit "
        f"(use descriptive anchor text, not raw URLs):\n{links}\n\n"
        f"Optimise for the primary keyword implied by the topic. Structure with "
        f"an intro, scannable H2/H3 sections, and a short FAQ near the end."
    )

    resp = client.messages.parse(
        model=CLAUDE_MODEL,
        max_tokens=8000,
        system=system,
        messages=[{"role": "user", "content": user}],
        output_format=BlogPost,
    )
    post = resp.parsed_output
    if post is None:
        raise RuntimeError(f"Model did not return a valid post (stop_reason={resp.stop_reason})")
    return post


# --- WordPress publishing ----------------------------------------------------

def wp_auth():
    return (WP_USER, WP_APP_PASSWORD)


def resolve_tag_ids(tags: List[str]) -> List[int]:
    ids = []
    for name in tags:
        # look for an existing tag, else create it
        r = requests.get(
            f"{WP_URL}/wp-json/wp/v2/tags", params={"search": name}, auth=wp_auth(), timeout=30
        )
        r.raise_for_status()
        match = next((t for t in r.json() if t["name"].lower() == name.lower()), None)
        if match:
            ids.append(match["id"])
        else:
            c = requests.post(
                f"{WP_URL}/wp-json/wp/v2/tags", json={"name": name}, auth=wp_auth(), timeout=30
            )
            if c.status_code in (200, 201):
                ids.append(c.json()["id"])
    return ids


def resolve_category_id(name: str) -> int | None:
    if not name:
        return None
    r = requests.get(
        f"{WP_URL}/wp-json/wp/v2/categories", params={"search": name}, auth=wp_auth(), timeout=30
    )
    r.raise_for_status()
    match = next((c for c in r.json() if c["name"].lower() == name.lower()), None)
    if match:
        return match["id"]
    c = requests.post(
        f"{WP_URL}/wp-json/wp/v2/categories", json={"name": name}, auth=wp_auth(), timeout=30
    )
    return c.json()["id"] if c.status_code in (200, 201) else None


def publish(post: BlogPost) -> str:
    payload = {
        "title": post.title,
        "slug": post.slug,
        "content": post.content_html,
        "excerpt": post.excerpt,
        "status": POST_STATUS,
        "tags": resolve_tag_ids(post.tags),
        # Requires the expose-yoast-rest.php mu-plugin to be installed so these
        # meta keys are writable via REST. Without it, these are silently ignored.
        "meta": {
            "_yoast_wpseo_title": post.title + " | Selkey",
            "_yoast_wpseo_metadesc": post.meta_description,
        },
    }
    cat = resolve_category_id(POST_CATEGORY)
    if cat:
        payload["categories"] = [cat]

    r = requests.post(f"{WP_URL}/wp-json/wp/v2/posts", json=payload, auth=wp_auth(), timeout=60)
    if r.status_code not in (200, 201):
        raise RuntimeError(f"WordPress rejected the post ({r.status_code}): {r.text[:500]}")
    data = r.json()
    return data.get("link") or data.get("guid", {}).get("rendered", "(unknown)")


# --- topic queue -------------------------------------------------------------

def next_topic() -> str | None:
    if not os.path.exists(TOPICS_FILE):
        return None
    with open(TOPICS_FILE, encoding="utf-8") as f:
        topics = [ln.strip() for ln in f if ln.strip() and not ln.startswith("#")]
    if not topics:
        return None
    topic = topics[0]
    # move it to the done file so it isn't reused
    with open(TOPICS_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(topics[1:]) + ("\n" if len(topics) > 1 else ""))
    with open(DONE_FILE, "a", encoding="utf-8") as f:
        f.write(f"{datetime.date.today()}\t{topic}\n")
    return topic


def main():
    topic = next_topic()
    if not topic:
        print("No topics left in topics.txt — add more and re-run.")
        return
    print(f"Generating post for: {topic}")
    post = generate(topic)
    print(f"  title: {post.title}")
    print(f"  slug:  {post.slug}")
    link = publish(post)
    print(f"Published as {POST_STATUS}: {link}")
    if POST_STATUS == "draft":
        print("Review it in wp-admin -> Posts before publishing.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:  # surface a clear error for cron/Actions logs
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
