import os
from typing import List

import google.generativeai as genai

# Configure the Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

EMBEDDING_MODEL = "models/gemini-embedding-001"
EMBEDDING_DIM = 3072


def generate_embedding(text: str) -> List[float]:
    """Generate an embedding vector for a single text using Gemini."""
    result = genai.embed_content(
        model=EMBEDDING_MODEL,
        content=text,
        task_type="retrieval_document",
    )
    return result["embedding"]


def generate_embeddings_batch(texts: List[str]) -> List[List[float]]:
    """Generate embedding vectors for a batch of texts using Gemini.

    Processes texts individually to handle potential failures gracefully.
    """
    embeddings = []
    for text in texts:
        try:
            embedding = generate_embedding(text)
            embeddings.append(embedding)
        except Exception as e:
            print(f"Error generating embedding for text: {text[:50]}... - {e}")
            # Use zero vector as fallback for failed embeddings
            embeddings.append([0.0] * EMBEDDING_DIM)
    return embeddings


def generate_query_embedding(query: str) -> List[float]:
    """Generate an embedding for a search query."""
    result = genai.embed_content(
        model=EMBEDDING_MODEL,
        content=query,
        task_type="retrieval_query",
    )
    return result["embedding"]
