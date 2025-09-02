import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Configuration
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("API_PORT", 8000))
    API_DEBUG = os.getenv("API_DEBUG", "False").lower() == "true"
    
    # Model Configuration
    MODEL_PATH = os.getenv("MODEL_PATH", "./model")
    DEFAULT_MAX_TOKENS = int(os.getenv("DEFAULT_MAX_TOKENS", 2000))
    DEFAULT_TEMPERATURE = float(os.getenv("DEFAULT_TEMPERATURE", 0.7))
    
    # CORS Configuration
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
