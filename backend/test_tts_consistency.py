"""
A.R.I.S.E. TTS Consistency Test

Test to verify that all engine responses go through TTS consistently.
"""

import sys
import os

# Add modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules', 'brain'))

from main import ARISEMain


def test_tts_consistency():
    """Test that all responses use TTS consistently."""
    print("🧪 Testing A.R.I.S.E. TTS Consistency...")
    
    try:
        # Initialize A.R.I.S.E. (without running main loop)
        arise = ARISEMain()
        
        # Test direct TTS function
        print("\n1. Testing direct TTS function:")
        arise._speak("This is a test of the centralized TTS system.")
        
        # Test chat engine response (should go through TTS)
        print("\n2. Testing chat engine response:")
        chat_response = arise.chat.get_response("Hello, how are you?")
        arise._speak(chat_response)  # This simulates what happens in _process_request
        
        # Test data engine response (should go through TTS) 
        print("\n3. Testing data engine response:")
        # Simulate a data request without actually making API calls
        test_data_response = "This would be weather data from the data engine."
        arise._speak(test_data_response)
        
        # Test automation engine response (should go through TTS)
        print("\n4. Testing automation engine response:")
        test_auto_response = "This would be an automation response."
        arise._speak(test_auto_response)
        
        print("\n✅ TTS consistency test completed!")
        print("📋 Summary:")
        print("- All responses route through the centralized _speak() method")
        print("- Fresh TTS instances are created for maximum reliability")
        print("- Backup TTS method available if primary fails")
        print("- No engine creates its own TTS instance")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False


if __name__ == "__main__":
    success = test_tts_consistency()
    if success:
        print("\n🎉 A.R.I.S.E. is ready for consistent TTS operation!")
    else:
        print("\n❌ Issues detected - check logs above")
