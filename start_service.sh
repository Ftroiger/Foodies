#!/bin/bash

# Foodies API - Startup Script

HOST="${HOST:-0.0.0.0}"
PORT="${PORT:-8000}"
WORKERS="${WORKERS:-1}"
RELOAD="${RELOAD:-false}"

if [ "$RELOAD" = "true" ]; then
    echo "Starting Foodies API in development mode (reload enabled)..."
    uvicorn app.main:app --host "$HOST" --port "$PORT" --reload
else
    echo "Starting Foodies API in production mode..."
    uvicorn app.main:app --host "$HOST" --port "$PORT" --workers "$WORKERS"
fi