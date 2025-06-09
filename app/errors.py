# ----------------------------------------------------------------------------
# File: app/errors.py
# Author: Vilhelm Hilding
# Project: Arxite – Hardened Web Application Architecture
# Description: Custom HTTP error handlers.
# ----------------------------------------------------------------------------

from flask import render_template
from . import app


# ----------------------------------------------------------------------------
# Forbidden (403) handler
# ----------------------------------------------------------------------------
@app.errorhandler(403)
def forbidden(e):
    """
    Returns a 403 Forbidden response rendered with the error template.
    """
    return render_template("error.html", code=403, message="Access denied."), 403


# ----------------------------------------------------------------------------
# Not Found (404) handler
# ----------------------------------------------------------------------------
@app.errorhandler(404)
def page_not_found(e):
    """
    Returns a 404 Not Found response rendered with the error template.
    """
    return render_template("error.html", code=404, message="Page not found."), 404


# ----------------------------------------------------------------------------
# Internal Server Error (500) handler
# ----------------------------------------------------------------------------
@app.errorhandler(500)
def server_error(e):
    """
    Returns a 500 Internal Server Error response rendered with the error template.
    """
    return render_template("error.html", code=500, message="Something went wrong."), 500


# ----------------------------------------------------------------------------
# Rate Limit Exceeded (429) handler
# ----------------------------------------------------------------------------
@app.errorhandler(429)
def rate_limit_handler(e):
    """
    Returns a 429 Too Many Requests response rendered with the error template.
    """
    return render_template("error.html", code=429, message="Too many requests."), 429
