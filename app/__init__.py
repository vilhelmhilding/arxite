# ----------------------------------------------------------------------------
# File: app/__init__.py
# Author: Vilhelm Hilding
# Project: Arxite – Hardened Web Application Architecture
# Description: Flask app factory and core service configuration.
# ----------------------------------------------------------------------------

import os
import logging
from pathlib import Path
from datetime import timedelta

from dotenv import load_dotenv
from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from authlib.integrations.flask_client import OAuth

# ----------------------------------------------------------------------------
# Load environment variables
# ----------------------------------------------------------------------------
env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=env_path)

# ----------------------------------------------------------------------------
# Flask application setup
# ----------------------------------------------------------------------------
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")
assert app.secret_key, "SECRET_KEY must be set in environment variables"

app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    PERMANENT_SESSION_LIFETIME=timedelta(days=1),
)

# ----------------------------------------------------------------------------
# Logging configuration
# ----------------------------------------------------------------------------
log_level = os.environ.get("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=getattr(logging, log_level, logging.INFO),
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

# ----------------------------------------------------------------------------
# Rate limiting using Redis as storage backend
# ----------------------------------------------------------------------------
redis_password = os.environ.get("REDIS_PASSWORD")
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    storage_uri=f"redis://:{redis_password}@redis:6379",
)

# ----------------------------------------------------------------------------
# OAuth2 client configuration for GitHub
# ----------------------------------------------------------------------------
oauth = OAuth(app)
github = oauth.register(
    name="github",
    client_id=os.environ.get("GITHUB_CLIENT_ID"),
    client_secret=os.environ.get("GITHUB_CLIENT_SECRET"),
    access_token_url="https://github.com/login/oauth/access_token",
    authorize_url="https://github.com/login/oauth/authorize",
    api_base_url="https://api.github.com/",
    client_kwargs={"scope": "read:user"},
)

# ----------------------------------------------------------------------------
# Import application modules (routes, authentication, security, error handlers)
# ----------------------------------------------------------------------------
from . import routes
from . import auth
from . import security
from . import errors
