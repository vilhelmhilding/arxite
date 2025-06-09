# ----------------------------------------------------------------------------
# File: app/routes.py
# Author: Vilhelm Hilding
# Project: Arxite – Hardened Web Application Architecture
# Description: Core application routes with rate limiting.
# ----------------------------------------------------------------------------

from flask import session, redirect, url_for, render_template

from . import app, limiter


# ----------------------------------------------------------------------------
# Home Route
# ----------------------------------------------------------------------------
@app.route("/")
@limiter.limit("10 per minute")
def home():
    """
    Renders the home page using the HTML template.

    If a user is authenticated, passes the GitHub user data to the template
    so the UI can show their username and a logout button.
    If not authenticated, the UI will show a GitHub login button.

    Returns:
        Rendered HTML page with dynamic content based on authentication state.
    """
    user = session.get("user")
    return render_template("index.html", user=user)


# ----------------------------------------------------------------------------
# Logout Route
# ----------------------------------------------------------------------------
@app.route("/logout")
def logout():
    """
    Clears the user session to log out the user and redirects back to the home page.
    """
    session.clear()
    app.logger.info("Session cleared and user logged out")
    return redirect(url_for("home"))
