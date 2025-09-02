import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

# Input your prompt here
USER_INPUT = """
Generate a GMSH script to create a 2D rectangular mesh with a circular hole at the center, applying finer mesh refinement near the hole and coarser mesh at the boundaries.
"""

def load_model(model_path):
    # Configure 6-bit quantization (good quality)
    quantization_config = BitsAndBytesConfig(
        load_in_6bit=True,
        bnb_6bit_compute_dtype=torch.float16,
        bnb_6bit_use_double_quant=True,  # Nested quantization
        bnb_6bit_quant_type="fp6"  # Float6 (good quality)
    )
    
    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        torch_dtype=torch.float16,
        device_map="auto",
        trust_remote_code=True,
        quantization_config=quantization_config,  # Use 8-bit quantization
        low_cpu_mem_usage=True
    )
    
    tokenizer = AutoTokenizer.from_pretrained(
        model_path,
        trust_remote_code=True
    )
    
    with open(f"{model_path}/chat_template.jinja", "r") as f:
        tokenizer.chat_template = f.read()
    
    return model, tokenizer

def generate_response(model, tokenizer, user_input):

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
    return response.split("<|im_start|>assistant\n")[-1].replace("<|im_end|>", "").strip()

def run_inference():
    model_path = "./model" # Path to your model weights
    
    model, tokenizer = load_model(model_path)
    result = generate_response(model, tokenizer, USER_INPUT)
    
    print(result)

if __name__ == "__main__":
    run_inference()
