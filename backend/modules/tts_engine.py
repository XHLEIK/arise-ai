"""
A.R.I.S.E. AI - Text-to-Speech Engine

Simple, reliable TTS engine for voice output.
"""

import logging

# Suppress pyttsx3 and comtypes logging
logging.getLogger('comtypes').setLevel(logging.WARNING)
logging.getLogger('pyttsx3').setLevel(logging.WARNING)


class TTSEngine:
    """Simple TTS engine for A.R.I.S.E. AI."""
    
    def __init__(self):
        """Initialize the TTS engine."""
        self.engine = None
        self.initialized = False
        
        try:
            import pyttsx3
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', 150)  # Normal speed
            self.engine.setProperty('volume', 1.0)  # Full volume (0.0 to 1.0)
            self.initialized = True
        except Exception as e:
            print(f"TTS error: {e}")
    
    def speak(self, text):
        """
        Speak the given text.
        
        Args:
            text (str): Text to speak
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.initialized or not text.strip():
            return False
        
        try:
            print(f"Speaking: {text}")
            self.engine.say(text)
            self.engine.runAndWait()
            # Clear any remaining speech queue
            self.engine.stop()
            return True
        except Exception as e:
            print(f"TTS error: {e}")
            return False
