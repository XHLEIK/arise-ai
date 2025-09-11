# Explanation: Pure automation engine to open applications and websites based on user commands
# Assumptions: applications.json exists with app paths, default browser handles URLs, subprocess can launch apps
# Files to create: backend/modules/automation_engine.py
# Run commands: python automation_engine.py

"""
A.R.I.S.E. AI - Automation Engine

Pure automation engine for opening applications and websites. Returns text responses only.
No TTS, STT, or other engine dependencies.
"""

import json
import os
import subprocess
import webbrowser
import re
from typing import Dict, Optional, Tuple

class AutomationEngine:
    """Pure automation engine for opening applications and websites. Text responses only."""
    def __init__(self):
        """Initialize automation engine with applications database."""
        self.applications = {}
        self.load_applications()
        print("Automation engine initialized - Pure automation mode only")
    
    def load_applications(self) -> None:
        """Load applications from applications.json file"""
        try:
            app_file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'applications.json')
            with open(app_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.applications = data.get('applications', {})
            print(f"Loaded {len(self.applications)} applications")
        except FileNotFoundError:
            print("Applications file not found. Please run app_scanner.py first.")
        except Exception as e:
            print(f"Error loading applications: {e}")
    
    def find_application(self, app_name: str) -> Optional[Tuple[str, str]]:
        """Find application by name (fuzzy matching)"""
        # Time: O(n), Space: O(1)
        app_name_lower = app_name.lower()
        
        # Exact match first
        for name, path in self.applications.items():
            if name.lower() == app_name_lower:
                return (name, path)
        
        # Partial match
        for name, path in self.applications.items():
            if app_name_lower in name.lower() or name.lower() in app_name_lower:
                return (name, path)
        
        # Keyword matching for common app names
        app_keywords = {
            'word': 'Microsoft Word',
            'excel': 'Microsoft Excel',
            'powerpoint': 'Microsoft PowerPoint',
            'ppt': 'Microsoft PowerPoint',
            'outlook': 'Microsoft Outlook',
            'notepad': 'Notepad',
            'calculator': 'Calculator',
            'paint': 'Paint',
            'chrome': 'Google Chrome',
            'firefox': 'Firefox',
            'edge': 'Microsoft Edge',
            'brave': 'Brave',
            'code': 'Visual Studio Code',
            'vscode': 'Visual Studio Code',
            'vs code': 'Visual Studio Code',
            'visual studio': 'Visual Studio',
            'pycharm': 'PyCharm',
            'steam': 'Steam',
            'discord': 'Discord',
            'spotify': 'Spotify',
            'vlc': 'VLC',
            'photoshop': 'Adobe Photoshop',
            'illustrator': 'Adobe Illustrator',
            'store': 'WindowsStore',
            'microsoft store': 'WindowsStore',
            'windows store': 'WindowsStore',
            'terminal': 'WindowsTerminal',
            'windows terminal': 'WindowsTerminal',
            'camera': 'WindowsCamera',
            'windows camera': 'WindowsCamera',
            'todos': 'Todos',
            'to do': 'Todos',
            'teams': 'MSTeams',
            'ms teams': 'MSTeams',
            'microsoft teams': 'MSTeams'
        }
        
        for keyword, app_name_mapped in app_keywords.items():
            if keyword in app_name_lower:
                for name, path in self.applications.items():
                    if app_name_mapped.lower() in name.lower():
                        return (name, path)
        
        return None
    
    def is_url(self, text: str) -> bool:
        """Check if text is a URL or website"""
        # Common URL patterns
        url_patterns = [
            r'https?://',  # http:// or https://
            r'www\.',      # www.
            r'\.com\b',    # .com
            r'\.org\b',    # .org
            r'\.net\b',    # .net
            r'\.edu\b',    # .edu
            r'\.gov\b',    # .gov
            r'\.co\.',     # .co.uk, .co.in, etc.
        ]
        
        text_lower = text.lower()
        for pattern in url_patterns:
            if re.search(pattern, text_lower):
                return True
        
        # Check for common website names
        website_keywords = [
            'google', 'youtube', 'facebook', 'twitter', 'instagram', 
            'linkedin', 'github', 'stackoverflow', 'reddit', 'wikipedia',
            'amazon', 'netflix', 'gmail', 'yahoo', 'bing', 'duckduckgo'
        ]
        
        for keyword in website_keywords:
            if keyword in text_lower:
                return True
        
        return False
    
    def format_url(self, text: str) -> str:
        """Format text to a proper URL"""
        text = text.strip()
        
        # If already has protocol, return as is
        if text.startswith(('http://', 'https://')):
            return text
        
        # If starts with www, add https://
        if text.startswith('www.'):
            return f"https://{text}"
        
        # Common website mappings (most popular first for speed)
        website_mappings = {
            'facebook': 'https://www.facebook.com',
            'fb': 'https://www.facebook.com',
            'google': 'https://www.google.com',
            'youtube': 'https://www.youtube.com',
            'gmail': 'https://mail.google.com',
            'twitter': 'https://www.twitter.com',
            'instagram': 'https://www.instagram.com',
            'insta': 'https://www.instagram.com',
            'linkedin': 'https://www.linkedin.com',
            'github': 'https://www.github.com',
            'stackoverflow': 'https://stackoverflow.com',
            'stack overflow': 'https://stackoverflow.com',
            'reddit': 'https://www.reddit.com',
            'wikipedia': 'https://www.wikipedia.org',
            'wiki': 'https://www.wikipedia.org',
            'amazon': 'https://www.amazon.com',
            'netflix': 'https://www.netflix.com',
            'yahoo': 'https://www.yahoo.com',
            'bing': 'https://www.bing.com',
            'duckduckgo': 'https://duckduckgo.com'
        }
        
        text_lower = text.lower()
        
        # Fast exact match first
        if text_lower in website_mappings:
            return website_mappings[text_lower]
        
        # Then check for partial matches
        for keyword, url in website_mappings.items():
            if keyword in text_lower:
                return url
        
        # If contains domain extension, add https://
        if any(ext in text_lower for ext in ['.com', '.org', '.net', '.edu', '.gov', '.co.']):
            return f"https://{text}"
        
        # Default: search on Google
        return f"https://www.google.com/search?q={text.replace(' ', '+')}"
    
    def open_application(self, app_name: str) -> Tuple[bool, str]:
        """Open application by name"""
        try:
            result = self.find_application(app_name)
            if result:
                name, path = result
                if os.path.exists(path):
                    subprocess.Popen([path], shell=True)
                    return True, f"Opening {name}"
                else:
                    return False, f"Application path not found: {path}"
            else:
                return False, f"Application '{app_name}' not found"
        except Exception as e:
            return False, f"Error opening application: {e}"
    
    def open_website(self, website: str) -> Tuple[bool, str]:
        """Open website in default browser"""
        try:
            url = self.format_url(website)
            webbrowser.open(url)
            return True, f"Opening {url}"
        except Exception as e:
            return False, f"Error opening website: {e}"
    
    def execute_command(self, command: str) -> Tuple[bool, str]:
        """Execute automation command (open app or website)"""
        command = command.strip().lower()
        
        # Remove common command prefixes
        prefixes = ['open', 'launch', 'start', 'run', 'execute', 'go to', 'visit']
        for prefix in prefixes:
            if command.startswith(prefix):
                command = command[len(prefix):].strip()
                break
        
        if not command:
            return False, "No command specified"
        
        # Check if it's a website request
        if self.is_url(command):
            return self.open_website(command)
        
        # Check for explicit website keywords
        website_indicators = ['website', 'site', '.com', 'www', 'http']
        if any(indicator in command for indicator in website_indicators):
            # Remove website indicators and open as website
            for indicator in website_indicators:
                command = command.replace(indicator, '').strip()
            return self.open_website(command)
        
        # Otherwise, try to open as application
        return self.open_application(command)

def main():
    """Test automation engine"""
    engine = AutomationEngine()
    
    # Test commands
    test_commands = [
        "open chrome",
        "launch notepad",
        "start visual studio code",
        "open google",
        "visit youtube",
        "go to facebook.com",
        "open calculator"
    ]
    
    print("Testing Automation Engine:")
    for cmd in test_commands:
        success, message = engine.execute_command(cmd)
        print(f"Command: '{cmd}' -> {'✓' if success else '✗'} {message}")

if __name__ == "__main__":
    main()
