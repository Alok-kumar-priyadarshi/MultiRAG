"""
Purpose:
Handles full ingestion pipeline:
Loader → Clean → Chunk → Embed → Store
"""

from app.utils.chunking import chunk_text
from app.utils.embeddings import get_embeddings
from app.db.vector_store import add_embeddings

from app.loaders.pdf_loader import load_pdf
from app.loaders.url_loader import load_url
from app.loaders.yt_loader import load_youtube

import re


# 🔹 TEXT CLEANING FUNCTION
def clean_text(text: str) -> str:
    """
    Cleans raw text before chunking.
    """

    if not text:
        return ""

    # remove extra spaces
    text = re.sub(r"\s+", " ", text)

    # remove weird characters
    text = re.sub(r"[^\w\s.,!?]", "", text)

    return text.strip()


def ingest_data(input_type: str, input_data: str):
    """
    Main ingestion pipeline.

    Args:
        input_type (str): TEXT / PDF / URL / YOUTUBE
        input_data (str): actual data

    Returns:
        dict
    """

    # 🔹 Step 1: Load data
    if input_type == "TEXT":
        raw_text = input_data

    elif input_type == "PDF":
        raw_text = load_pdf(input_data)

    elif input_type == "URL":
        raw_text = load_url(input_data)

    elif input_type == "YOUTUBE":
        raw_text = load_youtube(input_data)

        if not raw_text:
            return {"error": "No transcript available for this video"}

    else:
        return {"error": "Invalid input type"}

    # 🔴 VALIDATION (IMPORTANT)
    if not raw_text or len(raw_text.strip()) < 50:
        return {"error": "No meaningful content extracted"}

    # 🔹 Step 2: Clean text
    cleaned_text = clean_text(raw_text)

    # 🔹 Step 3: Chunk
    chunks = chunk_text(cleaned_text)

    # 🔴 FILTER BAD CHUNKS
    chunks = [c.strip() for c in chunks if len(c.strip()) > 10]

    if not chunks:
        return {"error": "No valid chunks generated"}

    # 🔹 Step 4: Embeddings
    embeddings = get_embeddings(chunks)

    if not embeddings or len(embeddings) == 0:
        return {"error": "Embedding failed"}

    # 🔹 Step 5: Store
    add_embeddings(embeddings, chunks)

    print(f"[DEBUG] Ingested {len(chunks)} chunks")

    return {
        "message": "Ingestion successful",
        "num_chunks": len(chunks)
    }