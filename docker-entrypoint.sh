#!/bin/sh
# Apply database migration
echo "Apply database migrations"
poetry run python manage.py migrate

# Create superuser
echo "Create superuser"
poetry run python manage.py create_superuser

# Collect staticfiles
echo "Collect staticfiles"
poetry run python manage.py collectstatic --no-input

# Start server
echo "Starting server"
make start