#!/bin/bash
# test.sh — run all tests

set -e

echo "Running docker services..."
docker compose -f out/docker-compose.yml up backend
