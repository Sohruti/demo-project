"""
Application Factory

Creates and configures the Flask application.
Using the factory pattern makes testing and configuration easier.
"""

import logging
from flask import Flask
from app.config import Config
from app.models import db


def create_app(config_class=Config):
    """
    Application factory — creates and configures the Flask app.

    Args:
        config_class: Configuration class to use (default: Config)

    Returns:
        Configured Flask application instance
    """
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)

    # Configure logging
    logging.basicConfig(
        level=getattr(logging, app.config["LOG_LEVEL"]),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    # Register the main blueprint (all routes)
    from app.routes import main
    app.register_blueprint(main)

    # Create database tables if they don't exist
    # In production, consider using Flask-Migrate for schema management
    with app.app_context():
        db.create_all()
        logging.getLogger(__name__).info("Database tables created/verified")

    return app
