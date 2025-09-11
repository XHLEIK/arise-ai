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
        Speak the given text with maximum reliability.
        
        Args:
            text (str): Text to speak
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not text.strip():
            return False
        
        try:
            import pyttsx3
            import time
            
            # Calculate expected speech duration
            word_count = len(text.split())
            char_count = len(text)
            # Conservative estimate: ~2 words per second + pause time
            estimated_duration = max(2.5, (word_count / 2.0) + 1.0)
            
            print(f"TTS: Speaking {word_count} words, estimated {estimated_duration:.1f}s")
            
            # Method 1: Complete engine recreation for maximum reliability
            try:
                # Force complete cleanup of any existing engine
                try:
                    if hasattr(self, 'engine') and self.engine:
                        self.engine.stop()
                        del self.engine
                except:
                    pass
                
                # Create completely fresh engine instance
                engine = pyttsx3.init(driverName='sapi5')  # Explicitly use Windows SAPI
                
                # Set properties
                voices = engine.getProperty('voices')
                if voices and len(voices) > 0:
                    engine.setProperty('voice', voices[0].id)
                
                engine.setProperty('rate', 120)  # Slower for reliability
                engine.setProperty('volume', 1.0)  # Full volume
                
                print(f"TTS: Using voice engine, speaking now...")
                
                start_time = time.time()
                engine.say(text)
                engine.runAndWait()
                actual_duration = time.time() - start_time
                
                # Force minimum wait time if completed too quickly (indicates audio didn't play)
                if actual_duration < (estimated_duration * 0.3):
                    remaining_wait = estimated_duration - actual_duration
                    print(f"TTS: Audio likely didn't play, forcing wait of {remaining_wait:.1f}s...")
                    time.sleep(remaining_wait)
                    actual_duration += remaining_wait
                
                # Complete cleanup
                engine.stop()
                del engine
                
                print(f"✅ TTS completed in {actual_duration:.1f}s")
                return True
                
            except Exception as method1_error:
                print(f"Method 1 failed: {method1_error}")
            
            # Method 2: Try alternative driver
            try:
                print("TTS: Trying alternative method...")
                
                # Try different initialization
                engine2 = pyttsx3.init()
                
                # Reset all properties
                voices = engine2.getProperty('voices')
                if voices and len(voices) > 1:  # Try second voice if available
                    engine2.setProperty('voice', voices[1].id)
                elif voices:
                    engine2.setProperty('voice', voices[0].id)
                
                engine2.setProperty('rate', 100)  # Even slower
                engine2.setProperty('volume', 1.0)
                
                engine2.say(text)
                engine2.runAndWait()
                
                # Always wait the full estimated duration
                print(f"TTS: Waiting full {estimated_duration:.1f}s for audio completion...")
                time.sleep(estimated_duration)
                
                engine2.stop()
                del engine2
                
                print("✅ Alternative TTS method completed")
                return True
                
            except Exception as method2_error:
                print(f"Method 2 failed: {method2_error}")
            
            # Method 3: Desperate fallback with system restart
            try:
                print("TTS: Final fallback method...")
                
                # Small delay to let system settle
                time.sleep(0.5)
                
                engine3 = pyttsx3.init(driverName='sapi5')
                engine3.setProperty('rate', 140)
                engine3.setProperty('volume', 1.0)
                
                # Try to ensure audio system is ready
                engine3.say(".")  # Tiny test sound
                engine3.runAndWait()
                time.sleep(0.2)
                
                # Now speak the actual text
                engine3.say(text)
                engine3.runAndWait()
                
                # Force wait based on word count
                forced_wait = max(2.0, word_count * 0.4)
                print(f"TTS: Forced wait {forced_wait:.1f}s...")
                time.sleep(forced_wait)
                
                engine3.stop()
                del engine3
                
                print("✅ Fallback TTS completed")
                return True
                
            except Exception as method3_error:
                print(f"All TTS methods failed: {method3_error}")
                return False
            
        except Exception as e:
            print(f"TTS system error: {e}")
            return False
