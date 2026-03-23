"""
Purpose:
Splits large text into smaller overlapping chunks for better retrieval.
"""

def chunk_text(text: str, chunk_size: int = 20, overlap: int = 5):
    """
    Splits text into overlapping chunks.

    Args:
        text (str): Input text
        chunk_size (int): Size of each chunk
        overlap (int): Overlap between chunks

    Returns:
        List[str]: List of text chunks
    """
    words = text.split()
    chunks = []

    start = 0
    total_words = len(words)

    while start < total_words:
        end = start + chunk_size
        chunk_words = words[start:end]

        chunk = " ".join(chunk_words)
        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks

