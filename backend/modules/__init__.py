"""
A.R.I.S.E. AI Assistant - Backend Modules

This package contains all the core modules for the A.R.I.S.E. AI assistant:

- app_scanner: Scans the system for installed applications
- tts_engine: Text-to-speech output system
- speech_recognition: Voice input processing (planned)
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
from .tts_engine import TTSEngine

__all__ = [
    'ApplicationScanner',
    'TTSEngine'
]
