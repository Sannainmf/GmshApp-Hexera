#!/usr/bin/env python3
"""
Simple test to verify your app works locally
"""

import subprocess
import time
import requests
import sys

def test_backend():
    """Test if backend is working"""
    try:
        response = requests.get("http://localhost:8000/", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is running!")
            return True
    except:
        pass
    
    print("❌ Backend not running. Starting it...")
    return False

def start_backend():
    """Start the backend server"""
    try:
        # Start backend in background
        subprocess.Popen([
            sys.executable, "-m", "uvicorn", 
            "backend.main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000"
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        print("🚀 Starting backend server...")
        time.sleep(5)  # Wait for server to start
        
        if test_backend():
            print("✅ Backend started successfully!")
            print("🌐 Open your browser to: http://localhost:8000")
            print("📊 API docs: http://localhost:8000/docs")
            return True
        else:
            print("❌ Failed to start backend")
            return False
            
    except Exception as e:
        print(f"❌ Error starting backend: {e}")
        return False

if __name__ == "__main__":
    if not test_backend():
        start_backend()
    else:
        print("🎉 Your app is already running!")
        print("🌐 Open: http://localhost:8000")
