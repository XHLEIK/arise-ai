"""
Speech-to-Text Engine for A.R.I.S.E. AI Assistant

Pure STT implementation using speech_recognition with 48kHz sample rate.
Returns text responses only. No TTS or other engine dependencies.
"""

import speech_recognition as sr
import logging
from typing import Optional

# Suppress verbose logging
logging.getLogger("speech_recognition").setLevel(logging.WARNING)


class STTEngine:
    """Pure Speech-to-Text engine with microphone input. Text responses only."""
    
    def __init__(self, sample_rate: int = 48000):
        """Initialize STT engine with specified sample rate."""
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone(sample_rate=sample_rate)
        
        # Calibrate microphone for ambient noise
        print("STT engine initialized - Calibrating microphone...")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
        print("STT ready to listen.")
    
    def listen_once(self, timeout: int = 15) -> Optional[str]:
        """
        Listen for speech and convert to text with extended timeout.
        
        Args:
            timeout: Max seconds to wait for speech (default 15s)
            
        Returns:
            Recognized text or None if failed
            
        Time: O(n) where n is audio duration, Space: O(1)
        """
        try:
            with self.microphone as source:
                print("Listening... (speak now, I'll wait for you to finish)")
                # Longer phrase_time_limit allows complete sentences
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=10)
            
            print("Processing speech...")
            text = self.recognizer.recognize_google(audio)
            return text
            
        except sr.WaitTimeoutError:
            print("No speech detected in time limit")
            return None
        except sr.UnknownValueError:
            print("Could not understand audio - try speaking more clearly")
            return None
        except Exception as e:
            print(f"STT error: {e}")
            return None
    
    def listen_and_respond(self):
        """Listen for user speech and respond via print (TTS handled elsewhere)."""
        text = self.listen_once()
        if text:
            response = f'You said "{text}"'
            print(response)
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
