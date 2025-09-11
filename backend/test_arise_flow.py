"""
Test the complete A.R.I.S.E. flow without STT to isolate TTS issues.
"""

import sys
import os

# Add modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules', 'brain'))

from main import ARISEMain


def test_arise_tts_flow():
    """Test A.R.I.S.E. TTS flow without STT input."""
    print("=== A.R.I.S.E. TTS Flow Test ===")
    
    # Initialize A.R.I.S.E.
    arise = ARISEMain()
    
    print("\n1. Testing direct _speak method:")
    arise._speak("This is a direct speak test.")
    
    print("\n2. Testing chat engine integration:")
    # Simulate user input without STT
    test_input = "Hello, how are you?"
    print(f"Simulated user input: {test_input}")
    
    # Classify request
    request_type = arise._classify_request(test_input)
    print(f"Request type: {request_type}")
    
    # Process request (this should use TTS)
    print("Processing request - should speak before displaying text:")
    arise._process_request(test_input)
    
    print("\n3. Testing different request types:")
    
    # Test automation request
    print("\nTesting automation request:")
    arise._process_request("open calculator")
    
    # Test data request  
    print("\nTesting data request:")
    arise._process_request("what's the weather")
    
    print("\n=== Test Complete ===")


if __name__ == "__main__":
    test_arise_tts_flow()
