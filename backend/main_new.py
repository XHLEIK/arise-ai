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
            
            # Initialize Chat Brain
            print("Initializing Chat Brain...")
            self.chat = ChatBrain()
            
            # Initialize Data Engine  
            print("Initializing Data Engine...")
            self.data = DataEngine()
            
            # Initialize Automation Engine
            print("Initializing Automation Engine...")
            self.automation = AutomationEngine()
            
            # Initialize App Scanner
            print("Initializing App Scanner...")
            self.scanner = ApplicationScanner("data/applications.json")
            
            print("✅ All engines initialized successfully!")
            
        except Exception as e:
            print(f"❌ Engine initialization error: {e}")
            sys.exit(1)
    
    def _check_app_database(self):
        """Step 1: Check if application database exists."""
        print("📋 Checking application database...")
        
        apps_file = Path("data/applications.json")
        
        if not apps_file.exists():
            print("❌ Applications database not found.")
            self._speak("Applications database not found. Should I scan for installed applications?")
            
            response = self.stt.listen_once(timeout=15)
            
            if response and any(word in response.lower() for word in ['yes', 'yeah', 'sure', 'okay', 'ok']):
                self._speak("Starting application scan. This may take a moment...")
                try:
                    apps = self.scanner.run_scan()
                    self.app_database_ready = True
                    self._speak(f"Application scan complete! Found {len(apps)} applications.")
                    print(f"✅ Found {len(apps)} applications")
                except Exception as e:
                    print(f"❌ Scanner error: {e}")
                    self._speak("Application scan failed. I can still help with other tasks.")
            else:
                self._speak("Skipping application scan. I can still help with chat and data requests.")
        else:
            # Check if file has content
            try:
                with open(apps_file, 'r') as f:
                    apps = json.load(f)
                    if len(apps) > 0:
                        self.app_database_ready = True
                        print(f"✅ Application database ready with {len(apps)} applications")
                    else:
                        print("❌ Application database is empty")
            except Exception as e:
                print(f"❌ Error reading application database: {e}")
    
    def _speak(self, text: str):
        """Centralized TTS function - ALL responses go through here."""
        if not text or not text.strip():
            return
            
        print(f"🤖 A.R.I.S.E: {text}")
        
        try:
            # Always create fresh TTS instance for maximum reliability
            tts_instance = TTSEngine()
            success = tts_instance.speak(text)
            
            if not success:
                print("⚠️ TTS failed - trying backup method...")
                # Backup TTS attempt
                try:
                    import pyttsx3
                    backup_engine = pyttsx3.init()
                    backup_engine.setProperty('rate', 150)
                    backup_engine.setProperty('volume', 1.0)
                    backup_engine.say(text)
                    backup_engine.runAndWait()
                    backup_engine.stop()
                    print("✅ Backup TTS successful")
                except Exception as backup_e:
                    print(f"❌ Backup TTS also failed: {backup_e}")
                    
        except Exception as e:
            print(f"❌ TTS error: {e}")
    
    def _greet_user(self):
        """Step 2: Greet user and wait for response."""
        greeting = "Hello! I'm A.R.I.S.E., your AI assistant. I can help with conversations, real-time data, and opening applications. What can I do for you?"
        self._speak(greeting)
    
    def _classify_request(self, user_input: str) -> str:
        """Step 3: Classify user request to determine which engine to use."""
        user_lower = user_input.lower()
        
        # Data engine keywords
        data_keywords = [
            'weather', 'temperature', 'temp', 'hot', 'cold', 'rain', 'sunny', 'climate',
            'news', 'headlines', 'latest', 'happening', 'current events',
            'stock', 'share', 'price', 'trading', 'market', 'nasdaq', 'dow', 'nifty'
        ]
        
        # Automation engine keywords  
        automation_keywords = [
            'open', 'launch', 'start', 'run', 'execute', 'close',
            'visit', 'go to', 'browse', 'navigate'
        ]
        
        # Check for data requests
        if any(keyword in user_lower for keyword in data_keywords):
            return 'data'
            
        # Check for automation requests
        if any(keyword in user_lower for keyword in automation_keywords):
            return 'automation'
            
        # Default to chat for everything else
        return 'chat'
    
    def _process_request(self, user_input: str):
        """Process user request through appropriate engine."""
        request_type = self._classify_request(user_input)
        
        print(f"📍 Request type: {request_type}")
        
        try:
            if request_type == 'data':
                # Data engine request
                response = self.data.process_data_request(user_input)
                self._speak(response)  # All responses go through TTS
                
            elif request_type == 'automation':
                # Automation engine request
                success, message = self.automation.execute_command(user_input)
                if success:
                    response = f"Done! {message}"
                else:
                    response = f"I couldn't do that. {message}"
                self._speak(response)  # All responses go through TTS
                
            else:  # chat
                # Chat brain request
                response = self.chat.get_response(user_input)
                self._speak(response)  # All responses go through TTS
                
        except Exception as e:
            error_msg = "Sorry, I encountered an error processing your request."
            print(f"❌ Request processing error: {e}")
            self._speak(error_msg)  # Even errors go through TTS
    
    def _should_exit(self, user_input: str) -> bool:
        """Check if user wants to exit."""
        exit_phrases = ['bye', 'goodbye', 'exit', 'quit', 'stop', 'end', 'see you later']
        return any(phrase in user_input.lower() for phrase in exit_phrases)
    
    def run(self):
        """Main A.R.I.S.E. execution flow."""
        try:
            # Step 1: Check app database
            self._check_app_database()
            
            # Step 2: Greet user and wait for response
            self._greet_user()
            
            # Step 3 & 4: Main conversation loop
            while True:
                print("\n🎤 Listening for your request...")
                
                # Wait for user input
                user_input = self.stt.listen_once(timeout=30)
                
                if not user_input:
                    continue
                    
                print(f"👤 You: {user_input}")
                
                # Check for exit
                if self._should_exit(user_input):
                    self._speak("Goodbye! Have a great day!")
                    break
                
                # Process request through appropriate engine
                self._process_request(user_input)
                
                # Step 4: Wait for next request (loop continues)
                
        except KeyboardInterrupt:
            self._speak("Goodbye!")
            print("\n👋 A.R.I.S.E. shutting down...")
        except Exception as e:
            error_msg = "I'm experiencing technical difficulties. Shutting down."
            print(f"❌ Main loop error: {e}")
            self._speak(error_msg)


def main():
    """Entry point for A.R.I.S.E. AI Assistant."""
    try:
        # Initialize and run A.R.I.S.E.
        arise = ARISEMain()
        arise.run()
        
    except KeyboardInterrupt:
        print("\n👋 A.R.I.S.E. interrupted by user")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
    finally:
        print("🔌 A.R.I.S.E. offline")


if __name__ == "__main__":
    main()
