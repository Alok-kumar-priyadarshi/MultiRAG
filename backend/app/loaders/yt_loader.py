"""
Purpose:
Fetches transcript from YouTube videos using YouTube Transcript API.
Compatible with latest versions.
"""

from youtube_transcript_api import YouTubeTranscriptApi
import re


def extract_video_id(url: str) -> str:
    patterns = [
        r"v=([^&]+)",
        r"youtu\.be/([^?]+)"
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)

    return None

def clean_transcript(text: str) -> str:
    # remove music symbols and brackets
    text = re.sub(r"\[.*?\]", "", text)
    text = re.sub(r"♪", "", text)

    # normalize spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()

def load_youtube(url: str) -> str:
    try:
        video_id = extract_video_id(url)

        if not video_id:
            return "Invalid YouTube URL"

        # 🔴 FIX: use instance method
        api = YouTubeTranscriptApi()

        transcript = api.fetch(video_id)

        text = " ".join([entry.text for entry in transcript])
        
        text = clean_transcript(text)

        return text

    except Exception as e:
        return f"Error loading YouTube transcript: {str(e)}"