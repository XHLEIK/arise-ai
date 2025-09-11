"""
A.R.I.S.E. AI - Chat Brain Module

Natural conversation using Gemini 2.5 Flash with STT/TTS integration.
"""

import os
import sys
sys.path.append('..')

import google.generativeai as genai
from dotenv import load_dotenv
from stt_engine import STTEngine
from tts_engine import TTSEngine
from data_engine import DataEngine
from automation_engine import AutomationEngine

# Load environment variables
load_dotenv()


class ChatBrain:
    """AI chat brain using Gemini 2.5 Flash for natural conversation."""
    
    def __init__(self):
        """Initialize chat brain with Gemini API and STT/TTS engines."""
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        # Configure Gemini
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        # Initialize engines
        self.stt = STTEngine()
        self.data_engine = DataEngine()
        self.automation = AutomationEngine()
        # Don't initialize TTS here to avoid threading issues
        
        # System prompt for short, human-like responses
        self.system_prompt = """You are A.R.I.S.E. AI, made by Subham — a smart, reliable, and witty assistant that feels like a helpful human friend.

Keep responses short (1–3 sentences), clear, and natural.

Sound conversational, never robotic or overly formal.

Be friendly but not overly enthusiastic.

Use light humor and playful wit when it fits, like casual banter.

Acknowledge emotions briefly and naturally, like a real friend.

Avoid filler or corporate-sounding phrases.

Balance usefulness with personality in every reply.
"""
        
        print("Chat brain initialized. Ready to talk!")
    
    def get_response(self, user_input: str) -> str:
        """
        Get AI response from Gemini 2.5 Flash.
        
        Args:
            user_input: User's message
            
        Returns:
            AI response text
            
        Time: O(1), Space: O(1)
        """
        try:
            prompt = f"{self.system_prompt}\n\nUser: {user_input}\nARISE AI:"
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"AI error: {e}")
            return "Sorry, I'm having trouble processing that right now."
    
    def should_stop(self, text: str) -> bool:
        """Check if user wants to stop the conversation."""
        stop_words = ['stop', 'end', 'bye', 'goodbye', 'quit', 'exit']
        return any(word in text.lower() for word in stop_words)
    
    def is_automation_request(self, text: str) -> bool:
        """Check if user is requesting to open an app or website."""
        automation_keywords = [
            'open', 'launch', 'start', 'run', 'execute', 
            'go to', 'visit', 'browse to', 'navigate to'
        ]
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in automation_keywords)
    
    def speak_response(self, text: str):
        """
        Speak a response with reliable TTS engine.
        
        Args:
            text: Text to speak
        """
        try:
            # Create fresh TTS instance for each response
            tts = TTSEngine()
            if tts.initialized:
                tts.speak(text)
            else:
                print("TTS not available")
        except Exception as e:
            print(f"TTS error: {e}")
            # Try one more time with a new instance
            try:
                tts = TTSEngine()
                tts.speak(text)
            except:
                print("TTS failed completely")

    def greet_user(self):
        """Greet the user using TTS."""
        greeting = "Hello! I'm ARISE AI. How can I help you today?"
        print(f"AI: {greeting}")
        self.speak_response(greeting)
    
    def chat_loop(self):
        """Main conversation loop with STT/TTS integration."""
        self.greet_user()
        
        while True:
            # Get user input via STT
            user_input = self.stt.listen_once(timeout=10)
            
            if not user_input:
                continue
                
            print(f"You: {user_input}")
            
            # Check for stop commands
            if self.should_stop(user_input):
                goodbye = "Goodbye! Have a great day!"
                print(f"AI: {goodbye}")
                self.speak_response(goodbye)
                break
            
            # Check for data requests first (weather, news, stock)
            data_response = self.data_engine.process_data_request(user_input)
            if data_response:
                print(f"AI: {data_response}")
                # Data engine already handles TTS, so continue to next iteration
                continue
            
            # Check for automation requests (open apps/websites)
            if self.is_automation_request(user_input):
                success, message = self.automation.execute_command(user_input)
                if success:
                    response = f"Sure! {message}"
                else:
                    response = f"I couldn't do that. {message}"
                print(f"AI: {response}")
                self.speak_response(response)
                continue
            
            # Get AI response for regular chat
            ai_response = self.get_response(user_input)
            print(f"AI: {ai_response}")
            
            # Speak response with reliable TTS
            self.speak_response(ai_response)


def main():
    """Start the chat conversation."""
    try:
        brain = ChatBrain()
        brain.chat_loop()
    except KeyboardInterrupt:
        print("\nChat ended by user")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
