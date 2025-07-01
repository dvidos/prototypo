#!/bin/bash
# This script is used to run the docker services for the application.

set -e

echo "Running docker services..."
docker compose -f out/docker-compose.yml up db backend frontend

