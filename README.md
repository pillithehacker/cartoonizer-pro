# 🎨 Cartoonizer Pro

A production-ready, premium AI-powered web application that transforms your photos into stunning cartoon illustrations using advanced computer vision techniques.

![Cartoonizer Pro](https://img.shields.io/badge/Version-1.0.0-brightgreen)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-3.0.0-orange)
![OpenCV](https://img.shields.io/badge/OpenCV-4.8.1-red)

## ✨ Features

- **🎭 Multiple Cartoon Styles**: Choose from 5 unique filter types
  - Classic Cartoon
  - Pencil Sketch
  - Comic Style
  - High Contrast Toon
  - Smooth Pastel

- **⚡ Real-Time Controls**: Fine-tune your results with adjustable sliders
  - Blur Intensity
  - Edge Detection Strength
  - Cartoon Intensity

- **📤 Drag & Drop Upload**: Easy image upload with instant preview
- **🔄 Before/After Comparison**: Interactive slider to compare results
- **⬇️ Download Options**: Export in PNG or JPG format
- **🌙 Dark Mode**: Premium dark theme with neon accents
- **📱 Fully Responsive**: Works on desktop, tablet, and mobile
- **🚀 Fast Processing**: Optimized pipeline for quick results

## 🏗️ Project Structure

```
cartoonizer-pro/
├── app.py                    # Main Flask application
├── config.py                  # Configuration settings
├── requirements.txt          # Python dependencies
│
├── templates/                # HTML templates
│   ├── base.html            # Base template with navigation
│   ├── index.html           # Landing page
│   ├── cartoonize.html      # Image processing page
│   └── developer.html       # Developer info page
│
├── static/                  # Static assets
│   ├── css/
│   │   └── style.css       # Global styles
│   ├── js/
│   │   └── script.js       # JavaScript functionality
│   ├── uploads/            # Uploaded images
│   └── outputs/            # Processed images
│
└── processing/             # Backend processing
    ├── cartoon.py          # Main image processing
    └── filters.py         # Filter definitions
```

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone or Download

```bash
git clone <repository-url>
cd cartoonizer-pro
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run the Application

```bash
python app.py
```

The application will start at `http://localhost:5000`

## 🚀 Deployment

### Render (Recommended)

1. Push your code to GitHub
2. Create a new Web Service on [Render](https://render.com)
3. Connect your GitHub repository
4. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
5. Add environment variables:
   - `DEBUG`: `false`
   - `SECRET_KEY`: Your secret key
6. Deploy!

### Railway

1. Install Railway CLI
2. Initialize project:
   ```bash
   railway init
   ```
3. Add environment variables
4. Deploy:
   ```bash
   railway up
   ```

### Local Production

```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 💻 Development

### Running in Debug Mode

```bash
export DEBUG=true  # Linux/Mac
set DEBUG=true     # Windows
python app.py
```

### Adding New Filters

To add a new cartoon filter:

1. Edit `processing/filters.py` to add filter definition
2. Add processing function in `processing/cartoon.py`
3. Update the filter selection in `templates/cartoonize.html`

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Flask secret key | Auto-generated |
| `DEBUG` | Debug mode | `True` |
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `5000` |

### Upload Settings

- **Max File Size**: 16MB
- **Allowed Formats**: PNG, JPG, JPEG, GIF, WEBP

## 🧪 Testing

```bash
# Install test dependencies
pip install pytest pytest-flask

# Run tests
pytest
```

## 📝 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Landing page |
| `/cartoonize` | GET | Cartoonizer page |
| `/developer` | GET | Developer page |
| `/upload` | POST | Upload image |
| `/process` | POST | Process image |
| `/download/<filename>` | GET | Download result |

## 🎨 Design

### Color Palette

- **Primary**: `#667eea` to `#764ba2` (Gradient)
- **Accent**: `#ff6b6b`
- **Background Light**: `#f8f9ff`
- **Background Dark**: `#1a202c`

### Typography

- **Headings**: Fredoka (Bold, playful)
- **Body**: Quicksand (Clean, readable)

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [OpenCV](https://opencv.org/) - Image processing
- [Flask](https://flask.palletsprojects.com/) - Web framework
- [Bootstrap](https://getbootstrap.com/) - UI framework
- [Google Fonts](https://fonts.google.com/) - Typography

## 📧 Support

For issues and feature requests, please [open an issue](https://github.com/yourusername/cartoonizer-pro/issues).

---

<p align="center">Made with ❤️ and AI magic</p>
<p align="center">© 2024 Cartoonizer Pro</p>