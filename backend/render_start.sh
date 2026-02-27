#!/usr/bin/env bash
# Render.com Start Script for Backend

set -o errexit

echo "Initializing database..."
python init_database.py

echo "Creating admin user..."
python ensure_admin.py

echo "Starting FastAPI server..."
uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
