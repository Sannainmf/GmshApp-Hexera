#!/bin/bash

# Quick start script for development
echo "🚀 Starting Mesh Generator in development mode..."

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "❌ Python is not installed. Please install Python 3.9+ first."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first."
    exit 1
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Install Node.js dependencies
echo "📦 Installing Node.js dependencies..."
cd frontend
npm install
cd ..

# Create output directory
mkdir -p output

# Start backend in background
echo "🔧 Starting backend server..."
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

# Wait for backend to start
sleep 5

# Start frontend
echo "🎨 Starting frontend development server..."
cd frontend
npm start &
FRONTEND_PID=$!

echo "✅ Application started!"
echo "🌐 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8000"
echo "📊 API docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop both servers"

# Wait for user to stop
wait $BACKEND_PID $FRONTEND_PID
