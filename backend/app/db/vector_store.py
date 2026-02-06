import json
import os
from typing import List, Optional, Tuple

import faiss
import numpy as np

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
INDEX_PATH = os.path.join(DATA_DIR, "faiss_index.bin")
METADATA_PATH = os.path.join(DATA_DIR, "faiss_metadata.json")

EMBEDDING_DIM = 3072  # Gemini gemini-embedding-001 dimension


class VectorStore:
    """FAISS vector store manager for incident embeddings."""

    def __init__(self):
        self.index: Optional[faiss.IndexFlatL2] = None
        self.metadata: List[str] = []  # Parallel list of log texts
        self._initialize()

    def _initialize(self):
        """Initialize a fresh FAISS index."""
        self.index = faiss.IndexFlatL2(EMBEDDING_DIM)
        self.metadata = []

    def add_vectors(self, vectors: List[List[float]], texts: List[str]) -> int:
        """Add vectors and their associated text metadata to the index.

        Returns the number of vectors added.
        """
        if not vectors:
            return 0

        np_vectors = np.array(vectors, dtype=np.float32)

        # Ensure correct dimensions
        if np_vectors.shape[1] != EMBEDDING_DIM:
            raise ValueError(
                f"Expected embedding dimension {EMBEDDING_DIM}, got {np_vectors.shape[1]}"
            )

        self.index.add(np_vectors)
        self.metadata.extend(texts)

        # Auto-save after adding
        self.save_index()

        return len(vectors)

    def search_similar(
        self, query_vector: List[float], k: int = 5
    ) -> List[Tuple[str, float]]:
        """Search for k most similar vectors.

        Returns list of (text, distance) tuples.
        """
        if self.index.ntotal == 0:
            return []

        k = min(k, self.index.ntotal)
        query_np = np.array([query_vector], dtype=np.float32)

        distances, indices = self.index.search(query_np, k)

        results = []
        for i, idx in enumerate(indices[0]):
            if idx < len(self.metadata) and idx >= 0:
                results.append((self.metadata[idx], float(distances[0][i])))

        return results

    def save_index(self) -> None:
        """Persist FAISS index and metadata to disk."""
        os.makedirs(DATA_DIR, exist_ok=True)

        if self.index is not None and self.index.ntotal > 0:
            faiss.write_index(self.index, INDEX_PATH)

            with open(METADATA_PATH, "w", encoding="utf-8") as f:
                json.dump(self.metadata, f, ensure_ascii=False, indent=2)

    def load_index(self) -> None:
        """Load FAISS index and metadata from disk."""
        if os.path.exists(INDEX_PATH) and os.path.exists(METADATA_PATH):
            try:
                self.index = faiss.read_index(INDEX_PATH)

                with open(METADATA_PATH, "r", encoding="utf-8") as f:
                    self.metadata = json.load(f)

                print(f"Loaded FAISS index with {self.index.ntotal} vectors")
            except Exception as e:
                print(f"Error loading FAISS index: {e}. Starting fresh.")
                self._initialize()
        else:
            print("No existing FAISS index found. Starting fresh.")
            self._initialize()

    def get_total_vectors(self) -> int:
        """Return the total number of vectors in the index."""
        return self.index.ntotal if self.index else 0

    def clear(self) -> None:
        """Clear the index and metadata."""
        self._initialize()
        # Remove persisted files
        if os.path.exists(INDEX_PATH):
            os.remove(INDEX_PATH)
        if os.path.exists(METADATA_PATH):
            os.remove(METADATA_PATH)


# Singleton instance
vector_store = VectorStore()
