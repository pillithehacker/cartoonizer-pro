"""
WSGI entry point for Vercel deployment
"""
from api.index import app

# Vercel requires the app to be exposed as 'app'
app = app

# For local testing
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)