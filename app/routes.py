"""
Application Routes (Blueprints)

Defines all HTTP endpoints for the Product Catalog.
Uses Flask Blueprint for modular organization.
"""

import logging
from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from app.models import db, Product

# Create a Blueprint — this groups all product-related routes
# The Blueprint is registered in __init__.py
main = Blueprint("main", __name__)

# Logger for this module
logger = logging.getLogger(__name__)


# -------------------------------------------------------------------
# Home / Product List
# -------------------------------------------------------------------

@main.route("/")
def index():
    """Display all products on the home page."""
    products = Product.query.order_by(Product.created_at.desc()).all()
    return render_template("index.html", products=products)


@main.route("/products")
def products_list():
    """Redirect to home page — keeps /products URL working."""
    return redirect(url_for("main.index"))


# -------------------------------------------------------------------
# Add Product
# -------------------------------------------------------------------

@main.route("/products/new", methods=["GET", "POST"])
def product_new():
    """Show form to add a new product, or handle form submission."""
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()
        price_str = request.form.get("price", "0").strip()

        # Basic validation
        if not name:
            return render_template(
                "product_form.html",
                error="Product name is required.",
                product=None,
            )

        try:
            price = float(price_str)
        except ValueError:
            return render_template(
                "product_form.html",
                error="Price must be a valid number.",
                product=None,
            )

        if price < 0:
            return render_template(
                "product_form.html",
                error="Price cannot be negative.",
                product=None,
            )

        product = Product(name=name, description=description, price=price)
        db.session.add(product)
        db.session.commit()
        logger.info("Created product: %s (id=%d)", name, product.id)
        return redirect(url_for("main.index"))

    return render_template("product_form.html", product=None, error=None)


# -------------------------------------------------------------------
# View / Edit / Delete Single Product
# -------------------------------------------------------------------

@main.route("/products/<int:product_id>")
def product_detail(product_id):
    """Display details for a single product."""
    product = Product.query.get_or_404(product_id)
    return render_template("product_detail.html", product=product)


@main.route("/products/<int:product_id>/edit", methods=["GET", "POST"])
def product_edit(product_id):
    """Show form to edit a product, or handle form submission."""
    product = Product.query.get_or_404(product_id)

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()
        price_str = request.form.get("price", "0").strip()

        if not name:
            return render_template(
                "product_form.html",
                product=product,
                error="Product name is required.",
            )

        try:
            price = float(price_str)
        except ValueError:
            return render_template(
                "product_form.html",
                product=product,
                error="Price must be a valid number.",
            )

        if price < 0:
            return render_template(
                "product_form.html",
                product=product,
                error="Price cannot be negative.",
            )

        product.name = name
        product.description = description
        product.price = price
        db.session.commit()
        logger.info("Updated product: %s (id=%d)", name, product.id)
        return redirect(url_for("main.product_detail", product_id=product.id))

    return render_template("product_form.html", product=product, error=None)


@main.route("/products/<int:product_id>/delete", methods=["POST"])
def product_delete(product_id):
    """Delete a product and redirect to home page."""
    product = Product.query.get_or_404(product_id)
    name = product.name
    db.session.delete(product)
    db.session.commit()
    logger.info("Deleted product: %s (id=%d)", name, product_id)
    return redirect(url_for("main.index"))


# -------------------------------------------------------------------
# Health & Ready Probes (for OpenShift / Kubernetes)
# -------------------------------------------------------------------

@main.route("/health")
def health():
    """
    Liveness probe — tells the platform the app is running.
    Returns HTTP 200 with a simple JSON body.
    """
    return jsonify({"status": "healthy"}), 200


@main.route("/ready")
def ready():
    """
    Readiness probe — tells the platform the app can accept traffic.
    Checks database connectivity before returning success.
    """
    try:
        # Execute a simple query to verify database is reachable
        db.session.execute(db.text("SELECT 1"))
        return jsonify({"status": "ready", "database": "connected"}), 200
    except Exception as e:
        logger.error("Readiness check failed: %s", str(e))
        return jsonify({"status": "not ready", "database": "disconnected"}), 503
