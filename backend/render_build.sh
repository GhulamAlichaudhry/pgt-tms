#!/usr/bin/env bash
# Render.com Build Script for Backend

set -o errexit

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Build complete!"
