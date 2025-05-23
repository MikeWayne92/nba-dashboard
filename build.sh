#!/bin/bash

# Ensure the script fails on any error
set -e

echo "Current directory: $(pwd)"
echo "Listing current directory contents:"
ls -la

# Create necessary directories
echo "Setting up deployment environment..."
mkdir -p ./deploy

# Copy necessary files
echo "Copying application files..."
cp nba_dashboard.py ./deploy/
cp PlayerIndex_nba_stats.csv ./deploy/
cp requirements.txt ./deploy/

# Verify files were copied
echo "Verifying copied files..."
ls -la ./deploy/

# Print success message
echo "Build completed successfully!"

# Additional debugging information
echo "Final directory structure:"
find . -type f -name "PlayerIndex_nba_stats.csv" 