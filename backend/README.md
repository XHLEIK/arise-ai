# A.R.I.S.E. Backend

The backend system for the Advanced Real-time Intelligent System for Execution (A.R.I.S.E.) AI assistant.

## Features

### ✅ Application Scanner
- Scans system for installed applications
- Supports Windows, macOS, and Linux
- Finds executable paths for popular applications
- Saves results to JSON for quick access
- Enables voice-controlled application launching

### 🔜 Planned Modules
- **Speech Recognition**: Voice input processing
- **Text-to-Speech**: AI response output
- **Chatbot**: Conversation handling with AI models
- **Automation**: System task automation
- **Real-time Search**: Live data fetching (weather, stocks, news)

## Installation

1. **Install Python 3.10+**
2. **Install dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

## Usage

### Quick Start
```bash
# Start the backend
python main.py

# Scan for applications only
python main.py --scan-apps

# List all found applications
python main.py --list-apps

# Launch a specific application
python main.py --run-app "Google Chrome"

# Enable debug logging
python main.py --debug
```

### Using the Application Scanner

```python
from modules.app_scanner import ApplicationScanner

# Create scanner
scanner = ApplicationScanner("data/applications.json")

# Scan for all applications
apps = scanner.run_scan()

# Get specific application path
chrome_path = scanner.get_application_path("Google Chrome")

# Launch application
import subprocess
subprocess.Popen([chrome_path])
```

## Project Structure

```
backend/
├── main.py                 # Main entry point
├── requirements.txt        # Python dependencies
├── modules/                # Core modules
│   ├── __init__.py
│   └── app_scanner.py      # Application scanner module
├── tests/                  # Test files (can be deleted after completion)
│   ├── __init__.py
│   ├── test_app_scanner.py # Application scanner tests
│   └── README.md           # Test documentation
└── data/                   # Data storage
    ├── applications.json   # Found applications (generated)
    ├── config.json         # Configuration (generated)
    └── arise.log          # Application logs
```

## Configuration

The backend creates a default configuration file at `data/config.json`:

```json
{
    "system": {
        "auto_scan_applications": true,
        "log_level": "INFO",
        "data_directory": "data"
    },
    "applications": {
        "scan_on_startup": true,
        "scan_interval_hours": 24,
        "applications_file": "data/applications.json"
    },
    "ai": {
        "model": "gemini",
        "max_response_length": 500,
        "conversation_memory": true
    }
}
```

## Application Scanner Details

The application scanner finds software by:

1. **Popular Applications**: Checks known installation paths for common software
2. **Registry Scanning** (Windows): Reads Windows registry for installed programs
3. **Directory Scanning**: Searches common installation directories
4. **Executable Detection**: Identifies valid executable files

### Supported Applications

The scanner automatically detects:
- **Browsers**: Chrome, Firefox, Edge, Safari
- **Communication**: WhatsApp, Discord, Telegram
- **Development**: VS Code, Notepad++, PyCharm
- **Media**: VLC, Spotify, iTunes
- **Productivity**: Microsoft Office, Adobe products
- **And many more...**

## Testing

Run the test script to verify everything works:

```bash
# Run application scanner test
python tests/test_app_scanner.py

# Or using pytest (recommended)
pip install pytest
pytest tests/ -v
```

## Logging

- Logs are saved to `data/arise.log`
- Console output shows real-time status
- Use `--debug` flag for detailed logging

## Platform Support

- ✅ **Windows**: Full support with registry scanning
- ✅ **macOS**: Application bundle detection
- ✅ **Linux**: Binary and package detection

## API Reference

### ApplicationScanner Class

```python
class ApplicationScanner:
    def __init__(self, output_file: str = "applications.json")
    def scan_all_applications(self) -> Dict[str, str]
    def save_to_json(self, applications: Dict[str, str] = None) -> None
    def load_from_json(self) -> Dict[str, str]
    def get_application_path(self, app_name: str) -> Optional[str]
    def run_scan(self) -> Dict[str, str]
```

### ARISEBackend Class

```python
class ARISEBackend:
    def __init__(self, config_file: str = "data/config.json")
    def start(self) -> None
    def stop(self) -> None
    def get_application_path(self, app_name: str) -> str
    def list_applications(self) -> Dict[str, str]
    def run_application(self, app_name: str) -> bool
```

## Future Development

The backend is designed to be modular and extensible. Planned additions include:

- Voice recognition with multiple languages
- Integration with popular AI models (GPT, Gemini, Claude)
- Real-time web scraping and API integration
- Advanced system automation
- Plugin architecture for custom modules

## Contributing

1. Follow Python PEP8 style guidelines
2. Add type hints to all functions
3. Include comprehensive docstrings
4. Write tests for new features
5. Update this README for new modules

## License

MIT License - See LICENSE file for details.
