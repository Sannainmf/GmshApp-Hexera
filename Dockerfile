# Multi-stage build for the mesh generation application
FROM node:18-alpine AS frontend-build

# Build frontend
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Python backend stage
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    gmsh \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ ./backend/
COPY gmsh.py ./
COPY model/ ./model/

# Create output directory
RUN mkdir -p output

# Copy built frontend
COPY --from=frontend-build /app/frontend/build ./frontend/build

# Expose port
EXPOSE 8000

# Set environment variables
ENV PYTHONPATH=/app
ENV MODEL_PATH=/app/model

# Start the application
CMD ["python", "-m", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
