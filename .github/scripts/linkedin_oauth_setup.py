#!/usr/bin/env python3
"""One-time helper to obtain a LinkedIn OAuth refresh token.

Usage:
    python3 .github/scripts/linkedin_oauth_setup.py <CLIENT_ID> <CLIENT_SECRET>

This starts a local server on port 3000, opens the LinkedIn authorization page
in your browser, and captures the callback to exchange the code for tokens.
Store the refresh_token as LINKEDIN_REFRESH_TOKEN in your GitHub Secrets.
"""
import http.server
import json
import sys
import urllib.parse
import urllib.request
import webbrowser

PORT = 3000
REDIRECT_URI = f"http://localhost:{PORT}/callback"
SCOPES = "w_member_social openid profile"


def exchange_code(code, client_id, client_secret):
    """Exchange authorization code for access + refresh tokens."""
    url = "https://www.linkedin.com/oauth/v2/accessToken"
    params = urllib.parse.urlencode({
        "grant_type": "authorization_code",
        "code": code,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": REDIRECT_URI,
    }).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=params,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())


def get_person_urn(access_token):
    """Fetch the authenticated user's LinkedIn person URN via OpenID Connect."""
    url = "https://api.linkedin.com/v2/userinfo"
    req = urllib.request.Request(
        url,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read())
        sub = data.get("sub", "")
        return f"urn:li:person:{sub}"


class CallbackHandler(http.server.BaseHTTPRequestHandler):
    token_response = None

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if not parsed.path.startswith("/callback"):
            self.send_response(404)
            self.end_headers()
            return

        params = urllib.parse.parse_qs(parsed.query)

        if "error" in params:
            self.send_response(400)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            error = params["error"][0]
            desc = params.get("error_description", [""])[0]
            self.wfile.write(f"<h1>Error: {error}</h1><p>{desc}</p>".encode())
            return

        code = params.get("code", [None])[0]
        if not code:
            self.send_response(400)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(b"<h1>No authorization code received</h1>")
            return

        # Exchange code for tokens
        try:
            result = exchange_code(code, CLIENT_ID, CLIENT_SECRET)
            CallbackHandler.token_response = result
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(b"<h1>Success!</h1><p>You can close this tab. Check your terminal for the tokens.</p>")
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(f"<h1>Token exchange failed</h1><p>{e}</p>".encode())

    def log_message(self, format, *args):
        pass  # Suppress request logging


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 linkedin_oauth_setup.py <CLIENT_ID> <CLIENT_SECRET>")
        sys.exit(1)

    CLIENT_ID = sys.argv[1]
    CLIENT_SECRET = sys.argv[2]

    # Build authorization URL
    auth_url = (
        "https://www.linkedin.com/oauth/v2/authorization?"
        + urllib.parse.urlencode({
            "response_type": "code",
            "client_id": CLIENT_ID,
            "redirect_uri": REDIRECT_URI,
            "scope": SCOPES,
        })
    )

    print(f"\n{'='*60}")
    print("LinkedIn OAuth Setup")
    print(f"{'='*60}")
    print(f"\nStarting local server on port {PORT}...")
    print("Opening LinkedIn authorization page in your browser...\n")

    server = http.server.HTTPServer(("localhost", PORT), CallbackHandler)

    webbrowser.open(auth_url)

    print("Waiting for callback... (authorize the app in your browser)\n")

    # Handle requests until we get the token
    while CallbackHandler.token_response is None:
        server.handle_request()

    server.server_close()
    result = CallbackHandler.token_response

    # Fetch person URN
    token_for_urn = result.get("access_token", "")
    person_urn = ""
    if token_for_urn:
        try:
            person_urn = get_person_urn(token_for_urn)
        except Exception as e:
            print(f"Warning: Could not fetch person URN: {e}")

    # Debug: show the full response from LinkedIn
    print(f"\n{'='*60}")
    print("RAW TOKEN RESPONSE FROM LINKEDIN:")
    print(f"{'='*60}")
    print(json.dumps(result, indent=2))
    print(f"{'='*60}\n")

    access_token_val = result.get("access_token", "")
    refresh_token = result.get("refresh_token", "")
    refresh_expires = result.get("refresh_token_expires_in", 0)
    expires_in = result.get("expires_in", 0)

    print("TOKENS RECEIVED — Add these as GitHub Secrets:\n")

    if access_token_val:
        days = expires_in // 86400 if expires_in else "?"
        print(f"ACCESS_TOKEN (expires in {days} days):\n{access_token_val}\n")

    if refresh_token:
        days = refresh_expires // 86400 if refresh_expires else "?"
        print(f"LINKEDIN_REFRESH_TOKEN (valid for {days} days):\n{refresh_token}\n")
    else:
        print("WARNING: No refresh token received!")
        print("Refresh tokens require 'Marketing Developer Platform' approval.")
        print("Without it, you'll need to use the access_token directly (60-day TTL).")
        print()
        if access_token_val:
            print("FALLBACK: Store the access token as a secret instead:")
            print(f"  gh secret set LINKEDIN_ACCESS_TOKEN")
            print("  (paste the access token when prompted)\n")

    if person_urn:
        print(f"LINKEDIN_PERSON_URN:\n{person_urn}\n")

    print(f"{'='*60}")
    print("Run these to add as GitHub secrets:")
    print(f"{'='*60}\n")
    if refresh_token:
        print('  gh secret set LINKEDIN_REFRESH_TOKEN')
        print('  (paste the refresh token when prompted)\n')
    elif access_token_val:
        print('  gh secret set LINKEDIN_ACCESS_TOKEN')
        print('  (paste the access token when prompted)\n')
    if person_urn:
        print(f'  gh secret set LINKEDIN_PERSON_URN --body "{person_urn}"')
    print()
