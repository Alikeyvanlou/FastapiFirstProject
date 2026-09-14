#!/bin/bash
set -e

echo "Running database migration ... "
alembic upgrade head

echo "Starting Application ..."
exec "$@"