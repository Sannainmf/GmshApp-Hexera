# GMSH Script Generator Backend

A simple FastAPI backend for generating GMSH scripts using a fine-tuned language model.

## Features

- RESTful API for GMSH script generation
- Model loading and management
- Health checks and monitoring
- Simple configuration management

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Copy the environment configuration:
```bash
cp env_example.txt .env
```

3. Update the `.env` file with your specific configuration.

## Usage

### Start the server:
```bash
python app.py
```

The API will be available at `http://localhost:8000`

### API Endpoints

- `GET /` - Root endpoint
- `GET /health` - Health check
- `POST /load-model` - Load the ML model
- `POST /generate` - Generate GMSH script

### Generate a GMSH script:
```bash
curl -X POST "http://localhost:8000/generate" \
     -H "Content-Type: application/json" \
     -d '{
       "prompt": "Generate a GMSH script for a 2D rectangular mesh with a circular hole",
       "max_tokens": 2000,
       "temperature": 0.7
     }'
```

## File Structure

- `app.py` - Main FastAPI application
- `gmsh_backend.py` - Backend service for model management
- `config.py` - Configuration management
- `gmsh.py` - Original GMSH generation script
- `requirements.txt` - Python dependencies

## Notes

- The model must be loaded before generating scripts
- Ensure your model files are in the `./model` directory
- The backend automatically detects GPU/CPU availability
