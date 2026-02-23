#!/usr/bin/env python3
"""Transcribe audio using Google Gemini API and format as Markdown.

Uses Gemini's native audio understanding to transcribe and structure
the content with timestamps. No separate transcription API needed —
just the same GOOGLE_API_KEY used for image generation and LinkedIn copy.
"""
import os
import sys
import json
import time
import urllib.request
import urllib.error


def upload_audio_to_gemini(audio_path, api_key):
    """Upload audio file to Gemini Files API for processing.

    Required for files >20MB. We always use it for consistency
    since video audio tracks can be large.
    """
    file_size = os.path.getsize(audio_path)
    mime_type = "audio/mpeg"  # mp3

    # Step 1: Initiate resumable upload
    url = f"https://generativelanguage.googleapis.com/upload/v1beta/files?key={api_key}"
    metadata = json.dumps({
        "file": {"displayName": os.path.basename(audio_path)}
    }).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=metadata,
        headers={
            "Content-Type": "application/json",
            "X-Goog-Upload-Protocol": "resumable",
            "X-Goog-Upload-Command": "start",
            "X-Goog-Upload-Header-Content-Length": str(file_size),
            "X-Goog-Upload-Header-Content-Type": mime_type,
        },
        method="POST",
    )

    with urllib.request.urlopen(req) as resp:
        upload_url = resp.headers.get("X-Goog-Upload-URL")

    if not upload_url:
        raise RuntimeError("Failed to get upload URL from Gemini Files API")

    # Step 2: Upload the file content
    with open(audio_path, "rb") as f:
        audio_data = f.read()

    req = urllib.request.Request(
        upload_url,
        data=audio_data,
        headers={
            "Content-Length": str(file_size),
            "X-Goog-Upload-Offset": "0",
            "X-Goog-Upload-Command": "upload, finalize",
        },
        method="POST",
    )

    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read())

    file_uri = result.get("file", {}).get("uri", "")
    file_name = result.get("file", {}).get("name", "")
    state = result.get("file", {}).get("state", "")

    print(f"Uploaded: {file_name} (state: {state})")

    # Step 3: Wait for processing
    if state == "PROCESSING":
        check_url = f"https://generativelanguage.googleapis.com/v1beta/{file_name}?key={api_key}"
        for _ in range(60):  # wait up to 5 minutes
            time.sleep(5)
            req = urllib.request.Request(check_url)
            with urllib.request.urlopen(req) as resp:
                status = json.loads(resp.read())
            state = status.get("state", "")
            if state == "ACTIVE":
                print("File processing complete")
                break
            print(f"  Still processing... ({state})")
        else:
            raise RuntimeError(f"File processing timed out (state: {state})")

    return file_uri


def transcribe_with_gemini(file_uri, api_key, post_title):
    """Use Gemini to transcribe the audio with timestamps."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent?key={api_key}"

    prompt = f"""Transcribe this audio recording in full. This is a vlog/talk titled "{post_title}".

Requirements:
- Transcribe every spoken word accurately
- Add timestamps in [M:SS] format at the start of each paragraph
- Start a new paragraph roughly every 30-60 seconds, or at natural topic breaks
- Use proper punctuation and capitalization
- If the speaker mentions specific technical terms, tools, or names, spell them correctly
- Keep filler words minimal but preserve the speaker's natural phrasing
- Write in the language that is spoken (do not translate)

Output ONLY the transcript in this format:
[0:00] First paragraph text here.

[0:45] Second paragraph text here.

Do not add any introduction, summary, or commentary — just the timestamped transcript."""

    payload = json.dumps({
        "contents": [{
            "parts": [
                {"fileData": {"mimeType": "audio/mpeg", "fileUri": file_uri}},
                {"text": prompt},
            ]
        }],
        "generationConfig": {
            "temperature": 0.1,
            "maxOutputTokens": 65536,
        },
    }).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urllib.request.urlopen(req, timeout=300) as resp:
        result = json.loads(resp.read())

    candidates = result.get("candidates", [])
    if candidates:
        parts = candidates[0].get("content", {}).get("parts", [])
        if parts:
            return parts[0]["text"].strip()

    raise RuntimeError(f"No transcript returned from Gemini: {json.dumps(result, indent=2)}")


def cleanup_file(file_uri, api_key):
    """Delete the uploaded file from Gemini storage."""
    # Extract file name from URI
    # URI format: https://generativelanguage.googleapis.com/v1beta/files/xxx
    file_name = file_uri.split("/v1beta/")[-1] if "/v1beta/" in file_uri else None
    if not file_name:
        return

    url = f"https://generativelanguage.googleapis.com/v1beta/{file_name}?key={api_key}"
    req = urllib.request.Request(url, method="DELETE")
    try:
        with urllib.request.urlopen(req) as resp:
            print(f"Cleaned up uploaded file: {file_name}")
    except urllib.error.HTTPError:
        pass  # Non-fatal


def main():
    if len(sys.argv) < 3:
        print("Usage: transcribe.py <audio_file> <post_title>")
        sys.exit(1)

    audio_path = sys.argv[1]
    post_title = sys.argv[2]

    api_key = os.environ.get("GOOGLE_API_KEY", "")
    if not api_key:
        print("GOOGLE_API_KEY not set")
        sys.exit(1)

    print(f"Transcribing: {audio_path}")
    print(f"Title: {post_title}")
    print(f"File size: {os.path.getsize(audio_path) / (1024*1024):.1f} MB")

    # Upload audio to Gemini Files API
    file_uri = upload_audio_to_gemini(audio_path, api_key)

    # Transcribe using Gemini
    try:
        transcript = transcribe_with_gemini(file_uri, api_key, post_title)
    finally:
        cleanup_file(file_uri, api_key)

    output_path = "/tmp/transcript.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(transcript)

    print(f"Transcript saved to: {output_path}")
    print(f"Length: {len(transcript)} characters")


if __name__ == "__main__":
    main()
