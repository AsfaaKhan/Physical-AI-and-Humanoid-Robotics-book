#!/usr/bin/env python3
"""
End-to-End Tests for RAG Chatbot System

This script performs comprehensive end-to-end tests covering all user stories:
1. Access RAG Chatbot Interface
2. Reliable Communication with Backend API
3. Context-Aware Query Processing
"""

import requests
import json
import time
import sys
from typing import Dict, Any, Optional

# Configuration
BACKEND_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:3000"  # Docusaurus dev server

class E2ETestRunner:
    def __init__(self):
        self.session = requests.Session()
        self.test_results = []
        self.current_session_id = None

    def log_test(self, test_name: str, passed: bool, details: str = ""):
        """Log a test result"""
        result = {
            "test": test_name,
            "passed": passed,
            "details": details
        }
        self.test_results.append(result)
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"  {status} {test_name}")
        if details:
            print(f"      {details}")

    def test_user_story_1_access_interface(self):
        """Test User Story 1: Access RAG Chatbot Interface"""
        print("\nTesting User Story 1: Access RAG Chatbot Interface")
        print("-" * 55)

        # Test 1: Backend health check
        try:
            response = self.session.get(f"{BACKEND_URL}/")
            if response.status_code == 200 and "message" in response.json():
                self.log_test("Backend API accessibility", True, "API endpoint responding")
            else:
                self.log_test("Backend API accessibility", False, f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("Backend API accessibility", False, str(e))

        # Test 2: Chat endpoint functionality
        try:
            sample_request = {
                "question": "What is Physical AI?",
                "session_id": None,
                "selected_text": None,
                "metadata": {}
            }

            response = self.session.post(
                f"{BACKEND_URL}/api/chat",
                json=sample_request,
                headers={"Content-Type": "application/json"}
            )

            if response.status_code == 200:
                data = response.json()
                has_answer = "answer" in data and len(data["answer"]) > 0
                has_sources = "sources" in data and isinstance(data["sources"], list)
                has_session = "session_id" in data and data["session_id"] is not None

                self.current_session_id = data.get("session_id")

                success = has_answer and has_sources and has_session
                details = f"Answer: {len(data['answer'][:50])} chars, Sources: {len(data['sources'])}, Session: {bool(data.get('session_id'))}"
                self.log_test("Chat endpoint response structure", success, details)
            else:
                self.log_test("Chat endpoint response structure", False, f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("Chat endpoint response structure", False, str(e))

        # Test 3: Response contains sources
        try:
            if self.current_session_id:
                sample_request = {
                    "question": "What are the main topics?",
                    "session_id": self.current_session_id,
                    "selected_text": None,
                    "metadata": {}
                }

                response = self.session.post(
                    f"{BACKEND_URL}/api/chat",
                    json=sample_request,
                    headers={"Content-Type": "application/json"}
                )

                if response.status_code == 200:
                    data = response.json()
                    has_sources = len(data.get("sources", [])) > 0
                    if has_sources:
                        source_titles = [s.get("title", "") for s in data["sources"][:2]]
                        details = f"Sources: {', '.join(source_titles)}"
                    else:
                        details = "No sources returned"
                    self.log_test("Response includes source references", has_sources, details)
                else:
                    self.log_test("Response includes source references", False, f"Status: {response.status_code}")
            else:
                self.log_test("Response includes source references", False, "No session ID available")
        except Exception as e:
            self.log_test("Response includes source references", False, str(e))

    def test_user_story_2_reliable_communication(self):
        """Test User Story 2: Reliable Communication with Backend API"""
        print("\nTesting User Story 2: Reliable Communication with Backend API")
        print("-" * 60)

        # Test 1: Error handling for empty question
        try:
            bad_request = {
                "question": "",  # Empty question should cause error
                "session_id": self.current_session_id,
                "selected_text": None,
                "metadata": {}
            }

            response = self.session.post(
                f"{BACKEND_URL}/api/chat",
                json=bad_request,
                headers={"Content-Type": "application/json"}
            )

            has_error = response.status_code == 400
            self.log_test("Error handling for empty question", has_error, f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("Error handling for empty question", False, str(e))

        # Test 2: Valid question should work
        try:
            valid_request = {
                "question": "What is the purpose of this system?",
                "session_id": self.current_session_id,
                "selected_text": None,
                "metadata": {}
            }

            response = self.session.post(
                f"{BACKEND_URL}/api/chat",
                json=valid_request,
                headers={"Content-Type": "application/json"}
            )

            success = response.status_code == 200
            if success:
                data = response.json()
                details = f"Answer length: {len(data.get('answer', ''))} chars"
            else:
                details = f"Status: {response.status_code}"
            self.log_test("Valid questions processed successfully", success, details)
        except Exception as e:
            self.log_test("Valid questions processed successfully", False, str(e))

        # Test 3: Session continuity
        try:
            # Use the same session ID to test continuity
            request1 = {
                "question": "Testing session continuity",
                "session_id": self.current_session_id,
                "selected_text": None,
                "metadata": {}
            }

            response1 = self.session.post(
                f"{BACKEND_URL}/api/chat",
                json=request1,
                headers={"Content-Type": "application/json"}
            )

            if response1.status_code == 200:
                data1 = response1.json()
                session_id_1 = data1.get("session_id")

                # Second request with same session
                request2 = {
                    "question": "Continue with this session",
                    "session_id": session_id_1,
                    "selected_text": None,
                    "metadata": {}
                }

                response2 = self.session.post(
                    f"{BACKEND_URL}/api/chat",
                    json=request2,
                    headers={"Content-Type": "application/json"}
                )

                if response2.status_code == 200:
                    data2 = response2.json()
                    session_continuity = data2.get("session_id") == session_id_1
                    self.log_test("Session continuity maintained", session_continuity,
                                f"Session ID preserved: {session_continuity}")
                else:
                    self.log_test("Session continuity maintained", False, f"Status: {response2.status_code}")
            else:
                self.log_test("Session continuity maintained", False, f"Status: {response1.status_code}")
        except Exception as e:
            self.log_test("Session continuity maintained", False, str(e))

    def test_user_story_3_context_aware_processing(self):
        """Test User Story 3: Context-Aware Query Processing"""
        print("\nTesting User Story 3: Context-Aware Query Processing")
        print("-" * 55)

        # Test 1: Query with selected text context
        selected_text = "Physical AI is an interdisciplinary field combining robotics, machine learning, and embodied intelligence to create systems that interact with the physical world."

        try:
            context_request = {
                "question": "What does this text say about Physical AI?",
                "session_id": self.current_session_id,
                "selected_text": selected_text,
                "metadata": {}
            }

            response = self.session.post(
                f"{BACKEND_URL}/api/chat",
                json=context_request,
                headers={"Content-Type": "application/json"}
            )

            if response.status_code == 200:
                data = response.json()
                # Check if the response makes reference to the provided context
                answer = data.get("answer", "").lower()
                has_context_ref = any(word in answer for word in ["interdisciplinary", "robotics", "machine learning"])

                details = f"Context-aware response: {has_context_ref}"
                self.log_test("Context-aware query processing", has_context_ref, details)
            else:
                self.log_test("Context-aware query processing", False, f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("Context-aware query processing", False, str(e))

        # Test 2: Query without context for comparison
        try:
            no_context_request = {
                "question": "What is Physical AI?",
                "session_id": self.current_session_id,
                "selected_text": None,  # No context provided
                "metadata": {}
            }

            response = self.session.post(
                f"{BACKEND_URL}/api/chat",
                json=no_context_request,
                headers={"Content-Type": "application/json"}
            )

            success = response.status_code == 200
            if success:
                data = response.json()
                details = f"Response length: {len(data.get('answer', ''))} chars"
            else:
                details = f"Status: {response.status_code}"
            self.log_test("Queries without context handled", success, details)
        except Exception as e:
            self.log_test("Queries without context handled", False, str(e))

    def test_session_management(self):
        """Test Session Management & Conversation Features"""
        print("\nTesting Session Management & Conversation Features")
        print("-" * 50)

        # Test 1: New session creation
        try:
            new_session_request = {
                "question": "Starting a new conversation",
                "session_id": None,  # Should create new session
                "selected_text": None,
                "metadata": {}
            }

            response = self.session.post(
                f"{BACKEND_URL}/api/chat",
                json=new_session_request,
                headers={"Content-Type": "application/json"}
            )

            if response.status_code == 200:
                data = response.json()
                has_new_session = data.get("session_id") is not None
                details = f"New session ID: {data['session_id'][:12]}..." if has_new_session else "No session created"
                self.log_test("New session creation", has_new_session, details)
            else:
                self.log_test("New session creation", False, f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("New session creation", False, str(e))

        # Test 2: Session persistence
        try:
            if hasattr(self, 'current_session_id') and self.current_session_id:
                # Use existing session
                existing_session_request = {
                    "question": "Following up in existing session",
                    "session_id": self.current_session_id,
                    "selected_text": None,
                    "metadata": {}
                }

                response = self.session.post(
                    f"{BACKEND_URL}/api/chat",
                    json=existing_session_request,
                    headers={"Content-Type": "application/json"}
                )

                if response.status_code == 200:
                    data = response.json()
                    correct_session = data.get("session_id") == self.current_session_id
                    details = f"Session preserved: {correct_session}"
                    self.log_test("Session persistence", correct_session, details)
                else:
                    self.log_test("Session persistence", False, f"Status: {response.status_code}")
            else:
                self.log_test("Session persistence", False, "No existing session to test")
        except Exception as e:
            self.log_test("Session persistence", False, str(e))

    def run_all_tests(self):
        """Run all end-to-end tests"""
        print("Starting End-to-End Tests for RAG Chatbot System\n")
        print("="*60)

        # Run all test suites
        self.test_user_story_1_access_interface()
        self.test_user_story_2_reliable_communication()
        self.test_user_story_3_context_aware_processing()
        self.test_session_management()

        # Summary
        print("\n" + "="*60)
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["passed"])

        print(f"Test Results Summary: {passed_tests}/{total_tests} tests passed")

        for result in self.test_results:
            status = "✓ PASS" if result["passed"] else "✗ FAIL"
            print(f"  {status} {result['test']}")

        print("\n" + "="*60)

        if passed_tests == total_tests:
            print("🎉 All end-to-end tests passed! System is working correctly.")
            return True
        else:
            failed_count = total_tests - passed_tests
            print(f"❌ {failed_count} test(s) failed. Please check the implementation.")
            return False

def main():
    """Main function to run the E2E tests"""
    runner = E2ETestRunner()
    success = runner.run_all_tests()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()