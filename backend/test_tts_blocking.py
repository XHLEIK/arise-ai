"""
Test TTS blocking behavior to diagnose threading issues.
"""

import sys
import os
import time

# Add modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))

from modules.tts_engine import TTSEngine


def test_tts_blocking():
    """Test if TTS actually blocks execution."""
    print("=== TTS Blocking Test ===")
    
    tts = TTSEngine()
    
    print("1. About to speak - should hear audio BEFORE seeing 'Speech completed'")
    start_time = time.time()
    
    success = tts.speak("This is a test of text to speech blocking.")
    
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"2. Speech completed! Duration: {duration:.2f} seconds")
    print(f"3. TTS success: {success}")
    
    if duration < 1.0:
        print("❌ WARNING: TTS completed too quickly - might not be working!")
    else:
        print("✅ TTS appears to be blocking properly")


def test_main_speak():
    """Test the main _speak method pattern."""
    print("\n=== Main _speak Method Test ===")
    
    def _speak_test(text: str):
        """Simulate main.py _speak method."""
        if not text or not text.strip():
            return
        
        print("About to speak...")
        tts_success = False
        
        try:
            tts_instance = TTSEngine()
            tts_success = tts_instance.speak(text)
        except Exception as e:
            print(f"TTS error: {e}")
        
        # Only print to terminal AFTER TTS completes
        if tts_success:
            print(f"🤖 A.R.I.S.E: {text}")
        else:
            print(f"🤖 A.R.I.S.E (no audio): {text}")
    
    _speak_test("Testing the main speak method pattern")


if __name__ == "__main__":
    test_tts_blocking()
    test_main_speak()
    print("\n=== Test Complete ===")
