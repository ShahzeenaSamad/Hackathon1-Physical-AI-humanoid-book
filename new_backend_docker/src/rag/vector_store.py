"""
Vector Store - Simple semantic search using sentence-transformers (FREE, no API keys)
"""
from typing import List, Dict, Tuple
import numpy as np
from sentence_transformers import SentenceTransformer
import torch

class VectorStore:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """Initialize with free sentence-transformers model"""
        print(f"Loading sentence-transformers model: {model_name}")
        self.model = SentenceTransformer(model_name)
        self.chunks = []
        self.embeddings = None

    def create_embeddings(self, chunks: List[Dict]) -> np.ndarray:
        """Create embeddings for all chunks"""
        print(f"Creating embeddings for {len(chunks)} chunks...")

        texts = [chunk['text'] for chunk in chunks]

        # Generate embeddings using sentence-transformers (FREE)
        embeddings = self.model.encode(
            texts,
            show_progress_bar=True,
            convert_to_numpy=True
        )

        print(f"Created embeddings shape: {embeddings.shape}")
        return embeddings

    def build_index(self, chunks: List[Dict]):
        """Build the vector index"""
        self.chunks = chunks
        self.embeddings = self.create_embeddings(chunks)
        print(f"Vector store built with {len(chunks)} chunks")

    def search(self, query: str, top_k: int = 3) -> List[Dict]:
        """Search for relevant chunks using cosine similarity"""
        if self.embeddings is None:
            raise ValueError("Index not built. Call build_index() first.")

        # Create query embedding
        query_embedding = self.model.encode([query])[0]

        # Calculate cosine similarity
        similarities = np.dot(self.embeddings, query_embedding) / (
            np.linalg.norm(self.embeddings, axis=1) * np.linalg.norm(query_embedding)
        )

        # Get top-k results
        top_indices = np.argsort(similarities)[::-1][:top_k]

        results = []
        for idx in top_indices:
            result = {
                'chunk': self.chunks[idx],
                'score': float(similarities[idx]),
                'rank': len(results) + 1
            }
            results.append(result)

        return results

    def save_index(self, filepath: str):
        """Save index to disk (optional)"""
        import pickle

        data = {
            'chunks': self.chunks,
            'embeddings': self.embeddings
        }

        with open(filepath, 'wb') as f:
            pickle.dump(data, f)

        print(f"Index saved to {filepath}")

    def load_index(self, filepath: str):
        """Load index from disk (optional)"""
        import pickle

        with open(filepath, 'rb') as f:
            data = pickle.load(f)

        self.chunks = data['chunks']
        self.embeddings = data['embeddings']

        print(f"Index loaded from {filepath} with {len(self.chunks)} chunks")
