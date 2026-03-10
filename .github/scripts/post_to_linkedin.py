#!/usr/bin/env python3
"""Generate LinkedIn copy via Gemini API and post to LinkedIn.

Authentication: Uses a stored OAuth access token (60-day TTL).
Since LinkedIn only provides refresh tokens to Marketing Developer Platform
partners, we use the access token directly and pair this with a scheduled
workflow (.github/workflows/linkedin-token-check.yml) that creates a GitHub
Issue reminder 14 days before expiry.

Required GitHub Secrets:
  LINKEDIN_ACCESS_TOKEN   - OAuth access token (valid ~60 days)
  LINKEDIN_PERSON_URN     - Your LinkedIn member URN (urn:li:person:xxxxxxx)
  LINKEDIN_CLIENT_ID      - OAuth app Client ID (for token introspection)
  LINKEDIN_CLIENT_SECRET  - OAuth app Client Secret (for token introspection)
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

    # Parse tags robustly
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
    """Use Gemini to generate engaging LinkedIn teaser."""
    style_examples = get_style_examples()
    examples_text = "\n\n---\n\n".join(
        f"Example {i+1}:\n{ex}" for i, ex in enumerate(style_examples)
    )

    # Get first 500 words of the new post
    post_excerpt = " ".join(body.split()[:500])

    prompt = f"""Schreibe einen LinkedIn teaser post fuer meinen neuen blog post.

Hier ist mein linkeding profile als Referenz und fuer deine Kontextrecherche: https://www.linkedin.com/in/alexander-heusingfeld/.

## Blog Post Inhalt

{post_excerpt}

## Immitiere meinen Schreibstil

Hier sind ein paar Beispiele meines Schreibstils:

{examples_text}

## MUST HAVE Anforderungen:
- Beginne mit einer provozierenden Frage oder Feststellung, die die Aufmerksamkeit der Leser weckt
- Verrate so wenig vom Inhalt wie moeglich, wecke die Neugier auf den Artikel
- Nutze weniger als 100 Worte
- Bleibe nachdenklich und authentisch, das ist kein Sales Pitch!
- Immitiere Alexanders reflektierten, systems-thinking Tonfall
- Write in German
- Schreibe einen klaren Aufruf den Artikel zu lesen
- Beende den Post mit einer Frage an die Leser, die sie in den Kommentaren beantworten sollen 

Return ONLY the LinkedIn post text, nothing else."""

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-preview:generateContent?key={api_key}"

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


def check_already_posted(post_title):
    """Check if a LinkedIn post was already made for this blog post.

    Looks for an existing GitHub Issue comment containing 'LinkedIn post'
    on the matching issue. This prevents duplicate LinkedIn posts on
    re-runs, retries, or workflow_dispatch.
    """
    gh_token = os.environ.get("GH_TOKEN", os.environ.get("GITHUB_TOKEN", ""))
    repo = os.environ.get("GITHUB_REPOSITORY", "")

    if not gh_token or not repo:
        return False  # Can't check, proceed cautiously

    # Search for matching open issue
    search_title = post_title.replace('"', '\\"')
    url = f"https://api.github.com/search/issues?q=repo:{repo}+is:issue+%22{urllib.parse.quote(search_title)}%22"

    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {gh_token}",
            "Accept": "application/vnd.github+json",
        },
    )

    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read())
            for issue in data.get("items", []):
                # Check comments on this issue for LinkedIn post link
                comments_url = issue.get("comments_url", "")
                if not comments_url:
                    continue
                req2 = urllib.request.Request(
                    comments_url,
                    headers={
                        "Authorization": f"Bearer {gh_token}",
                        "Accept": "application/vnd.github+json",
                    },
                )
                with urllib.request.urlopen(req2) as resp2:
                    comments = json.loads(resp2.read())
                    for comment in comments:
                        if "linkedin.com" in comment.get("body", "").lower():
                            print(f"LinkedIn post already exists for '{post_title}' — skipping")
                            return True
    except Exception as e:
        print(f"Deduplication check failed ({e}), proceeding")

    return False


def check_token_validity(access_token, client_id, client_secret):
    """Introspect the access token to check remaining validity.

    Returns remaining seconds or -1 if check fails (non-fatal).
    """
    url = "https://www.linkedin.com/oauth/v2/introspectToken"
    params = urllib.parse.urlencode({
        "token": access_token,
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
            if not result.get("active", False):
                print("::error::LinkedIn access token is no longer active!")
                print("Re-authorize: python3 /tmp/linkedin_oauth_setup.py <CLIENT_ID> <CLIENT_SECRET>")
                return 0
            expires_at = result.get("expires_at", 0)
            if expires_at:
                import time
                remaining = expires_at - int(time.time())
                days_left = remaining // 86400
                print(f"LinkedIn token valid for {days_left} more days")
                if days_left < 14:
                    print(f"::warning::LinkedIn access token expires in {days_left} days! Renew soon.")
                return remaining
    except urllib.error.HTTPError as e:
        # Introspection failure is non-fatal — we still try to post
        print(f"Token introspection failed ({e.code}), proceeding anyway")

    return -1


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
        if e.code == 401:
            print("::error::LinkedIn access token has expired. Renew it:")
            print("  python3 /tmp/linkedin_oauth_setup.py <CLIENT_ID> <CLIENT_SECRET>")
            print("  Then: gh secret set LINKEDIN_ACCESS_TOKEN")
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
    access_token = os.environ.get("LINKEDIN_ACCESS_TOKEN", "")
    person_urn = os.environ.get("LINKEDIN_PERSON_URN", "")
    client_id = os.environ.get("LINKEDIN_CLIENT_ID", "")
    client_secret = os.environ.get("LINKEDIN_CLIENT_SECRET", "")

    if not post_file or not os.path.exists(post_file):
        print("No new post file found, skipping LinkedIn posting")
        sys.exit(0)

    meta, body = extract_post_content(post_file)
    title = meta.get("title", "New Post")
    tags = meta.get("tags", [])
    post_url = construct_post_url(post_file, site_url)

    print(f"Generating LinkedIn copy for: {title}")
    print(f"Post URL: {post_url}")

    # Deduplication: skip if LinkedIn was already posted for this article
    if check_already_posted(title):
        sys.exit(0)

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

    if access_token and person_urn:
        # Check token validity if credentials available (non-fatal)
        if client_id and client_secret:
            check_token_validity(access_token, client_id, client_secret)

        post_id = post_to_linkedin(linkedin_text, access_token, person_urn)
        if post_id:
            # Save post ID for issue comment
            with open("/tmp/linkedin_post_id.txt", "w") as f:
                f.write(post_id)
    else:
        print("LinkedIn credentials not configured, skipping posting")
        print("Required secrets: LINKEDIN_ACCESS_TOKEN, LINKEDIN_PERSON_URN")


if __name__ == "__main__":
    main()
