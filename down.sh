#!/bin/bash
# This script is used to terminate the docker services and wipe the database.

set -e

echo "Terminating docker services and wiping data..."
docker compose -f out/docker-compose.yml down --volumes

