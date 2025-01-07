#!/bin/bash

# Exit script on any error
set -o errexit  

echo "Starting Build Script..."

# Print the current directory
echo "Current directory:"
pwd

# List the files in the directory
echo "Files in current directory:"
ls -l

# Go back one level to access requirements.txt
cd ..

# Verify the requirements file
echo "Checking requirements.txt:"
ls -l requirements.txt

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Move back to the project directory
cd docQA

# Print current directory
echo "Moved to project directory:"
pwd

# Apply migrations
echo "Running database migrations..."
python manage.py makemigrations
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Final message
echo "Build script completed successfully!"
