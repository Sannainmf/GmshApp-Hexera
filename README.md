# 🚀 GMSH Script Generator Backend

A **complete pipeline** FastAPI backend for generating and executing GMSH scripts using a fine-tuned language model.

## 🎯 **Complete Pipeline**

```
User Input → LLM → Prompt → LLM → GMSH Code → GMSH Engine → Mesh Files
```

**What this backend does:**
1. **Takes user text input** (e.g., "Create a 2D mesh with a hole")
2. **Generates GMSH script** using fine-tuned LLM
3. **Executes the script** with GMSH engine
4. **Returns mesh files** (.geo, .msh) ready for use

## ✨ **Features**

- **🚀 Complete Pipeline**: From text input to mesh files in one API call
- **🤖 AI-Powered**: Fine-tuned language model for GMSH script generation
- **🔧 GMSH Integration**: Direct execution of generated scripts
- **📁 File Management**: Generate, store, and download mesh files
- **🌐 RESTful API**: Easy integration with any frontend
- **📊 Health Monitoring**: System status and model management
- **⚡ Fast**: Optimized for quick mesh generation

## 🛠️ **Setup**

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Install GMSH:**
   - **Windows**: Download from [GMSH website](http://gmsh.info/)
   - **Mac**: `brew install gmsh`
   - **Linux**: `sudo apt-get install gmsh`

3. **Set up environment:**
```bash
cp env_example.txt .env
# Edit .env if needed
```

4. **Verify model files** are in `./model` directory

## 🚀 **Usage**

### **Start the server:**
```bash
python app.py
```

The API will be available at `http://localhost:8000`

### **Complete Pipeline Example:**

```bash
# 1. Load the model
curl -X POST http://localhost:8000/load-model

# 2. Execute complete pipeline (generate + execute)
curl -X POST "http://localhost:8000/execute-gmsh" \
     -H "Content-Type: application/json" \
     -d '{
       "prompt": "Generate a GMSH script for a 2D rectangular mesh with a circular hole",
       "max_tokens": 2000,
       "temperature": 0.7,
       "output_filename": "rectangular_mesh"
     }'

# 3. Download generated files
curl -O http://localhost:8000/download/rectangular_mesh.geo
curl -O http://localhost:8000/download/rectangular_mesh.msh
```

## 📡 **API Endpoints**

### **Core Pipeline:**
- `POST /execute-gmsh` - **Complete pipeline** (generate + execute)
- `POST /generate` - Generate GMSH script only
- `POST /execute-existing-script` - Execute existing script

### **Model Management:**
- `POST /load-model` - Load ML model
- `GET /model-info` - Model information

### **File Management:**
- `GET /output-files` - List generated files
- `GET /download/{filename}` - Download files
- `DELETE /cleanup` - Clean up files

### **System:**
- `GET /` - API information
- `GET /health` - Health check

## 📁 **File Structure**

```
gmsh-backend/
├── app.py                   # Main FastAPI application
├── gmsh_backend.py          # Backend service with GMSH integration
├── config.py                # Configuration management
├── requirements.txt         # Python dependencies
├── README.md                # This file
├── SETUP.md                 # Detailed setup guide
├── API_DOCS.md              # Complete API documentation
├── env_example.txt          # Environment template
├── gmsh.py                  # Original script
├── model/                   # ML model files
└── output/                  # Generated mesh files (created automatically)
```

## 🔧 **How It Works**

1. **User sends text prompt** via API
2. **LLM generates GMSH script** from the prompt
3. **Backend saves script** to temporary file
4. **GMSH executes script** and generates mesh
5. **Results are processed** and stored
6. **User downloads** generated mesh files

## 📋 **Requirements**

- **Python 3.8+**
- **GMSH** (mesh generation engine)
- **PyTorch** (ML framework)
- **Transformers** (Hugging Face)
- **FastAPI** (web framework)

## 🎯 **Use Cases**

- **Research**: Quick mesh generation for simulations
- **Education**: Teaching computational geometry
- **Prototyping**: Fast mesh design iterations
- **Automation**: Batch mesh generation
- **Integration**: Embed in larger applications

## 📚 **Documentation**

- **`SETUP.md`** - Detailed setup instructions
- **`API_DOCS.md`** - Complete API reference
- **`env_example.txt`** - Configuration template

## 🚨 **Important Notes**

- **Model must be loaded** before generating scripts
- **GMSH must be installed** and in your PATH
- **Generated files** are stored in `./output/` directory
- **60-second timeout** for GMSH execution
- **Automatic cleanup** available via API

## 🔮 **Future Enhancements**

- **3D mesh support**
- **Mesh quality optimization**
- **Batch processing**
- **User authentication**
- **Mesh visualization**
- **Cloud deployment**

## 📞 **Support**

If you encounter issues:
1. Check the health endpoint: `http://localhost:8000/health`
2. Verify GMSH installation: `gmsh --version`
3. Check error messages in terminal
4. Review the setup guide in `SETUP.md`

---

**Your complete GMSH mesh generation pipeline is ready! 🎉**
