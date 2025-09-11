"""
Speech-to-Text Engine for A.R.I.S.E. AI Assistant

Minimal STT implementation using speech_recognition with 48kHz sample rate.
"""

import speech_recognition as sr
import logging
from typing import Optional
from tts_engine import TTSEngine

# Suppress verbose logging
logging.getLogger("speech_recognition").setLevel(logging.WARNING)


class STTEngine:
    """Speech-to-Text engine with microphone input."""
    
    def __init__(self, sample_rate: int = 48000):
        """Initialize STT engine with specified sample rate."""
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone(sample_rate=sample_rate)
        # Don't initialize TTS here to avoid threading issues
        
        # Calibrate microphone for ambient noise
        print("Calibrating microphone...")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Ready to listen.")
    
    def listen_once(self, timeout: int = 5) -> Optional[str]:
        """
        Listen for speech and convert to text.
        
        Args:
            timeout: Max seconds to wait for speech
            
        Returns:
            Recognized text or None if failed
            
        Time: O(n) where n is audio duration, Space: O(1)
        """
        try:
            with self.microphone as source:
                print("Listening...")
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=5)
            
            print("Processing...")
            text = self.recognizer.recognize_google(audio)
            return text
            
        except sr.WaitTimeoutError:
            print("No speech detected")
            return None
        except sr.UnknownValueError:
            print("Could not understand audio")
            return None
        except Exception as e:
            print(f"STT error: {e}")
            return None
    
    def listen_and_respond(self):
        """Listen for user speech and respond via TTS."""
        text = self.listen_once()
        if text:
            response = f'You said "{text}"'
            print(response)
            # Create fresh TTS instance for each response to avoid threading issues
            tts = TTSEngine()
            tts.speak(response)
        return text


def main():
    """Test STT engine standalone."""
    stt = STTEngine()
    
    try:
        while True:
            result = stt.listen_and_respond()
            if result and "stop" in result.lower():
                print("Stopping...")
                break
    except KeyboardInterrupt:
        print("\nStopped by user")


if __name__ == "__main__":
    main()
