#!/usr/bin/env python3
"""Generate a fallback header image for a blog post using Gemini API (Imagen 3)."""
import os
import re
import sys
import json
import base64
import urllib.request
import urllib.error


def extract_frontmatter_and_content(filepath):
    """Extract frontmatter and first 200 words of content."""
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

    # Get first 200 words of body (strip markdown)
    words = re.sub(r"[#*_\[\]()>`]", "", body).split()[:200]
    excerpt = " ".join(words)

    return title, excerpt


def generate_image_with_gemini(title, excerpt, api_key):
    """Call Gemini API to generate an image."""
    prompt = (
        f'Create a minimalist, abstract blog header image for an article titled "{title}". '
        f"The article discusses: {excerpt[:300]}. "
        "Style: clean, professional, muted color palette with dark slate-blue (#34374C) as accent. "
        "Aspect ratio approximately 1200x630. No text overlay. "
        "Abstract and conceptual, suitable for a technology and leadership blog."
    )

    # Use Gemini's Imagen model for image generation
    url = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-002:predict?key={api_key}"

    payload = json.dumps({
        "instances": [{"prompt": prompt}],
        "parameters": {
            "sampleCount": 1,
            "aspectRatio": "16:9",
            "safetyFilterLevel": "block_few",
        },
    }).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read())
            # Extract base64 image from response
            predictions = result.get("predictions", [])
            if predictions:
                return base64.b64decode(predictions[0]["bytesBase64Encoded"])
    except urllib.error.HTTPError as e:
        print(f"Gemini API error: {e.code} - {e.read().decode()}")
        # Fallback: try text-to-image with gemini-3-pro-preview
        return generate_with_gemini_flash(title, api_key)

    return None


def generate_with_gemini_flash(title, api_key):
    """Fallback: use gemini-3-pro-preview for image generation."""
    try:
        import google.generativeai as genai

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-3-pro-preview")

        prompt = (
            f'Generate an image: minimalist abstract blog header for "{title}". '
            "Clean, professional, muted colors with dark slate-blue accent. No text."
        )

        response = model.generate_content(prompt)
        for part in response.parts:
            if hasattr(part, "inline_data") and part.inline_data.mime_type.startswith("image/"):
                return part.inline_data.data
    except Exception as e:
        print(f"Gemini Flash fallback also failed: {e}")

    return None


def update_frontmatter(filepath, image_path):
    """Add image path to post frontmatter."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Insert image block before the closing ---
    match = re.match(r"^(---\s*\n)(.*?)(\n---)", content, re.DOTALL)
    if match:
        fm = match.group(2)
        # Check if image block already exists
        if "image:" not in fm:
            new_fm = fm + f'\nimage:\n  path: "{image_path}"\n  alt: "Header image"\n  caption: "Generated with AI"'
            content = match.group(1) + new_fm + match.group(3) + content[match.end():]
        else:
            # Update existing empty image path
            content = re.sub(
                r'(image:\s*\n\s*path:\s*)"?"?\s*"?"?',
                f'\\1"{image_path}"',
                content,
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

    image_data = generate_image_with_gemini(title, excerpt, api_key)
    if not image_data:
        print("Image generation failed, post will use default teaser image")
        sys.exit(0)

    # Save image
    slug = os.path.basename(post_file).replace(".md", "").replace(".adoc", "")
    image_filename = f"{slug}.jpg"
    image_dir = "assets/images/posts"
    os.makedirs(image_dir, exist_ok=True)
    image_path = f"/{image_dir}/{image_filename}"
    full_path = f"{image_dir}/{image_filename}"

    with open(full_path, "wb") as f:
        f.write(image_data)

    print(f"Image saved to: {full_path}")

    # Update post frontmatter
    update_frontmatter(post_file, image_path)
    print(f"Updated frontmatter with image path: {image_path}")


if __name__ == "__main__":
    main()
