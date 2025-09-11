"""
Comprehensive TTS Audio Test
Tests audio output, voices, and system audio capabilities.
"""

import sys
import os
import time

# Add modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))

from modules.tts_engine import TTSEngine


def test_audio_system():
    """Test basic audio system."""
    print("=== Audio System Test ===")
    
    try:
        import pyttsx3
        
        print("1. Initializing pyttsx3 engine...")
        engine = pyttsx3.init()
        
        print("2. Getting audio properties...")
        voices = engine.getProperty('voices')
        rate = engine.getProperty('rate')
        volume = engine.getProperty('volume')
        
        print(f"   Current rate: {rate}")
        print(f"   Current volume: {volume}")
        print(f"   Available voices: {len(voices) if voices else 0}")
        
        if voices:
            for i, voice in enumerate(voices[:3]):  # Show first 3 voices
                print(f"   Voice {i}: {voice.name if hasattr(voice, 'name') else 'Unknown'}")
        
        print("3. Testing basic speech...")
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 1.0)
        
        print("   Speaking test message...")
        engine.say("This is an audio test. Can you hear me?")
        engine.runAndWait()
        print("   Speech completed")
        
        engine.stop()
        print("✅ Basic audio test completed")
        
    except Exception as e:
        print(f"❌ Audio test failed: {e}")
        import traceback
        traceback.print_exc()


def test_tts_engine_detailed():
    """Test TTS engine with detailed output."""
    print("\n=== TTS Engine Detailed Test ===")
    
    tts = TTSEngine()
    
    test_messages = [
        "First test message",
        "Second test with longer text to verify audio duration",
        "Third test with numbers: one, two, three, four, five"
    ]
    
    for i, message in enumerate(test_messages, 1):
        print(f"\nTest {i}: '{message}'")
        print(f"  About to speak... (listen for audio)")
        
        start_time = time.time()
        success = tts.speak(message)
        duration = time.time() - start_time
        
        print(f"  Duration: {duration:.2f}s, Success: {success}")
        
        if duration < 1.0:
            print(f"  ⚠️  Warning: Very short duration, audio might not be working")
        
        time.sleep(0.5)  # Brief pause between tests


def test_volume_levels():
    """Test different volume levels."""
    print("\n=== Volume Level Test ===")
    
    try:
        import pyttsx3
        
        volumes = [0.5, 0.7, 1.0]
        
        for vol in volumes:
            print(f"\nTesting volume {vol}...")
            engine = pyttsx3.init()
            engine.setProperty('volume', vol)
            engine.setProperty('rate', 150)
            
            engine.say(f"Volume test at {int(vol*100)} percent")
            engine.runAndWait()
            engine.stop()
            
            time.sleep(0.5)
            
    except Exception as e:
        print(f"Volume test failed: {e}")


def main():
    print("🔊 Starting Comprehensive TTS Audio Tests")
    print("=" * 50)
    
    test_audio_system()
    test_tts_engine_detailed()  
    test_volume_levels()
    
    print("\n" + "=" * 50)
    print("🎯 Test Summary:")
    print("If you heard audio for each test, TTS is working correctly.")
    print("If you heard NO audio, check:")
    print("  - Speaker/headphone connection")
    print("  - System volume levels")
    print("  - Windows audio output device")
    print("  - Audio drivers")


if __name__ == "__main__":
    main()
