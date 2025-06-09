# ----------------------------------------------------------------------------
# File: app/security.py
# Author: Vilhelm Hilding
# Project: Arxite – Hardened Web Application Architecture
# Description: Pre-request security filters and access controls.
# ----------------------------------------------------------------------------

from flask import request, abort

from . import app

# ----------------------------------------------------------------------------
# Configuration of blocked resources
# ----------------------------------------------------------------------------
blocked_paths = [
    "/.env",
    "/.git",
    "/server-status",
    "/debug",
    "/config.json",
    "/login.action",
    "/_all_dbs",
    "/telescope",
    "/info.php",
    "/about",
]

blocked_agents = [
    "curl",
    "python",
    "nmap",
    "dirbuster",
    "sqlmap",
    "http-client",
]


# ----------------------------------------------------------------------------
# Security filter middleware
# ----------------------------------------------------------------------------
@app.before_request
def security_filters():
    """
    Examine incoming requests before route handling:
    - Allow static assets and favicon without checks
    - Block known scanning User-Agent strings with 403 Forbidden
    - Block requests to sensitive or hidden paths with 404 Not Found
    """
    user_agent = request.headers.get("User-Agent", "").lower()

    if request.path.startswith("/static/") or request.path == "/favicon.ico":
        return

    if any(agent in user_agent for agent in blocked_agents):
        app.logger.warning(f"Blocked User-Agent: {user_agent}")
        abort(403)

    if (
        request.path in blocked_paths
        or request.path.startswith("/.")
        or request.path.endswith(".ico")
    ):
        app.logger.warning(f"Blocked suspicious path: {request.path}")
        abort(404)
