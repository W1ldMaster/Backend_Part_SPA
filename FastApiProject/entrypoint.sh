#!/bin/sh
set -e

echo "→ DB_PATH=${DB_PATH}"

echo "→ Применяем миграции Alembic..."
alembic upgrade head

echo "→ Запускаем uvicorn на 0.0.0.0:8000..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000