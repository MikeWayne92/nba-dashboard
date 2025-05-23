#!/bin/bash

# Ensure the script fails on any error
set -e

echo "Current directory: $(pwd)"
echo "Listing current directory contents:"
ls -la

# Create necessary directories
echo "Setting up deployment environment..."
mkdir -p ./deploy/data

# Verify data directory exists
echo "Checking data directory:"
if [ -d "data" ]; then
    echo "Data directory exists with contents:"
    ls -la data/
else
    echo "WARNING: Local data directory not found!"
fi

# Copy necessary files
echo "Copying application files..."
cp nba_dashboard.py ./deploy/
cp requirements.txt ./deploy/

# Copy data directory
echo "Copying data files..."
if [ -f "data/PlayerIndex_nba_stats.csv" ]; then
    cp -r data ./deploy/
    echo "Copied data directory to deploy"
elif [ -f "PlayerIndex_nba_stats.csv" ]; then
    cp PlayerIndex_nba_stats.csv ./deploy/data/
    echo "Copied CSV file to deploy/data"
else
    echo "ERROR: Could not find PlayerIndex_nba_stats.csv!"
    exit 1
fi

# Verify deployment structure
echo "Verifying deployment structure:"
echo "Deploy directory contents:"
ls -la ./deploy/
echo "Deploy data directory contents:"
ls -la ./deploy/data/

# Print success message
echo "Build completed successfully!"

# Additional debugging information
echo "Final directory structure:"
find . -type f -name "PlayerIndex_nba_stats.csv" 