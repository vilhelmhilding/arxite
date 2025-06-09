# ----------------------------------------------------------------------------
# File: app/auth.py
# Author: Vilhelm Hilding
# Project: Arxite – Hardened Web Application Architecture
# Description: GitHub OAuth authentication routes.
# ----------------------------------------------------------------------------

import os
from flask import redirect, url_for, session, abort

from . import app, github


# ----------------------------------------------------------------------------
# OAuth Login Endpoint
# ----------------------------------------------------------------------------
@app.route("/auth")
def auth():
    """
    Initiates the OAuth2 login process by redirecting the user to GitHub's authorize URL.
    """
    app.logger.info("Starting OAuth login process")

    redirect_uri = os.environ.get("REDIRECT_URI")
    assert redirect_uri, "REDIRECT_URI must be set in the .env file"

    return github.authorize_redirect(redirect_uri)


# ----------------------------------------------------------------------------
# OAuth Callback Endpoint
# ----------------------------------------------------------------------------
@app.route("/auth/callback")
def auth_callback():
    """
    Handles the OAuth2 callback from GitHub, exchanging the authorization code for an access token,
    fetching the authenticated user's profile, storing it in session, and redirecting to home.
    On failure, logs the error and aborts with a 403 Forbidden status.
    """
    try:
        token = github.authorize_access_token()
        user_data = github.get("user").json()
        session["user"] = {"login": user_data["login"]}
        app.logger.info(f"Logged in via GitHub: {user_data['login']}")
        return redirect(url_for("home"))

    except Exception as e:
        app.logger.error(f"OAuth error: {e}")
        abort(403)
