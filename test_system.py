#!/usr/bin/env python3
"""
System Integration Test for RAG Chatbot

This script tests the end-to-end integration between the frontend and backend
for the RAG chatbot system.
"""

import requests
import json
import time
import sys
from typing import Dict, Any

# Configuration
BACKEND_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:3000"  # Docusaurus dev server

def test_backend_health():
    """Test if the backend API is accessible"""
    print("Testing backend health...")
    try:
        response = requests.get(f"{BACKEND_URL}/")
        if response.status_code == 200:
            print(f"✓ Backend is accessible: {response.json()}")
            return True
        else:
            print(f"✗ Backend returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Backend is not accessible: {str(e)}")
        return False

def test_chat_endpoint():
    """Test the chat endpoint with a sample question"""
    print("\nTesting chat endpoint...")
    try:
        # Sample request
        sample_request = {
            "question": "What is Physical AI?",
            "session_id": None,
            "selected_text": None,
            "metadata": {}
        }

        response = requests.post(
            f"{BACKEND_URL}/api/chat",
            json=sample_request,
            headers={"Content-Type": "application/json"}
        )

        if response.status_code == 200:
            data = response.json()
            print(f"✓ Chat endpoint working. Response keys: {list(data.keys())}")
            print(f"  Answer preview: {data.get('answer', '')[:100]}...")
            print(f"  Sources: {len(data.get('sources', []))} source(s)")
            if 'confidence_score' in data:
                print(f"  Confidence score: {data['confidence_score']}")
            if 'metrics' in data:
                print(f"  Performance metrics: {data['metrics']}")
            return True
        else:
            print(f"✗ Chat endpoint returned status {response.status_code}: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Chat endpoint test failed: {str(e)}")
        return False

def test_session_handling():
    """Test session creation and continuity"""
    print("\nTesting session handling...")
    try:
        # First request - should create a session
        request1 = {
            "question": "What are the main topics covered?",
            "session_id": None,
            "selected_text": None,
            "metadata": {}
        }

        response1 = requests.post(
            f"{BACKEND_URL}/api/chat",
            json=request1,
            headers={"Content-Type": "application/json"}
        )

        if response1.status_code != 200:
            print(f"✗ First session request failed: {response1.status_code}")
            return False

        data1 = response1.json()
        session_id = data1.get('session_id')

        if not session_id:
            print("✗ No session ID returned")
            return False

        print(f"  Created session: {session_id[:10]}...")

        # Second request - should use the same session
        request2 = {
            "question": "Can you elaborate on the first topic?",
            "session_id": session_id,
            "selected_text": None,
            "metadata": {}
        }

        response2 = requests.post(
            f"{BACKEND_URL}/api/chat",
            json=request2,
            headers={"Content-Type": "application/json"}
        )

        if response2.status_code == 200:
            data2 = response2.json()
            session_id2 = data2.get('session_id')

            if session_id2 == session_id:
                print("✓ Session continuity working correctly")
                return True
            else:
                print(f"✗ Session ID changed: {session_id2} != {session_id}")
                return False
        else:
            print(f"✗ Second session request failed: {response2.status_code}")
            return False

    except Exception as e:
        print(f"✗ Session handling test failed: {str(e)}")
        return False

def test_source_references():
    """Test that source references are properly returned"""
    print("\nTesting source references...")
    try:
        sample_request = {
            "question": "What is embodied intelligence?",
            "session_id": None,
            "selected_text": None,
            "metadata": {}
        }

        response = requests.post(
            f"{BACKEND_URL}/api/chat",
            json=sample_request,
            headers={"Content-Type": "application/json"}
        )

        if response.status_code == 200:
            data = response.json()
            sources = data.get('sources', [])

            if len(sources) > 0:
                print(f"✓ Source references returned: {len(sources)} source(s)")
                for i, source in enumerate(sources[:2]):  # Show first 2 sources
                    print(f"  Source {i+1}: {source.get('title', 'No title')}")
                    print(f"    URL: {source.get('url', 'No URL')}")
                    print(f"    Relevance: {source.get('relevance_score', 'No score')}")
                return True
            else:
                print("✗ No source references returned")
                return False
        else:
            print(f"✗ Source reference test failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Source reference test failed: {str(e)}")
        return False

def run_all_tests():
    """Run all integration tests"""
    print("Starting RAG Chatbot System Integration Tests\n")
    print("="*50)

    tests = [
        ("Backend Health Check", test_backend_health),
        ("Chat Endpoint Functionality", test_chat_endpoint),
        ("Session Handling", test_session_handling),
        ("Source References", test_source_references),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        print("-" * len(test_name))
        if test_func():
            passed += 1
            print("✓ PASSED")
        else:
            print("✗ FAILED")

    print("\n" + "="*50)
    print(f"Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! System integration is working correctly.")
        return True
    else:
        print(f"❌ {total - passed} test(s) failed. Please check the configuration.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)