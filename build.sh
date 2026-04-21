#!/bin/bash
# Script to run on Render before starting the app

set -o errexit

echo "Running migrations..."
python pharmacy/manage.py migrate

echo "Collecting static files..."
python pharmacy/manage.py collectstatic --noinput

echo "Build completed successfully!"
