#!/bin/bash
set -e

# Use PORT environment variable from Railway, or default to 8000
export PORT=${PORT:-8000}

echo "Starting uvicorn on port $PORT"

# Start the FastAPI application
exec uvicorn app.main:app --host 0.0.0.0 --port $PORT