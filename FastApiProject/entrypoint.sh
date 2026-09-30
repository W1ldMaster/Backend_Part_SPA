#!/bin/sh
set -e

if [ "$#" -gt 0 ]; then
    exec "$@"
fi

attempt=0
max_attempts=10
until alembic upgrade head; do
  attempt=$((attempt + 1))
  if [ "$attempt" -ge "$max_attempts" ]; then
    echo "Alembic failed after $max_attempts attempts, exiting"
    exit 1
  fi
  echo "Alembic failed (attempt $attempt/$max_attempts), retrying in 2s..."
  sleep 2
done

exec uvicorn app.main:app --host 0.0.0.0 --port 8000