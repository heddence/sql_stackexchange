#!/bin/bash
set -e

source .env

# Build the docker image
echo "Building the docker image..."
docker compose build

# Start the database service
echo "Starting the database service..."
docker compose up -d db

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to be ready..."
until docker compose exec db pg_isready -U $DB_USER -d $DB_NAME; do
  sleep 2
done
echo "PostgreSQL is ready."

# Check if the database is empty
DB_CHECK=$(docker compose exec db psql -U $DB_USER -d $DB_NAME -c "\dt" 2>&1 | grep "Did not find any relations." || true)

echo "DB_CHECK: '$DB_CHECK'"

if [ -n "$DB_CHECK" ]; then
  echo "Database is empty. Restoring from backup..."
  docker compose exec db pg_restore --no-owner --no-privileges -U $DB_USER -d $DB_NAME /data/superuser.backup
  echo "Database restoration completed."
else
  echo "Database already contains data. Skipping restoration."
fi

# Restart database service
docker compose restart db

# Start the application service
echo "Starting the application service..."
docker compose up -d app

echo "All services are up and running."
