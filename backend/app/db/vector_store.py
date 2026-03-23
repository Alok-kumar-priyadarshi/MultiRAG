"""
Purpose:
Handles storing and retrieving embeddings using FAISS.
Includes relevance filtering to improve RAG quality.
"""

import faiss
import numpy as np

# 🔹 Global storage (in-memory)
dimension = 384  # MiniLM embedding size

index = faiss.IndexFlatL2(dimension)
stored_texts = []


def add_embeddings(embeddings, texts):
    """
    Adds embeddings to FAISS index.

    Args:
        embeddings (List[List[float]])
        texts (List[str])
    """
    global stored_texts

    if not embeddings or not texts:
        return

    vectors = np.array(embeddings).astype("float32")

    index.add(vectors)
    stored_texts.extend(texts)

    print(f"[DEBUG] Added {len(texts)} chunks. Total = {index.ntotal}")


def search(query_embedding, top_k=5, distance_threshold=1.8):
    """
    Searches for most similar chunks with filtering.

    Args:
        query_embedding (List[float])
        top_k (int)
        distance_threshold (float): lower = stricter

    Returns:
        List[str]
    """

    if index.ntotal == 0:
        print("[DEBUG] FAISS is empty")
        return []

    query_vector = np.array([query_embedding]).astype("float32")

    distances, indices = index.search(query_vector, top_k)

    results = []
    seen = set()

    for dist, idx in zip(distances[0], indices[0]):

        # 🔴 Filter invalid index
        if idx < 0 or idx >= len(stored_texts):
            continue

        # 🔴 FILTER IRRELEVANT RESULTS
        if dist > distance_threshold:
            continue

        text = stored_texts[idx]

        if text not in seen:
            results.append(text)
            seen.add(text)

    print(f"[DEBUG] FAISS total vectors: {index.ntotal}")
    print(f"[DEBUG] Retrieved {len(results)} relevant chunks")

    return results


def reset_index():
    """
    Resets FAISS index (clears all stored data).
    """

    global index, stored_texts

    index = faiss.IndexFlatL2(dimension)
    stored_texts = []

    print("[DEBUG] FAISS index reset")