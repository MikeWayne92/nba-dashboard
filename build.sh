#!/bin/bash

# Ensure the script fails on any error
set -e

echo "Current directory: $(pwd)"
echo "Listing current directory contents:"
ls -la

# Create necessary directories
echo "Setting up deployment environment..."
mkdir -p ./deploy

# Verify CSV file exists and show its size
echo "Checking CSV file:"
if [ -f "PlayerIndex_nba_stats.csv" ]; then
    echo "CSV file exists with size:"
    ls -lh PlayerIndex_nba_stats.csv
    echo "First few lines of CSV:"
    head -n 5 PlayerIndex_nba_stats.csv
else
    echo "ERROR: PlayerIndex_nba_stats.csv not found!"
    exit 1
fi

# Copy necessary files
echo "Copying application files..."
cp nba_dashboard.py ./deploy/
cp PlayerIndex_nba_stats.csv ./deploy/
cp requirements.txt ./deploy/

# Verify files were copied
echo "Verifying copied files..."
ls -la ./deploy/

# Verify CSV file in deploy directory
echo "Verifying CSV file in deploy directory:"
if [ -f "./deploy/PlayerIndex_nba_stats.csv" ]; then
    echo "CSV file successfully copied with size:"
    ls -lh ./deploy/PlayerIndex_nba_stats.csv
    echo "First few lines of copied CSV:"
    head -n 5 ./deploy/PlayerIndex_nba_stats.csv
else
    echo "ERROR: CSV file not copied to deploy directory!"
    exit 1
fi

# Print success message
echo "Build completed successfully!"

# Additional debugging information
echo "Final directory structure:"
find . -type f -name "PlayerIndex_nba_stats.csv" 