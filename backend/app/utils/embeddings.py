"""
Purpose:
Generates embeddings using sentence-transformers.
"""

from sentence_transformers import SentenceTransformer
from app.core.config import settings
import numpy as np



# load model once
model = SentenceTransformer(settings.sentence_transformer_model)

def get_embeddings(texts):
    """
    Converts list of texts into embeddings.

    Args:
        texts (List[str])

    Returns:
        List[List[float]]
    """
    if not texts or not isinstance(texts, list):
        raise ValueError("Invalid input for embeddings")

    embeddings = model.encode(texts)

    # ✅ Convert numpy → Python list
    if isinstance(embeddings, np.ndarray):
        embeddings = embeddings.tolist()

    # ✅ Safety check
    if len(embeddings) == 0:
        raise ValueError("Embeddings empty")

    return embeddings
    

