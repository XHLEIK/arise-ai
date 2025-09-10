"""
A.R.I.S.E. AI Assistant - Backend Modules

This package contains all the core modules for the A.R.I.S.E. AI assistant:

- app_scanner: Scans the system for installed applications
- speech_recognition: Voice input processing (planned)
- tts: Text-to-speech output (planned)
- chatbot: AI conversation handling (planned)
- automation: System automation tasks (planned)
- realtime_search: Real-time data fetching (planned)

Author: A.R.I.S.E. AI Team
Date: September 2025
"""

__version__ = "1.0.0"
__author__ = "A.R.I.S.E. AI Team"

# Import available modules
from .app_scanner import ApplicationScanner

__all__ = [
    'ApplicationScanner'
]
