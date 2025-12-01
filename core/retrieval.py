"""Retrieval module for semantic search and chunk retrieval"""

import logging
from typing import List, Dict, Tuple, Optional
from core.embedder import EnhancedEmbedder
from utils.helpers import calculate_relevance_score, format_citation, highlight_text

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RetrievalEngine:
    """Retrieval engine for finding relevant chunks"""
    
    def __init__(self, embedder: EnhancedEmbedder):
        """
        Initialize retrieval engine
        
        Args:
            embedder: EnhancedEmbedder instance
        """
        self.embedder = embedder
        self.logger = logger
    
    def retrieve(
        self,
        query: str,
        top_k: int = 5,
        min_relevance: float = 0.3
    ) -> List[Dict]:
        """
        Retrieve relevant chunks for a query
        
        Args:
            query: Search query
            top_k: Number of results to return
            min_relevance: Minimum relevance score threshold
            
        Returns:
            List of source dictionaries with full metadata
        """
        try:
            # Search using embedder
            results = self.embedder.search(query, top_k=top_k, min_relevance=min_relevance)
            
            # Format results
            sources = []
            for i, (chunk_text, metadata, distance, relevance) in enumerate(results, 1):
                source = {
                    'id': i,
                    'text': chunk_text,
                    'snippet': highlight_text(chunk_text, query, context_chars=150),
                    'full_text': chunk_text,
                    'distance': round(distance, 4),
                    'relevance_score': round(relevance, 4),
                    'relevance_percent': round(relevance * 100, 1),
                    'filename': metadata.get('filename', 'Unknown'),
                    'page': metadata.get('page', metadata.get('page_num', 0)),
                    'chunk_id': metadata.get('chunk_id', i),
                    'citation': format_citation(metadata),
                    **metadata
                }
                sources.append(source)
            
            self.logger.info(f"Retrieved {len(sources)} sources for query: {query[:50]}...")
            return sources
            
        except Exception as e:
            self.logger.error(f"Error in retrieval: {str(e)}")
            return []
    
    def get_context_for_qa(
        self,
        query: str,
        top_k: int = 3
    ) -> Tuple[str, List[Dict]]:
        """
        Get formatted context for QA
        
        Args:
            query: User question
            top_k: Number of chunks to retrieve
            
        Returns:
            Tuple of (formatted_context, sources_list)
        """
        sources = self.retrieve(query, top_k=top_k)
        
        if not sources:
            return "No relevant context found.", []
        
        # Format context with source markers
        context_parts = []
        for source in sources:
            source_marker = f"[Source {source['id']}: {source['filename']}"
            if source['page']:
                source_marker += f", Page {source['page']}"
            source_marker += "]"
            
            context_parts.append(f"{source_marker}\n{source['text']}\n")
        
        formatted_context = "\n".join(context_parts)
        return formatted_context, sources
    
    def get_stats(self) -> Dict:
        """Get retrieval statistics"""
        return self.embedder.get_stats()

