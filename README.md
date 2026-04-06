# Cartoonizer Pro - Deployment Guide

## Vercel Deployment Steps

### Prerequisites
1. A Vercel account (sign up at vercel.com)
2. Git installed locally

### Deployment Process

1. **Prepare the project:**
   - Ensure all files are in the `cartoonizer-pro` folder
   - The project is already configured for Vercel

2. **Deploy using Vercel CLI:**
   ```bash
   # Install Vercel CLI if not already installed
   npm i -g vercel

   # Navigate to project directory
   cd cartoonizer-pro

   # Deploy to Vercel
   vercel
   ```

3. **Or deploy via GitHub:**
   - Push your code to a GitHub repository
   - Go to vercel.com and "Import Project"
   - Select your repository and deploy

### Important Notes for Vercel Deployment

1. **Serverless Functions**: Vercel has a 60-second timeout for Python functions. Image processing may timeout for large images.

2. **File Storage**: Vercel serverless functions use ephemeral `/tmp` storage. Files are deleted after each request.

3. **Static Files**: All static files (CSS, JS, uploads) must be served from Vercel's static storage or use Vercel Blob for file uploads.

4. **Environment Variables**: Set your SECRET_KEY in Vercel dashboard under "Environment Variables"

### Alternative: Deploy as Static Site with Backend API

For production use with image processing, consider:
- **Frontend**: Deploy static files to Vercel
- **Backend**: Use a dedicated backend service (Render, Railway, Heroku) for image processing

### Files for Deployment:
- `vercel.json` - Vercel configuration
- `api/index.py` - Serverless function handler
- `wsgi.py` - WSGI entry point
- `requirements.txt` - Python dependencies
- `templates/` - HTML templates
- `static/` - CSS, JS, and media files

### Local Testing:
```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
python wsgi.py
# or
python app.py
```

The app will be available at http://localhost:5000