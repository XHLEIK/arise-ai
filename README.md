# A.R.I.S.E. �
**Advanced Real-time Intelligent System for Execution**  

![Python](https://img.shields.io/badge/Python-3.10+-blue) ![React](https://img.shields.io/badge/React-Frontend-cyan) ![License](https://img.shields.io/badge/License-MIT-yellow) ![GitHub](https://img.shields.io/github/stars/XHLEIK/arise-ai)

A.R.I.S.E. is a voice-controlled desktop AI assistant that combines speech recognition, intelligent conversation, real-time data fetching, and system automation into a seamless experience. Talk to it naturally and watch it execute tasks, answer questions, and control your computer.

---

## � Current Status
**✅ FULLY FUNCTIONAL** - A.R.I.S.E. is complete and ready to use!

- � **Voice Recognition**: Real-time speech-to-text with Google Speech Recognition
- � **Text-to-Speech**: Natural voice responses at 180 WPM (human-like speed)
- � **Multi-Engine Architecture**: Chat, Data, and Automation engines working independently
- ⚡ **Ultra-Fast Automation**: Opens applications in ~0.06 seconds
- � **Real-time Data**: Weather, stocks, news, and web information
- �️ **Consistent Audio**: Every response includes voice output - no silent responses

---

## � Features

### Core Functionality
- **�️ Voice-First Interface**: Speak naturally, no keywords needed
- **� Intelligent Classification**: Automatically routes requests to appropriate engine
- **� Conversational AI**: Powered by Google Gemini for natural conversations
- **� Real-time Data**: Live weather, stock prices, news headlines
- **�️ System Automation**: Voice-controlled application launching (Chrome, Facebook, etc.)
- **� Continuous Operation**: Hands-free conversation loop with exit commands

### Technical Excellence
- **⚡ Optimized Performance**: Sub-second response times
- **� Reliable TTS**: Audio plays for every single response
- **� Modular Design**: Independent engines with centralized coordination
- **� Comprehensive Logging**: Full debug and performance tracking
- **�️ Error Handling**: Graceful fallbacks and recovery mechanisms

---

## � Tech Stack

**Backend:** Python 3.10+, speech_recognition, pyttsx3, google-generativeai, requests  
**Frontend:** Vite + React, Electron for desktop app  
**Voice:** Google Speech Recognition, Windows SAPI Text-to-Speech  
**APIs:** Google Gemini AI, OpenWeatherMap, News APIs  
**Architecture:** Event-driven, multi-engine with centralized TTS  

---

## � Project Structure

```
arise-ai/
├── backend/
│   ├── main.py                    # Main orchestrator with centralized TTS
│   ├── modules/
│   │   ├── tts_engine.py         # Optimized text-to-speech (180 WPM)
│   │   ├── stt_engine.py         # Speech recognition
│   │   ├── automation_engine.py   # Ultra-fast app launching
│   │   ├── app_scanner.py        # System application detection
│   │   └── brain/
│   │       ├── chat_brain.py     # Conversational AI (Gemini)
│   │       └── data_engine.py    # Real-time data fetching
│   ├── data/
│   │   └── applications.json     # Scanned applications database
│   └── requirements.txt
├── frontend/
│   ├── src/                      # React components
│   ├── electron/                 # Electron main process
│   └── package.json
└── README.md
```

---

## ⚡ Installation & Setup

### 1. Clone Repository
```bash
git clone https://github.com/XHLEIK/arise-ai.git
cd arise-ai
```

### 2. Backend Setup
```bash
cd backend
pip install -r requirements.txt

# Set up your API keys in modules/brain/.env
echo "GEMINI_API_KEY=your_gemini_api_key_here" > modules/brain/.env
```

### 3. Run A.R.I.S.E.
```bash
python main.py
```

### 4. Frontend (Optional)
```bash
cd ../frontend
npm install
npm run dev
```

---

## � How to Use

1. **Start A.R.I.S.E.**: Run python main.py in the backend directory
2. **Listen for greeting**: Wait for "Hello! I'm A.R.I.S.E..."
3. **Speak naturally**: No wake words needed, just talk

### Example Commands:
- **� Chat**: "How are you today?" / "Tell me a joke"
- **�️ Weather**: "What's the weather like?" / "Is it going to rain?"
- **� Stocks**: "Tesla stock price" / "How's the market doing?"
- **� News**: "Latest news" / "What's happening today?"
- **�️ Apps**: "Open Facebook" / "Launch Chrome" / "Start calculator"
- **� Exit**: "Goodbye" / "Exit" / "Stop"

---

## �️ Architecture Overview

A.R.I.S.E. uses a **centralized TTS architecture** ensuring every response includes voice:

```
User Speech → STT Engine → Request Classifier → Engine Router
                                                     ↓
Chat Engine ←→ Data Engine ←→ Automation Engine
                                                     ↓
                            All Responses → Centralized TTS → Audio Output
```

### Engine Responsibilities:
- **� Chat Brain**: Conversational AI using Google Gemini
- **� Data Engine**: Real-time information (weather, stocks, news)
- **⚙️ Automation Engine**: System tasks and application launching
- **� STT Engine**: Speech recognition and audio processing
- **� TTS Engine**: Voice synthesis with optimized timing
- **� App Scanner**: System application discovery and management

---

## � Troubleshooting

### Audio Issues
- Ensure microphone permissions are granted
- Check Windows audio settings (44.1kHz recommended)
- Verify speakers/headphones are working

### API Issues
- Confirm Gemini API key is set in modules/brain/.env
- Check internet connection for data requests
- Review logs in console for specific errors

### Performance
- A.R.I.S.E. is optimized for sub-second responses
- Application launching: ~0.06 seconds
- TTS speed: 180 WPM (natural human speech)

---

## � Project Status & Roadmap

| Component | Status | Performance |
|-----------|--------|-------------|
| � Speech Recognition | ✅ Complete | Real-time, Google API |
| � Text-to-Speech | ✅ Complete | 180 WPM, 100% reliability |
| � Chat Engine | ✅ Complete | Gemini AI integration |
| � Data Engine | ✅ Complete | Weather, stocks, news |
| ⚙️ Automation | ✅ Complete | 0.06s app launching |
| �️ Desktop UI | � In Progress | React + Electron |
| � Mobile App | � Planned | Cross-platform |

### Recent Achievements ✨
- **Fixed TTS Consistency**: Audio now plays for every response
- **Optimized Voice Speed**: Natural 180 WPM speech rate
- **Ultra-Fast Automation**: 30-second delays reduced to 0.06 seconds
- **Centralized Architecture**: Eliminated circular dependencies
- **Enhanced Reliability**: Multiple TTS fallback methods

---

## � Contributing

1. Fork the repository
2. Create feature branch: git checkout -b feature-name
3. Make changes and test thoroughly
4. Commit: git commit -m 'Add feature'
5. Push: git push origin feature-name
6. Create Pull Request

**Development Guidelines:**
- Follow Python PEP8 standards
- Maintain modular architecture
- Add comprehensive error handling
- Test voice functionality thoroughly
- Update documentation

---

## � License

MIT License - Feel free to use, modify, and distribute.

---

**� A.R.I.S.E. is production-ready and actively maintained.**

**Built with ❤️ by XHLEIK** | [GitHub](https://github.com/XHLEIK/arise-ai)
