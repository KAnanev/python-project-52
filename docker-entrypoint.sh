#!/bin/sh
# Create superuser
echo "Create superuser"
poetry run python manage.py create_superuser

# Collect staticfiles
echo "Collect staticfiles"
poetry run python manage.py collectstatic --no-input

# Start server
echo "Starting server"
make start