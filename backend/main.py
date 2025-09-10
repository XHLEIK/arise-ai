"""
A.R.I.S.E. AI Assistant - Backend Entry Point

Advanced Real-time Intelligent System for Execution

This is the main entry point for the A.R.I.S.E. AI backend system.
It initializes all modules and starts the AI assistant services.

Author: A.R.I.S.E. AI Team
Date: September 2025
"""

import os
import sys
import json
import logging
import argparse
from pathlib import Path
from typing import Dict, Any

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import modules
from modules.app_scanner import ApplicationScanner

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data/arise.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger('ARISE')


class ARISEBackend:
    """
    Main backend class for A.R.I.S.E. AI Assistant.
    """
    
    def __init__(self, config_file: str = "data/config.json"):
        """
        Initialize the A.R.I.S.E. backend.
        
        Args:
            config_file (str): Path to configuration file
        """
        self.config_file = config_file
        self.config = {}
        self.app_scanner = None
        self.applications = {}
        
        # Create data directory if it doesn't exist
        Path("data").mkdir(exist_ok=True)
        
        logger.info("🤖 A.R.I.S.E. AI Assistant Backend Initializing...")
        
    def load_config(self) -> None:
        """
        Load configuration from JSON file.
        """
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    self.config = json.load(f)
                logger.info(f"✅ Configuration loaded from {self.config_file}")
            else:
                # Create default configuration
                self.config = self.create_default_config()
                self.save_config()
                logger.info(f"📝 Default configuration created at {self.config_file}")
                
        except Exception as e:
            logger.error(f"❌ Error loading configuration: {e}")
            self.config = self.create_default_config()
    
    def create_default_config(self) -> Dict[str, Any]:
        """
        Create default configuration.
        
        Returns:
            Dict[str, Any]: Default configuration dictionary
        """
        return {
            "system": {
                "auto_scan_applications": True,
                "log_level": "INFO",
                "data_directory": "data"
            },
            "applications": {
                "scan_on_startup": True,
                "scan_interval_hours": 24,
                "applications_file": "data/applications.json"
            },
            "ai": {
                "model": "gemini",
                "max_response_length": 500,
                "conversation_memory": True
            },
            "speech": {
                "recognition_language": "en-US",
                "tts_voice": "default",
                "tts_rate": 150
            },
            "automation": {
                "allow_system_control": True,
                "safe_mode": True
            }
        }
    
    def save_config(self) -> None:
        """
        Save configuration to JSON file.
        """
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=4)
            logger.info(f"💾 Configuration saved to {self.config_file}")
            
        except Exception as e:
            logger.error(f"❌ Error saving configuration: {e}")
    
    def initialize_app_scanner(self) -> None:
        """
        Initialize the application scanner module.
        """
        try:
            applications_file = self.config.get("applications", {}).get(
                "applications_file", "data/applications.json"
            )
            
            self.app_scanner = ApplicationScanner(applications_file)
            logger.info("✅ Application scanner initialized")
            
            # Load existing applications or scan if configured
            if self.config.get("applications", {}).get("scan_on_startup", True):
                logger.info("🔍 Scanning for applications...")
                self.applications = self.app_scanner.run_scan()
                logger.info(f"📱 Found {len(self.applications)} applications")
            else:
                self.applications = self.app_scanner.load_from_json()
                logger.info(f"📂 Loaded {len(self.applications)} applications from file")
                
        except Exception as e:
            logger.error(f"❌ Error initializing application scanner: {e}")
    
    def get_application_path(self, app_name: str) -> str:
        """
        Get the executable path for an application.
        
        Args:
            app_name (str): Name of the application
            
        Returns:
            str: Path to the application executable
        """
        if self.app_scanner:
            return self.app_scanner.get_application_path(app_name)
        return None
    
    def list_applications(self) -> Dict[str, str]:
        """
        Get list of all available applications.
        
        Returns:
            Dict[str, str]: Dictionary of application names and paths
        """
        return self.applications.copy()
    
    def run_application(self, app_name: str) -> bool:
        """
        Launch an application by name.
        
        Args:
            app_name (str): Name of the application to run
            
        Returns:
            bool: True if application was launched successfully
        """
        try:
            app_path = self.get_application_path(app_name)
            if not app_path:
                logger.warning(f"Application '{app_name}' not found")
                return False
            
            if not os.path.exists(app_path):
                logger.error(f"Application path does not exist: {app_path}")
                return False
            
            # Launch the application
            import subprocess
            subprocess.Popen([app_path], shell=True)
            logger.info(f"🚀 Launched application: {app_name} ({app_path})")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error launching application '{app_name}': {e}")
            return False
    
    def start(self) -> None:
        """
        Start the A.R.I.S.E. backend services.
        """
        logger.info("🚀 Starting A.R.I.S.E. AI Assistant Backend...")
        
        # Load configuration
        self.load_config()
        
        # Initialize modules
        self.initialize_app_scanner()
        
        # TODO: Initialize other modules
        # self.initialize_speech_recognition()
        # self.initialize_tts()
        # self.initialize_chatbot()
        # self.initialize_automation()
        
        logger.info("✅ A.R.I.S.E. Backend started successfully!")
        logger.info(f"📱 {len(self.applications)} applications available for automation")
        
        # Display some available applications
        if self.applications:
            logger.info("🔥 Popular applications found:")
            popular_apps = ['Google Chrome', 'Visual Studio Code', 'WhatsApp', 'Discord']
            for app in popular_apps:
                if self.get_application_path(app):
                    logger.info(f"  ✅ {app}")
    
    def stop(self) -> None:
        """
        Stop the A.R.I.S.E. backend services.
        """
        logger.info("🛑 Stopping A.R.I.S.E. AI Assistant Backend...")
        # TODO: Cleanup resources
        logger.info("✅ A.R.I.S.E. Backend stopped successfully!")


