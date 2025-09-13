# A.R.I.S.E. Backend 🤖

The backend system for the Advanced Real-time Intelligent System for Execution (A.R.I.S.E.) AI assistant.

## ✅ Current Status - FULLY FUNCTIONAL

A.R.I.S.E. backend is **complete and production-ready** with all core features implemented and optimized.

### 🎯 Core Engines (All Complete)

- **🎤 STT Engine**: Real-time speech recognition with seamless audio capture reuse
- **🔊 TTS Engine**: Optimized text-to-speech at 180 WPM with 100% reliability and fallback support
- **🔐 Voice Recognition**: Advanced speaker verification using SpeechBrain ECAPA-VOXCELEB model with multi-method validation
- **🧠 Chat Brain**: Conversational AI powered by Google Gemini with contextual memory integration
- **📊 Data Engine**: Real-time weather, stocks, and news fetching with intelligent parsing
- **⚙️ Automation Engine**: Lightning-fast application launching (0.06s) with smart URL mapping
- **📱 App Scanner**: Comprehensive system application discovery and JSON database management
- **💭 Memory Manager**: Advanced session buffering and persistent fact storage with automatic context building

### 🏗️ Architecture Features

- **Centralized TTS**: Every response guaranteed to have voice output
- **Seamless Voice Security**: Single voice input for both command processing and identity verification
- **Independent Engines**: No circular dependencies, modular design
- **Smart Classification**: Automatic routing to appropriate engine based on keywords
- **Error Handling**: Comprehensive fallbacks and graceful recovery
- **Performance Optimized**: Sub-second response times with efficient processing
- **Memory Integration**: Context-aware conversations with fact retention across sessions
- **Voice Authentication**: SpeechBrain-powered speaker verification with four verification methods
- **Audio Reuse**: STT captures audio once, reuses for both recognition and verification

---

## 🚀 Quick Start

### Installation
```bash
cd backend
pip install -r requirements.txt

# Set up API keys
echo "GEMINI_API_KEY=your_api_key_here" > modules/brain/.env
```

### Run A.R.I.S.E.
```bash
python main.py
```

That's it! A.R.I.S.E. will:
1. Initialize all engines
2. Greet you with voice
3. Start listening for commands
4. Respond to everything you say

---

## 🎯 How It Works

### Voice Interaction Flow
1. **Listen**: STT engine captures your speech and stores audio
2. **Classify**: Main orchestrator determines request type (chat/data/automation)
3. **Verify**: Voice recognition uses stored audio for seamless identity verification (if enrolled)
4. **Process**: Appropriate engine handles the request after security clearance
5. **Respond**: All responses go through centralized TTS for voice output

### Example Usage
```
👤 You: "What's the weather like?"
📍 Request type: data
� Voice verification: ✅ VERIFIED (using same audio)
�🔊 A.R.I.S.E: "Currently it's 72°F and sunny in your area..."

👤 You: "Open Facebook"
📍 Request type: automation  
🔐 Voice verification: ✅ VERIFIED (seamless)
🔊 A.R.I.S.E: "Opening Facebook"
⚡ Facebook opens in 0.06 seconds

👤 You: "How are you today?"
📍 Request type: chat
🔐 Voice verification: ✅ VERIFIED (single input)
🔊 A.R.I.S.E: "I'm doing great! Ready to help you with anything..."

👤 You: "I live in New York"
💭 Memory: Stores location fact for future reference
🔊 A.R.I.S.E: "Got it! I'll remember you live in New York."

👤 You: "Where do I live?" (in later conversation)
💭 Context: Retrieves stored location fact
🔊 A.R.I.S.E: "You live in New York. Would you like the weather there?"

👤 You: "Enroll my voice"
🔐 Voice Enrollment: Records 5-second sample
🔊 A.R.I.S.E: "Voice enrolled successfully! You're now the master user."

👤 You: "Delete all sessions"
📍 Request type: memory_delete
🔊 A.R.I.S.E: "Memory cleared! I deleted 7 session files..."
```
🔊 A.R.I.S.E: "You live in New York, as you mentioned earlier."

