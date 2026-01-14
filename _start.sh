#!/usr/bin/env bash
# Exit on error
set -o errexit

# Run migrations automatically
python manage.py migrate

# Start Gunicorn using the PORT assigned by Render
gunicorn Purchaseproject.wsgi:application --bind 0.0.0.0:${PORT:-8000}