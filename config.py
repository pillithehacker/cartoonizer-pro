import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent

# Flask Configuration
SECRET_KEY = os.environ.get('SECRET_KEY', 'cartoonizer-pro-secret-key-2024')
DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'
HOST = os.environ.get('HOST', '0.0.0.0')
PORT = int(os.environ.get('PORT', 5000))

# Upload Configuration - Use /tmp for Vercel compatibility
UPLOAD_FOLDER = Path('/tmp' if os.environ.get('VERCEL') else BASE_DIR / 'static' / 'uploads')
OUTPUT_FOLDER = Path('/tmp' if os.environ.get('VERCEL') else BASE_DIR / 'static' / 'outputs')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload and output directories exist
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

# Image Processing Configuration
DEFAULT_BLUR_INTENSITY = 5
DEFAULT_EDGE_STRENGTH = 100
DEFAULT_CARTOON_INTENSITY = 8

# Cartoon Filter Types
FILTER_TYPES = {
    'classic': 'Classic Cartoon',
    'pencil': 'Pencil Sketch',
    'comic': 'Comic Style',
    'high_contrast': 'High Contrast Toon',
    'pastel': 'Smooth Pastel'
}