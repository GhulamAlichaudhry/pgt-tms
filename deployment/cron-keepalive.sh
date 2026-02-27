#!/bin/bash
# Cron Job to Keep Backend Running
# Add to cPanel Cron Jobs: */5 * * * * /home/pgtinter/tms-backend/cron-keepalive.sh

# Check if backend is running
if ! pgrep -f "uvicorn main:app" > /dev/null; then
    cd /home/pgtinter/tms-backend
    source /home/pgtinter/virtualenv/tms-backend/3.9/bin/activate
    nohup uvicorn main:app --host 0.0.0.0 --port 8002 > /dev/null 2>&1 &
fi
