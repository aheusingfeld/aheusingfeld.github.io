#!/usr/bin/env python3
"""Find the matching GitHub Issue for a published post and add a comment with links."""
import os
import sys
import json
import urllib.request
import urllib.error


def find_matching_issue(repo, title, token):
    """Search for an open issue matching the post title."""
    # Search for issues with matching title
    query = title.replace('"', "").replace("'", "")[:50]
    search_url = f"https://api.github.com/search/issues?q={urllib.parse.quote(query)}+repo:{repo}+is:issue+is:open"

    req = urllib.request.Request(
        search_url,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )

    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read())
            items = result.get("items", [])
            if items:
                return items[0]  # Return best match
    except urllib.error.HTTPError as e:
        print(f"GitHub search error: {e.code} - {e.read().decode()}")

    return None


def add_comment(repo, issue_number, comment, token):
    """Add a comment to a GitHub issue."""
    url = f"https://api.github.com/repos/{repo}/issues/{issue_number}/comments"

    payload = json.dumps({"body": comment}).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read())
            print(f"Comment added: {result.get('html_url', '')}")
            return True
    except urllib.error.HTTPError as e:
        print(f"GitHub comment error: {e.code} - {e.read().decode()}")

    return False


def close_issue(repo, issue_number, token):
    """Close a GitHub issue."""
    url = f"https://api.github.com/repos/{repo}/issues/{issue_number}"

    payload = json.dumps({"state": "closed"}).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "Content-Type": "application/json",
        },
        method="PATCH",
    )

    try:
        with urllib.request.urlopen(req) as resp:
            print(f"Issue #{issue_number} closed")
            return True
    except urllib.error.HTTPError as e:
        print(f"GitHub close error: {e.code} - {e.read().decode()}")

    return False


def main():
    import urllib.parse

    token = os.environ.get("GH_TOKEN", "")
    post_title = os.environ.get("POST_TITLE", "")
    post_slug = os.environ.get("POST_SLUG", "")
    site_url = os.environ.get("SITE_URL", "https://blog.heusingfeld.de")
    repo = "aheusingfeld/aheusingfeld.github.io"

    if not token or not post_title:
        print("Missing GH_TOKEN or POST_TITLE, skipping issue comment")
        sys.exit(0)

    # Read post URL and LinkedIn text from previous step
    post_url = site_url
    linkedin_text = ""
    linkedin_post_id = ""

    try:
        with open("/tmp/post_url.txt", "r") as f:
            post_url = f.read().strip()
    except FileNotFoundError:
        pass

    try:
        with open("/tmp/linkedin_text.txt", "r") as f:
            linkedin_text = f.read().strip()
    except FileNotFoundError:
        pass

    try:
        with open("/tmp/linkedin_post_id.txt", "r") as f:
            linkedin_post_id = f.read().strip()
    except FileNotFoundError:
        pass

    # Find matching issue
    issue = find_matching_issue(repo, post_title, token)
    if not issue:
        print(f'No matching issue found for: "{post_title}"')
        sys.exit(0)

    issue_number = issue["number"]
    print(f'Found matching issue #{issue_number}: {issue["title"]}')

    # Build comment
    comment_parts = [
        f"## Published! :rocket:",
        f"",
        f"**Blog post:** {post_url}",
    ]

    if linkedin_post_id:
        linkedin_url = f"https://www.linkedin.com/feed/update/{linkedin_post_id}"
        comment_parts.append(f"**LinkedIn post:** {linkedin_url}")
    elif linkedin_text:
        comment_parts.append(f"")
        comment_parts.append(f"**LinkedIn copy:**")
        comment_parts.append(f"```")
        comment_parts.append(linkedin_text)
        comment_parts.append(f"```")

    comment = "\n".join(comment_parts)

    # Add comment and close issue
    add_comment(repo, issue_number, comment, token)
    close_issue(repo, issue_number, token)


if __name__ == "__main__":
    main()
