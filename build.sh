#!/bin/bash

# Ensure the script fails on any error
set -e

# Create necessary directories
echo "Setting up deployment environment..."
mkdir -p ./deploy

# Copy necessary files
echo "Copying application files..."
cp nba_dashboard.py ./deploy/
cp PlayerIndex_nba_stats.csv ./deploy/
cp requirements.txt ./deploy/

# Print success message
echo "Build completed successfully!" 