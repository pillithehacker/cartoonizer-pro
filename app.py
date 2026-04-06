"""
Cartoonizer Pro - Main Flask Application
A premium AI-powered web application for converting images to cartoon style
"""

import os
import uuid
import logging
from flask import Flask, render_template, request, jsonify, send_file, flash, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from config import (
    UPLOAD_FOLDER, OUTPUT_FOLDER, ALLOWED_EXTENSIONS, 
    MAX_CONTENT_LENGTH, SECRET_KEY, DEBUG, HOST, PORT,
    DEFAULT_BLUR_INTENSITY, DEFAULT_EDGE_STRENGTH, DEFAULT_CARTOON_INTENSITY,
    FILTER_TYPES
)
from processing.cartoon import process_image

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config['UPLOAD_FOLDER'] = str(UPLOAD_FOLDER)
app.config['OUTPUT_FOLDER'] = str(OUTPUT_FOLDER)
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH


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


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded images from the uploads directory"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/outputs/<filename>')
def output_file(filename):
    """Serve processed images from the outputs directory"""
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename)


@app.route('/upload', methods=['POST'])
def upload_image():
    """Handle image upload and return preview"""
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
        logger.info(f"Image uploaded: {filename}")
        
        # Get image dimensions
        from PIL import Image
        with Image.open(filepath) as img:
            width, height = img.size
        
        # Return URL that will be served by uploaded_file route
        return jsonify({
            'success': True,
            'filename': filename,
            'preview_url': f"/uploads/{filename}",
            'width': width,
            'height': height
        })
        
    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        return jsonify({'success': False, 'error': f'Upload failed: {str(e)}'}), 500


@app.route('/process', methods=['POST'])
def process_image_route():
    """Process the uploaded image with cartoon effect"""
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
        
        logger.info(f"Processing image: {filename} with filter: {filter_type}")
        
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
        
        # Return URLs for both original and cartoonized images
        return jsonify({
            'success': True,
            'original_image': f"/uploads/{filename}",
            'cartoon_image': f"/outputs/{output_filename}",
            'output_filename': output_filename
        })
        
    except Exception as e:
        logger.error(f"Processing error: {str(e)}")
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
        logger.error(f"Download error: {str(e)}")
        return jsonify({'success': False, 'error': f'Download failed: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=DEBUG)
