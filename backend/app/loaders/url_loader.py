"""
Purpose:
Fetches and extracts readable text from web pages.
"""

import requests
from bs4 import BeautifulSoup

def load_url(url: str) -> str:
    """
    Extracts text from a webpage.

    Args:
        url (str): Webpage URL

    Returns:
        str: Extracted text
    """
    
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code != 200:
            return f"Error: Status code {response.status_code}"

        soup = BeautifulSoup(response.text, "html.parser")

        for tag in soup(["script", "style"]):
            tag.decompose()

        text = soup.get_text(separator=" ")

        return text.strip()

    except Exception as e:
        return f"Error loading URL: {str(e)}"

