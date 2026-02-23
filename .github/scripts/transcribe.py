#!/usr/bin/env python3
"""Transcribe audio using OpenAI Whisper API and format as Markdown."""
import os
import sys


def transcribe_with_whisper(audio_path, api_key):
    """Transcribe audio file using OpenAI Whisper API."""
    from openai import OpenAI

    client = OpenAI(api_key=api_key)

    with open(audio_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="verbose_json",
            timestamp_granularities=["segment"],
        )

    return transcript


def format_timestamp(seconds):
    """Format seconds as M:SS or H:MM:SS."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    if hours > 0:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    return f"{minutes}:{secs:02d}"


def format_transcript(transcript):
    """Convert Whisper transcript to Markdown with timestamps."""
    lines = []

    segments = transcript.segments if hasattr(transcript, "segments") else []

    current_paragraph = []
    last_timestamp = None
    paragraph_start = 0

    for segment in segments:
        start = segment.get("start", segment.start if hasattr(segment, "start") else 0)
        text = segment.get("text", segment.text if hasattr(segment, "text") else "").strip()

        if not text:
            continue

        if last_timestamp is None:
            paragraph_start = start

        current_paragraph.append(text)

        # Start new paragraph roughly every 60 seconds or at sentence endings
        is_sentence_end = text.endswith((".", "!", "?"))
        time_gap = start - paragraph_start > 60

        if is_sentence_end and (time_gap or len(current_paragraph) > 5):
            timestamp = format_timestamp(paragraph_start)
            paragraph_text = " ".join(current_paragraph)
            lines.append(f"[{timestamp}] {paragraph_text}")
            lines.append("")
            current_paragraph = []
            paragraph_start = start

        last_timestamp = start

    # Flush remaining text
    if current_paragraph:
        timestamp = format_timestamp(paragraph_start)
        paragraph_text = " ".join(current_paragraph)
        lines.append(f"[{timestamp}] {paragraph_text}")
        lines.append("")

    return "\n".join(lines)


def main():
    if len(sys.argv) < 3:
        print("Usage: transcribe.py <audio_file> <post_title>")
        sys.exit(1)

    audio_path = sys.argv[1]
    post_title = sys.argv[2]

    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        print("OPENAI_API_KEY not set")
        sys.exit(1)

    print(f"Transcribing: {audio_path}")
    print(f"Title: {post_title}")

    transcript = transcribe_with_whisper(audio_path, api_key)
    markdown = format_transcript(transcript)

    output_path = "/tmp/transcript.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(markdown)

    print(f"Transcript saved to: {output_path}")
    print(f"Length: {len(markdown)} characters")


if __name__ == "__main__":
    main()
