"""
Cartoonizer Pro - Image Processing Module
Core cartoon effect processing using OpenCV and NumPy
"""

import cv2
import numpy as np
import uuid
import os
from pathlib import Path


def apply_bilateral_filter(image, d=9, sigma_color=75, sigma_space=75):
    """Apply bilateral filter for edge-preserving smoothing"""
    return cv2.bilateralFilter(image, d, sigma_color, sigma_space)


def detect_edges(image, method='canny', threshold1=50, threshold2=150):
    """Detect edges using Canny or adaptive thresholding"""
    if method == 'canny':
        edges = cv2.Canny(image, threshold1, threshold2)
        edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    else:  # adaptive threshold
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY, 11, 2
        )
        edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    return edges


def quantize_colors(image, k=8):
    """Apply K-Means color quantization for posterization effect"""
    # Convert to float32
    pixels = image.reshape((-1, 3)).astype(np.float32)
    
    # Define criteria and apply K-means
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
    _, labels, centers = cv2.kmeans(pixels, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    
    # Convert back to uint8
    centers = np.uint8(centers)
    quantized = centers[labels.flatten()]
    return quantized.reshape(image.shape)


def apply_gaussian_blur(image, kernel_size=5):
    """Apply Gaussian blur for smoothing"""
    return cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)


def enhance_contrast(image, clip_limit=2.0, tile_grid_size=8):
    """Enhance contrast using CLAHE"""
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(tile_grid_size, tile_grid_size))
    l = clahe.apply(l)
    enhanced = cv2.merge([l, a, b])
    return cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)


