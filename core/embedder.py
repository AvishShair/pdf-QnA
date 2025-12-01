"""Enhanced Embedder with FAISS vector store and improved chunking"""

import logging
import numpy as np
from typing import List, Dict, Tuple, Optional
import google.generativeai as genai

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EnhancedEmbedder:
    """Enhanced embedder with FAISS and improved metadata tracking"""
    
    def __init__(self, api_key: str):
        """
        Initialize the embedder
        
        Args:
            api_key: Google Gemini API key
        """
        self.api_key = api_key
        genai.configure(api_key=api_key)
        self.chunks = []
        self.embeddings = []
        self.metadata = []
        self.index = None
        self.logger = logger
    
    def create_embeddings(
        self,
        text_chunks: List[Dict],
        progress_callback: Optional[callable] = None
    ) -> bool:
        """
        Create embeddings for text chunks (500-800 tokens each)
        
        Args:
            text_chunks: List of dicts with 'text' and 'metadata' keys
            progress_callback: Optional callback function(progress, total)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not text_chunks:
                self.logger.warning("No text chunks provided for embedding")
                return False
            
            self.logger.info(f"Creating embeddings for {len(text_chunks)} chunks...")
            
            embeddings_list = []
            total = len(text_chunks)
            
            for i, chunk_data in enumerate(text_chunks):
                try:
                    chunk_text = chunk_data.get('text', '')
                    chunk_metadata = chunk_data.get('metadata', {})
                    
                    if not chunk_text:
                        continue
                    
                    # Create embedding
                    result = genai.embed_content(
                        model="models/embedding-001",
                        content=chunk_text,
                        task_type="retrieval_document"
                    )
                    embeddings_list.append(result['embedding'])
                    
                    # Store chunk and metadata
                    self.chunks.append(chunk_text)
                    self.metadata.append(chunk_metadata)
                    
                    # Progress callback
                    if progress_callback:
                        progress_callback(i + 1, total)
                    
                    if (i + 1) % 10 == 0:
                        self.logger.info(f"Processed {i + 1}/{total} chunks")
                
                except Exception as e:
                    self.logger.error(f"Error embedding chunk {i}: {str(e)}")
                    # Use zero vector as fallback
                    embeddings_list.append([0.0] * 768)
                    self.chunks.append(chunk_data.get('text', ''))
                    self.metadata.append(chunk_data.get('metadata', {}))
            
            # Convert to numpy array
            self.embeddings = np.array(embeddings_list, dtype=np.float32)
            
            # Create FAISS index
            self._create_faiss_index()
            
            self.logger.info(f"Successfully created embeddings for {len(self.chunks)} chunks")
            return True
            
        except Exception as e:
            self.logger.error(f"Error creating embeddings: {str(e)}")
            return False
    
    def _create_faiss_index(self):
        """Create FAISS index from embeddings"""
        try:
            import faiss
            
            if len(self.embeddings) == 0:
                raise ValueError("No embeddings to index")
            
            dimension = self.embeddings.shape[1]
            self.index = faiss.IndexFlatL2(dimension)
            self.index.add(self.embeddings)
            
            self.logger.info(f"FAISS index created with {self.index.ntotal} vectors (dim={dimension})")
            
        except ImportError:
            self.logger.error("FAISS not available. Install: pip install faiss-cpu")
            raise
        except Exception as e:
            self.logger.error(f"Error creating FAISS index: {str(e)}")
            raise
    
    def search(
        self,
        query: str,
        top_k: int = 5,
        min_relevance: float = 0.0
    ) -> List[Tuple[str, Dict, float, float]]:
        """
        Search for relevant chunks
        
        Args:
            query: Query text
            top_k: Number of results to return
            min_relevance: Minimum relevance score (0-1)
            
        Returns:
            List of tuples: (chunk_text, metadata, distance, relevance_score)
        """
        try:
            if self.index is None or len(self.chunks) == 0:
                self.logger.warning("No index available for search")
                return []
            
            # Create query embedding
            result = genai.embed_content(
                model="models/embedding-001",
                content=query,
                task_type="retrieval_query"
            )
            query_embedding = np.array([result['embedding']], dtype=np.float32)
            
            # Search in FAISS
            import faiss
            k = min(top_k, len(self.chunks))
            distances, indices = self.index.search(query_embedding, k)
            
            # Prepare results with relevance scores
            results = []
            for dist, idx in zip(distances[0], indices[0]):
                if idx < len(self.chunks):
                    # Calculate relevance score (0-1)
                    relevance = 1 / (1 + dist)  # Convert distance to similarity
                    
                    if relevance >= min_relevance:
                        results.append((
                            self.chunks[idx],
                            self.metadata[idx],
                            float(dist),
                            float(relevance)
                        ))
            
            # Sort by relevance (highest first)
            results.sort(key=lambda x: x[3], reverse=True)
            
            return results[:top_k]
            
        except Exception as e:
            self.logger.error(f"Error searching: {str(e)}")
            return []
    
    def get_stats(self) -> Dict:
        """Get statistics about the vector store"""
        return {
            'total_chunks': len(self.chunks),
            'total_embeddings': len(self.embeddings),
            'index_size': self.index.ntotal if self.index else 0,
            'embedding_dimension': self.embeddings.shape[1] if len(self.embeddings) > 0 else 0,
            'index_type': 'FAISS' if self.index else 'None'
        }
    
    def clear(self):
        """Clear all stored data"""
        self.chunks = []
        self.embeddings = []
        self.metadata = []
        self.index = None
        self.logger.info("Embedder cleared")