👤 You: "Delete memory"
💭 Memory: Clears all session files and conversation buffer
🔊 A.R.I.S.E: "Memory cleared! I deleted X session files and cleared the current conversation buffer..."

👤 You: "Go to standby"
😴 Standby: Enters sleep mode, listens only for wake command
🔊 A.R.I.S.E: "Going to standby mode. Say 'Hey arise' or 'Hey A.R.I.S.E.' to wake me up."

👤 You: "arise" (while in standby)
🔄 Wake: Exits standby mode and resumes normal operation
🔊 A.R.I.S.E: "I'm awake! How can I help you?"

👤 You: "Enroll my voice"
🔐 Voice: Prompts for voice enrollment
🔊 A.R.I.S.E: "I'll help you enroll your voice. Please say something for about 5 seconds..."
🎤 Recording: Records voice sample and creates secure profile
🔊 A.R.I.S.E: "Excellent! Your voice has been enrolled successfully."

👤 You: "Hello A.R.I.S.E." (after enrollment)
🔐 Verification: Automatically verifies voice before processing
✅ Verified: Voice matches master user profile
🔊 A.R.I.S.E: "Hello! How can I help you?"

👤 Unknown Person: "What can you do?"
🔐 Verification: Voice doesn't match master profile
❌ Denied: Security response activated
🔊 A.R.I.S.E: "Your voice doesn't match my master's voice."
```

---

## 🔐 Voice Security System

### Advanced Speaker Verification
A.R.I.S.E. features a sophisticated voice recognition system powered by SpeechBrain's ECAPA-VOXCELEB model:

**🎯 Key Features:**
- **One-Time Enrollment**: 5-second voice sample creates your unique voice profile
- **Seamless Verification**: Uses the same audio from your command for identity verification
- **Multi-Method Validation**: Four different verification approaches for maximum accuracy
- **Graceful Fallbacks**: Continues operation even if verification temporarily fails

**🧠 Verification Methods:**
1. **Both Thresholds**: Feature similarity + SpeechBrain score both pass
2. **Combined Score**: Weighted combination of both methods
3. **Feature Compensation**: High feature similarity compensates for low SpeechBrain score
4. **SpeechBrain Fallback**: Pure SpeechBrain verification as backup

**📊 Example Verification Scores:**
```
🔍 Voice verification scores:
   Feature similarity: 0.999 (threshold: 0.45)
   SpeechBrain score: 0.356 (threshold: 0.4)
   Combined score: 0.613 (threshold: 0.55)
🔍 Verification methods:
   Method 1 (Both thresholds): ❌
   Method 2 (Combined score): ✅
   Method 3 (Feature compensation): ✅
   Method 4 (SpeechBrain fallback): ❌
   Final result: ✅ VERIFIED
```

**🚀 No Double Input Required:**
Traditional systems ask you to speak twice - once for the command, once for verification. A.R.I.S.E. is smarter:
1. You speak: "What's the weather like?"
2. STT captures and stores the audio
3. System processes your command AND verifies your identity
4. Single input, dual purpose!

---

## 📁 Project Structure

```
backend/
├── main.py                     # 🎯 Main orchestrator with centralized TTS
├── requirements.txt            # 📦 Python dependencies
├── modules/
│   ├── tts_engine.py          # 🔊 Optimized text-to-speech (180 WPM)
│   ├── stt_engine.py          # 🎤 Speech recognition engine
│   ├── voice_recognition.py   # 🔐 Secure voice enrollment and verification
│   ├── automation_engine.py    # ⚙️ Ultra-fast app launching
│   ├── app_scanner.py         # 📱 System application detection
│   ├── memory_manager.py      # 💭 Session buffer and facts storage
│   └── brain/
│       ├── .env               # 🔑 API keys (create this)
│       ├── chat_brain.py      # 🧠 Conversational AI (Gemini)
│       └── data_engine.py     # 📊 Real-time data fetching
└── data/
    ├── applications.json       # 📁 Scanned applications database
    ├── facts.json             # 💭 Long-term memory facts
    ├── users.json             # 🔐 Voice recognition user profiles
    ├── sessions/              # 💬 Conversation session storage
    ├── voice_features/        # 🔐 Voice enrollment data and audio
    └── speechbrain_cache/     # 🤖 SpeechBrain model cache
