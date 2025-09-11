"""
A.R.I.S.E. AI - Chat Brain Module

Pure text-based chat using Gemini 2.5 Flash. Returns text responses only.
No TTS, STT, or other engine dependencies.
"""

import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class ChatBrain:
    """Pure text-based AI chat using Gemini 2.5 Flash."""
    
    def __init__(self):
        """Initialize chat brain with Gemini API only."""
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        # Configure Gemini
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
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
        
        print("Chat brain initialized. Text-only mode.")
    
    def get_response(self, user_input: str) -> str:
        """
        Get AI response from Gemini 2.5 Flash.
        
        Args:
            user_input: User's message
            
        Returns:
            AI response text only
            
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
    
    def chat_loop(self):
        """Simple text-based chat loop using keyboard input."""
        print("A.R.I.S.E. Chat Brain - Text Mode")
        print("Type your messages and press Enter. Type 'bye' to exit.")
        print("-" * 50)
        
        while True:
            try:
                # Get user input from keyboard
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                # Check for stop commands
                if self.should_stop(user_input):
                    print("AI: Goodbye! Have a great day!")
                    break
                
                # Get AI response for chat only
                ai_response = self.get_response(user_input)
                print(f"AI: {ai_response}")
                
            except KeyboardInterrupt:
                print("\nAI: Goodbye! Chat ended by user.")
                break
            except Exception as e:
                print(f"Error: {e}")


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
