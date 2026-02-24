#!/usr/bin/env python3
"""Generate a fallback header image for a blog post using Gemini Nano Banana Pro."""
import os
import re
import sys


def extract_frontmatter_and_content(filepath):
    """Extract title and body content (first 500 words) from a Jekyll post."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)", content, re.DOTALL)
    if not match:
        return "", ""

    frontmatter = match.group(1)
    body = match.group(2)

    # Extract title
    title = ""
    for line in frontmatter.splitlines():
        if line.strip().startswith("title:"):
            title = line.split(":", 1)[1].strip().strip('"').strip("'")
            break

    # Strip markup from body based on file extension
    ext = os.path.splitext(filepath)[1].lower()
    if ext == ".html":
        clean = re.sub(r"<[^>]+>", " ", body)
    elif ext in (".adoc", ".asciidoc"):
        clean = re.sub(r"^=+\s+.*$", "", body, flags=re.MULTILINE)
        clean = re.sub(r"\[source[^\]]*\]", "", clean)
        clean = re.sub(r"----.*?----", " ", clean, flags=re.DOTALL)
        clean = re.sub(r"https?://\S+\[([^\]]*)\]", r"\1", clean)
        clean = re.sub(r"[*_`]", "", clean)
    else:
        clean = re.sub(r"```.*?```", " ", body, flags=re.DOTALL)
        clean = re.sub(r"`[^`]+`", " ", clean)
        clean = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", clean)
        clean = re.sub(r"[#*_\[\]()>`~]", "", clean)

    # Get first 500 words of body content
    words = clean.split()[:500]
    excerpt = " ".join(words)

    return title, excerpt


def generate_image(title, excerpt, api_key):
    """Generate header image using Gemini Nano Banana Pro (google-genai SDK)."""
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=api_key)

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
        else:
            # Update existing empty image path
            content = re.sub(
                r"^image:.*$",
                f"image: {image_path}",
                content,
                count=1,
                flags=re.MULTILINE,
            )

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)


def main():
    if len(sys.argv) < 2:
        print("Usage: generate_header_image.py <post_file>")
        sys.exit(1)

    post_file = sys.argv[1]
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("GOOGLE_API_KEY not set, skipping image generation")
        sys.exit(0)

    title, excerpt = extract_frontmatter_and_content(post_file)
    if not title:
        print("Could not extract title from post")
        sys.exit(1)

    print(f"Generating header image for: {title}")
    print(f"Content excerpt: {excerpt[:100]}...")

    image = generate_image(title, excerpt, api_key)
    if not image:
        print("Image generation failed, post will use default teaser image")
        sys.exit(0)

    # Save image
    slug = os.path.basename(post_file)
    for ext in [".html", ".asciidoc", ".adoc", ".md"]:
        slug = slug.replace(ext, "")
    image_filename = f"{slug}.png"
    image_dir = "assets/img"
    os.makedirs(image_dir, exist_ok=True)
    full_path = f"{image_dir}/{image_filename}"

    image.save(full_path)
    print(f"Image saved to: {full_path}")

    # Update post frontmatter (Lagrange expects just the filename)
    update_frontmatter(post_file, image_filename)
    print(f"Updated frontmatter with image: {image_filename}")


if __name__ == "__main__":
    main()
