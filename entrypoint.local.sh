#!/bin/bash

set -e

echo "Running database migrations..."
python manage.py migrate --noinput

echo "Starting Django development server..."

opentelemetry-instrument python manage.py runserver 0.0.0.0:8000