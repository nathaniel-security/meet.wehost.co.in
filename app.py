import os
import sys
import time
from flask import Flask, request
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

app = Flask(__name__)

# Get Google Meet URL from environment variable
MEET_URL = os.environ.get("MEET_URL")

# If it's empty or not set, use a fallback and print a warning
if not MEET_URL:
    MEET_URL = "https://meet.google.com/lookup/default"
    print("WARNING: MEET_URL environment variable is not set! Using fallback.", file=sys.stderr)
else:
    # Ensure the URL starts with http:// or https://
    if not MEET_URL.startswith(("http://", "https://")):
        MEET_URL = f"https://{MEET_URL}"
    print(f"INFO: Redirecting to {MEET_URL}", file=sys.stdout)

_REDIRECT_HTML = """\
<!DOCTYPE html>
<html>
<head>
<meta http-equiv="refresh" content="0;url={url}">
<script>window.location.replace("{url}");</script>
</head>
<body></body>
</html>
"""

@app.route('/')
def index():
    t_start = time.monotonic()
    source_ip = request.remote_addr
    cf_connecting_ip = request.headers.get("CF-Connecting-IP", "-")
    x_forwarded_for = request.headers.get("X-Forwarded-For", "-")
    html = _REDIRECT_HTML.format(url=MEET_URL)
    latency_ms = (time.monotonic() - t_start) * 1000
    print(
        f"INFO: redirect source_ip={source_ip} cf_connecting_ip={cf_connecting_ip} x_forwarded_for={x_forwarded_for} latency_ms={latency_ms:.2f}",
        file=sys.stdout,
        flush=True,
    )
    return html, 200, {"Content-Type": "text/html"}

@app.route('/health')
def health():
    """Health check endpoint."""
    t_start = time.monotonic()
    source_ip = request.remote_addr
    cf_connecting_ip = request.headers.get("CF-Connecting-IP", "-")
    x_forwarded_for = request.headers.get("X-Forwarded-For", "-")
    html = _REDIRECT_HTML.format(url=MEET_URL)
    latency_ms = (time.monotonic() - t_start) * 1000
    print(
        f"INFO: redirect source_ip={source_ip} cf_connecting_ip={cf_connecting_ip} x_forwarded_for={x_forwarded_for} latency_ms={latency_ms:.2f}",
        file=sys.stdout,
        flush=True,
    )
    return {"status": "healthy"}, 200

if __name__ == "__main__":
    # Use port 8080 as it's common for web services
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
