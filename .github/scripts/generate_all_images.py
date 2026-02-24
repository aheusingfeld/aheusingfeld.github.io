#!/usr/bin/env python3
"""
Batch-generate header images for all existing Jekyll posts using
Google Gemini Nano Banana Pro (gemini-3-pro-image-preview).

Usage:
    GOOGLE_API_KEY=your_key python3 .github/scripts/generate_all_images.py

Requires:
    pip install google-genai Pillow

Features:
- Scans _posts/ for all post files (.html, .md, .adoc, .asciidoc)
- Extracts title AND body content (first 500 words) for content-aware prompts
- Generates header images via Gemini Nano Banana Pro
- Saves images to assets/img/<slug>.png
- Updates each post's front matter with the image path
- Rate limiting (5s between calls) with exponential backoff on 429s
- Skips posts that already have an image defined
"""
import os
import re
import sys
import time
import glob


def extract_frontmatter_and_content(filepath):
    """Extract title and body content from a Jekyll post (any format)."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)", content, re.DOTALL)
    if not match:
        return "", "", False

    frontmatter = match.group(1)
    body = match.group(2)

    # Check if image is already defined
    has_image = "image:" in frontmatter

    # Extract title
    title = ""
    for line in frontmatter.splitlines():
        if line.strip().startswith("title:"):
            title = line.split(":", 1)[1].strip().strip('"').strip("'")
            break

    # Strip markup from body based on file extension
    ext = os.path.splitext(filepath)[1].lower()
    if ext == ".html":
        # Strip HTML tags
        clean = re.sub(r"<[^>]+>", " ", body)
    elif ext in (".adoc", ".asciidoc"):
        # Strip AsciiDoc syntax
        clean = re.sub(r"^=+\s+.*$", "", body, flags=re.MULTILINE)  # headers
        clean = re.sub(r"\[source[^\]]*\]", "", clean)  # source blocks
        clean = re.sub(r"----.*?----", " ", clean, flags=re.DOTALL)  # code blocks
        clean = re.sub(r"https?://\S+\[([^\]]*)\]", r"\1", clean)  # links
        clean = re.sub(r"[*_`]", "", clean)
    else:
        # Strip Markdown syntax
        clean = re.sub(r"```.*?```", " ", body, flags=re.DOTALL)  # code blocks
        clean = re.sub(r"`[^`]+`", " ", clean)  # inline code
        clean = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", clean)  # links
        clean = re.sub(r"[#*_\[\]()>`~]", "", clean)

    # Get first 500 words
    words = clean.split()[:500]
    excerpt = " ".join(words)

    return title, excerpt, has_image


def get_slug(filename):
    """Derive image slug from post filename."""
    base = os.path.basename(filename)
    # Remove extension
    for ext in [".html", ".asciidoc", ".adoc", ".md"]:
        if base.endswith(ext):
            base = base[: -len(ext)]
            break
    # Remove leading date (YYYY-MM-DD-)
    parts = base.split("-", 3)
    if len(parts) >= 4 and len(parts[0]) == 4 and parts[0].isdigit():
        return parts[3]
    return base


def generate_image(title, excerpt, client):
    """Generate a header image using Gemini Nano Banana Pro."""
    from google.genai import types

    prompt = (
        f'Create a minimalist, abstract blog header image for an article titled "{title}". '
        f"The article discusses: {excerpt[:500]}. "
        "Style: clean, professional, muted color palette with dark slate-blue (#34374C) as accent. "
        "No text overlay. Abstract and conceptual, suitable for a technology and leadership blog. "
        "16:9 aspect ratio."
    )

    response = client.models.generate_content(
        model="gemini-3-pro-image-preview",
        contents=[prompt],
        config=types.GenerateContentConfig(
            response_modalities=["IMAGE"],
        ),
    )

    for part in response.parts:
        if part.inline_data is not None:
            return part.as_image()
    return None


def update_frontmatter(filepath, image_path):
    """Add image path to post frontmatter."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    match = re.match(r"^(---\s*\n)(.*?)(\n---)", content, re.DOTALL)
    if match:
        fm = match.group(2)
        if "image:" not in fm:
            new_fm = fm + f"\nimage: {image_path}"
            content = (
                match.group(1) + new_fm + match.group(3) + content[match.end() :]
            )

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)


def log(msg):
    """Print with flush for unbuffered output."""
    print(msg, flush=True)


def main():
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        log("ERROR: GOOGLE_API_KEY environment variable not set")
        sys.exit(1)

    from google import genai

    client = genai.Client(api_key=api_key)

    # Find all posts
    post_dir = "_posts"
    patterns = ["*.html", "*.md", "*.adoc", "*.asciidoc"]
    posts = []
    for pattern in patterns:
        posts.extend(glob.glob(os.path.join(post_dir, pattern)))
    posts.sort()

    image_dir = "assets/img"
    os.makedirs(image_dir, exist_ok=True)

    total = len(posts)
    success = 0
    skipped = 0
    failed = 0

    log(f"Found {total} posts to process")
    log(f"Images will be saved to {image_dir}/")
    log("=" * 60)

    for i, post_file in enumerate(posts, 1):
        title, excerpt, has_image = extract_frontmatter_and_content(post_file)
        slug = get_slug(post_file)
        image_filename = f"{slug}.png"
        full_path = f"{image_dir}/{image_filename}"

        if has_image and os.path.exists(full_path):
            log(f"[{i}/{total}] SKIP (already has image): {os.path.basename(post_file)}")
            skipped += 1
            continue

        if not title:
            log(f"[{i}/{total}] SKIP (no title): {os.path.basename(post_file)}")
            skipped += 1
            continue

        log(f"[{i}/{total}] Generating: {title[:60]}...")

        # Retry with exponential backoff
        max_retries = 3
        for attempt in range(max_retries):
            try:
                image = generate_image(title, excerpt, client)
                if image:
                    image.save(full_path)
                    update_frontmatter(post_file, image_filename)
                    log(f"         -> Saved: {full_path}")
                    success += 1
                    break
                else:
                    log(f"         -> No image returned")
                    failed += 1
                    break
            except Exception as e:
                error_msg = str(e)
                if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
                    wait = 10 * (2**attempt)
                    log(f"         -> Rate limited, waiting {wait}s (attempt {attempt + 1}/{max_retries})")
                    time.sleep(wait)
                    if attempt == max_retries - 1:
                        log(f"         -> FAILED after {max_retries} retries: {error_msg[:100]}")
                        failed += 1
                else:
                    log(f"         -> ERROR: {error_msg[:100]}")
                    failed += 1
                    break

        # Rate limiting between calls
        if i < total:
            time.sleep(5)

    log("=" * 60)
    log(f"Done! Success: {success}, Skipped: {skipped}, Failed: {failed}")


if __name__ == "__main__":
    main()
