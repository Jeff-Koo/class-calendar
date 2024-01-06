#!/bin/bash

# Apply database migrations
echo "Apply database migrations... "
python manage.py migrate
echo "DONE database migrations!"

# Start server
echo "Starting server"
python manage.py runserver 0.0.0.0:8000
