#!/usr/bin/env bash
set -e

# Start the backend API in the background.
python api.py &
API_PID=$!

cleanup() {
    kill "$API_PID" 2>/dev/null || true
}
trap cleanup EXIT INT TERM

echo "Backend API running at http://127.0.0.1:8000"
echo "API docs available at http://127.0.0.1:8000/docs"
echo "Starting Tkinter frontend..."

python app.py
