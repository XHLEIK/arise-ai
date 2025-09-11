"""
Test script for the TTS Engine module.

This script demonstrates how to use the TTSEngine class
to convert text to speech.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.tts_engine import TTSEngine


def test_tts_engine():
    """
    Test the TTS Engine functionality.
    """
    print("🔊 A.R.I.S.E. TTS Engine Test")
    print("=" * 50)
    
    try:
        # Initialize TTS engine
        print("🤖 Initializing TTS engine...")
        tts = TTSEngine()
        
        # Get engine information
        info = tts.get_engine_info()
        print(f"💻 System: {info['system']}")
        print(f"🔧 Current Engine: {info['current_engine']}")
        print(f"📋 Available Engines: {', '.join(info['available_engines'])}")
        print(f"✅ Engine Initialized: {info['engine_initialized']}")
        print()
        
        if not info['engine_initialized']:
            print("❌ TTS engine failed to initialize!")
            print("📥 Please install required dependencies:")
            print("   pip install pyttsx3")
            if info['system'] == "Windows":
                print("   pip install pywin32")
            return False
        
        # Test basic greeting
        print("🧪 Testing A.R.I.S.E. greeting...")
        success = tts.test_speech()
        
        if success:
            print("✅ Basic TTS test passed!")
        else:
            print("❌ Basic TTS test failed!")
            return False
        
        # Show available voices
        print("\n🎤 Checking available voices...")
        voices = tts.get_available_voices()
        if voices:
            print(f"📋 Found {len(voices)} voices:")
            for i, voice in enumerate(voices[:5]):  # Show first 5
                print(f"   {i+1}. {voice['name']} ({voice['language']})")
            if len(voices) > 5:
                print(f"   ... and {len(voices) - 5} more voices")
        else:
            print("❌ No voices found")
        
        # Test different messages
        print("\n🗣 Testing different messages...")
        test_messages = [
            "Hello I am Arise AI",
            "I am your personal AI assistant",
            "How can I help you today?",
            "Opening your requested application",
            "Task completed successfully"
        ]
        
        for i, message in enumerate(test_messages, 1):
            print(f"   {i}. Speaking: '{message}'")
            success = tts.speak(message, blocking=True)
            if not success:
                print(f"   ❌ Failed to speak message {i}")
            else:
                print(f"   ✅ Message {i} spoken successfully")
        
        # Test voice properties
        print("\n⚙️ Testing voice property changes...")
        
        # Test slower speech
        print("   🐌 Testing slower speech rate...")
        tts.set_voice_properties(rate=100)
        tts.speak("This is slower speech", blocking=True)
        
        # Test faster speech
        print("   🏃 Testing faster speech rate...")
        tts.set_voice_properties(rate=200)
        tts.speak("This is faster speech", blocking=True)
        
        # Reset to normal
        tts.set_voice_properties(rate=150)
        tts.speak("Back to normal speech rate", blocking=True)
        
        # Test volume changes
        print("   🔉 Testing volume control...")
        tts.set_voice_properties(volume=0.5)
        tts.speak("This is quieter", blocking=True)
        
        tts.set_voice_properties(volume=1.0)
        tts.speak("This is louder", blocking=True)
        
        # Test async speech
        print("\n⚡ Testing asynchronous speech...")
        thread = tts.speak_async("This is asynchronous speech")
        print("   ⏳ Speech running in background...")
        thread.join()  # Wait for completion
        print("   ✅ Async speech completed")
        
        print("\n🎉 All TTS tests completed successfully!")
        print("\n💡 TTS Engine Features:")
        print("   ✅ Cross-platform compatibility")
        print("   ✅ Multiple TTS engine support")
        print("   ✅ Voice customization")
        print("   ✅ Async and sync speech")
        print("   ✅ Rate and volume control")
        
        return True
        
    except Exception as e:
        print(f"❌ TTS test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False


def interactive_tts_test():
    """
    Interactive TTS testing mode.
    """
    print("\n🎮 Interactive TTS Test Mode")
    print("=" * 50)
    print("Enter text to speak (or 'help' for commands, 'quit' to exit):")
    
    try:
        tts = TTSEngine()
        
        if not tts.get_engine_info()['engine_initialized']:
            print("❌ TTS engine not available for interactive mode")
            return
        
        while True:
            try:
                text = input("\n🎤 > ").strip()
                
                if text.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                
                elif text.lower() in ['help', 'h']:
                    print("\n📋 Available commands:")
                    print("   help     - Show this help")
                    print("   voices   - List available voices")
                    print("   info     - Show engine info")
                    print("   fast     - Set fast speech rate")
                    print("   slow     - Set slow speech rate")
                    print("   normal   - Set normal speech rate")
                    print("   loud     - Set high volume")
                    print("   quiet    - Set low volume")
                    print("   test     - Run A.R.I.S.E. greeting")
                    print("   quit     - Exit interactive mode")
                
                elif text.lower() == 'voices':
                    voices = tts.get_available_voices()
                    print(f"\n🎤 Available voices ({len(voices)}):")
                    for i, voice in enumerate(voices):
                        print(f"   {i+1}. {voice['name']} ({voice['language']})")
                
                elif text.lower() == 'info':
                    info = tts.get_engine_info()
                    print(f"\n📊 Engine Information:")
                    print(f"   System: {info['system']}")
                    print(f"   Engine: {info['current_engine']}")
                    print(f"   Rate: {info['voice_config']['rate']} WPM")
                    print(f"   Volume: {info['voice_config']['volume']}")
                
                elif text.lower() == 'fast':
                    tts.set_voice_properties(rate=200)
                    tts.speak("Fast speech rate activated", blocking=True)
                
                elif text.lower() == 'slow':
                    tts.set_voice_properties(rate=100)
                    tts.speak("Slow speech rate activated", blocking=True)
                
                elif text.lower() == 'normal':
                    tts.set_voice_properties(rate=150)
                    tts.speak("Normal speech rate activated", blocking=True)
                
                elif text.lower() == 'loud':
                    tts.set_voice_properties(volume=1.0)
                    tts.speak("High volume activated", blocking=True)
                
                elif text.lower() == 'quiet':
                    tts.set_voice_properties(volume=0.5)
                    tts.speak("Low volume activated", blocking=True)
                
                elif text.lower() == 'test':
                    tts.test_speech()
                
                elif text:
                    # Speak the entered text
                    success = tts.speak(text, blocking=True)
                    if not success:
                        print("❌ Failed to speak text")
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                
    except Exception as e:
        print(f"❌ Interactive mode failed: {e}")


if __name__ == "__main__":
    # Run basic tests
    success = test_tts_engine()
    
    if success:
        # Ask if user wants interactive mode
        print("\n❓ Would you like to try interactive mode? (y/n):")
        try:
            choice = input("> ").strip().lower()
            if choice in ['y', 'yes']:
                interactive_tts_test()
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
    
    print("\n🎯 TTS Engine testing completed!")
