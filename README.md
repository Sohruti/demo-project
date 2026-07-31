# Product Catalog - OpenShift S2I Demo

A simple yet production-ready Flask web application for managing a product catalog. Designed to be deployed on OpenShift using Source-to-Image (S2I).

---

## Overview

This application demonstrates how to build a Flask web app that is ready for OpenShift deployment. It includes proper project structure, environment-based configuration, health/readiness probes, and database support.

---

## Features

- **Product CRUD** — Create, Read, Update, Delete products
- **Health Probe** (`/health`) — Liveness check for OpenShift/Kubernetes
- **Ready Probe** (`/ready`) — Readiness check that verifies database connectivity
- **Environment Configuration** — All settings read from environment variables
- **SQLite Fallback** — Works locally without PostgreSQL
- **Gunicorn** — Production-grade WSGI server
- **Blueprint Architecture** — Modular Flask code organization
- **Bootstrap 5 UI** — Clean, responsive web interface

---

## Folder Structure

```
demo-openshift-app/
│
├── app/
│   ├── __init__.py          # Application factory — creates and configures Flask app
│   ├── config.py            # Configuration class — reads env vars
│   ├── models.py            # SQLAlchemy models (Product)
│   ├── routes.py            # Flask Blueprints — all HTTP endpoints
│   └── templates/
│       ├── base.html            # Base HTML template (Bootstrap 5)
│       ├── index.html           # Home page — product list
│       ├── product_form.html    # Add/Edit product form
│       └── product_detail.html  # Single product view
│
├── static/                  # Static files (CSS, JS, images) — currently unused
├── requirements.txt         # Python dependencies
├── run.py                   # Application entry point
├── Procfile                 # Process type definition for S2I
├── .gitignore               # Git ignore rules
├── LICENSE                  # MIT License
└── README.md                # This file
```

---

## Local Setup

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)

### Steps

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd demo-openshift-app
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   python run.py
   ```

5. **Open in browser:**
   ```
   http://localhost:5000
   ```

The app will use SQLite locally — no database setup required.

---

## Environment Variables

| Variable       | Required | Default                  | Description                                      |
|----------------|----------|--------------------------|--------------------------------------------------|
| `DATABASE_URL` | No       | `sqlite:///products.db`  | Database connection URL (PostgreSQL in prod)      |
| `SECRET_KEY`   | No       | `dev-secret-change-me`   | Flask secret key (MUST set in production)         |
| `FLASK_ENV`    | No       | `production`             | Flask environment (`development` or `production`) |
| `PORT`         | No       | `5000`                   | Port the app listens on                          |
| `LOG_LEVEL`    | No       | `INFO`                   | Logging level (`DEBUG`, `INFO`, `WARNING`, etc.)  |

---

## API Endpoints

| Method | Endpoint                | Description                          |
|--------|-------------------------|--------------------------------------|
| GET    | `/`                     | Home page — displays all products    |
| GET    | `/products`             | Redirects to home page               |
| GET    | `/products/new`         | Form to add a new product            |
| POST   | `/products/new`         | Create a new product                 |
| GET    | `/products/<id>`        | View a single product                |
| GET    | `/products/<id>/edit`   | Form to edit a product               |
| POST   | `/products/<id>/edit`   | Update an existing product           |
| POST   | `/products/<id>/delete` | Delete a product                     |
| GET    | `/health`               | Liveness probe — returns `200 OK`    |
| GET    | `/ready`                | Readiness probe — checks DB health   |

---

## Deploying to OpenShift (S2I)

This app is designed for OpenShift Source-to-Image deployment:

1. **Push code to a Git repository**
2. **Create a new OpenShift project:**
   ```bash
   oc new-project demo-catalog
   ```
3. **Create the app from the Git URL:**
   ```bash
   oc new-app python:3.11~<your-git-url> --name=product-catalog
   ```
4. **Set environment variables:**
   ```bash
   oc set env dc/product-catalog SECRET_KEY=$(openssl rand -hex 32)
   oc set env dc/product-catalog DATABASE_URL=postgresql://user:pass@host:5432/dbname
   ```
5. **Expose the route:**
   ```bash
   oc expose svc/product-catalog
   ```

The OpenShift Python builder image will:
- Detect the `Procfile`
- Install `requirements.txt`
- Start Gunicorn using the `Procfile` command

---

## Database

### Product Model

| Field        | Type      | Constraints            |
|--------------|-----------|------------------------|
| `id`         | Integer   | Primary key, auto-gen  |
| `name`       | String    | Required, max 100 chars|
| `description`| Text      | Optional               |
| `price`      | Float     | Required               |
| `created_at` | DateTime  | Auto-set to UTC now    |

### SQLite (Local Development)
- Database file: `instance/products.db`
- Tables are created automatically on first run

### PostgreSQL (Production)
- Set `DATABASE_URL` environment variable
- Format: `postgresql://user:password@host:5432/dbname`
- Consider using Flask-Migrate for schema migrations

---

## Future Improvements

- [ ] Add user authentication (login/signup)
- [ ] Implement product categories
- [ ] Add image upload for products
- [ ] Pagination for product list
- [ ] Search functionality
- [ ] REST API with JSON responses
- [ ] Flask-Migrate for database migrations
- [ ] Unit and integration tests
- [ ] Dockerfile (for custom builds beyond S2I)
- [ ] CI/CD pipeline configuration
- [ ] Rate limiting and request validation
- [ ] Structured JSON logging

---

## License

MIT License — see [LICENSE](LICENSE) for details.
