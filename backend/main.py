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
from modules.memory_manager import MemoryManager


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
        self.memory = None
        
        # System state
        self.running = False
        self.app_database_ready = False
        self.standby_mode = False
        
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
            
            # Initialize Memory Manager (needed by other engines)
            print("Initializing Memory Manager...")
            self.memory = MemoryManager()
            
            # Initialize Chat Brain
            print("Initializing Chat Brain...")
            self.chat = ChatBrain()
            
            # Initialize Data Engine with memory manager
            print("Initializing Data Engine...")
            self.data = DataEngine(self.memory)
            
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
        
        # IMPORTANT: Speak FIRST, then display text
        tts_success = False
        
        try:
            # Always create fresh TTS instance for maximum reliability
            tts_instance = TTSEngine()
            tts_success = tts_instance.speak(text)
            
            if not tts_success:
                print("⚠️ Primary TTS failed - trying backup method...")
                # Backup TTS attempt
                try:
                    import pyttsx3
                    backup_engine = pyttsx3.init()
                    backup_engine.setProperty('rate', 150)
                    backup_engine.setProperty('volume', 1.0)
                    backup_engine.say(text)
                    backup_engine.runAndWait()
                    backup_engine.stop()
                    tts_success = True
                    print("✅ Backup TTS successful")
                except Exception as backup_e:
                    print(f"❌ Backup TTS also failed: {backup_e}")
                    
        except Exception as e:
            print(f"❌ TTS error in _speak(): {e}")
        
        # Only print to terminal AFTER TTS completes (successful or not)
        if tts_success:
            print(f"🤖 A.R.I.S.E: {text}")
        else:
            print(f"🤖 A.R.I.S.E (no audio): {text}")
    
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
        
        # Memory deletion keywords
        memory_deletion_keywords = [
            'delete memory', 'remove memory', 'clear memory', 'forget everything',
            'erase memory', 'wipe memory', 'reset memory', 'delete sessions',
            'clear sessions', 'forget all', 'delete all memory', 'delete my memory',
            'clear the memory', 'remove all memory', 'wipe all memory'
        ]
        
        # Standby mode keywords
        standby_keywords = [
            'go to standby', 'standby mode', 'go to sleep', 'sleep mode',
            'stand by', 'enter standby', 'go standby', 'sleep now'
        ]
        
        # Check for standby requests
        if any(keyword in user_lower for keyword in standby_keywords):
            return 'standby'
        
        # Check for memory deletion requests
        if any(keyword in user_lower for keyword in memory_deletion_keywords):
            return 'memory_delete'
        
        # Check for data requests
        if any(keyword in user_lower for keyword in data_keywords):
            return 'data'
            
        # Check for automation requests
        if any(keyword in user_lower for keyword in automation_keywords):
            return 'automation'
            
        # Default to chat for everything else
        return 'chat'
    
    def _build_memory_context(self) -> str:
        """Build context string from recent session and facts for AI."""
        context_parts = []
        
        # Add facts from long-term memory
        facts = self.memory.load_facts()
        if facts:
            facts_text = ", ".join([f"{k}: {v}" for k, v in facts.items()])
            context_parts.append(f"User facts: {facts_text}")
        
        # Add recent conversation from session buffer (last 5 messages)
        if self.memory.session_buffer:
            recent_messages = self.memory.session_buffer[-10:]  # Last 10 messages for context
            conversation = []
            for msg in recent_messages:
                role = "User" if msg["role"] == "user" else "AI"
                conversation.append(f"{role}: {msg['content']}")
            if conversation:
                context_parts.append(f"Recent conversation: {' | '.join(conversation)}")
        
        return " | ".join(context_parts) if context_parts else ""
    
    def _extract_and_update_facts(self, user_input: str, ai_response: str):
        """Extract important facts from conversation and update long-term memory."""
        # Simple fact extraction for location, name, preferences
        facts_to_update = {}
        
        # Extract location information
        location_keywords = ['live in', 'from', 'located in', 'based in', 'i am in']
        for keyword in location_keywords:
            if keyword in user_input.lower():
                # Simple extraction - this could be made more sophisticated
                words = user_input.lower().split()
                try:
                    keyword_index = next(i for i, word in enumerate(words) if keyword.split()[0] in word)
                    # Get the next 1-2 words after the keyword
                    if keyword_index + 1 < len(words):
                        location = words[keyword_index + 1]
                        if keyword_index + 2 < len(words) and len(words[keyword_index + 2]) > 2:
                            location += f" {words[keyword_index + 2]}"
                        facts_to_update['location'] = location.title()
                except:
                    pass
        
        # Extract name information
        if 'my name is' in user_input.lower() or 'i am' in user_input.lower():
            words = user_input.lower().split()
            try:
                if 'my name is' in user_input.lower():
                    name_index = user_input.lower().find('my name is') + len('my name is')
                    name = user_input[name_index:].strip().split()[0]
                    facts_to_update['name'] = name.title()
                elif 'i am' in user_input.lower() and len(words) > 2:
                    i_am_index = next(i for i, word in enumerate(words) if word == 'i' and i+1 < len(words) and words[i+1] == 'am')
                    if i_am_index + 2 < len(words):
                        name = words[i_am_index + 2]
                        if name.isalpha() and len(name) > 1:
                            facts_to_update['name'] = name.title()
            except:
                pass
        
        # Update facts if any were extracted
        if facts_to_update:
            self.memory.update_facts(facts_to_update)
    
    def _process_request(self, user_input: str):
        """Process user request through appropriate engine."""
        request_type = self._classify_request(user_input)
        
        print(f"📍 Request type: {request_type}")
        
        try:
            if request_type == 'standby':
                # Standby mode request
                self.standby_mode = True
                response = "Going to standby mode. Say 'Hey arise' or 'Hey A.R.I.S.E.' to wake me up."
                self._speak(response)
                self.memory.add_message("assistant", response)
                # Enter standby mode
                self._enter_standby_mode()
                
            elif request_type == 'memory_delete':
                # Memory deletion request
                stats = self.memory.get_memory_stats()
                success = self.memory.delete_all_sessions()
                
                if success:
                    response = f"Memory cleared! I deleted {stats['saved_sessions']} session files and cleared the current conversation buffer. I've forgotten all our previous conversations but I still remember your stored facts."
                else:
                    response = "I had trouble clearing the memory. Some files might still remain."
                
                self._speak(response)
                # Note: We don't add this to memory since we just cleared it
                
            elif request_type == 'data':
                # Data engine request
                response = self.data.process_data_request(user_input)
                self._speak(response)  # All responses go through TTS
                self.memory.add_message("assistant", response)
                
            elif request_type == 'automation':
                # Automation engine request
                success, message = self.automation.execute_command(user_input)
                if success:
                    response = f"Done! {message}"
                else:
                    response = f"I couldn't do that. {message}"
                self._speak(response)  # All responses go through TTS
                self.memory.add_message("assistant", response)
                
            else:  # chat
                # Chat brain request with memory context
                memory_context = self._build_memory_context()
                response = self.chat.get_response(user_input, memory_context)
                self._speak(response)  # All responses go through TTS
                self.memory.add_message("assistant", response)
                
                # Extract and store important facts from conversation
                self._extract_and_update_facts(user_input, response)
                
        except Exception as e:
            error_msg = "Sorry, I encountered an error processing your request."
            print(f"❌ Request processing error: {e}")
            self._speak(error_msg)  # Even errors go through TTS
            self.memory.add_message("assistant", error_msg)
    
    def _should_exit(self, user_input: str) -> bool:
        """Check if user wants to exit."""
        exit_phrases = ['bye', 'goodbye', 'exit', 'quit', 'stop', 'end', 'see you later']
        return any(phrase in user_input.lower() for phrase in exit_phrases)
    
    def _enter_standby_mode(self):
        """Enter standby mode, listen only for wake command."""
        print("💤 Entering standby mode... Say 'Hey arise' or 'arise' to wake up")
        
        while self.standby_mode:
            try:
                # Listen for wake command only
                user_input = self.stt.listen_once(timeout=60)  # Longer timeout in standby
                
                if user_input:
                    user_lower = user_input.lower()
                    
                    # Check for wake commands - more flexible detection
                    wake_commands = [
                        'hey arise', 'hey a.r.i.s.e', 'hey a r i s e',
                        'arise wake up', 'wake up arise', 'arise',
                        'hey arize', 'hey a rise', 'wake arise',
                        'a.r.i.s.e', 'arrise', 'a rise'
                    ]
                    
                    # Also check if "arise" appears anywhere in the input
                    contains_arise = any(word in user_lower for word in ['arise', 'arize', 'a.r.i.s.e', 'arrise'])
                    
                    if any(wake_cmd in user_lower for wake_cmd in wake_commands) or contains_arise:
                        self.standby_mode = False
                        response = "I'm awake! How can I help you?"
                        self._speak(response)
                        self.memory.add_message("assistant", response)
                        print("🔄 Exiting standby mode")
                        break
                    else:
                        # Ignore other commands in standby mode
                        print(f"💤 In standby - ignoring: {user_input}")
                        
            except KeyboardInterrupt:
                # Allow Ctrl+C to exit standby
                self.standby_mode = False
                print("\n🔄 Forced exit from standby mode")
                break
            except Exception as e:
                # Handle any other errors gracefully
                print(f"Error in standby mode: {e}")
                continue
    
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
                
                # Add user input to memory
                self.memory.add_message("user", user_input)
                
                # Check for exit
                if self._should_exit(user_input):
                    response = "Goodbye! Have a great day!"
                    self._speak(response)
                    self.memory.add_message("assistant", response)
                    # Save session before exit
                    self.memory.save_session()
                    break
                
                # Process request through appropriate engine
                self._process_request(user_input)
                
                # Step 4: Wait for next request (loop continues)
                
        except KeyboardInterrupt:
            response = "Goodbye!"
            self._speak(response)
            self.memory.add_message("assistant", response)
            # Save session before shutdown
            self.memory.save_session()
            print("\n👋 A.R.I.S.E. shutting down...")
        except Exception as e:
            error_msg = "I'm experiencing technical difficulties. Shutting down."
            print(f"❌ Main loop error: {e}")
            self._speak(error_msg)
            self.memory.add_message("assistant", error_msg)
            # Save session even on error
            self.memory.save_session()


def main():
    """Entry point for A.R.I.S.E. AI Assistant."""
    try:
        # Initialize and run A.R.I.S.E.
        arise = ARISEMain()
        arise.run()
        
    except KeyboardInterrupt:
        print("\n👋 A.R.I.S.E. interrupted by user")
        # Ensure session is saved if arise instance exists
        if 'arise' in locals() and hasattr(arise, 'memory'):
            arise.memory.save_session()
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        # Ensure session is saved if arise instance exists
        if 'arise' in locals() and hasattr(arise, 'memory'):
            arise.memory.save_session()
    finally:
        print("🔌 A.R.I.S.E. offline")


if __name__ == "__main__":
    main()
