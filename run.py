# ----------------------------------------------------------------------------
# File: run.py
# Author: Vilhelm Hilding
# Project: Arxite – Hardened Web Application Architecture
# Description: WSGI entry point using Waitress for production deployment.
# ----------------------------------------------------------------------------

from waitress import serve
from app import app

# ----------------------------------------------------------------------------
# Application Entry Point
# ----------------------------------------------------------------------------
if __name__ == "__main__":
    # Launch Waitress WSGI server
    # - host: Bind to all interfaces (0.0.0.0) to allow connections from Docker and Cloudflared
    # - port: Must align with Docker Compose, Flask app, and Cloudflare Tunnel settings
    serve(app, host="0.0.0.0", port=51821)
