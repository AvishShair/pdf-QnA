"""Embedder utility to create and manage FAISS vector store"""

import logging
import numpy as np
from typing import List, Dict, Tuple
import google.generativeai as genai

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TextEmbedder:
    """Create embeddings and manage FAISS vector store for text chunks"""
    
    def __init__(self, api_key: str):
        """
        Initialize the embedder with Google API key
        
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
    
    def create_embeddings(self, text_chunks: List[str], metadata: List[Dict] = None) -> bool:
        """
        Create embeddings for text chunks using Google's embedding model
        
        Args:
            text_chunks: List of text chunks to embed
            metadata: Optional metadata for each chunk (e.g., filename, page number)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not text_chunks:
                self.logger.warning("No text chunks provided for embedding")
                return False
            
            self.logger.info(f"Creating embeddings for {len(text_chunks)} chunks...")
            
            embeddings_list = []
            for i, chunk in enumerate(text_chunks):
                try:
                    # Use Google's embedding model
                    result = genai.embed_content(
                        model="models/embedding-001",
                        content=chunk,
                        task_type="retrieval_document"
                    )
                    embeddings_list.append(result['embedding'])
                    
                    if (i + 1) % 10 == 0:
                        self.logger.info(f"Processed {i + 1}/{len(text_chunks)} chunks")
                        
                except Exception as e:
                    self.logger.error(f"Error embedding chunk {i}: {str(e)}")
                    # Use zero vector as fallback
                    embeddings_list.append([0.0] * 768)
            
            self.chunks = text_chunks
            self.embeddings = np.array(embeddings_list, dtype=np.float32)
            self.metadata = metadata if metadata else [{"index": i} for i in range(len(text_chunks))]
            
            # Create FAISS index
            self._create_faiss_index()
            
            self.logger.info(f"Successfully created embeddings for {len(text_chunks)} chunks")
            return True
            
        except Exception as e:
            self.logger.error(f"Error creating embeddings: {str(e)}")
            return False
    
    def _create_faiss_index(self):
        """Create FAISS index from embeddings"""
        try:
            import faiss
            
            dimension = self.embeddings.shape[1]
            self.index = faiss.IndexFlatL2(dimension)
            self.index.add(self.embeddings)
            
            self.logger.info(f"FAISS index created with {self.index.ntotal} vectors")
            
        except Exception as e:
            self.logger.error(f"Error creating FAISS index: {str(e)}")
            raise
    
    def search(self, query: str, top_k: int = 3) -> List[Tuple[str, Dict, float]]:
        """
        Search for most relevant chunks for a query
        
        Args:
            query: Query text
            top_k: Number of top results to return
            
        Returns:
            List of tuples (chunk_text, metadata, distance)
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
            distances, indices = self.index.search(query_embedding, min(top_k, len(self.chunks)))
            
            # Prepare results
            results = []
            for dist, idx in zip(distances[0], indices[0]):
                if idx < len(self.chunks):
                    results.append((
                        self.chunks[idx],
                        self.metadata[idx],
                        float(dist)
                    ))
            
            return results
            
        except Exception as e:
            self.logger.error(f"Error searching: {str(e)}")
            return []
    
    def get_stats(self) -> Dict:
        """Get statistics about the current index"""
        return {
            'total_chunks': len(self.chunks),
            'total_embeddings': len(self.embeddings),
            'index_size': self.index.ntotal if self.index else 0,
            'embedding_dimension': self.embeddings.shape[1] if len(self.embeddings) > 0 else 0
        }


class SimpleVectorStore:
    """
    Simple vector store without FAISS (fallback option)
    Uses cosine similarity for search
    """
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        genai.configure(api_key=api_key)
        self.chunks = []
        self.embeddings = []
        self.metadata = []
        self.logger = logger
    
    def create_embeddings(self, text_chunks: List[str], metadata: List[Dict] = None) -> bool:
        """Create embeddings for text chunks"""
        try:
            if not text_chunks:
                return False
            
            embeddings_list = []
            for chunk in text_chunks:
                try:
                    result = genai.embed_content(
                        model="models/embedding-001",
                        content=chunk,
                        task_type="retrieval_document"
                    )
                    embeddings_list.append(result['embedding'])
                except Exception as e:
                    self.logger.error(f"Error embedding chunk: {str(e)}")
                    embeddings_list.append([0.0] * 768)
            
            self.chunks = text_chunks
            self.embeddings = np.array(embeddings_list, dtype=np.float32)
            self.metadata = metadata if metadata else [{"index": i} for i in range(len(text_chunks))]
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error creating embeddings: {str(e)}")
            return False
    
    def search(self, query: str, top_k: int = 3) -> List[Tuple[str, Dict, float]]:
        """Search using cosine similarity"""
        try:
            if len(self.chunks) == 0:
                return []
            
            # Create query embedding
            result = genai.embed_content(
                model="models/embedding-001",
                content=query,
                task_type="retrieval_query"
            )
            query_embedding = np.array(result['embedding'], dtype=np.float32)
            
            # Calculate cosine similarity
            similarities = []
            for emb in self.embeddings:
                similarity = np.dot(query_embedding, emb) / (
                    np.linalg.norm(query_embedding) * np.linalg.norm(emb)
                )
                similarities.append(similarity)
            
            # Get top k
            top_indices = np.argsort(similarities)[::-1][:top_k]
            
            results = []
            for idx in top_indices:
                results.append((
                    self.chunks[idx],
                    self.metadata[idx],
                    float(1 - similarities[idx])  # Convert to distance
                ))
            
            return results
            
        except Exception as e:
            self.logger.error(f"Error searching: {str(e)}")
            return []
    
    def get_stats(self) -> Dict:
        """Get statistics"""
        return {
            'total_chunks': len(self.chunks),
            'total_embeddings': len(self.embeddings),
            'embedding_dimension': self.embeddings.shape[1] if len(self.embeddings) > 0 else 0
        }

