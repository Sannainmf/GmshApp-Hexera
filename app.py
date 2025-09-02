from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from gmsh_backend import GMSHBackend
import os
from dotenv import load_dotenv

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

@app.post("/load-model")
async def load_model():
    try:
        gmsh_backend.load_model()
        return {"message": "Model loaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load model: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
