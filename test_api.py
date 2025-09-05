#!/usr/bin/env python3
"""
Test script for the Mesh Generator API
"""

import requests
import json
import time

API_BASE = "http://localhost:8000"

def test_health():
    """Test if the API is running"""
    try:
        response = requests.get(f"{API_BASE}/")
        if response.status_code == 200:
            print("✅ API is running")
            return True
        else:
            print(f"❌ API returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Make sure it's running on port 8000")
        return False

def test_mesh_generation():
    """Test mesh generation endpoint"""
    test_prompt = "Create a simple 2D square mesh with 4 elements"
    
    payload = {
        "prompt": test_prompt,
        "mesh_type": "2D",
        "element_size": 0.2
    }
    
    print(f"🧪 Testing mesh generation with prompt: '{test_prompt}'")
    
    try:
        response = requests.post(f"{API_BASE}/generate-mesh", json=payload)
        
        if response.status_code == 200:
            data = response.json()
            if data["status"] == "success":
                print("✅ Mesh generation successful!")
                print(f"📋 Mesh ID: {data['mesh_id']}")
                print(f"📝 Generated script preview: {data['gmsh_script'][:100]}...")
                return data["mesh_id"]
            else:
                print(f"❌ Mesh generation failed: {data['message']}")
                return None
        else:
            print(f"❌ API returned status code: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error during mesh generation: {e}")
        return None

def test_mesh_files(mesh_id):
    """Test mesh file retrieval"""
    if not mesh_id:
        print("⏭️ Skipping file test - no mesh ID")
        return
    
    print(f"🧪 Testing mesh file retrieval for ID: {mesh_id}")
    
    try:
        response = requests.get(f"{API_BASE}/mesh/{mesh_id}/files")
        
        if response.status_code == 200:
            files = response.json()
            print("✅ Mesh files retrieved successfully!")
            for file_type, url in files.items():
                print(f"📁 {file_type}: {url}")
        else:
            print(f"❌ Failed to retrieve mesh files: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error retrieving mesh files: {e}")

def main():
    """Run all tests"""
    print("🚀 Starting Mesh Generator API Tests")
    print("=" * 50)
    
    # Test 1: Health check
    if not test_health():
        print("\n❌ Health check failed. Please start the API first.")
        return
    
    print()
    
    # Test 2: Mesh generation
    mesh_id = test_mesh_generation()
    
    print()
    
    # Test 3: File retrieval
    test_mesh_files(mesh_id)
    
    print("\n" + "=" * 50)
    print("🎉 Tests completed!")
    
    if mesh_id:
        print(f"\n🌐 You can view the generated mesh at: {API_BASE}/mesh/{mesh_id}/files")
        print(f"📊 API documentation: {API_BASE}/docs")

if __name__ == "__main__":
    main()
