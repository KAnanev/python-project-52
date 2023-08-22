#!/bin/sh

# Create superuser
echo "Migrate "
make migrate

# Create superuser
echo "Create superuser"
make create_superuser

# Collect staticfiles
echo "Collect staticfiles"
make collect_static

# Start server
echo "Starting server"
make start