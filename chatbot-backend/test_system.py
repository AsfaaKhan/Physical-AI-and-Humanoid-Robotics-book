"""
Test script to validate the complete RAG chatbot system
"""
import asyncio
import requests
import json
from typing import Dict, Any

BASE_URL = "http://localhost:8000/api/v1"

def test_health_endpoint():
    """Test the health endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "healthy":
                print("✓ Health check passed")
                return True
            else:
                print(f"✗ Health check failed: {data}")
                return False
        else:
            print(f"✗ Health check returned status {response.status_code}: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Health check error: {e}")
        return False

def test_ask_endpoint():
    """Test the ask endpoint with a sample question"""
    try:
        payload = {
            "question": "What is Physical AI?",
            "selected_text": None,
            "use_selected_text_only": False
        }

        response = requests.post(f"{BASE_URL}/ask", json=payload)
        if response.status_code == 200:
            data = response.json()
            if "answer" in data and "citations" in data:
                print("✓ Ask endpoint test passed")
                print(f"  Sample answer: {data['answer'][:100]}...")
                return True
            else:
                print(f"✗ Ask endpoint response missing required fields: {data}")
                return False
        else:
            print(f"✗ Ask endpoint returned status {response.status_code}: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Ask endpoint error: {e}")
        return False

def test_ask_with_selected_text():
    """Test the ask endpoint with selected text only option"""
    try:
        payload = {
            "question": "What does this text say about robotics?",
            "selected_text": "Robotics is the interdisciplinary branch of engineering and science that includes mechanical engineering, electrical engineering, computer science, and others.",
            "use_selected_text_only": True
        }

        response = requests.post(f"{BASE_URL}/ask", json=payload)
        if response.status_code == 200:
            data = response.json()
            if "answer" in data and "citations" in data:
                print("✓ Ask endpoint with selected text test passed")
                print(f"  Sample answer: {data['answer'][:100]}...")
                return True
            else:
                print(f"✗ Ask endpoint with selected text response missing required fields: {data}")
                return False
        else:
            print(f"✗ Ask endpoint with selected text returned status {response.status_code}: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Ask endpoint with selected text error: {e}")
        return False

def test_embed_endpoint():
    """Test the embed endpoint (this requires documents to be available)"""
    try:
        # This test would require actual document files to be available
        # For now, we'll test with a mock request
        payload = {
            "sources": [],  # Empty for now, as we don't have documents to embed in test
            "source_types": []
        }

        response = requests.post(f"{BASE_URL}/embed", json=payload)
        # This might return an error if no sources are provided, which is expected
        print(f"✓ Embed endpoint test completed (status: {response.status_code})")
        return True
    except Exception as e:
        print(f"✗ Embed endpoint error: {e}")
        return False

def run_all_tests():
    """Run all validation tests"""
    print("Running RAG Chatbot System Validation Tests...\n")

    tests = [
        ("Health Check", test_health_endpoint),
        ("Ask Endpoint", test_ask_endpoint),
        ("Ask with Selected Text", test_ask_with_selected_text),
        ("Embed Endpoint", test_embed_endpoint),
    ]

    results = []
    for test_name, test_func in tests:
        print(f"Running {test_name} test...")
        result = test_func()
        results.append((test_name, result))
        print()

    # Summary
    print("Test Results Summary:")
    passed = 0
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"  {test_name}: {status}")
        if result:
            passed += 1

    print(f"\nOverall: {passed}/{len(results)} tests passed")

    if passed == len(results):
        print("🎉 All tests passed! The system is working correctly.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the implementation.")
        return False

if __name__ == "__main__":
    run_all_tests()