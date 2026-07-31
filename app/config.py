"""
Application Configuration

Reads all settings from environment variables.
Falls back to sensible defaults for local development.
Never hardcode credentials here.
"""

import os


class Config:
    """Base configuration class."""

    # Secret key for session signing — MUST be set in production
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-me-in-production")

    # Database URL — defaults to SQLite for local development
    # In production (OpenShift), this will be a PostgreSQL URL like:
    # postgresql://user:password@host:5432/dbname
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "sqlite:///products.db"
    )

    # Disable modification tracking to save resources
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Application port — OpenShift injects this via PORT env var
    PORT = int(os.environ.get("PORT", 5000))

    # Flask environment
    FLASK_ENV = os.environ.get("FLASK_ENV", "production")

    # Logging level
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