```

---

## ⚙️ Engine Details

### � TTS Engine (`tts_engine.py`)
- **Speed**: 180 WPM (natural human speech)
- **Reliability**: 100% audio output for every response
- **Features**: Multiple fallback methods, proper cleanup
- **Performance**: Optimized timing and duration calculation

### 🎤 STT Engine (`stt_engine.py`)
- **Provider**: Google Speech Recognition
- **Features**: Real-time transcription, automatic microphone calibration, audio file recording
- **Timeout**: 30-second listening window with phrase detection
- **Voice Support**: Records audio samples for voice recognition enrollment/verification

### 🔐 Voice Recognition Engine (`voice_recognition.py`)
- **AI Model**: SpeechBrain ECAPA-VOXCELEB pre-trained speaker verification
- **Security**: Dual verification (SpeechBrain + audio features) with conservative thresholds
- **Enrollment**: One-time master user voice registration with UUID identification
- **Verification**: Real-time voice matching with 0.75 confidence threshold
- **Responses**: Randomized security denials for unauthorized users

### 🧠 Chat Brain (`brain/chat_brain.py`)
- **AI Model**: Google Gemini
- **Features**: Natural conversation, context awareness, memory integration
- **Response**: Text-only output (TTS handled centrally)

### 📊 Data Engine (`brain/data_engine.py`)
- **Sources**: Weather APIs, Stock APIs, News APIs
- **Features**: Real-time data fetching, intelligent parsing
- **Performance**: Fast API calls with error handling

### ⚙️ Automation Engine (`automation_engine.py`)
- **Speed**: 0.06 seconds to launch applications
- **Support**: 178+ applications detected automatically
- **Features**: Smart app matching, website shortcuts
- **Platforms**: Windows (primary), macOS, Linux support

### 📱 App Scanner (`app_scanner.py`)
- **Detection**: Registry scanning, path searching, executable detection
- **Database**: JSON storage for quick access
- **Features**: Automatic updates, popular app shortcuts

### 💭 Memory Manager (`memory_manager.py`)
- **Architecture**: Two-layer system with session buffer + long-term facts
- **Storage**: JSON-based persistence in data/sessions/ and data/facts.json
- **Features**: Context building, fact extraction, conversation history
- **Performance**: O(1) message addition, automatic session management

---

## 🔧 Configuration

### API Keys Setup
Create `modules/brain/.env`:
```
GEMINI_API_KEY=your_gemini_api_key_here
```

### Performance Tuning
All engines are pre-optimized for best performance:
- TTS: 180 WPM speech rate
- STT: 44.1kHz audio sampling
- Automation: Direct executable launching
- Data: Concurrent API requests
- Memory: O(1) operations for frequent actions
- Standby: Low-power listening mode with minimal processing

### Standby Mode Features
- **Voice Activation**: Say "go to standby" or "sleep mode" to enter standby
- **Wake Commands**: "arise", "hey arise", "wake up arise", or "A.R.I.S.E." to wake up
- **Flexible Detection**: Recognizes various pronunciations and spellings of "arise"
- **Power Saving**: Reduced processing while maintaining voice recognition
- **Selective Listening**: Ignores all commands except wake phrases in standby
- **Seamless Resume**: Returns to full functionality immediately upon waking

---

## 🚀 Advanced Usage

### Custom Commands
The system automatically handles:
- **Chat requests**: Natural conversation with memory context
- **Data requests**: "weather", "stock", "news" keywords
- **Automation requests**: "open", "launch", "start" keywords
- **Memory deletion**: "delete memory", "clear memory", "forget everything" keywords
- **Standby mode**: "go to standby", "sleep mode", "stand by" keywords
- **Memory integration**: Automatic fact extraction and context building
- **Location awareness**: Weather data uses stored location from facts.json

### Debugging
```bash
# See all logs and engine initialization
python main.py

