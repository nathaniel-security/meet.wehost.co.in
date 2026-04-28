import os
from flask import Flask, redirect
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Get Google Meet URL from environment variable
# If it's empty or not set, use the placeholder
MEET_URL = os.environ.get("MEET_URL") or "https://meet.google.com/lookup/default"

# Ensure the URL starts with http:// or https://
if not MEET_URL.startswith(("http://", "https://")):
    MEET_URL = f"https://{MEET_URL}"

@app.route('/')
def index():
    """Redirect to Google Meet."""
    return redirect(MEET_URL, code=302)

@app.route('/health')
def health():
    """Health check endpoint."""
    return {"status": "healthy"}, 200

if __name__ == "__main__":
    # Use port 8080 as it's common for web services
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
