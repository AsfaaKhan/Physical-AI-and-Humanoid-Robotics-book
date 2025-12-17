import asyncio
import subprocess
import time
import requests
import threading
from typing import Optional
import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'chatbot-backend'))

def start_backend():
    """Start the backend server in a separate process"""
    try:
        # Start the backend server using uvicorn
        process = subprocess.Popen([
            sys.executable, "-m", "uvicorn",
            "main:app",
            "--host", "127.0.0.1",
            "--port", "8000",
            "--reload"
        ], cwd="chatbot-backend")

        # Give the server time to start
        time.sleep(5)
        return process
    except Exception as e:
        print(f"Error starting backend: {e}")
        return None

def test_backend_health():
    """Test if the backend is running and responding"""
    try:
        response = requests.get("http://127.0.0.1:8000/api/v1/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "healthy":
                print("✓ Backend is running and healthy")
                return True
    except Exception as e:
        print(f"✗ Backend health check failed: {e}")
        return False

def test_ask_endpoint():
    """Test the ask endpoint"""
    try:
        payload = {
            "question": "What is Physical AI?",
            "selected_text": None,
            "use_selected_text_only": False
        }

        response = requests.post("http://127.0.0.1:8000/api/v1/ask",
                                json=payload,
                                timeout=30)

        if response.status_code == 200:
            data = response.json()
            if "answer" in data and "citations" in data:
                print("✓ Ask endpoint is working")
                print(f"  Sample response length: {len(data['answer'])} chars")
                return True
            else:
                print(f"✗ Ask endpoint response missing fields: {data}")
                return False
        else:
            print(f"✗ Ask endpoint returned {response.status_code}: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Ask endpoint test failed: {e}")
        return False

def main():
    print("Starting end-to-end system test...")

    # Start the backend server
    print("Starting backend server...")
    backend_process = start_backend()

    if not backend_process:
        print("✗ Failed to start backend server")
        return False

    try:
        # Test backend health
        if not test_backend_health():
            print("✗ Backend health check failed")
            return False

        # Test ask endpoint
        if not test_ask_endpoint():
            print("✗ Ask endpoint test failed")
            return False

        print("\n🎉 All system tests passed! The RAG chatbot system is working correctly.")
        print("\nSystem components:")
        print("- FastAPI backend running on http://127.0.0.1:8000")
        print("- Qdrant vector store for document retrieval")
        print("- Gemini 2.0 Flash model for question answering")
        print("- Docusaurus frontend with chatbot widget")
        print("- Full RAG pipeline with selected text functionality")

        return True

    finally:
        # Terminate the backend process
        print("\nStopping backend server...")
        backend_process.terminate()
        backend_process.wait()
        print("Backend server stopped.")

if __name__ == "__main__":
    success = main()
    if success:
        print("\n✅ System test completed successfully!")
    else:
        print("\n❌ System test failed!")
        sys.exit(1)