def process_classic_cartoon(image, blur_intensity, edge_strength, cartoon_intensity):
    """Classic cartoon effect pipeline"""
    # Step 1: Bilateral filter for smooth colors
    blurred = apply_bilateral_filter(image, d=blur_intensity, sigma_color=75, sigma_space=75)
    
    # Step 2: Quantize colors
    k_value = 8 + (cartoon_intensity // 2)
    quantized = quantize_colors(blurred, k=k_value)
    
    # Step 3: Detect edges
    edges = detect_edges(image, method='canny', threshold1=50, threshold2=edge_strength)
    
    # Step 4: Combine quantized colors with edges
    cartoon = cv2.bitwise_and(quantized, edges)
    
    return cartoon


def process_pencil_sketch(image, blur_intensity, edge_strength, cartoon_intensity):
    """Pencil sketch effect pipeline"""
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Invert grayscale
    inverted = 255 - gray
    
    # Apply Gaussian blur
    blur_size = blur_intensity * 2 + 1
    blurred = cv2.GaussianBlur(inverted, (blur_size, blur_size), 0)
    
    # Invert again
    inverted_blur = 255 - blurred
    
    # Create sketch
    sketch = cv2.divide(gray, inverted_blur, scale=256.0)
    
    # Convert back to BGR for display
    sketch_bgr = cv2.cvtColor(sketch, cv2.COLOR_GRAY2BGR)
    
    return sketch_bgr


def process_comic_style(image, blur_intensity, edge_strength, cartoon_intensity):
    """Comic style effect pipeline"""
    # Step 1: Apply bilateral filter
    smoothed = apply_bilateral_filter(image, d=blur_intensity)
    
    # Step 2: Enhance contrast
    enhanced = enhance_contrast(smoothed, clip_limit=1.5 + (cartoon_intensity / 10))
    
    # Step 3: Color boost - increase saturation
    hsv = cv2.cvtColor(enhanced, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    s = cv2.add(s, 30)  # Increase saturation
    s = np.clip(s, 0, 255)
    boosted = cv2.merge([h, s, v])
    comic = cv2.cvtColor(boosted, cv2.COLOR_HSV2BGR)
    
    # Step 4: Add edge lines
    edges = detect_edges(image, method='canny', threshold1=30, threshold2=edge_strength)
    comic = cv2.bitwise_and(comic, edges)
    
    return comic


def process_high_contrast(image, blur_intensity, edge_strength, cartoon_intensity):
    """High contrast toon effect pipeline"""
    # Step 1: Apply bilateral filter
    smoothed = apply_bilateral_filter(image, d=blur_intensity)
    
    # Step 2: Strong color quantization
    k_value = 6 + (cartoon_intensity // 3)
    quantized = quantize_colors(smoothed, k=k_value)
    
    # Step 3: Apply high contrast
    # Create posterized look
    alpha = 1.2 + (cartoon_intensity / 20)  # Contrast control
    beta = -30  # Brightness adjustment
    contrasted = cv2.convertScaleAbs(quantized, alpha=alpha, beta=beta)
    
    # Step 4: Strong edge detection
    edges = detect_edges(image, method='canny', threshold1=30, threshold2=edge_strength)
    
    # Step 5: Combine
    toon = cv2.bitwise_and(contrasted, edges)
    
    return toon


def process_pastel(image, blur_intensity, edge_strength, cartoon_intensity):
    """Smooth pastel effect pipeline"""
    # Step 1: Strong bilateral filter for soft look
    soft = apply_bilateral_filter(image, d=blur_intensity + 3, sigma_color=100, sigma_space=100)
    
    # Step 2: Gentle color quantization
    k_value = 16 + cartoon_intensity
    quantized = quantize_colors(soft, k=k_value)
    
    # Step 3: Apply slight blur for smoothness
    smoothed = cv2.bilateralFilter(quantized, 9, 50, 50)
    
    # Step 4: Soft edge overlay
    edges = detect_edges(image, method='canny', threshold1=80, threshold2=edge_strength)
    edges = cv2.GaussianBlur(edges, (3, 3), 0)
    
    # Step 5: Blend edges gently
    pastel = cv2.addWeighted(smoothed, 0.9, edges, 0.1, 0)
    
    return pastel


def process_image(input_path, output_dir, filter_type='classic', 
                  blur_intensity=5, edge_strength=100, cartoon_intensity=8):
    """
    Main image processing function
    Applies cartoon effect based on filter type and parameters
    
    Args:
        input_path: Path to input image
        output_dir: Directory to save output
        filter_type: Type of cartoon filter
        blur_intensity: Bilateral filter blur amount
        edge_strength: Edge detection threshold
        cartoon_intensity: Color quantization level
    
    Returns:
        Output filename if successful, None otherwise
    """
    try:
        # Read the image
        image = cv2.imread(input_path)
        if image is None:
            print(f"Error: Could not read image from {input_path}")
            return None
        
        # Process based on filter type
        if filter_type == 'classic':
            result = process_classic_cartoon(image, blur_intensity, edge_strength, cartoon_intensity)
        elif filter_type == 'pencil':
            result = process_pencil_sketch(image, blur_intensity, edge_strength, cartoon_intensity)
        elif filter_type == 'comic':
            result = process_comic_style(image, blur_intensity, edge_strength, cartoon_intensity)
        elif filter_type == 'high_contrast':
            result = process_high_contrast(image, blur_intensity, edge_strength, cartoon_intensity)
        elif filter_type == 'pastel':
            result = process_pastel(image, blur_intensity, edge_strength, cartoon_intensity)
        else:
            result = process_classic_cartoon(image, blur_intensity, edge_strength, cartoon_intensity)
        
        # Generate output filename
        ext = os.path.splitext(input_path)[1]
        output_filename = f"cartoonized_{uuid.uuid4().hex}{ext}"
        output_path = Path(output_dir) / output_filename
        
        # Ensure output directory exists
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # Save the processed image
        cv2.imwrite(str(output_path), result, [cv2.IMWRITE_JPEG_QUALITY, 95])
        
        print(f"Image processed successfully: {output_filename}")
        return output_filename
        
    except Exception as e:
        print(f"Error processing image: {str(e)}")
        import traceback
        traceback.print_exc()
        return None