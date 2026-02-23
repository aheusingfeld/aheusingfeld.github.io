#!/usr/bin/env python3
"""Check if a Jekyll post has a header image defined in frontmatter."""
import sys
import re
import os


def extract_frontmatter(filepath):
    """Extract YAML frontmatter from a Jekyll post."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return ""
    return match.group(1)


def has_image(frontmatter):
    """Check if frontmatter contains a non-empty image path."""
    for line in frontmatter.splitlines():
        stripped = line.strip()
        if stripped.startswith("path:"):
            value = stripped.split(":", 1)[1].strip().strip('"').strip("'")
            if value:
                return True
    return False


def main():
    if len(sys.argv) < 2:
        print("Usage: check_missing_images.py <post_file>")
        sys.exit(1)

    post_file = sys.argv[1]
    if not os.path.exists(post_file):
        print(f"File not found: {post_file}")
        # Set output for GitHub Actions
        with open(os.environ.get("GITHUB_OUTPUT", "/dev/null"), "a") as f:
            f.write("needs_image=false\n")
        sys.exit(0)

    frontmatter = extract_frontmatter(post_file)
    needs_image = not has_image(frontmatter)

    print(f"Post: {post_file}")
    print(f"Needs image: {needs_image}")

    # Set output for GitHub Actions
    output_file = os.environ.get("GITHUB_OUTPUT", "")
    if output_file:
        with open(output_file, "a") as f:
            f.write(f"needs_image={'true' if needs_image else 'false'}\n")


if __name__ == "__main__":
    main()
