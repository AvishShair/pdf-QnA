"""PDF Parser utility to extract text from PDF files"""

import logging
from typing import List, Dict
import PyPDF2
import pdfplumber
from io import BytesIO

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PDFParser:
    """Extract text from PDF files using PyPDF2 with pdfplumber fallback"""
    
    def __init__(self):
        self.logger = logger
    
    def extract_text_from_pdf(self, file_bytes: bytes, filename: str) -> Dict[str, any]:
        """
        Extract text from a PDF file
        
        Args:
            file_bytes: PDF file content as bytes
            filename: Name of the PDF file
            
        Returns:
            Dictionary with filename, text content, and page count
        """
        try:
            # Try PyPDF2 first
            text = self._extract_with_pypdf2(file_bytes)
            
            # If PyPDF2 fails or returns empty text, try pdfplumber
            if not text or len(text.strip()) < 50:
                self.logger.info(f"PyPDF2 returned insufficient text for {filename}, trying pdfplumber...")
                text = self._extract_with_pdfplumber(file_bytes)
            
            # Count pages
            pdf_reader = PyPDF2.PdfReader(BytesIO(file_bytes))
            page_count = len(pdf_reader.pages)
            
            return {
                'filename': filename,
                'text': text,
                'page_count': page_count,
                'success': True,
                'error': None
            }
            
        except Exception as e:
            self.logger.error(f"Error extracting text from {filename}: {str(e)}")
            return {
                'filename': filename,
                'text': '',
                'page_count': 0,
                'success': False,
                'error': str(e)
            }
    
    def _extract_with_pypdf2(self, file_bytes: bytes) -> str:
        """Extract text using PyPDF2"""
        try:
            pdf_reader = PyPDF2.PdfReader(BytesIO(file_bytes))
            text_content = []
            
            for page_num, page in enumerate(pdf_reader.pages):
                try:
                    page_text = page.extract_text()
                    if page_text:
                        text_content.append(f"\n--- Page {page_num + 1} ---\n")
                        text_content.append(page_text)
                except Exception as e:
                    self.logger.warning(f"Error extracting page {page_num + 1}: {str(e)}")
                    continue
            
            return '\n'.join(text_content)
            
        except Exception as e:
            self.logger.error(f"PyPDF2 extraction failed: {str(e)}")
            return ''
    
    def _extract_with_pdfplumber(self, file_bytes: bytes) -> str:
        """Extract text using pdfplumber (fallback method)"""
        try:
            text_content = []
            
            with pdfplumber.open(BytesIO(file_bytes)) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    try:
                        page_text = page.extract_text()
                        if page_text:
                            text_content.append(f"\n--- Page {page_num + 1} ---\n")
                            text_content.append(page_text)
                    except Exception as e:
                        self.logger.warning(f"Error extracting page {page_num + 1}: {str(e)}")
                        continue
            
            return '\n'.join(text_content)
            
        except Exception as e:
            self.logger.error(f"pdfplumber extraction failed: {str(e)}")
            return ''
    
    def extract_from_multiple_pdfs(self, files: List[tuple]) -> List[Dict]:
        """
        Extract text from multiple PDF files
        
        Args:
            files: List of tuples (filename, file_bytes)
            
        Returns:
            List of extraction results
        """
        results = []
        
        for filename, file_bytes in files:
            result = self.extract_text_from_pdf(file_bytes, filename)
            results.append(result)
            
            if result['success']:
                self.logger.info(f"Successfully extracted {len(result['text'])} characters from {filename}")
            else:
                self.logger.error(f"Failed to extract text from {filename}: {result['error']}")
        
        return results


def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    """
    Split text into overlapping chunks
    
    Args:
        text: Input text to chunk
        chunk_size: Maximum size of each chunk
        overlap: Number of characters to overlap between chunks
        
    Returns:
        List of text chunks
    """
    if not text or len(text) == 0:
        return []
    
    chunks = []
    start = 0
    text_length = len(text)
    
    while start < text_length:
        end = start + chunk_size
        
        # If this is not the last chunk, try to break at a sentence or word boundary
        if end < text_length:
            # Look for sentence boundary (., !, ?)
            for i in range(end, max(start + overlap, end - 100), -1):
                if text[i] in ['.', '!', '?', '\n']:
                    end = i + 1
                    break
            else:
                # Look for word boundary (space)
                for i in range(end, max(start + overlap, end - 50), -1):
                    if text[i] == ' ':
                        end = i
                        break
        
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        
        start = end - overlap
    
    return chunks

