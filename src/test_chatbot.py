import requests
import json
import os
import time
import uuid
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Test configuration
BASE_URL = "http://localhost:8000"
TEST_USER_ID = str(uuid.uuid4())  # Generate a UUID for the test user

def send_message(prompt: str, user_id: str = TEST_USER_ID) -> None:
    """Send a message to the chatbot and print the response"""
    try:
        response = requests.post(
            f"{BASE_URL}/chat",
            json={"user_id": user_id, "prompt": prompt}
        )
        response.raise_for_status()
        data = response.json()
        print(f"\n[20:47:30] You: {prompt}")
        print(f"[20:47:30] Assistant: {data['response']}")
        print(f"\nFull Response:")
        print(f"Session ID: {data['session_id']}")
        print(f"Timestamp: {data['timestamp']}")
    except Exception as e:
        print(f"Error: {str(e)}")
        if hasattr(e, 'response'):
            print(f"Response: {e.response.text}")

def test_session_management():
    print("\n=== Testing Session Management ===")
    print(f"Using test user ID: {TEST_USER_ID}")
    
    # First message - should create new session
    print("\nSending first message...")
    send_message("Hi! My name is Alice.")
    
    # Wait for 1 minute (to test session timeout)
    print("\nWaiting for session timeout (1 minute)...")
    time.sleep(60)  # 1 minute
    
    # Second message - should create new session
    print("\nSending second message...")
    send_message("What is my name?")

if __name__ == "__main__":
    test_session_management() 