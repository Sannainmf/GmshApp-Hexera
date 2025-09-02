# 🚀 GMSH Backend API Documentation

## 📋 Overview

This API provides a complete pipeline for GMSH mesh generation:
1. **User Input** → LLM → **Prompt Generation**
2. **Prompt** → LLM → **GMSH Code**
3. **Code** → GMSH Engine → **Mesh Files**

## 🌐 Base URL

```
http://localhost:8000
```

## 📡 API Endpoints

### 🔍 **System & Health**

#### GET `/`
- **Description**: Root endpoint with API information
- **Response**: Basic API message
- **Example Response**:
```json
{
  "message": "GMSH Script Generator API"
}
```

#### GET `/health`
- **Description**: System health check
- **Response**: System status and model loading state
- **Example Response**:
```json
{
  "status": "healthy",
  "model_loaded": true
}
```

### 🤖 **Model Management**

#### POST `/load-model`
- **Description**: Load the ML model into memory
- **Request Body**: None required
- **Response**: Model loading status
- **Example Response**:
```json
{
  "message": "Model loaded successfully"
}
```

#### GET `/model-info`
- **Description**: Get information about the loaded model
- **Response**: Model details and status
- **Example Response**:
```json
{
  "status": "Model loaded",
  "device": "cuda",
  "model_path": "./model",
  "model_type": "AutoModelForCausalLM",
  "tokenizer_type": "AutoTokenizer"
}
```

### 📝 **Script Generation**

#### POST `/generate`
- **Description**: Generate GMSH script from text prompt (LLM only)
- **Request Body**:
```json
{
  "prompt": "Generate a GMSH script for a 2D rectangular mesh with a circular hole",
  "max_tokens": 2000,
  "temperature": 0.7
}
```
- **Response**: Generated GMSH script
- **Example Response**:
```json
{
  "script": "// Generated GMSH script content...",
  "status": "success",
  "message": "GMSH script generated successfully"
}
```

### 🚀 **Complete Pipeline**

#### POST `/execute-gmsh`
- **Description**: **Complete pipeline** - Generate script AND execute with GMSH
- **Request Body**:
```json
{
  "prompt": "Create a 2D mesh with a hole",
  "max_tokens": 2000,
  "temperature": 0.7,
  "output_filename": "my_mesh"
}
```
- **Response**: Complete execution results
- **Example Response**:
```json
{
  "status": "success",
  "message": "GMSH script executed successfully",
  "generated_script": "// Generated GMSH script...",
  "output_files": {
    ".geo": "./output/my_mesh.geo",
    ".msh": "./output/my_mesh.msh"
  },
  "gmsh_output": "GMSH execution log..."
}
```

### 🔧 **GMSH Execution**

#### POST `/execute-existing-script`
- **Description**: Execute an existing GMSH script
- **Request Body**: Script content as string
- **Query Parameters**: `output_filename` (optional)
- **Response**: Execution results

### 📁 **File Management**

#### GET `/output-files`
- **Description**: List all generated output files
- **Response**: List of files with metadata
- **Example Response**:
```json
{
  "files": [
    {
      "filename": "generated_mesh.geo",
      "size": 1024,
      "created": 1640995200.0
    },
    {
      "filename": "generated_mesh.msh",
      "size": 2048,
      "created": 1640995200.0
    }
  ]
}
```

#### GET `/download/{filename}`
- **Description**: Download a generated file
- **Path Parameters**: `filename` - Name of file to download
- **Response**: File download

#### DELETE `/cleanup`
- **Description**: Clean up all output files
- **Response**: Cleanup confirmation
- **Example Response**:
```json
{
  "message": "Output files cleaned up successfully"
}
```

## 🔄 **Complete Pipeline Usage**

### **Step-by-Step Process:**

1. **Load Model**:
```bash
curl -X POST http://localhost:8000/load-model
```

2. **Execute Complete Pipeline**:
```bash
curl -X POST "http://localhost:8000/execute-gmsh" \
     -H "Content-Type: application/json" \
     -d '{
       "prompt": "Generate a GMSH script for a 2D rectangular mesh with a circular hole",
       "max_tokens": 2000,
       "temperature": 0.7,
       "output_filename": "rectangular_mesh"
     }'
```

3. **Download Generated Files**:
```bash
# Download .geo file
curl -O http://localhost:8000/download/rectangular_mesh.geo

# Download .msh file
curl -O http://localhost:8000/download/rectangular_mesh.msh
```

## 🐍 **Python Example**

```python
import requests

# Base URL
base_url = "http://localhost:8000"

# 1. Load model
response = requests.post(f"{base_url}/load-model")
print("Model loaded:", response.json())

# 2. Execute complete pipeline
data = {
    "prompt": "Create a 2D mesh with a hole",
    "max_tokens": 2000,
    "temperature": 0.7,
    "output_filename": "test_mesh"
}

response = requests.post(f"{base_url}/execute-gmsh", json=data)
result = response.json()

print("Generated script:", result["generated_script"])
print("Output files:", result["output_files"])

# 3. Download mesh file
mesh_file = requests.get(f"{base_url}/download/test_mesh.msh")
with open("test_mesh.msh", "wb") as f:
    f.write(mesh_file.content)
```

## ⚠️ **Error Handling**

### **Common Error Codes:**

- **400**: Bad Request - Invalid input parameters
- **404**: Not Found - File or resource not found
- **500**: Internal Server Error - Server-side error
- **503**: Service Unavailable - Model not loaded

### **Error Response Format**:
```json
{
  "detail": "Error message description"
}
```

## 🔧 **Requirements**

- **GMSH**: Must be installed and available in PATH
- **Python Dependencies**: See `requirements.txt`
- **Model Files**: Must be present in `./model` directory

## 📝 **Notes**

- **Model Loading**: Model must be loaded before generating scripts
- **File Cleanup**: Use cleanup endpoint to manage disk space
- **Timeout**: GMSH execution has 60-second timeout
- **Output Directory**: Generated files are stored in `./output/`
