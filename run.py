"""Entry point for the Sicredi management system.

This script imports the Flask application instance (``app``) defined in
``app/routes/principal/principal.py`` and starts the development server so that
executing ``python run.py`` will launch the web application.
"""

from app.routes.principal.principal import app


if __name__ == "__main__":
    # Run the Flask development server
    # Set host to 0.0.0.0 so the app is accessible on the local network if needed
    app.run(host="0.0.0.0", port=5000, debug=True)
