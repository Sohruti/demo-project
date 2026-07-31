"""
Application Entry Point

This file starts the Flask application.
In development, it runs the Flask development server.
In production, Gunicorn uses this as the WSGI entry point.
"""

from app import create_app

# Create the application using the factory pattern
app = create_app()

if __name__ == "__main__":
    # Run locally — in production, Gunicorn handles this
    # Bind to 0.0.0.0 so the app is accessible from outside the container
    from app.config import Config
    app.run(host="0.0.0.0", port=Config.PORT, debug=Config.FLASK_ENV == "development")
