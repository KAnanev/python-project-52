#!/bin/sh
# Apply database migration
echo "Apply database migrations"
poetry run python manage.py migrate

# Create superuser
#echo "Create superuser"
#poetry run python manage.py createsuperuser \
#--username $DJANGO_SUPERUSER \
#--email $DJANGO_SUPERUSER_EMAIL \
#--no-input || true

# Collect staticfiles
echo "Collect staticfiles"
poetry run python manage.py collectstatic --no-input

# Start server
echo "Starting server"
make start