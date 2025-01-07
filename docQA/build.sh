#!/bin/bash

# Exit script on error
set -o errexit  

echo "Starting Build Script..."

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r ../requirements.txt  # Move one level up to access requirements.txt

# Apply migrations
echo "Running database migrations..."
python manage.py makemigrations
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Final message
echo "Build script completed successfully!"
