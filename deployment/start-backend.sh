#!/bin/bash
# Start Backend Script for cPanel
# Place this in: /home/pgtinter/tms-backend/start-backend.sh

cd /home/pgtinter/tms-backend

# Activate virtual environment
source /home/pgtinter/virtualenv/tms-backend/3.9/bin/activate

# Ensure admin credentials
python ensure_admin.py

# Start FastAPI with Uvicorn
uvicorn main:app --host 0.0.0.0 --port 8002 --reload
