#!/bin/sh
set -e

echo "Waiting for postgres..."

until psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -c "SELECT 1;" > /dev/null 2>&1; do
  sleep 1
done

echo "Postgres is up!"

echo "Running migrations..."
alembic upgrade head

echo "Starting uvicorn..."
exec "$@"
