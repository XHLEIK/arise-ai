# A.R.I.S.E. Ì¥ñ
**Advanced Real-time Intelligent System for Execution**  

![Python](https://img.shields.io/badge/Python-3.10+-blue) ![React](https://img.shields.io/badge/React-Frontend-cyan) ![License](https://img.shields.io/badge/License-MIT-yellow) ![GitHub](https://img.shields.io/github/stars/XHLEIK/arise-ai)

A.R.I.S.E. is a voice-controlled desktop AI assistant that combines speech recognition, intelligent conversation, real-time data fetching, and system automation into a seamless experience. Talk to it naturally and watch it execute tasks, answer questions, and control your computer.

---

## Ìæ• Current Status
**‚úÖ FULLY FUNCTIONAL** - A.R.I.S.E. is complete and ready to use!

- Ìæ§ **Voice Recognition**: Real-time speech-to-text with Google Speech Recognition
- Ì¥ä **Text-to-Speech**: Natural voice responses at 180 WPM (human-like speed)
- Ì∑† **Multi-Engine Architecture**: Chat, Data, and Automation engines working independently
- ‚ö° **Ultra-Fast Automation**: Opens applications in ~0.06 seconds
- Ìºê **Real-time Data**: Weather, stocks, news, and web information
- Ì∑£Ô∏è **Consistent Audio**: Every response includes voice output - no silent responses

---

## Ì∫Ä Features

### Core Functionality
- **ÌæôÔ∏è Voice-First Interface**: Speak naturally, no keywords needed
- **Ì∑† Intelligent Classification**: Automatically routes requests to appropriate engine
- **Ì≤¨ Conversational AI**: Powered by Google Gemini for natural conversations
- **Ì≥ä Real-time Data**: Live weather, stock prices, news headlines
- **Ì∂•Ô∏è System Automation**: Voice-controlled application launching (Chrome, Facebook, etc.)
- **Ì¥Ñ Continuous Operation**: Hands-free conversation loop with exit commands

### Technical Excellence
- **‚ö° Optimized Performance**: Sub-second response times
- **ÌæØ Reliable TTS**: Audio plays for every single response
- **Ì¥ß Modular Design**: Independent engines with centralized coordination
- **Ì≥ù Comprehensive Logging**: Full debug and performance tracking
- **Ìª°Ô∏è Error Handling**: Graceful fallbacks and recovery mechanisms

---

## Ìª† Tech Stack

**Backend:** Python 3.10+, speech_recognition, pyttsx3, google-generativeai, requests  
**Frontend:** Vite + React, Electron for desktop app  
**Voice:** Google Speech Recognition, Windows SAPI Text-to-Speech  
**APIs:** Google Gemini AI, OpenWeatherMap, News APIs  
**Architecture:** Event-driven, multi-engine with centralized TTS  

---

## Ì≥Å Project Structure

```
arise-ai/
‚îú‚îÄ‚îÄ backend/
‚îÇ   ‚îú‚îÄ‚îÄ main.py                    # Main orchestrator with centralized TTS
‚îÇ   ‚îú‚îÄ‚îÄ modules/
‚îÇ   ‚îÇ   ‚îú‚îÄ‚îÄ tts_engine.py         # Optimized text-to-speech (180 WPM)
‚îÇ   ‚îÇ   ‚îú‚îÄ‚îÄ stt_engine.py         # Speech recognition
‚îÇ   ‚îÇ   ‚îú‚îÄ‚îÄ automation_engine.py   # Ultra-fast app launching
‚îÇ   ‚îÇ   ‚îú‚îÄ‚îÄ app_scanner.py        # System application detection
‚îÇ   ‚îÇ   ‚îî‚îÄ‚îÄ brain/
‚îÇ   ‚îÇ       ‚îú‚îÄ‚îÄ chat_brain.py     # Conversational AI (Gemini)
‚îÇ   ‚îÇ       ‚îî‚îÄ‚îÄ data_engine.py    # Real-time data fetching
‚îÇ   ‚îú‚îÄ‚îÄ data/
‚îÇ   ‚îÇ   ‚îî‚îÄ‚îÄ applications.json     # Scanned applications database
‚îÇ   ‚îî‚îÄ‚îÄ requirements.txt
‚îú‚îÄ‚îÄ frontend/
‚îÇ   ‚îú‚îÄ‚îÄ src/                      # React components
‚îÇ   ‚îú‚îÄ‚îÄ electron/                 # Electron main process
‚îÇ   ‚îî‚îÄ‚îÄ package.json
‚îî‚îÄ‚îÄ README.md
```

---

## ‚ö° Installation & Setup

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

## ÌæØ How to Use

1. **Start A.R.I.S.E.**: Run python main.py in the backend directory
2. **Listen for greeting**: Wait for "Hello! I'm A.R.I.S.E..."
3. **Speak naturally**: No wake words needed, just talk

### Example Commands:
- **Ì≤¨ Chat**: "How are you today?" / "Tell me a joke"
- **Ìº§Ô∏è Weather**: "What's the weather like?" / "Is it going to rain?"
- **Ì≥à Stocks**: "Tesla stock price" / "How's the market doing?"
- **Ì≥∞ News**: "Latest news" / "What's happening today?"
- **Ì∂•Ô∏è Apps**: "Open Facebook" / "Launch Chrome" / "Start calculator"
- **Ì∫™ Exit**: "Goodbye" / "Exit" / "Stop"

---

## ÌøóÔ∏è Architecture Overview

A.R.I.S.E. uses a **centralized TTS architecture** ensuring every response includes voice:

```
User Speech ‚Üí STT Engine ‚Üí Request Classifier ‚Üí Engine Router
                                                     ‚Üì
Chat Engine ‚Üê‚Üí Data Engine ‚Üê‚Üí Automation Engine
                                                     ‚Üì
                            All Responses ‚Üí Centralized TTS ‚Üí Audio Output
```

### Engine Responsibilities:
- **Ì∑† Chat Brain**: Conversational AI using Google Gemini
- **Ì≥ä Data Engine**: Real-time information (weather, stocks, news)
- **‚öôÔ∏è Automation Engine**: System tasks and application launching
- **Ìæ§ STT Engine**: Speech recognition and audio processing
- **Ì¥ä TTS Engine**: Voice synthesis with optimized timing
- **Ì≥± App Scanner**: System application discovery and management

---

## Ìª† Troubleshooting

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

## Ì≥à Project Status & Roadmap

| Component | Status | Performance |
|-----------|--------|-------------|
| Ìæ§ Speech Recognition | ‚úÖ Complete | Real-time, Google API |
| Ì¥ä Text-to-Speech | ‚úÖ Complete | 180 WPM, 100% reliability |
| Ì≤¨ Chat Engine | ‚úÖ Complete | Gemini AI integration |
| Ì≥ä Data Engine | ‚úÖ Complete | Weather, stocks, news |
| ‚öôÔ∏è Automation | ‚úÖ Complete | 0.06s app launching |
| Ì∂•Ô∏è Desktop UI | Ì∫ß In Progress | React + Electron |
| Ì≥± Mobile App | Ì¥ú Planned | Cross-platform |

### Recent Achievements ‚ú®
- **Fixed TTS Consistency**: Audio now plays for every response
- **Optimized Voice Speed**: Natural 180 WPM speech rate
- **Ultra-Fast Automation**: 30-second delays reduced to 0.06 seconds
- **Centralized Architecture**: Eliminated circular dependencies
- **Enhanced Reliability**: Multiple TTS fallback methods

---

## Ì¥ù Contributing

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

## Ì≥ú License

MIT License - Feel free to use, modify, and distribute.

---

**ÌæØ A.R.I.S.E. is production-ready and actively maintained.**

**Built with ‚ù§Ô∏è by XHLEIK** | [GitHub](https://github.com/XHLEIK/arise-ai)
