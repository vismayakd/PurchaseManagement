#!/usr/bin/env bash
# Exit on error
set -o errexit

# Run migrations
python manage.py migrate

# Create a superuser automatically (only if variables are set)
if [ "$DJANGO_SUPERUSER_USERNAME" ]; then
    python manage.py createsuperuser \
        --no-input \
        --username $DJANGO_SUPERUSER_USERNAME \
        --email $DJANGO_SUPERUSER_EMAIL || true
fi

# Start Gunicorn
gunicorn Purchaseproject.wsgi:application --bind 0.0.0.0:${PORT:-8000}