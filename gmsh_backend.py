import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
import os
import subprocess
import tempfile
import json
import shutil
from pathlib import Path

class GMSHBackend:
    def __init__(self, model_path="./model"):
        self.model_path = model_path
        self.model = None
        self.tokenizer = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.output_dir = Path("./output")
        self.output_dir.mkdir(exist_ok=True)
    
    def is_model_loaded(self):
        return self.model is not None and self.tokenizer is not None
    
    def load_model(self):
        """Load the GMSH generation model"""
        try:
            # Configure 6-bit quantization
            quantization_config = BitsAndBytesConfig(
                load_in_6bit=True,
                bnb_6bit_compute_dtype=torch.float16,
                bnb_6bit_use_double_quant=True,
                bnb_6bit_quant_type="fp6"
            )
            
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_path,
                torch_dtype=torch.float16,
                device_map="auto",
                trust_remote_code=True,
                quantization_config=quantization_config,
                low_cpu_mem_usage=True
            )
            
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_path,
                trust_remote_code=True
            )
            
            # Load chat template
            template_path = os.path.join(self.model_path, "chat_template.jinja")
            if os.path.exists(template_path):
                with open(template_path, "r") as f:
                    self.tokenizer.chat_template = f.read()
            
            print(f"Model loaded successfully on {self.device}")
            
        except Exception as e:
            print(f"Error loading model: {e}")
            raise
    
    def generate_script(self, prompt, max_tokens=2000, temperature=0.7):
        """Generate GMSH script from prompt"""
        if not self.is_model_loaded():
            raise RuntimeError("Model not loaded. Call load_model() first.")
        
        try:
            # Format input with GMSH instruction tags
            formatted_input = f"<gmsh_instruction>{prompt.strip()}</gmsh_instruction>"
            messages = [{"role": "user", "content": formatted_input}]
            
            # Apply chat template
            prompt_text = self.tokenizer.apply_chat_template(
                messages, 
                tokenize=False, 
                add_generation_prompt=True
            )
            
            # Tokenize input
            inputs = self.tokenizer(prompt_text, return_tensors="pt").to(self.model.device)
            
            # Generate response
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_tokens,
                temperature=temperature,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )
            
            # Decode and clean response
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=False)
            clean_response = response.split("<|im_start|>assistant\n")[-1].replace("<|im_end|>", "").strip()
            
            return clean_response
            
        except Exception as e:
            print(f"Error generating script: {e}")
            raise
    
    def execute_gmsh_script(self, script_content, output_filename="generated_mesh"):
        """Execute GMSH script and generate mesh files"""
        try:
            # Create temporary directory for this execution
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_path = Path(temp_dir)
                
                # Save script to temporary .geo file
                geo_file = temp_path / f"{output_filename}.geo"
                with open(geo_file, 'w') as f:
                    f.write(script_content)
                
                # Execute GMSH command
                gmsh_command = [
                    "gmsh",  # GMSH executable
                    "-2",    # 2D mesh generation
                    "-o",    # Output file
                    str(temp_path / f"{output_filename}.msh"),  # Output mesh file
                    str(geo_file)  # Input .geo file
                ]
                
                print(f"Executing GMSH command: {' '.join(gmsh_command)}")
                
                # Run GMSH
                result = subprocess.run(
                    gmsh_command,
                    capture_output=True,
                    text=True,
                    cwd=temp_path,
                    timeout=60  # 60 second timeout
                )
                
                if result.returncode != 0:
                    raise RuntimeError(f"GMSH execution failed: {result.stderr}")
                
                # Check if output files were created
                msh_file = temp_path / f"{output_filename}.msh"
                if not msh_file.exists():
                    raise RuntimeError("GMSH did not generate output mesh file")
                
                # Copy files to output directory
                output_files = {}
                for file_path in temp_path.glob(f"{output_filename}.*"):
                    dest_path = self.output_dir / file_path.name
                    shutil.copy2(file_path, dest_path)
                    output_files[file_path.suffix] = str(dest_path)
                
                return {
                    "status": "success",
                    "message": "GMSH script executed successfully",
                    "output_files": output_files,
                    "gmsh_output": result.stdout,
                    "script_content": script_content
                }
                
        except subprocess.TimeoutExpired:
            raise RuntimeError("GMSH execution timed out (60 seconds)")
        except FileNotFoundError:
            raise RuntimeError("GMSH executable not found. Please install GMSH and ensure it's in your PATH")
        except Exception as e:
            raise RuntimeError(f"GMSH execution error: {str(e)}")
    
    def generate_and_execute(self, prompt, max_tokens=2000, temperature=0.7, output_filename="generated_mesh"):
        """Complete pipeline: Generate script and execute with GMSH"""
        try:
            # Step 1: Generate GMSH script
            print("Generating GMSH script...")
            script = self.generate_script(prompt, max_tokens, temperature)
            
            # Step 2: Execute the script
            print("Executing GMSH script...")
            result = self.execute_gmsh_script(script, output_filename)
            
            # Add generated script to result
            result["generated_script"] = script
            
            return result
            
        except Exception as e:
            raise RuntimeError(f"Pipeline execution failed: {str(e)}")
    
    def get_model_info(self):
        """Get information about the loaded model"""
        if not self.is_model_loaded():
            return {"status": "Model not loaded"}
        
        return {
            "status": "Model loaded",
            "device": self.device,
            "model_path": self.model_path,
            "model_type": type(self.model).__name__,
            "tokenizer_type": type(self.tokenizer).__name__
        }
    
    def list_output_files(self):
        """List all generated output files"""
        files = []
        if self.output_dir.exists():
            for file_path in self.output_dir.iterdir():
                if file_path.is_file():
                    files.append({
                        "filename": file_path.name,
                        "size": file_path.stat().st_size,
                        "created": file_path.stat().st_ctime
                    })
        return files
    
    def cleanup_output_files(self):
        """Clean up all output files"""
        if self.output_dir.exists():
            for file_path in self.output_dir.iterdir():
                if file_path.is_file():
                    file_path.unlink()
        return {"message": "Output files cleaned up successfully"}
