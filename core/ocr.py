"""OCR module for extracting text from scanned PDFs"""

import logging
from typing import List, Dict, Optional
from io import BytesIO
import numpy as np

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OCRProcessor:
    """Process scanned PDFs using OCR"""
    
    def __init__(self):
        self.logger = logger
        self.ocr_available = self._check_ocr_availability()
    
    def _check_ocr_availability(self) -> bool:
        """Check if OCR dependencies are available"""
        try:
            import pytesseract
            from pdf2image import convert_from_bytes
            return True
        except ImportError:
            self.logger.warning("OCR dependencies not available. Install: pip install pytesseract pdf2image")
            return False
    
    def extract_text_with_ocr(self, file_bytes: bytes, filename: str) -> Dict:
        """
        Extract text from scanned PDF using OCR
        
        Args:
            file_bytes: PDF file content as bytes
            filename: Name of the PDF file
            
        Returns:
            Dictionary with extracted text and metadata
        """
        if not self.ocr_available:
            return {
                'success': False,
                'text': '',
                'pages': [],
                'error': 'OCR dependencies not installed'
            }
        
        try:
            from pdf2image import convert_from_bytes
            import pytesseract
            
            self.logger.info(f"Starting OCR extraction for {filename}...")
            
            # Convert PDF pages to images
            images = convert_from_bytes(file_bytes, dpi=300)
            
            extracted_pages = []
            full_text = []
            
            for page_num, image in enumerate(images, 1):
                try:
                    # Perform OCR
                    page_text = pytesseract.image_to_string(image, lang='eng')
                    
                    if page_text.strip():
                        extracted_pages.append({
                            'page': page_num,
                            'text': page_text,
                            'method': 'OCR'
                        })
                        full_text.append(f"\n--- Page {page_num} ---\n{page_text}")
                    
                    self.logger.info(f"OCR completed for page {page_num}/{len(images)}")
                    
                except Exception as e:
                    self.logger.error(f"Error in OCR for page {page_num}: {str(e)}")
                    continue
            
            return {
                'success': True,
                'text': '\n'.join(full_text),
                'pages': extracted_pages,
                'page_count': len(images),
                'method': 'OCR',
                'error': None
            }
            
        except Exception as e:
            self.logger.error(f"OCR extraction failed for {filename}: {str(e)}")
            return {
                'success': False,
                'text': '',
                'pages': [],
                'error': str(e)
            }
    
    def extract_images_from_pdf(self, file_bytes: bytes, filename: str) -> List[Dict]:
        """
        Extract images from PDF for vision-based Q&A
        
        Args:
            file_bytes: PDF file content as bytes
            filename: Name of the PDF file
            
        Returns:
            List of image dictionaries with page numbers
        """
        if not self.ocr_available:
            return []
        
        try:
            from pdf2image import convert_from_bytes
            
            self.logger.info(f"Extracting images from {filename}...")
            
            # Convert PDF pages to images
            images = convert_from_bytes(file_bytes, dpi=200)
            
            image_list = []
            
            for page_num, image in enumerate(images, 1):
                # Convert PIL image to bytes
                from io import BytesIO
                img_bytes = BytesIO()
                image.save(img_bytes, format='PNG')
                img_bytes.seek(0)
                
                image_list.append({
                    'page': page_num,
                    'image': image,
                    'image_bytes': img_bytes.getvalue(),
                    'filename': filename
                })
            
            self.logger.info(f"Extracted {len(image_list)} images from {filename}")
            return image_list
            
        except Exception as e:
            self.logger.error(f"Error extracting images: {str(e)}")
            return []

