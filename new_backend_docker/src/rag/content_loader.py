"""
Content Loader - Extract text from markdown files
"""
import os
from pathlib import Path
from typing import List, Dict
import re

class ContentLoader:
    def __init__(self, content_dir: str = "../../contentdocs"):
        self.content_dir = Path(content_dir)
        self.documents = []

    def load_markdown_files(self) -> List[Dict]:
        """Load all markdown files from content directory"""
        documents = []

        if not self.content_dir.exists():
            print(f"Warning: Content directory {self.content_dir} not found")
            return documents

        # Find all markdown files
        md_files = list(self.content_dir.rglob("*.md"))

        for md_file in md_files:
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Extract metadata from filename/path
                relative_path = md_file.relative_to(self.content_dir)
                parts = str(relative_path).replace('\\', '/').split('/')

                doc = {
                    'content': content,
                    'source': str(relative_path),
                    'module': parts[0] if len(parts) > 0 else 'general',
                    'filename': md_file.stem,
                    'full_path': str(md_file)
                }

                documents.append(doc)
            except Exception as e:
                print(f"Error loading {md_file}: {e}")

        print(f"Loaded {len(documents)} markdown documents")
        return documents

    def extract_text_from_markdown(self, content: str) -> str:
        """Extract clean text from markdown"""
        # Remove markdown syntax
        text = content

        # Remove headers
        text = re.sub(r'^#+\s+', '', text, flags=re.MULTILINE)

        # Remove bold/italic
        text = re.sub(r'\*\*\*(.+?)\*\*\*', r'\1', text)
        text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
        text = re.sub(r'\*(.+?)\*', r'\1', text)

        # Remove links
        text = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', text)

        # Remove code blocks
        text = re.sub(r'```[\s\S]+?```', '', text)
        text = re.sub(r'`(.+?)`', r'\1', text)

        # Clean up extra whitespace
        text = re.sub(r'\n\s*\n', '\n\n', text)

        return text.strip()

    def load_and_process(self) -> List[Dict]:
        """Load and process all documents"""
        raw_docs = self.load_markdown_files()

        processed_docs = []
        for doc in raw_docs:
            clean_text = self.extract_text_from_markdown(doc['content'])

            if len(clean_text) > 100:  # Only keep substantial content
                processed_doc = {
                    'text': clean_text,
                    'source': doc['source'],
                    'module': doc['module'],
                    'filename': doc['filename']
                }
                processed_docs.append(processed_doc)

        print(f"Processed {len(processed_docs)} documents")
        return processed_docs
