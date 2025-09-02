import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
import os

class GMSHBackend:
    def __init__(self, model_path="./model"):
        self.model_path = model_path
        self.model = None
        self.tokenizer = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
    
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
