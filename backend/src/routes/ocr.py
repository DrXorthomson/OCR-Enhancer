"""
OCR Routes
Flask routes for OCR processing and AI correction
"""

import os
import tempfile
import uuid
from datetime import datetime
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from src.ocr_engines import OCRManager
from src.ai_corrector import AICorrector
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create blueprint
ocr_bp = Blueprint('ocr', __name__)

# Initialize OCR manager and AI corrector
ocr_manager = OCRManager()
ai_corrector = AICorrector()

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'tiff', 'tif', 'pdf', 'txt'}

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@ocr_bp.route('/engines', methods=['GET'])
def get_available_engines():
    """Get list of available OCR engines"""
    try:
        engines = ocr_manager.get_available_engines()
        ai_available = ai_corrector.is_available()
        
        return jsonify({
            'success': True,
            'engines': engines,
            'ai_correction_available': ai_available,
            'supported_formats': list(ALLOWED_EXTENSIONS)
        })
    except Exception as e:
        logger.error(f"Error getting engines: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@ocr_bp.route('/process', methods=['POST'])
def process_file():
    """Process uploaded file with OCR and AI correction"""
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No file provided'
            }), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected'
            }), 400
        
        if not allowed_file(file.filename):
            return jsonify({
                'success': False,
                'error': f'File type not supported. Allowed types: {", ".join(ALLOWED_EXTENSIONS)}'
            }), 400
        
        # Get processing options
        engines = request.form.getlist('engines') or ['tesseract']
        language = request.form.get('language', 'eng+ara')
        use_ai_correction = request.form.get('ai_correction', 'true').lower() == 'true'
        combination_method = request.form.get('combination_method', 'best_confidence')
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        file_id = str(uuid.uuid4())
        file_extension = filename.rsplit('.', 1)[1].lower()
        temp_filename = f"{file_id}.{file_extension}"
        
        # Create uploads directory if it doesn't exist
        uploads_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'uploads')
        os.makedirs(uploads_dir, exist_ok=True)
        
        file_path = os.path.join(uploads_dir, temp_filename)
        file.save(file_path)
        
        # Process based on file type
        if file_extension == 'pdf':
            ocr_results = ocr_manager.process_pdf(file_path, engines, language)
        elif file_extension == 'txt':
            # Handle external OCR text files
            with open(file_path, 'r', encoding='utf-8') as f:
                text_content = f.read()
            
            external_engine_name = request.form.get('external_engine', 'External OCR')
            confidence = float(request.form.get('confidence', 85.0))
            
            ocr_results = {
                'external': ocr_manager.process_external_text(text_content, external_engine_name, confidence)
            }
        else:
            # Image file
            ocr_results = ocr_manager.process_image(file_path, engines, language)
        
        # Combine OCR results
        if len(ocr_results) > 1:
            combined_result = ocr_manager.combine_results(ocr_results, combination_method)
        else:
            # Single engine result
            engine_name = list(ocr_results.keys())[0]
            if file_extension == 'pdf':
                # For PDF, combine all pages
                pages_text = []
                for page_result in ocr_results[engine_name]:
                    if page_result.get('success', False):
                        pages_text.append(page_result['text'])
                
                combined_text = '\n\n'.join(pages_text)
                avg_confidence = sum(page.get('confidence', 0) for page in ocr_results[engine_name]) / len(ocr_results[engine_name])
                
                combined_result = {
                    'combined_text': combined_text,
                    'confidence': avg_confidence,
                    'method': 'single_engine',
                    'engines_used': [engine_name],
                    'success': bool(combined_text.strip()),
                    'best_engine': engine_name
                }
            else:
                result = ocr_results[engine_name]
                combined_result = {
                    'combined_text': result.get('text', ''),
                    'confidence': result.get('confidence', 0),
                    'method': 'single_engine',
                    'engines_used': [engine_name],
                    'success': result.get('success', False),
                    'best_engine': engine_name
                }
        
        # Apply AI correction if requested
        ai_result = None
        final_text = combined_result['combined_text']
        
        if use_ai_correction and ai_corrector.is_available() and combined_result['success']:
            context = request.form.get('context', '')
            ai_result = ai_corrector.correct_text(combined_result['combined_text'], language, context)
            if ai_result['success']:
                final_text = ai_result['corrected_text']
        
        # Clean up uploaded file
        try:
            os.remove(file_path)
        except:
            pass
        
        # Prepare response
        response_data = {
            'success': True,
            'file_id': file_id,
            'filename': filename,
            'processing_time': datetime.now().isoformat(),
            'ocr_results': ocr_results,
            'combined_result': combined_result,
            'ai_correction': ai_result,
            'final_text': final_text,
            'settings': {
                'engines': engines,
                'language': language,
                'ai_correction': use_ai_correction,
                'combination_method': combination_method
            }
        }
        
        return jsonify(response_data)
        
    except Exception as e:
        logger.error(f"Error processing file: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@ocr_bp.route('/correct-text', methods=['POST'])
def correct_text():
    """Correct text using AI without OCR processing"""
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({
                'success': False,
                'error': 'No text provided'
            }), 400
        
        text = data['text']
        language = data.get('language', 'mixed')
        context = data.get('context', '')
        
        if not ai_corrector.is_available():
            return jsonify({
                'success': False,
                'error': 'AI correction not available - OpenAI API key not configured'
            }), 503
        
        result = ai_corrector.correct_text(text, language, context)
        
        return jsonify({
            'success': True,
            'result': result
        })
        
    except Exception as e:
        logger.error(f"Error correcting text: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@ocr_bp.route('/suggest-improvements', methods=['POST'])
def suggest_improvements():
    """Get AI suggestions for text improvement"""
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({
                'success': False,
                'error': 'No text provided'
            }), 400
        
        text = data['text']
        language = data.get('language', 'mixed')
        
        if not ai_corrector.is_available():
            return jsonify({
                'success': False,
                'error': 'AI suggestions not available - OpenAI API key not configured'
            }), 503
        
        result = ai_corrector.suggest_improvements(text, language)
        
        return jsonify({
            'success': True,
            'result': result
        })
        
    except Exception as e:
        logger.error(f"Error getting suggestions: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@ocr_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'success': True,
        'status': 'healthy',
        'engines_available': ocr_manager.get_available_engines(),
        'ai_available': ai_corrector.is_available(),
        'timestamp': datetime.now().isoformat()
    })

