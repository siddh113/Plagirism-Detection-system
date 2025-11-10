import re
from typing import List

class DocumentProcessor:
    """
    Handles document processing and text chunking.
    """
    
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        """
        Initialize document processor.
        
        Args:
            chunk_size: Number of words per chunk
            chunk_overlap: Number of overlapping words between chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def clean_text(self, text: str) -> str:
        """
        Clean and normalize text.
        """
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep punctuation
        text = text.strip()
        return text
    
    def chunk_document(self, text: str) -> List[str]:
        """
        Split document into overlapping chunks for context-aware comparison.
        
        Args:
            text: Input document text
            
        Returns:
            List of text chunks
        """
        # Clean text
        text = self.clean_text(text)
        
        # Split into sentences first for better chunking
        sentences = re.split(r'(?<=[.!?])\s+', text)
        
        chunks = []
        current_chunk = []
        current_word_count = 0
        
        for sentence in sentences:
            words = sentence.split()
            sentence_word_count = len(words)
            
            # If adding this sentence would exceed chunk size, save current chunk
            if current_word_count + sentence_word_count > self.chunk_size and current_chunk:
                chunks.append(' '.join(current_chunk))
                
                # Start new chunk with overlap
                if self.chunk_overlap > 0:
                    # Get last few sentences for overlap
                    overlap_words = []
                    overlap_count = 0
                    for s in reversed(current_chunk):
                        s_words = s.split()
                        if overlap_count + len(s_words) <= self.chunk_overlap:
                            overlap_words.insert(0, s)
                            overlap_count += len(s_words)
                        else:
                            break
                    current_chunk = overlap_words
                    current_word_count = overlap_count
                else:
                    current_chunk = []
                    current_word_count = 0
            
            current_chunk.append(sentence)
            current_word_count += sentence_word_count
        
        # Add remaining chunk
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        # If document is smaller than chunk_size, return as single chunk
        if not chunks:
            chunks = [text]
        
        return chunks
    
    def get_chunk_info(self, chunks: List[str]) -> dict:
        """
        Get information about chunks.
        """
        return {
            "total_chunks": len(chunks),
            "avg_chunk_size": sum(len(chunk.split()) for chunk in chunks) / len(chunks) if chunks else 0,
            "total_words": sum(len(chunk.split()) for chunk in chunks)
        }

