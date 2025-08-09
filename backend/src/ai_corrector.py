"""
AI Corrector Module
Handles text correction and improvement using AI models (OpenAI GPT)
"""

import os
import logging
from typing import Dict, Any, Optional, List
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AICorrector:
    """AI-powered text corrector using OpenAI GPT models"""
    
    def __init__(self):
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize OpenAI client"""
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            logger.warning("OpenAI API key not found. AI correction will not be available.")
            return
        
        try:
            self.client = OpenAI(api_key=api_key)
            logger.info("OpenAI client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI client: {e}")
    
    def is_available(self) -> bool:
        """Check if AI correction is available"""
        return self.client is not None
    
    def correct_text(self, text: str, language: str = 'mixed', context: str = None) -> Dict[str, Any]:
        """Correct OCR text using AI"""
        if not self.is_available():
            return {
                'original_text': text,
                'corrected_text': text,
                'confidence': 0,
                'changes_made': [],
                'success': False,
                'error': 'AI correction not available - OpenAI API key not configured'
            }
        
        if not text.strip():
            return {
                'original_text': text,
                'corrected_text': text,
                'confidence': 100,
                'changes_made': [],
                'success': True,
                'error': None
            }
        
        try:
            # Prepare the prompt based on language
            prompt = self._create_correction_prompt(text, language, context)
            
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert text corrector specializing in fixing OCR errors in Arabic and English texts. You maintain the original meaning while fixing spelling, grammar, and OCR-specific errors."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,  # Low temperature for consistent corrections
                max_tokens=2000
            )
            
            corrected_text = response.choices[0].message.content.strip()
            
            # Analyze changes
            changes = self._analyze_changes(text, corrected_text)
            
            # Calculate confidence based on the number of changes
            confidence = self._calculate_confidence(text, corrected_text, changes)
            
            return {
                'original_text': text,
                'corrected_text': corrected_text,
                'confidence': confidence,
                'changes_made': changes,
                'success': True,
                'error': None,
                'model_used': 'gpt-3.5-turbo'
            }
            
        except Exception as e:
            logger.error(f"Error in AI correction: {e}")
            return {
                'original_text': text,
                'corrected_text': text,
                'confidence': 0,
                'changes_made': [],
                'success': False,
                'error': str(e)
            }
    
    def _create_correction_prompt(self, text: str, language: str, context: str = None) -> str:
        """Create correction prompt based on language and context"""
        
        base_prompt = f"""Please correct the following OCR-extracted text. Fix spelling errors, grammar mistakes, and typical OCR errors while preserving the original meaning and structure.

Text to correct:
{text}

Instructions:
- Fix obvious OCR errors (like 'rn' instead of 'm', '0' instead of 'O', etc.)
- Correct spelling and grammar mistakes
- Maintain the original language and meaning
- Keep the same paragraph structure
- If the text contains both Arabic and English, preserve both languages
- Only return the corrected text, no explanations"""
        
        if language == 'ara' or 'arabic' in language.lower():
            base_prompt += """
- Pay special attention to Arabic text direction (RTL)
- Fix common Arabic OCR errors (ة/ه, ي/ى, همزة forms)
- Correct Arabic diacritics if clearly wrong"""
        
        if context:
            base_prompt += f"\n- Context: {context}"
        
        return base_prompt
    
    def _analyze_changes(self, original: str, corrected: str) -> List[Dict[str, str]]:
        """Analyze changes made during correction"""
        changes = []
        
        # Simple word-level comparison
        original_words = original.split()
        corrected_words = corrected.split()
        
        # Find differences (simplified approach)
        if len(original_words) == len(corrected_words):
            for i, (orig_word, corr_word) in enumerate(zip(original_words, corrected_words)):
                if orig_word != corr_word:
                    changes.append({
                        'type': 'word_change',
                        'original': orig_word,
                        'corrected': corr_word,
                        'position': i
                    })
        else:
            # Length difference indicates insertions/deletions
            changes.append({
                'type': 'structure_change',
                'original': f"{len(original_words)} words",
                'corrected': f"{len(corrected_words)} words",
                'position': -1
            })
        
        return changes
    
    def _calculate_confidence(self, original: str, corrected: str, changes: List[Dict]) -> float:
        """Calculate confidence score for the correction"""
        if original == corrected:
            return 100.0  # No changes needed
        
        # Base confidence
        confidence = 85.0
        
        # Adjust based on number of changes
        change_ratio = len(changes) / max(len(original.split()), 1)
        
        if change_ratio < 0.1:  # Less than 10% of words changed
            confidence = 95.0
        elif change_ratio < 0.3:  # Less than 30% of words changed
            confidence = 85.0
        elif change_ratio < 0.5:  # Less than 50% of words changed
            confidence = 70.0
        else:  # More than 50% of words changed
            confidence = 50.0
        
        return confidence
    
    def correct_multiple_texts(self, texts: List[str], language: str = 'mixed', context: str = None) -> List[Dict[str, Any]]:
        """Correct multiple texts"""
        results = []
        
        for text in texts:
            result = self.correct_text(text, language, context)
            results.append(result)
        
        return results
    
    def batch_correct_ocr_results(self, ocr_results: Dict[str, Any], language: str = 'mixed', context: str = None) -> Dict[str, Any]:
        """Correct OCR results from multiple engines"""
        corrected_results = {}
        
        for engine_name, result in ocr_results.items():
            if result.get('success', False) and result.get('text'):
                correction = self.correct_text(result['text'], language, context)
                
                corrected_results[engine_name] = {
                    'original_ocr': result,
                    'ai_correction': correction,
                    'final_text': correction['corrected_text'],
                    'improvement_score': correction['confidence'] - result.get('confidence', 0)
                }
            else:
                corrected_results[engine_name] = {
                    'original_ocr': result,
                    'ai_correction': {
                        'success': False,
                        'error': 'Original OCR failed'
                    },
                    'final_text': '',
                    'improvement_score': 0
                }
        
        return corrected_results
    
    def suggest_improvements(self, text: str, language: str = 'mixed') -> Dict[str, Any]:
        """Suggest improvements for text quality"""
        if not self.is_available():
            return {
                'suggestions': [],
                'success': False,
                'error': 'AI correction not available'
            }
        
        try:
            prompt = f"""Analyze the following text and suggest specific improvements for clarity, grammar, and style. Focus on:
1. Grammar and syntax errors
2. Word choice improvements
3. Sentence structure enhancements
4. OCR-related errors that might have been missed

Text to analyze:
{text}

Provide suggestions in a structured format with specific examples."""
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a text quality analyst. Provide specific, actionable suggestions for text improvement."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=1000
            )
            
            suggestions = response.choices[0].message.content.strip()
            
            return {
                'suggestions': suggestions,
                'success': True,
                'error': None
            }
            
        except Exception as e:
            logger.error(f"Error in suggestion generation: {e}")
            return {
                'suggestions': [],
                'success': False,
                'error': str(e)
            }

