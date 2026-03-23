"""
Purpose:
Determines the type of input (text, PDF, URL, YouTube).
Acts as the decision-making layer before ingestion.
"""

import re


# 🔹 YouTube detection (robust)
def is_youtube_url(text: str) -> bool:
    youtube_patterns = [
        r"(youtube\.com/watch\?v=)",
        r"(youtu\.be/)",
        r"(youtube\.com/shorts/)"
    ]
    return any(re.search(pattern, text) for pattern in youtube_patterns)


# 🔹 PDF detection
def is_pdf_url(text: str) -> bool:
    return text.lower().endswith(".pdf")


# 🔹 General URL detection
def is_general_url(text: str) -> bool:
    url_pattern = r"https?://[^\s]+"
    return re.search(url_pattern, text) is not None


def classify_input(query: str = None, url: str = None, file=None):
    """
    Classifies the incoming request into a type.

    Returns:
        str: one of ["TEXT", "PDF", "URL", "YOUTUBE"]
    """

    # 🔴 Case 1: File upload (highest priority)
    if file:
        return "PDF"

    # 🔴 Case 2: Explicit URL field
    if url:
        if is_youtube_url(url):
            return "YOUTUBE"
        elif is_pdf_url(url):
            return "PDF"
        else:
            return "URL"

    # 🔴 Case 3: Query contains URL
    if query and is_general_url(query):
        if is_youtube_url(query):
            return "YOUTUBE"
        elif is_pdf_url(query):
            return "PDF"
        else:
            return "URL"

    # 🔴 Default
    return "TEXT"