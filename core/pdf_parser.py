"""Enhanced PDF Parser with OCR, table extraction, and image extraction"""

import logging
from typing import List, Dict, Optional, Tuple
import pdfplumber
import PyPDF2
from io import BytesIO
import re

from core.ocr import OCRProcessor
from utils.helpers import clean_text, extract_page_number

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EnhancedPDFParser:
    """Enhanced PDF parser with multiple extraction methods"""
    
    def __init__(self):
        self.logger = logger
        self.ocr_processor = OCRProcessor()
    
    def extract_from_pdf(
        self,
        file_bytes: bytes,
        filename: str,
        use_ocr: bool = False,
        extract_tables: bool = True,
        extract_images: bool = False
    ) -> Dict:
        """
        Extract text, tables, and images from PDF
        
        Args:
            file_bytes: PDF file content as bytes
            filename: Name of the PDF file
            use_ocr: Whether to use OCR for scanned PDFs
            extract_tables: Whether to extract tables
            extract_images: Whether to extract images
            
        Returns:
            Dictionary with extracted content and metadata
        """
        result = {
            'filename': filename,
            'text': '',
            'tables': [],
            'images': [],
            'pages': [],
            'page_count': 0,
            'success': False,
            'method': 'pdfplumber',
            'error': None
        }
        
        try:
            # First, try pdfplumber for high-quality text extraction
            pdfplumber_result = self._extract_with_pdfplumber(
                file_bytes, filename, extract_tables
            )
            
            # Check if we got sufficient text
            text_length = len(pdfplumber_result.get('text', '').strip())
            
            if text_length < 50 and use_ocr:
                # Try OCR if text extraction yielded little
                self.logger.info(f"Insufficient text from pdfplumber for {filename}, trying OCR...")
                ocr_result = self.ocr_processor.extract_text_with_ocr(file_bytes, filename)
                
                if ocr_result['success']:
                    result.update(ocr_result)
                    result['method'] = 'OCR'
                else:
                    # Use pdfplumber result even if minimal
                    result.update(pdfplumber_result)
            else:
                result.update(pdfplumber_result)
            
            # Extract images if requested
            if extract_images:
                images = self.ocr_processor.extract_images_from_pdf(file_bytes, filename)
                result['images'] = images
            
            # Process pages with metadata
            result['pages'] = self._process_pages(result.get('text', ''), filename)
            
            result['success'] = True
            result['text'] = clean_text(result.get('text', ''))
            
            self.logger.info(
                f"Extracted {len(result['text'])} chars, "
                f"{len(result['tables'])} tables, "
                f"{len(result['images'])} images from {filename}"
            )
            
        except Exception as e:
            self.logger.error(f"Error extracting from {filename}: {str(e)}")
            result['error'] = str(e)
            result['success'] = False
        
        return result
    
    def _extract_with_pdfplumber(
        self,
        file_bytes: bytes,
        filename: str,
        extract_tables: bool = True
    ) -> Dict:
        """Extract text and tables using pdfplumber"""
        try:
            text_content = []
            tables = []
            pages_data = []
            
            with pdfplumber.open(BytesIO(file_bytes)) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    try:
                        # Extract text
                        page_text = page.extract_text()
                        
                        if page_text:
                            text_content.append(f"\n--- Page {page_num} ---\n{page_text}")
                            pages_data.append({
                                'page': page_num,
                                'text': page_text,
                                'method': 'pdfplumber'
                            })
                        
                        # Extract tables if requested
                        if extract_tables:
                            page_tables = page.extract_tables()
                            for table_num, table in enumerate(page_tables, 1):
                                if table:
                                    # Convert table to text representation
                                    table_text = self._table_to_text(table)
                                    tables.append({
                                        'page': page_num,
                                        'table_num': table_num,
                                        'data': table,
                                        'text': table_text
                                    })
                                    # Add table text to page text
                                    text_content.append(f"\n[Table {table_num} on Page {page_num}]\n{table_text}\n")
                    
                    except Exception as e:
                        self.logger.warning(f"Error extracting page {page_num}: {str(e)}")
                        continue
            
            return {
                'text': '\n'.join(text_content),
                'tables': tables,
                'pages': pages_data,
                'page_count': len(pages_data),
                'method': 'pdfplumber'
            }
            
        except Exception as e:
            self.logger.error(f"pdfplumber extraction failed: {str(e)}")
            return {
                'text': '',
                'tables': [],
                'pages': [],
                'page_count': 0,
                'method': 'pdfplumber',
                'error': str(e)
            }
    
    def _table_to_text(self, table: List[List]) -> str:
        """Convert table data to readable text"""
        if not table:
            return ""
        
        text_rows = []
        for row in table:
            # Filter out None values and join
            clean_row = [str(cell) if cell is not None else '' for cell in row]
            text_rows.append(' | '.join(clean_row))
        
        return '\n'.join(text_rows)
    
    def _process_pages(self, text: str, filename: str) -> List[Dict]:
        """Process text and extract page-level metadata"""
        pages = []
        
        # Split by page markers
        page_pattern = r'---\s*Page\s+(\d+)\s*---'
        page_matches = list(re.finditer(page_pattern, text, re.IGNORECASE))
        
        for i, match in enumerate(page_matches):
            page_num = int(match.group(1))
            start_pos = match.end()
            
            # Find end position (next page marker or end of text)
            if i + 1 < len(page_matches):
                end_pos = page_matches[i + 1].start()
            else:
                end_pos = len(text)
            
            page_text = text[start_pos:end_pos].strip()
            
            pages.append({
                'page': page_num,
                'text': page_text,
                'start_char': start_pos,
                'end_char': end_pos,
                'filename': filename
            })
        
        return pages
    
    def extract_from_multiple_pdfs(
        self,
        files: List[Tuple[str, bytes]],
        use_ocr: bool = False,
        extract_tables: bool = True,
        extract_images: bool = False
    ) -> List[Dict]:
        """
        Extract content from multiple PDF files
        
        Args:
            files: List of tuples (filename, file_bytes)
            use_ocr: Whether to use OCR
            extract_tables: Whether to extract tables
            extract_images: Whether to extract images
            
        Returns:
            List of extraction results
        """
        results = []
        
        for filename, file_bytes in files:
            result = self.extract_from_pdf(
                file_bytes,
                filename,
                use_ocr=use_ocr,
                extract_tables=extract_tables,
                extract_images=extract_images
            )
            results.append(result)
            
            if result['success']:
                self.logger.info(
                    f"Successfully extracted from {filename}: "
                    f"{len(result['text'])} chars, "
                    f"{len(result['tables'])} tables"
                )
            else:
                self.logger.error(f"Failed to extract from {filename}: {result.get('error', 'Unknown error')}")
        
        return results

