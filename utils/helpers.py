"""Helper utility functions"""

import re
from typing import List, Dict

# Try to import tiktoken, but use fallback if not available
try:
    import tiktoken
    TIKTOKEN_AVAILABLE = True
except ImportError:
    TIKTOKEN_AVAILABLE = False


def estimate_tokens(text: str, model: str = "gpt-3.5-turbo") -> int:
    """
    Estimate token count for text
    
    Args:
        text: Input text
        model: Model name for tokenizer (not used if tiktoken unavailable)
        
    Returns:
        Estimated token count
    """
    if TIKTOKEN_AVAILABLE:
        try:
            encoding = tiktoken.encoding_for_model(model)
            return len(encoding.encode(text))
        except:
            pass
    
    # Fallback: approximate 1 token = 4 characters
    return len(text) // 4


def chunk_text_by_tokens(
    text: str,
    chunk_size: int = 600,
    overlap: int = 100,
    metadata: Dict = None
) -> List[Dict]:
    """
    Split text into chunks based on token count (500-800 tokens)
    
    Args:
        text: Input text to chunk
        chunk_size: Target token size (default 600, range 500-800)
        overlap: Overlap in tokens between chunks
        metadata: Base metadata to attach to each chunk
        
    Returns:
        List of chunk dictionaries with text and metadata
    """
    if not text or len(text) == 0:
        return []
    
    # Estimate tokens per character (rough approximation)
    # Average: 1 token ≈ 4 characters for English text
    char_per_token = 4
    char_chunk_size = chunk_size * char_per_token
    char_overlap = overlap * char_per_token
    
    chunks = []
    start = 0
    text_length = len(text)
    chunk_id = 0
    
    while start < text_length:
        end = min(start + char_chunk_size, text_length)
        
        # Try to break at sentence boundary
        if end < text_length:
            # Look for sentence boundary (., !, ?)
            for i in range(end, max(start + char_overlap, end - 200), -1):
                if text[i] in ['.', '!', '?', '\n']:
                    end = i + 1
                    break
            else:
                # Look for word boundary (space)
                for i in range(end, max(start + char_overlap, end - 100), -1):
                    if text[i] == ' ':
                        end = i
                        break
        
        chunk_text = text[start:end].strip()
        
        if chunk_text:
            chunk_metadata = {
                'chunk_id': chunk_id,
                'start_char': start,
                'end_char': end,
                **(metadata or {})
            }
            chunks.append({
                'text': chunk_text,
                'metadata': chunk_metadata
            })
            chunk_id += 1
        
        start = max(end - char_overlap, start + 1)
    
    return chunks


def extract_page_number(text: str) -> int:
    """
    Extract page number from text that contains page markers
    
    Args:
        text: Text that may contain "--- Page X ---" markers
        
    Returns:
        Page number or 0 if not found
    """
    match = re.search(r'---\s*Page\s+(\d+)\s*---', text, re.IGNORECASE)
    if match:
        return int(match.group(1))
    return 0


def calculate_relevance_score(distance: float) -> float:
    """
    Convert FAISS distance to relevance score (0-1)
    
    Args:
        distance: FAISS L2 distance
        
    Returns:
        Relevance score between 0 and 1
    """
    # Convert distance to similarity (lower distance = higher similarity)
    # Using exponential decay: score = 1 / (1 + distance)
    return 1 / (1 + distance)


def format_citation(source: Dict) -> str:
    """
    Format citation string from source metadata
    
    Args:
        source: Source dictionary with metadata
        
    Returns:
        Formatted citation string
    """
    parts = []
    if 'filename' in source:
        parts.append(source['filename'])
    if 'page' in source:
        parts.append(f"Page {source['page']}")
    if 'chunk_id' in source:
        parts.append(f"Chunk {source['chunk_id']}")
    
    return " | ".join(parts) if parts else "Unknown source"


def highlight_text(text: str, query: str, context_chars: int = 100) -> str:
    """
    Highlight query terms in text and return snippet
    
    Args:
        text: Full text
        query: Query string to highlight
        context_chars: Characters of context around match
        
    Returns:
        Highlighted text snippet
    """
    query_lower = query.lower()
    text_lower = text.lower()
    
    # Find first occurrence
    idx = text_lower.find(query_lower)
    
    if idx == -1:
        # No match, return beginning
        return text[:context_chars * 2] + "..."
    
    # Extract context around match
    start = max(0, idx - context_chars)
    end = min(len(text), idx + len(query) + context_chars)
    
    snippet = text[start:end]
    
    # Highlight (simple version - in UI we'll use markdown)
    highlighted = snippet.replace(
        text[idx:idx+len(query)],
        f"**{text[idx:idx+len(query)]}**"
    )
    
    if start > 0:
        highlighted = "..." + highlighted
    if end < len(text):
        highlighted = highlighted + "..."
    
    return highlighted


def clean_text(text: str) -> str:
    """
    Clean extracted text
    
    Args:
        text: Raw extracted text
        
    Returns:
        Cleaned text
    """
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove special characters that might cause issues
    text = re.sub(r'[\x00-\x08\x0b-\x0c\x0e-\x1f]', '', text)
    return text.strip()

