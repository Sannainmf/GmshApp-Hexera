# 🚀 GMSH Backend Setup Guide

## 📋 Prerequisites

- Python 3.8+ installed
- pip package manager
- Git (for cloning the repository)

## 🛠️ Installation Steps

### 1. Clone the Repository
```bash
git clone <repository-url>
cd gmsh-backend
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up Environment
```bash
# Copy the environment template
cp env_example.txt .env

# Edit .env file with your settings (optional)
# The defaults should work for most cases
```

### 4. Verify Model Files
Make sure you have the model files in the `./model` directory:
```
model/
├── config.json
├── generation_config.json
├── model-00001-of-00004.safetensors
├── model-00002-of-00004.safetensors
├── model-00003-of-00004.safetensors
├── model-00004-of-00004.safetensors
├── model.safetensors.index.json
├── special_tokens_map.json
├── tokenizer_config.json
├── tokenizer.json
├── vocab.json
└── chat_template.jinja
```

## 🚀 Running the Backend

### Start the Server
```bash
python app.py
```

The server will start on `http://localhost:8000`

### Verify It's Working
Open your browser and go to:
- `http://localhost:8000` - Should show API message
- `http://localhost:8000/health` - Should show health status

## 📡 API Usage

### 1. Load the Model
```bash
curl -X POST http://localhost:8000/load-model
```

### 2. Generate a GMSH Script
```bash
curl -X POST "http://localhost:8000/generate" \
     -H "Content-Type: application/json" \
     -d '{
       "prompt": "Generate a GMSH script for a 2D rectangular mesh with a circular hole",
       "max_tokens": 2000,
       "temperature": 0.7
     }'
```

## 🔧 Troubleshooting

### Common Issues:

1. **Port Already in Use**
   - Change port in `.env` file: `API_PORT=8001`
   - Or kill the process using port 8000

2. **Model Not Found**
   - Ensure model files are in `./model` directory
   - Check file permissions

3. **Dependencies Issues**
   - Try: `pip install --upgrade pip`
   - Then: `pip install -r requirements.txt`

4. **CUDA/GPU Issues**
   - The backend automatically detects GPU/CPU
   - If GPU fails, it falls back to CPU

## 📱 Testing the API

### Using Postman:
1. Import the collection (if provided)
2. Set base URL to `http://localhost:8000`
3. Test each endpoint

### Using Python Requests:
```python
import requests

# Load model
response = requests.post("http://localhost:8000/load-model")
print(response.json())

# Generate script
data = {
    "prompt": "Create a 2D mesh with a hole",
    "max_tokens": 2000,
    "temperature": 0.7
}
response = requests.post("http://localhost:8000/generate", json=data)
print(response.json()["script"])
```

## 🎯 Next Steps

1. **Test the API** endpoints
2. **Create a frontend** that connects to these endpoints
3. **Customize** the configuration as needed

## 📞 Support

If you encounter issues:
1. Check the error messages in the terminal
2. Verify all files are in place
3. Check the health endpoint: `http://localhost:8000/health`
