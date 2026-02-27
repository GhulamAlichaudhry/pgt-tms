"""
Passenger WSGI Configuration for cPanel Deployment
PGT International TMS
"""

import sys
import os

# Add application directory to Python path
INTERP = os.path.join(os.environ['HOME'], 'virtualenv', 'tms-backend', '3.9', 'bin', 'python')
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

sys.path.insert(0, os.path.dirname(__file__))

# Load environment variables from .env.production
from dotenv import load_dotenv
load_dotenv('.env.production')

# Import FastAPI app
from main import app as application

# Passenger expects 'application' variable
# This will be the ASGI application that Passenger will run
