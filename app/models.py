"""
Database Models

Defines the Product model using SQLAlchemy.
Each product has a name, description, price, and timestamp.
"""

from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy

# SQLAlchemy database instance — initialized in __init__.py
db = SQLAlchemy()


class Product(db.Model):
    """Product catalog item."""

    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    created_at = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )

    def to_dict(self):
        """Convert product to dictionary for JSON responses."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "created_at": self.created_at.isoformat(),
        }

    def __repr__(self):
        return f"<Product {self.name}>"