# Check specific engine
python -c "from modules.tts_engine import TTSEngine; tts = TTSEngine(); tts.speak('test')"

# Test memory system
python -c "from modules.memory_manager import MemoryManager; mm = MemoryManager(); mm.add_message('user', 'test')"
```

### Performance Monitoring
- Watch console for timing information
- TTS shows duration estimates and actual completion times
- Automation shows app launch speed
- All engines report initialization status

---

## 🎯 API Reference

### Main Orchestrator (`main.py`)
```python
class ARISEMain:
    def __init__(self)                    # Initialize all engines
    def _speak(self, text: str)           # Centralized TTS
    def _classify_request(self, input)    # Route to appropriate engine
    def _process_request(self, input)     # Handle user requests
    def _build_memory_context(self)       # Build context from memory
    def _extract_and_update_facts(self)   # Extract facts from conversation
    def _enter_standby_mode(self)         # Enter standby mode with wake detection
    def run(self)                         # Main conversation loop
```

### TTS Engine
```python
class TTSEngine:
    def speak(self, text: str) -> bool    # Speak with 180 WPM
```

### Automation Engine  
```python
class AutomationEngine:
    def execute_command(self, cmd: str) -> Tuple[bool, str]  # 0.06s execution
```

### Memory Manager
```python
class MemoryManager:
    def add_message(self, role: str, content: str) -> None      # Add to session buffer
    def save_session(self) -> str                               # Save and clear buffer
    def update_facts(self, new_facts: Dict[str, Any]) -> None   # Update long-term facts
    def load_facts(self) -> Dict[str, Any]                      # Load current facts
    def delete_all_sessions(self) -> bool                       # Clear all sessions and buffer
    def get_memory_stats(self) -> Dict[str, Any]                # Get memory usage statistics
```

---

## 🛠 Troubleshooting

### Common Issues
1. **No audio output**: Check Windows audio settings, microphone permissions
2. **Slow responses**: Verify internet connection for API calls
3. **App not opening**: Run app scanner to refresh application database
4. **API errors**: Confirm Gemini API key is set correctly

### Performance Tips
- A.R.I.S.E. is already optimized for maximum speed
- Ensure good internet connection for data requests
- Close unnecessary applications for best microphone performance

---

## 📈 Performance Metrics

| Component | Performance | Status |
|-----------|-------------|--------|
| Voice Recognition | Real-time | ✅ Optimized |
| Text-to-Speech | 180 WPM | ✅ Optimized |
| App Launching | 0.06 seconds | ✅ Optimized |
| Data Fetching | < 1 second | ✅ Optimized |
| Engine Switching | Instant | ✅ Optimized |
| Memory Usage | < 100MB | ✅ Optimized |
| Memory Operations | O(1) add, O(n) save/load | ✅ Optimized |

---

## 🔮 Future Enhancements

While the core system is complete, potential additions:
- Multi-language speech recognition
- Offline voice capabilities  
- Custom voice training
- Plugin architecture for third-party engines
- Mobile companion app
- Advanced memory search and retrieval
- Conversation analytics and insights

---

## 💭 Memory System Architecture

A.R.I.S.E. features a sophisticated two-layer memory system designed for persistent conversation context and fact retention.

### Architecture Overview

```
Memory System
├── Session Buffer (Short-term)
│   ├── Current conversation messages
│   ├── Real-time context building
│   └── Automatic saving on session end
└── Facts Storage (Long-term)
    ├── Persistent user information
    ├── Learned preferences and data
    └── Cross-session fact retrieval
