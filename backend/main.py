from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
import gmsh
import os
import tempfile
import json
from pydantic import BaseModel
from typing import Optional
import uuid
import aiofiles

app = FastAPI(title="Mesh Generation API", version="1.0.0")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for model
model = None
tokenizer = None

class MeshRequest(BaseModel):
    prompt: str
    mesh_type: str = "2D"  # 2D or 3D
    element_size: Optional[float] = 0.1

class MeshResponse(BaseModel):
    mesh_id: str
    gmsh_script: str
    status: str
    message: str

def load_model(model_path="./model"):
    """Load the LLM model and tokenizer"""
    global model, tokenizer
    
    if model is not None:
        return model, tokenizer
    
    try:
        # Configure 6-bit quantization
        quantization_config = BitsAndBytesConfig(
            load_in_6bit=True,
            bnb_6bit_compute_dtype=torch.float16,
            bnb_6bit_use_double_quant=True,
            bnb_6bit_quant_type="fp6"
        )
        
        model = AutoModelForCausalLM.from_pretrained(
            model_path,
            torch_dtype=torch.float16,
            device_map="auto",
            trust_remote_code=True,
            quantization_config=quantization_config,
            low_cpu_mem_usage=True
        )
        
        tokenizer = AutoTokenizer.from_pretrained(
            model_path,
            trust_remote_code=True
        )
        
        # Load chat template
        chat_template_path = os.path.join(model_path, "chat_template.jinja")
        if os.path.exists(chat_template_path):
            with open(chat_template_path, "r") as f:
                tokenizer.chat_template = f.read()
        
        return model, tokenizer
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load model: {str(e)}")

def generate_gmsh_script(model, tokenizer, user_input):
    """Generate GMSH script using the LLM"""
    try:
        formatted_input = f"<gmsh_instruction>{user_input.strip()}</gmsh_instruction>"
        messages = [{"role": "user", "content": formatted_input}]
        
        prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
        
        outputs = model.generate(
            **inputs,
            max_new_tokens=2000,
            temperature=0.7,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id
        )
        
        response = tokenizer.decode(outputs[0], skip_special_tokens=False)
        gmsh_script = response.split("<|im_start|>assistant\n")[-1].replace("<|im_end|>", "").strip()
        
        return gmsh_script
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate GMSH script: {str(e)}")

def execute_gmsh_script(gmsh_script, mesh_id, element_size=0.1):
    """Execute GMSH script and generate mesh files"""
    try:
        # Initialize GMSH
        gmsh.initialize()
        gmsh.option.setNumber("General.Terminal", 1)
        
        # Set element size
        gmsh.option.setNumber("Mesh.CharacteristicLengthMin", element_size * 0.5)
        gmsh.option.setNumber("Mesh.CharacteristicLengthMax", element_size * 2.0)
        
        # Execute the generated script
        exec(gmsh_script)
        
        # Generate mesh
        gmsh.model.mesh.generate(2)  # 2D mesh
        
        # Create output directory
        output_dir = f"./output/{mesh_id}"
        os.makedirs(output_dir, exist_ok=True)
        
        # Save mesh files
        mesh_file = os.path.join(output_dir, f"{mesh_id}.msh")
        gmsh.write(mesh_file)
        
        # Also save as STL for visualization
        stl_file = os.path.join(output_dir, f"{mesh_id}.stl")
        gmsh.write(stl_file)
        
        # Save the GMSH script
        script_file = os.path.join(output_dir, f"{mesh_id}.geo")
        with open(script_file, 'w') as f:
            f.write(gmsh_script)
        
        gmsh.finalize()
        
        return {
            "mesh_file": mesh_file,
            "stl_file": stl_file,
            "script_file": script_file
        }
        
    except Exception as e:
        gmsh.finalize()
        raise HTTPException(status_code=500, detail=f"Failed to execute GMSH script: {str(e)}")

@app.on_event("startup")
async def startup_event():
    """Load model on startup"""
    try:
        load_model()
        print("Model loaded successfully!")
    except Exception as e:
        print(f"Failed to load model: {e}")

@app.get("/")
async def root():
    return {"message": "Mesh Generation API is running!"}

@app.post("/generate-mesh", response_model=MeshResponse)
async def generate_mesh(request: MeshRequest):
    """Generate mesh from user prompt"""
    try:
        # Load model if not already loaded
        model, tokenizer = load_model()
        
        # Generate unique mesh ID
        mesh_id = str(uuid.uuid4())
        
        # Generate GMSH script using LLM
        gmsh_script = generate_gmsh_script(model, tokenizer, request.prompt)
        
        # Execute GMSH script and generate mesh files
        mesh_files = execute_gmsh_script(gmsh_script, mesh_id, request.element_size)
        
        return MeshResponse(
            mesh_id=mesh_id,
            gmsh_script=gmsh_script,
            status="success",
            message="Mesh generated successfully"
        )
        
    except Exception as e:
        return MeshResponse(
            mesh_id="",
            gmsh_script="",
            status="error",
            message=str(e)
        )

@app.get("/mesh/{mesh_id}/files")
async def get_mesh_files(mesh_id: str):
    """Get mesh files for a given mesh ID"""
    output_dir = f"./output/{mesh_id}"
    
    if not os.path.exists(output_dir):
        raise HTTPException(status_code=404, detail="Mesh not found")
    
    files = {
        "mesh_file": f"/mesh/{mesh_id}/download/msh",
        "stl_file": f"/mesh/{mesh_id}/download/stl",
        "script_file": f"/mesh/{mesh_id}/download/geo"
    }
    
    return files

@app.get("/mesh/{mesh_id}/download/{file_type}")
async def download_mesh_file(mesh_id: str, file_type: str):
    """Download mesh files"""
    output_dir = f"./output/{mesh_id}"
    file_path = os.path.join(output_dir, f"{mesh_id}.{file_type}")
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        file_path,
        media_type="application/octet-stream",
        filename=f"{mesh_id}.{file_type}"
    )

@app.get("/mesh/{mesh_id}/preview")
async def get_mesh_preview(mesh_id: str):
    """Get mesh data for frontend visualization"""
    output_dir = f"./output/{mesh_id}"
    stl_file = os.path.join(output_dir, f"{mesh_id}.stl")
    
    if not os.path.exists(stl_file):
        raise HTTPException(status_code=404, detail="Mesh file not found")
    
    # Read STL file and return as JSON
    try:
        with open(stl_file, 'rb') as f:
            content = f.read()
        
        return {
            "mesh_id": mesh_id,
            "stl_data": content.hex(),  # Convert to hex string for JSON
            "file_size": len(content)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read mesh file: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
