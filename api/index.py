"""
Vercel Serverless Function for Cartoonizer Pro
This file handles all HTTP requests for the application on Vercel
"""

import os
import sys
import uuid
import logging
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import Flask app components
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename

# Try to import config and processing
try:
    from config import (
        UPLOAD_FOLDER, OUTPUT_FOLDER, ALLOWED_EXTENSIONS, 
        MAX_CONTENT_LENGTH, SECRET_KEY,
        DEFAULT_BLUR_INTENSITY, DEFAULT_EDGE_STRENGTH, DEFAULT_CARTOON_INTENSITY,
        FILTER_TYPES
    )
    from processing.cartoon import process_image
    CONFIG_AVAILABLE = True
except ImportError as e:
    logging.warning(f"Config not available: {e}")
    CONFIG_AVAILABLE = False
    # Default values if config not available
    UPLOAD_FOLDER = Path("/tmp/uploads")
    OUTPUT_FOLDER = Path("/tmp/outputs")
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    FILTER_TYPES = ['classic', 'pencil', 'comic', 'high_contrast', 'pastel']
    DEFAULT_BLUR_INTENSITY = 5
    DEFAULT_EDGE_STRENGTH = 100
    DEFAULT_CARTOON_INTENSITY = 50

# Create Flask app for Vercel
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'cartoonizer-pro-secret-key')

# Ensure upload directories exist
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

def allowed_file(filename):
    """Check if the file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def validate_image(file):
    """Validate uploaded image file"""
    if not file:
        return False, "No file uploaded"
    
    if file.filename == '':
        return False, "No file selected"
    
    if not allowed_file(file.filename):
        return False, "Invalid file type. Allowed: png, jpg, jpeg, gif, webp"
    
    return True, "Valid"


@app.route('/')
def index():
    """Landing page route"""
    return render_template('index.html', filter_types=FILTER_TYPES)


@app.route('/cartoonize')
def cartoonize_page():
    """Cartoonizer processing page route"""
    return render_template('cartoonize.html', filter_types=FILTER_TYPES)


@app.route('/developer')
def developer_page():
    """Developer page route"""
    return render_template('developer.html')


@app.route('/upload', methods=['POST'])
def upload_image():
    """Handle image upload and return preview"""
    if not CONFIG_AVAILABLE:
        return jsonify({'success': False, 'error': 'Server configuration not available'}), 500
    
    try:
        if 'image' not in request.files:
            return jsonify({'success': False, 'error': 'No image file provided'}), 400
        
        file = request.files['image']
        
        # Validate file
        is_valid, message = validate_image(file)
        if not is_valid:
            return jsonify({'success': False, 'error': message}), 400
        
        # Generate unique filename
        ext = file.filename.rsplit('.', 1)[1].lower()
        filename = f"{uuid.uuid4().hex}.{ext}"
        filepath = UPLOAD_FOLDER / filename
        
        # Save the file
        file.save(filepath)
        
        # Get image dimensions
        from PIL import Image
        with Image.open(filepath) as img:
            width, height = img.size
        
        return jsonify({
            'success': True,
            'filename': filename,
            'preview_url': f"/static/uploads/{filename}",
            'width': width,
            'height': height
        })
        
    except Exception as e:
        logging.error(f"Upload error: {str(e)}")
        return jsonify({'success': False, 'error': f'Upload failed: {str(e)}'}), 500


@app.route('/process', methods=['POST'])
def process_image_route():
    """Process the uploaded image with cartoon effect"""
    if not CONFIG_AVAILABLE:
        return jsonify({'success': False, 'error': 'Server configuration not available'}), 500
    
    try:
        data = request.get_json()
        
        if not data or 'filename' not in data:
            return jsonify({'success': False, 'error': 'No filename provided'}), 400
        
        filename = data['filename']
        filepath = UPLOAD_FOLDER / filename
        
        if not filepath.exists():
            return jsonify({'success': False, 'error': 'File not found'}), 404
        
        # Get processing parameters
        filter_type = data.get('filter_type', 'classic')
        blur_intensity = int(data.get('blur_intensity', DEFAULT_BLUR_INTENSITY))
        edge_strength = int(data.get('edge_strength', DEFAULT_EDGE_STRENGTH))
        cartoon_intensity = int(data.get('cartoon_intensity', DEFAULT_CARTOON_INTENSITY))
        
        # Process the image
        output_filename = process_image(
            str(filepath),
            str(OUTPUT_FOLDER),
            filter_type=filter_type,
            blur_intensity=blur_intensity,
            edge_strength=edge_strength,
            cartoon_intensity=cartoon_intensity
        )
        
        if not output_filename:
            return jsonify({'success': False, 'error': 'Processing failed'}), 500
        
        return jsonify({
            'success': True,
            'output_url': f"/static/outputs/{output_filename}",
            'output_filename': output_filename
        })
        
    except Exception as e:
        logging.error(f"Processing error: {str(e)}")
        return jsonify({'success': False, 'error': f'Processing failed: {str(e)}'}), 500


@app.route('/download/<filename>')
def download_image(filename):
    """Download the processed image"""
    try:
        filepath = OUTPUT_FOLDER / filename
        
        if not filepath.exists():
            return jsonify({'success': False, 'error': 'File not found'}), 404
        
        return send_file(filepath, as_attachment=True, download_name=f"cartoonized_{filename}")
        
    except Exception as e:
        logging.error(f"Download error: {str(e)}")
        return jsonify({'success': False, 'error': f'Download failed: {str(e)}'}), 500


# Vercel handler
def handler(request):
    """Vercel serverless function handler"""
    return app(request)