#!/usr/bin/env python3
"""Generate LinkedIn copy via Gemini API and post to LinkedIn.

Authentication: Uses OAuth 2.0 refresh token flow to obtain a fresh access token
at runtime. This avoids storing short-lived access tokens (60-day TTL) as secrets.
Instead, store the refresh token (365-day TTL) along with client_id and client_secret.

Required GitHub Secrets:
  LINKEDIN_CLIENT_ID      - OAuth app Client ID
  LINKEDIN_CLIENT_SECRET  - OAuth app Client Secret
  LINKEDIN_REFRESH_TOKEN  - OAuth refresh token (valid 365 days)
  LINKEDIN_PERSON_URN     - Your LinkedIn member URN (e.g. urn:li:person:xxxxxxx)
  GOOGLE_API_KEY          - Gemini API key for copy generation
"""
import os
import re
import sys
import json
import glob
import urllib.request
import urllib.error
import urllib.parse


def extract_post_content(filepath):
    """Extract title, tags, and full content from a Jekyll post."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)", content, re.DOTALL)
    if not match:
        return {}, ""

    frontmatter = match.group(1)
    body = match.group(2)

    meta = {}
    for line in frontmatter.splitlines():
        if line.strip().startswith("title:"):
            meta["title"] = line.split(":", 1)[1].strip().strip('"').strip("'")
        elif line.strip().startswith("- ") and "tags" in "\n".join(frontmatter.splitlines()[:frontmatter.splitlines().index(line)]):
            meta.setdefault("tags", []).append(line.strip().lstrip("- ").strip())

    # Parse tags more robustly
    in_tags = False
    tags = []
    for line in frontmatter.splitlines():
        if line.strip() == "tags:":
            in_tags = True
            continue
        if in_tags:
            if line.strip().startswith("- "):
                tags.append(line.strip().lstrip("- ").strip())
            else:
                in_tags = False
    meta["tags"] = tags

    return meta, body


def get_style_examples():
    """Load 3 previous posts as writing style examples."""
    posts = sorted(glob.glob("_posts/*.md"), reverse=True)
    examples = []
    for post_path in posts[:5]:
        with open(post_path, "r", encoding="utf-8") as f:
            content = f.read()
        match = re.match(r"^---\s*\n.*?\n---\s*\n(.*)", content, re.DOTALL)
        if match:
            body = match.group(1)
            # Get first 300 words
            words = body.split()[:300]
            examples.append(" ".join(words))
        if len(examples) >= 3:
            break
    return examples


def generate_linkedin_copy(title, body, tags, api_key):
    """Use Gemini to generate engaging LinkedIn copy."""
    style_examples = get_style_examples()
    examples_text = "\n\n---\n\n".join(
        f"Example {i+1}:\n{ex}" for i, ex in enumerate(style_examples)
    )

    # Get first 500 words of the new post
    post_excerpt = " ".join(body.split()[:500])

    prompt = f"""You are writing a LinkedIn post for Alexander Heusingfeld, Head of Platforms & Lifecycle at Vorwerk HOME. He writes about technology, software architecture, organizational development, and how AI changes the way we work.

Here are examples of his writing style:

{examples_text}

Now write a LinkedIn post for his new blog article titled: "{title}"

The article content:
{post_excerpt}

Requirements:
- Open with a provocative question or bold observation that makes people stop scrolling
- Keep it under 200 words
- Be thoughtful and authentic, not salesy
- End with a clear call to read the full article
- Add 3-5 relevant hashtags at the end
- Match Alexander's reflective, systems-thinking tone
- Write in English

