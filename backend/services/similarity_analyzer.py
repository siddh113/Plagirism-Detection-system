import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Tuple
import torch

class SimilarityAnalyzer:
    """
    Analyzes semantic similarity between documents using Sentence-BERT.
    """
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2", similarity_threshold: float = 0.3):
        """
        Initialize similarity analyzer with Sentence-BERT model.
        
        Args:
            model_name: Name of the Sentence-BERT model to use
            similarity_threshold: Minimum similarity score to consider as plagiarism
        """
        print(f"Loading Sentence-BERT model: {model_name}")
        try:
            self.model = SentenceTransformer(model_name)
            self.similarity_threshold = similarity_threshold
            print("Model loaded successfully!")
        except Exception as e:
            print(f"Error loading model: {e}")
            raise
    
    def compute_embeddings(self, texts: List[str]) -> np.ndarray:
        """
        Compute embeddings for a list of texts.
        
        Args:
            texts: List of text chunks
            
        Returns:
            Numpy array of embeddings
        """
        embeddings = self.model.encode(texts, convert_to_numpy=True, show_progress_bar=False)
        return embeddings
    
    def find_matches(
        self, 
        source_embeddings: np.ndarray, 
        corpus_embeddings: np.ndarray,
        source_chunks: List[str],
        corpus_chunks: List[str],
        corpus_filename: str
    ) -> List[Dict]:
        """
        Find matching chunks between source and corpus.
        
        Args:
            source_embeddings: Embeddings of source document chunks
            corpus_embeddings: Embeddings of corpus document chunks
            source_chunks: Original source text chunks
            corpus_chunks: Original corpus text chunks
            corpus_filename: Name of the corpus document
            
        Returns:
            List of match dictionaries
        """
        matches = []
        
        # Compute similarity matrix
        similarity_matrix = cosine_similarity(source_embeddings, corpus_embeddings)
        
        # Find matches above threshold
        for i, source_chunk in enumerate(source_chunks):
            for j, corpus_chunk in enumerate(corpus_chunks):
                similarity = float(similarity_matrix[i][j])
                
                if similarity >= self.similarity_threshold:
                    matches.append({
                        "source_chunk": source_chunk,
                        "corpus_chunk": corpus_chunk,
                        "similarity": similarity,
                        "source_chunk_index": i,
                        "corpus_chunk_index": j,
                        "corpus_filename": corpus_filename
                    })
        
        return matches
    
    def analyze(
        self,
        source_chunks: List[str],
        corpus_chunks_list: List[List[str]],
        corpus_filenames: List[str]
    ) -> Dict:
        """
        Analyze similarity between source document and corpus documents.
        
        Args:
            source_chunks: Chunks of source document
            corpus_chunks_list: List of chunk lists for each corpus document
            corpus_filenames: List of corpus document filenames
            
        Returns:
            Dictionary containing analysis results
        """
        # Compute embeddings for source
        print("Computing embeddings for source document...")
        source_embeddings = self.compute_embeddings(source_chunks)
        
        all_matches = []
        similarity_scores = []
        detailed_results = []
        
        # Process each corpus document
        for corpus_chunks, corpus_filename in zip(corpus_chunks_list, corpus_filenames):
            print(f"Processing corpus document: {corpus_filename}")
            
            # Compute embeddings for corpus
            corpus_embeddings = self.compute_embeddings(corpus_chunks)
            
            # Find matches
            matches = self.find_matches(
                source_embeddings,
                corpus_embeddings,
                source_chunks,
                corpus_chunks,
                corpus_filename
            )
            
            all_matches.extend(matches)
            
            # Calculate average similarity across ALL chunks (not just matches)
            similarity_matrix = cosine_similarity(source_embeddings, corpus_embeddings)
            all_similarities = similarity_matrix.flatten()
            avg_similarity = float(np.mean(all_similarities))
            max_similarity = float(np.max(all_similarities))
            min_similarity = float(np.min(all_similarities))
            
            # Debug output
            print(f"  Similarity stats for {corpus_filename}:")
            print(f"    Average: {avg_similarity:.3f}, Max: {max_similarity:.3f}, Min: {min_similarity:.3f}")
            print(f"    Matches found: {len(matches)} (threshold: {self.similarity_threshold})")
            
            # Also calculate average of matched chunks only
            if matches:
                avg_matched_similarity = np.mean([m["similarity"] for m in matches])
            else:
                avg_matched_similarity = 0.0
            
            similarity_scores.append(avg_similarity)
            
            # Calculate plagiarism percentage for this document
            total_source_words = sum(len(chunk.split()) for chunk in source_chunks)
            matched_words = sum(len(m["source_chunk"].split()) for m in matches)
            plagiarism_pct = (matched_words / total_source_words * 100) if total_source_words > 0 else 0.0
            
            detailed_results.append({
                "filename": corpus_filename,
                "avg_similarity": float(avg_similarity),  # Average across all chunks
                "avg_matched_similarity": float(avg_matched_similarity),  # Average of matched chunks only
                "max_similarity": float(max_similarity),
                "min_similarity": float(min_similarity),
                "plagiarism_percentage": float(plagiarism_pct),
                "match_count": len(matches),
                "threshold_used": float(self.similarity_threshold),
                "matches": matches[:10]  # Limit to top 10 matches per document
            })
        
        # Calculate overall plagiarism percentage
        total_source_words = sum(len(chunk.split()) for chunk in source_chunks)
        unique_matched_chunks = set()
        for match in all_matches:
            unique_matched_chunks.add(match["source_chunk_index"])
        
        matched_words = sum(
            len(source_chunks[idx].split()) 
            for idx in unique_matched_chunks
        )
        overall_plagiarism_pct = (matched_words / total_source_words * 100) if total_source_words > 0 else 0.0
        
        # Sort matches by similarity
        all_matches.sort(key=lambda x: x["similarity"], reverse=True)
        
        return {
            "similarity_scores": [float(score) for score in similarity_scores],
            "matches": all_matches[:50],  # Top 50 matches
            "plagiarism_percentage": float(overall_plagiarism_pct),
            "detailed_results": detailed_results,
            "total_matches": len(all_matches),
            "source_chunk_count": len(source_chunks),
            "corpus_document_count": len(corpus_chunks_list)
        }

