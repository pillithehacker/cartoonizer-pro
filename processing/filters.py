"""
Cartoonizer Pro - Filter Module
Provides filter preview information and metadata
"""

FILTER_INFO = {
    'classic': {
        'name': 'Classic Cartoon',
        'description': 'Traditional cartoon effect with smooth colors and bold edges',
        'icon': '🎨',
        'preview_params': {
            'blur_intensity': 5,
            'edge_strength': 100,
            'cartoon_intensity': 8
        }
    },
    'pencil': {
        'name': 'Pencil Sketch',
        'description': 'Transforms your image into a hand-drawn pencil sketch',
        'icon': '✏️',
        'preview_params': {
            'blur_intensity': 7,
            'edge_strength': 150,
            'cartoon_intensity': 10
        }
    },
    'comic': {
        'name': 'Comic Style',
        'description': 'Vibrant colors with enhanced saturation and comic book aesthetics',
        'icon': '💥',
        'preview_params': {
            'blur_intensity': 5,
            'edge_strength': 80,
            'cartoon_intensity': 6
        }
    },
    'high_contrast': {
        'name': 'High Contrast Toon',
        'description': 'Bold, dramatic look with strong color blocking and sharp edges',
        'icon': '⚡',
        'preview_params': {
            'blur_intensity': 4,
            'edge_strength': 120,
            'cartoon_intensity': 12
        }
    },
    'pastel': {
        'name': 'Smooth Pastel',
        'description': 'Soft, dreamy appearance with gentle colors and subtle edges',
        'icon': '🌸',
        'preview_params': {
            'blur_intensity': 8,
            'edge_strength': 60,
            'cartoon_intensity': 4
        }
    }
}


def get_filter_info(filter_type):
    """Get information about a specific filter type"""
    return FILTER_INFO.get(filter_type, FILTER_INFO['classic'])


def get_all_filters():
    """Get information about all available filters"""
    return FILTER_INFO


def get_filter_preview(filter_type):
    """Get preview parameters for a filter type"""
    filter_info = get_filter_info(filter_type)
    return {
        'success': True,
        'filter_type': filter_type,
        'name': filter_info['name'],
        'description': filter_info['description'],
        'icon': filter_info['icon'],
        'preview_params': filter_info['preview_params']
    }


def get_default_params():
    """Get default processing parameters"""
    return {
        'blur_intensity': 5,
        'edge_strength': 100,
        'cartoon_intensity': 8
    }


def get_param_ranges():
    """Get valid ranges for processing parameters"""
    return {
        'blur_intensity': {'min': 1, 'max': 15, 'default': 5},
        'edge_strength': {'min': 20, 'max': 250, 'default': 100},
        'cartoon_intensity': {'min': 1, 'max': 20, 'default': 8}
    }