"""
A.R.I.S.E. AI Assistant - Main Entry Point

Advanced Real-time Intelligent System for Execution

Simple Flow:
1. Check app database
2. Greet user and wait for response
3. Route to appropriate engine (chat/data/automation)
4. All responses go through TTS for consistent voice output
5. Wait for next request
"""

import os
import sys
import json
from pathlib import Path

# Add modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules', 'brain'))

from modules.tts_engine import TTSEngine
from modules.stt_engine import STTEngine
from modules.app_scanner import ApplicationScanner
from modules.automation_engine import AutomationEngine
from modules.brain.chat_brain import ChatBrain
from modules.brain.data_engine import DataEngine


class ARISEMain:
    """Main A.R.I.S.E. orchestrator with centralized TTS."""
    
    def __init__(self):
        """Initialize all engines."""
        print("🚀 Initializing A.R.I.S.E...")
        
        # Engine instances
        self.tts = None
        self.stt = None
        self.scanner = None  
        self.automation = None
        self.chat = None
        self.data = None
        
        # System state
        self.running = False
        self.app_database_ready = False
        
        # Initialize all engines
        self._init_engines()
        
        print("✅ A.R.I.S.E. initialization complete!")
    
    def _init_engines(self):
        """Initialize all engines independently."""
        try:
            # Initialize TTS first (most important for consistent voice output)
            print("Initializing TTS engine...")
            self.tts = TTSEngine()
            
            # Initialize STT
            print("Initializing STT engine...")
            self.stt = STTEngine()
            self.automation = AutomationEngine()
            self.data = DataEngine()
            # Don't create chat brain with duplicate engines - just create the AI model interface
            self.chat = ChatBrain()
            self.scanner = ApplicationScanner("data/applications.json")
        except Exception as e:
            print(f"Engine init error: {e}")
    
    def _check_applications(self):
        """Check if applications.json exists, ask user if scan needed."""
        apps_file = Path("data/applications.json")
        
        if not apps_file.exists() or apps_file.stat().st_size == 0:
            # Keep asking until we get a clear answer
            max_attempts = 3
            attempt = 0
            
            while attempt < max_attempts:
                if attempt == 0:
                    self._speak("Applications database missing. Should I scan for apps? Please say yes or no.")
                else:
                    self._speak("I couldn't understand. Should I scan for applications? Please say yes or no clearly.")
                
                response = self.stt.listen_once(timeout=15)
                
                if response:
                    response_lower = response.lower()
                    if any(word in response_lower for word in ['yes', 'yeah', 'sure', 'okay', 'ok']):
                        self._speak("Starting application scan...")
                        try:
                            apps = self.scanner.run_scan()
                            self._speak(f"Scan complete. Found {len(apps)} applications.")
                            return
                        except Exception as e:
                            print(f"Scanner error: {e}")
                            self._speak("Application scan failed. Continuing without scan.")
                            return
                    elif any(word in response_lower for word in ['no', 'nope', 'skip']):
                        self._speak("Skipping application scan.")
                        return
                
                attempt += 1
            
            # If we still can't understand after max attempts
            self._speak("I'll skip the application scan for now. You can run it later if needed.")
    
    def _speak(self, text: str):
        """Speak and print response with maximum reliability."""
        print(f"A.R.I.S.E: {text}")
        
        try:
            # Create fresh TTS instance for maximum reliability
            tts = TTSEngine()
            success = tts.speak(text)
            if not success:
                print("TTS failed - audio output unavailable")
        except Exception as e:
            print(f"TTS error: {e}")
            # One more attempt with direct pyttsx3 call
            try:
                import pyttsx3
                engine = pyttsx3.init()
                engine.setProperty('rate', 150)
                engine.setProperty('volume', 1.0)
                print(f"Backup TTS speaking: {text}")
                engine.say(text)
                engine.runAndWait()
                engine.stop()
            except Exception as backup_error:
                print(f"Backup TTS also failed: {backup_error}")
    
    def _is_data_request(self, text: str) -> bool:
        """Check if request is for real-time data."""
        data_keywords = ['weather', 'news', 'stock', 'price', 'temperature', 'headlines']
        return any(word in text.lower() for word in data_keywords)
    
    def _is_automation_request(self, text: str) -> bool:
        """Check if request is for automation."""
        auto_keywords = ['open', 'launch', 'start', 'run', 'execute', 'visit', 'go to']
        return any(word in text.lower() for word in auto_keywords)
    
    def _process_request(self, user_input: str):
        """Route request to appropriate engine."""
        try:
            # Data requests
            if self._is_data_request(user_input):
                response = self.data.process_data_request(user_input)
                if response:
                    self._speak(response)
                    return
            
            # Automation requests  
            if self._is_automation_request(user_input):
                success, message = self.automation.execute_command(user_input)
                response = f"Sure! {message}" if success else f"Sorry, {message}"
                self._speak(response)
                return
            
            # Chat requests
            response = self.chat.get_response(user_input)
            self._speak(response)
            
        except Exception as e:
            print(f"Request error: {e}")
            self._speak("Sorry, I had trouble with that.")
    
    def run(self):
        """Main conversation loop."""
        # Initial greeting
        self._speak("Hello — ARISE is online. How can I help?")
        
        while True:
            try:
                # Listen for user input with extended timeout
                user_input = self.stt.listen_once(timeout=20)
                
                if not user_input:
                    continue
                
                print(f"You: {user_input}")
                
                # Check for exit
                if any(word in user_input.lower() for word in ['bye', 'goodbye', 'quit', 'exit', 'stop']):
                    self._speak("Goodbye!")
                    break
                
                # Process request
                self._process_request(user_input)
                
            except KeyboardInterrupt:
                self._speak("Goodbye!")
                break
            except Exception as e:
                print(f"Loop error: {e}")


def main():
    """Entry point."""
    try:
        arise = ARISEMain()
        arise.run()
    except KeyboardInterrupt:
        print("\nShutdown")
    except Exception as e:
        print(f"Fatal error: {e}")


if __name__ == "__main__":
    main()