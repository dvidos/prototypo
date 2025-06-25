#!/bin/bash
# run.sh — quick runner for prototypo

set -e

INPUT_FILE=${1:-examples/hello-world/hello.dsl}

echo "Running prototypo on $INPUT_FILE..."

PYTHONPATH=src python src/cli/main.py "$INPUT_FILE"
