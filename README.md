# AI-Powered Mesh Generator

A full-stack application that generates 3D meshes using AI-powered GMSH scripting and provides interactive visualization.

## 🏗️ Architecture

```
Backend: User Input → LLM → Code → GMSH → Mesh Files
Frontend: Mesh Files → Rendered Mesh Visualization → Interactive Display
```

## ✨ Features

- **AI-Powered Generation**: Uses a fine-tuned LLM to generate GMSH scripts from natural language descriptions
- **Interactive Visualization**: 3D mesh viewer with Three.js for real-time visualization
- **Multiple Export Formats**: Download meshes in MSH, STL, and GEO formats
- **Responsive UI**: Modern, responsive interface with real-time feedback
- **Docker Deployment**: Easy deployment with Docker and Docker Compose

## 🚀 Quick Start

### Option 1: Docker Deployment (Recommended)

1. **Clone and navigate to the project:**
   ```bash
   cd /path/to/your/project
   ```

2. **Make the deployment script executable and run it:**
   ```bash
   chmod +x deploy.sh
   ./deploy.sh
   ```

3. **Open your browser:**
   - Application: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Option 2: Development Mode

1. **Install dependencies:**
   ```bash
   # Python dependencies
   pip install -r requirements.txt
   
   # Node.js dependencies
   cd frontend
   npm install
   cd ..
   ```

2. **Start the application:**
   ```bash
   chmod +x start.sh
   ./start.sh
   ```

3. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000

## 📁 Project Structure

```
├── backend/
│   └── main.py              # FastAPI backend server
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   └── App.js          # Main React app
│   └── package.json        # Frontend dependencies
├── model/                  # LLM model files
├── output/                 # Generated mesh files
├── gmsh.py                # Original LLM integration
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose setup
└── deploy.sh              # Deployment script
```

## 🎯 Usage

1. **Enter a mesh description** in the left panel (e.g., "Create a 2D rectangular mesh with a circular hole at the center")

2. **Configure mesh parameters:**
   - Mesh Type: 2D or 3D
   - Element Size: Controls mesh density

3. **Click "Generate Mesh"** to create the mesh using AI

4. **View the result** in the 3D viewer on the right

5. **Download files** in various formats (MSH, STL, GEO)

## 🔧 API Endpoints

- `POST /generate-mesh` - Generate a new mesh from description
- `GET /mesh/{mesh_id}/files` - Get available mesh files
- `GET /mesh/{mesh_id}/download/{file_type}` - Download mesh files
- `GET /mesh/{mesh_id}/preview` - Get mesh data for visualization

## 🛠️ Development

### Backend Development
```bash
cd backend
python -m uvicorn main:app --reload
```

### Frontend Development
```bash
cd frontend
npm start
```

### Testing
```bash
# Test the API
curl -X POST "http://localhost:8000/generate-mesh" \
     -H "Content-Type: application/json" \
     -d '{"prompt": "Create a simple square mesh", "mesh_type": "2D", "element_size": 0.1}'
```

## 🐳 Docker Commands

```bash
# Build and start
docker-compose up --build

# View logs
docker-compose logs -f

# Stop the application
docker-compose down

# Rebuild without cache
docker-compose build --no-cache
```

## 📋 Requirements

### System Requirements
- Docker & Docker Compose (for deployment)
- OR Python 3.9+ & Node.js 18+ (for development)

### Model Requirements
- The application expects the LLM model files to be in the `./model/` directory
- Model files should include: `config.json`, `tokenizer.json`, `model.safetensors`, etc.

## 🔍 Troubleshooting

### Common Issues

1. **Model not loading:**
   - Ensure model files are in the `./model/` directory
   - Check that all required model files are present

2. **GMSH errors:**
   - Verify GMSH is properly installed in the Docker container
   - Check the generated GMSH script for syntax errors

3. **Frontend not loading:**
   - Ensure the backend is running on port 8000
   - Check browser console for CORS errors

4. **Port conflicts:**
   - Change ports in `docker-compose.yml` if 8000 is already in use
   - Update frontend proxy settings if needed

### Logs
```bash
# View application logs
docker-compose logs mesh-generator

# View real-time logs
docker-compose logs -f mesh-generator
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- GMSH for mesh generation capabilities
- Three.js for 3D visualization
- FastAPI for the backend framework
- React for the frontend framework
