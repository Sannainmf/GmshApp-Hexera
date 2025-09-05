#!/bin/bash

# Mesh Generator Deployment Script
echo "🚀 Starting Mesh Generator Deployment..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create output directory if it doesn't exist
mkdir -p output

# Build and start the application
echo "🔨 Building and starting the application..."
docker-compose up --build -d

# Wait for the application to start
echo "⏳ Waiting for the application to start..."
sleep 10

# Check if the application is running
if curl -f http://localhost:8000/ > /dev/null 2>&1; then
    echo "✅ Application is running successfully!"
    echo "🌐 Open your browser and go to: http://localhost:8000"
    echo "📊 API documentation available at: http://localhost:8000/docs"
else
    echo "❌ Application failed to start. Check the logs with: docker-compose logs"
    exit 1
fi

echo "🎉 Deployment complete!"
