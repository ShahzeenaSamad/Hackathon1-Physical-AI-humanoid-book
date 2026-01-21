"""
Text Chunker - Split documents into smaller chunks for vector search
"""
from typing import List, Dict
import re

class TextChunker:
    def __init__(self, chunk_size: int = 500, overlap: int = 50):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk_by_paragraph(self, text: str, metadata: Dict) -> List[Dict]:
        """Chunk text by paragraphs first, then by size"""
        chunks = []

        # Split by paragraphs
        paragraphs = re.split(r'\n\n+', text)

        current_chunk = ""
        chunk_id = 0

        for para in paragraphs:
            para = para.strip()
            if not para:
                continue

            # If paragraph is too long, split it
            if len(para) > self.chunk_size:
                words = para.split()
                for i in range(0, len(words), self.chunk_size - self.overlap):
                    chunk_text = ' '.join(words[i:i + self.chunk_size])

                    chunks.append({
                        'text': chunk_text,
                        'chunk_id': chunk_id,
                        'source': metadata['source'],
                        'module': metadata['module'],
                        'filename': metadata['filename']
                    })
                    chunk_id += 1
            else:
                # Add paragraph to current chunk
                if len(current_chunk) + len(para) + 2 <= self.chunk_size:
                    current_chunk += ('\n\n' if current_chunk else '') + para
                else:
                    # Save current chunk and start new one
                    if current_chunk:
                        chunks.append({
                            'text': current_chunk,
                            'chunk_id': chunk_id,
                            'source': metadata['source'],
                            'module': metadata['module'],
                            'filename': metadata['filename']
                        })
                        chunk_id += 1

                    current_chunk = para

        # Add remaining content
        if current_chunk:
            chunks.append({
                'text': current_chunk,
                'chunk_id': chunk_id,
                'source': metadata['source'],
                'module': metadata['module'],
                'filename': metadata['filename']
            })

        return chunks

    def chunk_documents(self, documents: List[Dict]) -> List[Dict]:
        """Chunk all documents"""
        all_chunks = []

        for doc in documents:
            chunks = self.chunk_by_paragraph(
                doc['text'],
                {
                    'source': doc['source'],
                    'module': doc['module'],
                    'filename': doc['filename']
                }
            )
            all_chunks.extend(chunks)

        print(f"Created {len(all_chunks)} chunks from {len(documents)} documents")
        return all_chunks
