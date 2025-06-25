#!/bin/bash
# test.sh — run all tests

set -e

echo "Running tests with pytest..."
PYTHONPATH=src pytest tests/

