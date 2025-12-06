"""
Test script to verify selected text functionality
"""
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_selected_text_functionality():
    """Test the selected text functionality"""
    print("Testing selected text functionality...")

    # Test 1: Regular question (should work with RAG)
    print("\n1. Testing regular question...")
    payload1 = {
        "question": "What is Physical AI?",
        "selected_text": None,
        "use_selected_text_only": False
    }

    try:
        response1 = requests.post(f"{BASE_URL}/ask", json=payload1)
        if response1.status_code == 200:
            data1 = response1.json()
            print(f"   ✓ Regular question successful")
            print(f"   Answer preview: {data1['answer'][:100]}...")
        else:
            print(f"   ✗ Regular question failed: {response1.status_code} - {response1.text}")
    except Exception as e:
        print(f"   ✗ Regular question error: {e}")

    # Test 2: Question with selected text only
    print("\n2. Testing question with selected text only...")
    sample_text = """
    Physical AI is an approach to artificial intelligence that emphasizes
    the importance of physical interaction with the environment as a
    fundamental aspect of intelligence. Unlike traditional AI that focuses
    primarily on processing information in abstract computational spaces,
    Physical AI recognizes that real-world interaction provides essential
    feedback and learning opportunities.
    """

    payload2 = {
        "question": "What is Physical AI?",
        "selected_text": sample_text,
        "use_selected_text_only": True
    }

    try:
        response2 = requests.post(f"{BASE_URL}/ask", json=payload2)
        if response2.status_code == 200:
            data2 = response2.json()
            print(f"   ✓ Selected text question successful")
            print(f"   Answer preview: {data2['answer'][:100]}...")
        else:
            print(f"   ✗ Selected text question failed: {response2.status_code} - {response2.text}")
    except Exception as e:
        print(f"   ✗ Selected text question error: {e}")

    # Test 3: Health check
    print("\n3. Testing health endpoint...")
    try:
        response3 = requests.get(f"{BASE_URL}/health")
        if response3.status_code == 200:
            data3 = response3.json()
            print(f"   ✓ Health check successful: {data3}")
        else:
            print(f"   ✗ Health check failed: {response3.status_code}")
    except Exception as e:
        print(f"   ✗ Health check error: {e}")

    print("\nTest completed!")

if __name__ == "__main__":
    test_selected_text_functionality()