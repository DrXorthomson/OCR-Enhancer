"""
OCR Engines Module
Handles different OCR processing methods including Tesseract and external OCR results
"""

import os
import tempfile
from typing import List, Dict, Any, Optional
from PIL import Image
import pytesseract
from pdf2image import convert_from_path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OCREngine:
    """Base class for OCR engines"""
    
    def __init__(self, name: str):
        self.name = name
    
    def extract_text(self, image_path: str, language: str = 'eng+ara') -> Dict[str, Any]:
        """Extract text from image"""
        raise NotImplementedError
    
    def process_pdf(self, pdf_path: str, language: str = 'eng+ara') -> List[Dict[str, Any]]:
        """Process PDF file and extract text from all pages"""
        raise NotImplementedError

class TesseractEngine(OCREngine):
    """Tesseract OCR Engine"""
    
    def __init__(self):
        super().__init__("Tesseract")
        # Test if Tesseract is available
        try:
            pytesseract.get_tesseract_version()
            logger.info("Tesseract OCR is available")
        except Exception as e:
            logger.error(f"Tesseract OCR is not available: {e}")
            raise
    
    def extract_text(self, image_path: str, language: str = 'eng+ara') -> Dict[str, Any]:
        """Extract text from image using Tesseract"""
        try:
            # Open image
            image = Image.open(image_path)
            
            # Configure Tesseract
            config = '--oem 3 --psm 6'  # Use LSTM OCR Engine Mode with uniform text block
            
            # Extract text
            text = pytesseract.image_to_string(image, lang=language, config=config)
            
            # Get confidence scores
            data = pytesseract.image_to_data(image, lang=language, config=config, output_type=pytesseract.Output.DICT)
            
            # Calculate average confidence
            confidences = [int(conf) for conf in data['conf'] if int(conf) > 0]
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0
            
            return {
                'engine': self.name,
                'text': text.strip(),
                'confidence': avg_confidence,
                'word_count': len(text.split()),
                'language': language,
                'success': True,
                'error': None
            }
            
        except Exception as e:
            logger.error(f"Error in Tesseract OCR: {e}")
            return {
                'engine': self.name,
                'text': '',
                'confidence': 0,
                'word_count': 0,
                'language': language,
                'success': False,
                'error': str(e)
            }
    
    def process_pdf(self, pdf_path: str, language: str = 'eng+ara') -> List[Dict[str, Any]]:
        """Process PDF file and extract text from all pages"""
        results = []
        
        try:
            # Convert PDF to images
            images = convert_from_path(pdf_path, dpi=300)
            
            for page_num, image in enumerate(images, 1):
                # Save image to temporary file
                with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
                    image.save(temp_file.name, 'PNG')
                    
                    # Extract text from image
                    result = self.extract_text(temp_file.name, language)
                    result['page_number'] = page_num
                    results.append(result)
                    
                    # Clean up temporary file
                    os.unlink(temp_file.name)
            
            return results
            
        except Exception as e:
            logger.error(f"Error processing PDF: {e}")
            return [{
                'engine': self.name,
                'text': '',
                'confidence': 0,
                'word_count': 0,
                'language': language,
                'success': False,
                'error': str(e),
                'page_number': 1
            }]

class ExternalOCREngine(OCREngine):
    """Handler for external OCR results (ABBYY FineReader, Readiris, etc.)"""
    
    def __init__(self, engine_name: str = "External"):
        super().__init__(engine_name)
    
    def process_external_text(self, text: str, confidence: Optional[float] = None) -> Dict[str, Any]:
        """Process externally provided OCR text"""
        return {
            'engine': self.name,
            'text': text.strip(),
            'confidence': confidence or 85.0,  # Default confidence for external OCR
            'word_count': len(text.split()),
            'language': 'mixed',
            'success': True,
            'error': None
        }

class OCRManager:
    """Manages multiple OCR engines and combines results"""
    
    def __init__(self):
        self.engines = {}
        self._initialize_engines()
    
    def _initialize_engines(self):
        """Initialize available OCR engines"""
        try:
            self.engines['tesseract'] = TesseractEngine()
            logger.info("Tesseract engine initialized")
        except Exception as e:
            logger.warning(f"Could not initialize Tesseract: {e}")
        
        self.engines['external'] = ExternalOCREngine()
        logger.info("External OCR handler initialized")
    
    def get_available_engines(self) -> List[str]:
        """Get list of available OCR engines"""
        return list(self.engines.keys())
    
    def process_image(self, image_path: str, engines: List[str] = None, language: str = 'eng+ara') -> Dict[str, Any]:
        """Process image with specified OCR engines"""
        if engines is None:
            engines = ['tesseract']
        
        results = {}
        
        for engine_name in engines:
            if engine_name in self.engines:
                engine = self.engines[engine_name]
                if hasattr(engine, 'extract_text'):
                    result = engine.extract_text(image_path, language)
                    results[engine_name] = result
                else:
                    logger.warning(f"Engine {engine_name} does not support image processing")
            else:
                logger.warning(f"Engine {engine_name} not available")
        
        return results
    
    def process_pdf(self, pdf_path: str, engines: List[str] = None, language: str = 'eng+ara') -> Dict[str, List[Dict[str, Any]]]:
        """Process PDF with specified OCR engines"""
        if engines is None:
            engines = ['tesseract']
        
        results = {}
        
        for engine_name in engines:
            if engine_name in self.engines:
                engine = self.engines[engine_name]
                if hasattr(engine, 'process_pdf'):
                    result = engine.process_pdf(pdf_path, language)
                    results[engine_name] = result
                else:
                    logger.warning(f"Engine {engine_name} does not support PDF processing")
            else:
                logger.warning(f"Engine {engine_name} not available")
        
        return results
    
    def process_external_text(self, text: str, engine_name: str = "ABBYY", confidence: Optional[float] = None) -> Dict[str, Any]:
        """Process externally provided OCR text"""
        external_engine = ExternalOCREngine(engine_name)
        return external_engine.process_external_text(text, confidence)
    
    def combine_results(self, results: Dict[str, Any], method: str = 'best_confidence') -> Dict[str, Any]:
        """Combine results from multiple OCR engines"""
        if not results:
            return {
                'combined_text': '',
                'confidence': 0,
                'method': method,
                'engines_used': [],
                'success': False
            }
        
        successful_results = {k: v for k, v in results.items() if v.get('success', False)}
        
        if not successful_results:
            return {
                'combined_text': '',
                'confidence': 0,
                'method': method,
                'engines_used': list(results.keys()),
                'success': False
            }
        
        if method == 'best_confidence':
            # Choose result with highest confidence
            best_result = max(successful_results.values(), key=lambda x: x.get('confidence', 0))
            return {
                'combined_text': best_result['text'],
                'confidence': best_result['confidence'],
                'method': method,
                'engines_used': list(successful_results.keys()),
                'success': True,
                'best_engine': best_result['engine']
            }
        
        elif method == 'longest_text':
            # Choose result with most text
            best_result = max(successful_results.values(), key=lambda x: len(x.get('text', '')))
            return {
                'combined_text': best_result['text'],
                'confidence': best_result['confidence'],
                'method': method,
                'engines_used': list(successful_results.keys()),
                'success': True,
                'best_engine': best_result['engine']
            }
        
        else:
            # Default to first successful result
            first_result = list(successful_results.values())[0]
            return {
                'combined_text': first_result['text'],
                'confidence': first_result['confidence'],
                'method': method,
                'engines_used': list(successful_results.keys()),
                'success': True,
                'best_engine': first_result['engine']
            }

