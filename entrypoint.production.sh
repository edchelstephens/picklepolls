#!/bin/bash

set -e

echo "Running database migrations..."
python manage.py migrate --no-input

echo "Collecting static files..."
python manage.py collectstatic --no-input

echo "Starting Gunicorn server..."
exec gunicorn --bind 0.0.0.0:8000 --access-logfile - --workers 1 picklepolls.wsgi:application