def main():
    """
    Main entry point for the A.R.I.S.E. backend.
    """
    parser = argparse.ArgumentParser(description='A.R.I.S.E. AI Assistant Backend')
    parser.add_argument('--debug', action='store_true', help='Enable debug logging')
    parser.add_argument('--scan-apps', action='store_true', help='Scan for applications and exit')
    parser.add_argument('--list-apps', action='store_true', help='List found applications and exit')
    parser.add_argument('--run-app', type=str, help='Run a specific application by name')
    
    args = parser.parse_args()
    
    # Set logging level
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("🐛 Debug logging enabled")
    
    # Create backend instance
    backend = ARISEBackend()
    
    try:
        if args.scan_apps:
            # Just scan for applications and exit
            backend.initialize_app_scanner()
            print(f"Found {len(backend.applications)} applications")
            return 0
            
        elif args.list_apps:
            # List all applications and exit
            backend.load_config()
            backend.initialize_app_scanner()
            apps = backend.list_applications()
            
            print(f"\nFound {len(apps)} applications:")
            print("-" * 50)
            for i, (name, path) in enumerate(apps.items(), 1):
                print(f"{i:3d}. {name}")
                print(f"     {path}")
                print()
            return 0
            
        elif args.run_app:
            # Run a specific application and exit
            backend.load_config()
            backend.initialize_app_scanner()
            
            if backend.run_application(args.run_app):
                print(f"✅ Successfully launched: {args.run_app}")
                return 0
            else:
                print(f"❌ Failed to launch: {args.run_app}")
                return 1
        
        else:
            # Start the full backend
            backend.start()
            
            # Keep the backend running
            try:
                logger.info("🎯 A.R.I.S.E. is ready! Press Ctrl+C to stop.")
                while True:
                    import time
                    time.sleep(1)
                    
            except KeyboardInterrupt:
                logger.info("🛑 Shutdown signal received")
                
            finally:
                backend.stop()
    
    except Exception as e:
        logger.error(f"💥 Fatal error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