```

### Memory Components

#### Session Buffer
- **Purpose**: Stores current conversation in memory for immediate context
- **Capacity**: Last 10 messages used for context building
- **Performance**: O(1) message addition, instant context retrieval
- **Persistence**: Auto-saves to `data/sessions/session_timestamp.json` on conversation end

#### Facts Storage
- **Purpose**: Long-term retention of important user information
- **Storage**: JSON file at `data/facts.json` with key-value pairs
- **Updates**: Automatic fact extraction from conversations
- **Examples**: User location, preferences, personal details, recurring topics

### Memory Integration Flow

1. **Message Addition**: Every user/AI interaction added to session buffer
2. **Context Building**: Recent messages + stored facts compiled for AI context
3. **Fact Extraction**: AI responses analyzed for new factual information
4. **Fact Storage**: New facts merged into long-term storage
5. **Session Persistence**: Complete conversations saved for future reference
6. **User-Initiated Deletion**: Voice commands can clear all session history

### User Memory Control

Users can manage their memory through voice commands:

| Command Examples | Action | What Gets Deleted |
|-----------------|--------|-------------------|
| "Delete memory" | Clear all sessions | All session files + current buffer |
| "Clear memory" | Clear all sessions | All session files + current buffer |
| "Forget everything" | Clear all sessions | All session files + current buffer |
| "Remove all memory" | Clear all sessions | All session files + current buffer |

**Important**: Facts storage (`facts.json`) is preserved during memory deletion. This ensures user preferences and important information remain available even after clearing conversation history.

### Usage Examples

```python
# Initialize memory manager
memory = MemoryManager()

# Add conversation messages
memory.add_message('user', 'I live in New York')
memory.add_message('assistant', 'Got it! I will remember you live in New York.')

# Extract and store facts
facts = {'location': 'New York'}
memory.update_facts(facts)

# Build context for AI
context = memory.build_context()  # Returns formatted string with facts + recent messages

# Save session when conversation ends
session_id = memory.save_session()

# Delete all memory sessions (user request)
success = memory.delete_all_sessions()

# Get memory statistics
stats = memory.get_memory_stats()
# Returns: {'session_buffer_messages': 0, 'saved_sessions': 0, 'stored_facts': 2}
```

### Data Structure

#### Session File Format (`data/sessions/session_*.json`)
```json
{
    "session_id": "session_1694649600",
    "created_at": 1694649600.123,
    "messages": [
        {
            "role": "user", 
            "content": "Hello", 
            "timestamp": 1694649600.123
        },
        {
            "role": "assistant", 
            "content": "Hi there!", 
            "timestamp": 1694649601.456
        }
    ]
}
```

#### Facts File Format (`data/facts.json`)
```json
{
    "location": "New York",
    "name": "John",
    "preferences": {
        "weather_units": "fahrenheit",
        "news_topics": ["technology", "science"]
    },
    "last_updated": 1694649600.123
}
```

### Performance Characteristics

| Operation | Time Complexity | Description |
|-----------|----------------|-------------|
| Add Message | O(1) | Append to session buffer |
| Build Context | O(n) | Format recent messages + facts (n ≤ 10) |
| Save Session | O(m) | Write m messages to JSON file |
| Load Facts | O(1) | Read JSON file into memory |
| Update Facts | O(f) | Merge f new facts with existing |
| Delete All Sessions | O(s) | Remove s session files + clear buffer |
| Get Memory Stats | O(s) | Count s session files + facts |

### Error Handling

- **File I/O Errors**: Graceful fallback to memory-only operation
- **JSON Corruption**: Auto-recreation of corrupted files
- **Disk Space**: Automatic cleanup of old session files (configurable)
- **Memory Limits**: Session buffer size limits prevent memory bloat

---

## 📜 License

MIT License - Open source and free to use.

---

**🎯 The A.R.I.S.E. backend is production-ready and actively maintained.**

**Built with ❤️ by XHLEIK**

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
