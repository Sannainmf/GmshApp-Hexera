from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uvicorn
from gmsh_backend import GMSHBackend
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

app = FastAPI(title="GMSH Script Generator API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize backend
gmsh_backend = GMSHBackend()

class GMSHRequest(BaseModel):
    prompt: str
    max_tokens: int = 2000
    temperature: float = 0.7

class GMSHResponse(BaseModel):
    script: str
    status: str
    message: str

class GMSHExecuteRequest(BaseModel):
    prompt: str
    max_tokens: int = 2000
    temperature: float = 0.7
    output_filename: str = "generated_mesh"

class GMSHExecuteResponse(BaseModel):
    status: str
    message: str
    generated_script: str
    output_files: dict
    gmsh_output: str

@app.get("/")
async def root():
    return {"message": "GMSH Script Generator API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "model_loaded": gmsh_backend.is_model_loaded()}

@app.post("/generate", response_model=GMSHResponse)
async def generate_gmsh_script(request: GMSHRequest):
    try:
        if not gmsh_backend.is_model_loaded():
            raise HTTPException(status_code=503, detail="Model not loaded")
        
        script = gmsh_backend.generate_script(
            request.prompt,
            max_tokens=request.max_tokens,
            temperature=request.temperature
        )
        
        return GMSHResponse(
            script=script,
            status="success",
            message="GMSH script generated successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/execute-gmsh", response_model=GMSHExecuteResponse)
async def execute_gmsh_script(request: GMSHExecuteRequest):
    """Complete pipeline: Generate script and execute with GMSH"""
    try:
        if not gmsh_backend.is_model_loaded():
            raise HTTPException(status_code=503, detail="Model not loaded")
        
        result = gmsh_backend.generate_and_execute(
            request.prompt,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
            output_filename=request.output_filename
        )
        
        return GMSHExecuteResponse(**result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/execute-existing-script")
async def execute_existing_script(script_content: str, output_filename: str = "generated_mesh"):
    """Execute an existing GMSH script"""
    try:
        result = gmsh_backend.execute_gmsh_script(script_content, output_filename)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/output-files")
async def list_output_files():
    """List all generated output files"""
    try:
        files = gmsh_backend.list_output_files()
        return {"files": files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/download/{filename}")
async def download_file(filename: str):
    """Download a generated file"""
    try:
        file_path = Path("./output") / filename
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="File not found")
        
        return FileResponse(
            path=str(file_path),
            filename=filename,
            media_type='application/octet-stream'
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/cleanup")
async def cleanup_output_files():
    """Clean up all output files"""
    try:
        result = gmsh_backend.cleanup_output_files()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/load-model")
async def load_model():
    try:
        gmsh_backend.load_model()
        return {"message": "Model loaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load model: {str(e)}")

@app.get("/model-info")
async def get_model_info():
    """Get information about the loaded model"""
    try:
        info = gmsh_backend.get_model_info()
        return info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
