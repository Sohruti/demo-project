# Procfile tells OpenShift S2I (and Heroku) how to run the app.
# Gunicorn serves the Flask app in production.
# -w 4: use 4 worker processes (adjust based on CPU cores)
# -b 0.0.0.0:$PORT: bind to all interfaces on the configured port
web: gunicorn run:app -w 4 -b 0.0.0.0:$PORT
