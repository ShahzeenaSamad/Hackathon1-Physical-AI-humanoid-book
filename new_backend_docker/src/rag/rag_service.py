"""
RAG Service - Complete RAG pipeline
"""
from typing import List, Dict
from pathlib import Path
from .content_loader import ContentLoader
from .text_chunker import TextChunker
from .vector_store import VectorStore

class RAGService:
    def __init__(self, content_dir: str = None):
        """Initialize RAG service"""
        # Set content directory - try multiple locations
        if content_dir:
            self.content_dir = content_dir
        else:
            # Try to find content directory
            possible_paths = [
                "../../contentdocs",
                "../contentdocs",
                "./contentdocs",
                "../../../contentdocs"
            ]

            self.content_dir = None
            for path in possible_paths:
                if Path(path).exists():
                    self.content_dir = path
                    break

        self.loader = ContentLoader(self.content_dir) if self.content_dir else None
        self.chunker = TextChunker(chunk_size=500, overlap=50)
        self.vector_store = VectorStore()
        self.is_initialized = False

    def initialize(self):
        """Initialize the RAG pipeline"""
        print("Initializing RAG service...")

        if not self.loader:
            print("Warning: Content directory not found, using fallback mode")
            return False

        # Load documents
        documents = self.loader.load_and_process()

        if not documents:
            print("Warning: No documents loaded, using fallback mode")
            return False

        # Chunk documents
        chunks = self.chunker.chunk_documents(documents)

        if not chunks:
            print("Warning: No chunks created, using fallback mode")
            return False

        # Build vector index
        self.vector_store.build_index(chunks)
        self.is_initialized = True

        print("RAG service initialized successfully!")
        return True

    def search(self, query: str, top_k: int = 3) -> List[Dict]:
        """Search for relevant content"""
        if not self.is_initialized:
            return []

        results = self.vector_store.search(query, top_k=top_k)
        return results

    def get_context_for_query(self, query: str, top_k: int = 3) -> str:
        """Get relevant context for a query"""
        results = self.search(query, top_k=top_k)

        if not results:
            return ""

        # Combine top chunks into context
        context_parts = []
        for result in results:
            chunk = result['chunk']
            source = chunk['source']
            text = chunk['text']

            context_part = f"[Source: {source}]\n{text}"
            context_parts.append(context_part)

        return "\n\n---\n\n".join(context_parts)

    def format_sources(self, results: List[Dict]) -> List[Dict]:
        """Format search results for API response"""
        sources = []

        for result in results:
            chunk = result['chunk']
            sources.append({
                "title": chunk['filename'].replace('-', ' ').title(),
                "chapter_id": chunk['filename'],
                "module": chunk['module'].replace('-', ' ').title(),
                "score": round(result['score'], 2)
            })

        return sources
