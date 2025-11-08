#!/bin/bash

# LeetCode Blind 75 IDE - Quick Start Script

echo "🚀 Starting LeetCode Blind 75 IDE..."
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed!"
    echo "Please install Docker Desktop from: https://www.docker.com/products/docker-desktop"
    exit 1
fi

# Check if Docker Compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed!"
    echo "Please install Docker Compose"
    exit 1
fi

# Start the application
echo "📦 Building and starting Docker container..."
docker-compose up --build

# Note: Press Ctrl+C to stop the application

