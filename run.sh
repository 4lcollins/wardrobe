#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status
set -e

# Ensure we are in the script's parent directory (repository root)
cd "$(dirname "$0")"

# Activate the virtual environment if 'uv' or '.venv' is used
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Run the Shiny application
echo "Starting Wardrobe Shiny App..."
export PYTHONPATH=.
shiny run shiny_app/app.py