Return ONLY the LinkedIn post text, nothing else."""

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"

    payload = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 500,
        },
    }).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read())
        candidates = result.get("candidates", [])
        if candidates:
            parts = candidates[0].get("content", {}).get("parts", [])
            if parts:
                return parts[0]["text"].strip()

    return None


def get_access_token(client_id, client_secret, refresh_token):
    """Exchange a refresh token for a fresh access token.

    Refresh tokens are valid for 365 days. Each call returns a new access token
    (60-day TTL) without consuming the refresh token's remaining lifespan.
    """
    url = "https://www.linkedin.com/oauth/v2/accessToken"

    params = urllib.parse.urlencode({
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": client_id,
        "client_secret": client_secret,
    }).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=params,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read())
            access_token = result.get("access_token")
            expires_in = result.get("expires_in")
            refresh_ttl = result.get("refresh_token_expires_in")
            print(f"Access token obtained (expires in {expires_in}s)")
            if refresh_ttl:
                days_left = refresh_ttl // 86400
                print(f"Refresh token valid for {days_left} more days")
                if days_left < 30:
                    print(f"::warning::LinkedIn refresh token expires in {days_left} days! Re-authorize soon.")
            return access_token
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        print(f"::error::LinkedIn token refresh failed: {e.code} - {error_body}")
        print("The refresh token may have expired. Re-authorize at:")
        print("https://www.linkedin.com/oauth/v2/authorization?response_type=code"
              f"&client_id={client_id}&scope=w_member_social%20openid%20profile"
              "&redirect_uri=https://localhost:3000/callback")
        return None


def post_to_linkedin(text, access_token, person_urn):
    """Post to LinkedIn using the Posts API."""
    url = "https://api.linkedin.com/v2/ugcPosts"

    payload = json.dumps({
        "author": person_urn,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": text},
                "shareMediaCategory": "NONE",
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        },
    }).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
            "X-Restli-Protocol-Version": "2.0.0",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read())
            post_id = result.get("id", "")
            print(f"LinkedIn post created: {post_id}")
            return post_id
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        print(f"LinkedIn API error: {e.code} - {error_body}")
        return None


def construct_post_url(post_file, site_url):
    """Construct the blog post URL from the filename."""
    basename = os.path.basename(post_file).replace(".md", "").replace(".adoc", "")
    # Parse: YYYY-MM-DD-title-slug
    parts = basename.split("-", 3)
    if len(parts) >= 4:
        slug = parts[3]
    else:
        slug = basename

    # Read categories from frontmatter
    meta, _ = extract_post_content(post_file)
    # Simple URL construction — matches permalink: /:categories/:title/
    # For now, use the slug directly; exact URL depends on category
    with open(post_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Extract first category
    category = ""
    in_categories = False
    for line in content.splitlines():
        if line.strip() == "categories:":
            in_categories = True
            continue
        if in_categories and line.strip().startswith("- "):
            category = line.strip().lstrip("- ").strip()
            break

    if category:
        return f"{site_url}/{category}/{slug}/"
    return f"{site_url}/{slug}/"


def main():
    post_file = os.environ.get("POST_FILE", "")
    site_url = os.environ.get("SITE_URL", "https://blog.heusingfeld.de")
    api_key = os.environ.get("GOOGLE_API_KEY", "")
    client_id = os.environ.get("LINKEDIN_CLIENT_ID", "")
    client_secret = os.environ.get("LINKEDIN_CLIENT_SECRET", "")
    refresh_token = os.environ.get("LINKEDIN_REFRESH_TOKEN", "")
    person_urn = os.environ.get("LINKEDIN_PERSON_URN", "")

    if not post_file or not os.path.exists(post_file):
        print("No new post file found, skipping LinkedIn posting")
        sys.exit(0)

    meta, body = extract_post_content(post_file)
    title = meta.get("title", "New Post")
    tags = meta.get("tags", [])
    post_url = construct_post_url(post_file, site_url)

    print(f"Generating LinkedIn copy for: {title}")
    print(f"Post URL: {post_url}")

    if not api_key:
        print("GOOGLE_API_KEY not set, using fallback LinkedIn copy")
        linkedin_text = f'I just published a new article: "{title}"\n\nRead it here: {post_url}'
    else:
        linkedin_text = generate_linkedin_copy(title, body, tags, api_key)
        if linkedin_text and post_url not in linkedin_text:
            linkedin_text += f"\n\nRead the full article: {post_url}"

    if not linkedin_text:
        linkedin_text = f'I just published a new article: "{title}"\n\nRead it here: {post_url}'

    print(f"\nLinkedIn copy:\n{linkedin_text}\n")

    # Save LinkedIn text for the issue comment step
    with open("/tmp/linkedin_text.txt", "w") as f:
        f.write(linkedin_text)

    with open("/tmp/post_url.txt", "w") as f:
        f.write(post_url)

    if client_id and client_secret and refresh_token and person_urn:
        # Mint a fresh access token from the refresh token
        access_token = get_access_token(client_id, client_secret, refresh_token)
        if access_token:
            post_id = post_to_linkedin(linkedin_text, access_token, person_urn)
            if post_id:
                # Save post ID for issue comment
                with open("/tmp/linkedin_post_id.txt", "w") as f:
                    f.write(post_id)
        else:
            print("::error::Failed to obtain LinkedIn access token. Check refresh token validity.")
            sys.exit(1)
    else:
        print("LinkedIn credentials not configured, skipping posting")
        print("Required secrets: LINKEDIN_CLIENT_ID, LINKEDIN_CLIENT_SECRET, "
              "LINKEDIN_REFRESH_TOKEN, LINKEDIN_PERSON_URN")


if __name__ == "__main__":
    main()
