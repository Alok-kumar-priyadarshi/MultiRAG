    
"""
Purpose:
Generate embeddings using HuggingFace Inference API (FREE)
"""

from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv

load_dotenv()


# Initialize client
client = InferenceClient(
    model="sentence-transformers/all-MiniLM-L6-v2",
    token=os.getenv("HF_TOKEN")
)

def get_embeddings(texts):
    if not texts or not isinstance(texts, list):
        raise ValueError("Invalid input")

    texts = [str(t).strip() for t in texts if t]

    embeddings = []

    for text in texts:
        emb = client.feature_extraction(text)
        embeddings.append(emb)

    return embeddings
