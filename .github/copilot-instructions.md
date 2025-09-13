# A.R.I.S.E. AI Assistant - Copilot Instructions

## Project Overview
A.R.I.S.E. (Advanced Real-time Intelligent System for Execution) is a **voice-controlled AI assistant** with a centralized TTS architecture ensuring every response includes audio. The system routes user requests through specialized engines using keyword-based classification.

## Core Architecture Pattern

### Centralized TTS Design
```python
# ALL responses must go through main.py's _speak() method
def _speak(self, text: str):
    """Centralized TTS function - ALL responses go through here."""
    # Creates fresh TTS instance, handles fallbacks, prints AFTER audio
```

**Critical Rule**: Engine modules (`brain/`, `automation_engine.py`) return text only. Never call TTS directly from engines - only `main.py` handles voice output.

## Development Rules (Strictly Enforced)

### Code Quality Standards
- **Minimal & Necessary**: Ship smallest correct solution, no extra dependencies
- **Clarity First**: Clean naming, clear structure, readable code
- **No Junk**: Never output placeholders, lorem code, or unnecessary boilerplate
- **Project Boundaries**: Do NOT modify `main.py` unless explicitly instructed

### Logging & Error Handling
```python
# ✅ Correct: Minimal, meaningful logs
print("Initializing TTS Engine...")
print("Speaking: Hello")
print("Done.")

# ✅ Correct: Short, clear error handling
except Exception as e:
    print(f"TTS error: {e}")

# ❌ Wrong: Verbose debug spam, internal library logs
```

### Output Format Requirements
Every code response must include this header:
```
# Explanation: <1-2 lines, why this approach>
# Assumptions: <bullet list of assumptions>  
# Files to create: <paths>
# Run commands: <commands to run/test>
```

## Key Components

### Main Orchestrator (`backend/main.py`)
- **Flow**: Check app DB → Greet → Listen → Classify → Route → Speak → Loop
- **Classification**: Keyword-based routing (`data_keywords`, `automation_keywords`, default `chat`)
- **Error Handling**: All exceptions go through `_speak()` for voice feedback
- **DO NOT MODIFY** unless explicitly requested

### Engine Modules (`backend/modules/`)
```
🔊 tts_engine.py         # 180 WPM optimized, multiple fallbacks
🎤 stt_engine.py         # Google Speech Recognition, 30s timeout
⚙️ automation_engine.py   # 0.06s app launching, URL mapping
📱 app_scanner.py        # System app discovery → data/applications.json
🧠 brain/chat_brain.py   # Google Gemini conversational AI
📊 brain/data_engine.py  # Weather/stocks/news APIs
🧠 memory_manager.py     # Session buffer + long-term facts storage
```

## Development Patterns

### Engine Independence
```python
# ✅ Correct: Engines return text responses
def get_response(self, text: str) -> str:
    return "Weather is sunny today"

# ❌ Wrong: Don't call TTS from engines  
def get_response(self, text: str):
    self.tts.speak("Weather is sunny")  # Never do this
```

### Algorithm & Performance Standards
```python
# Time: O(n), Space: O(1) - Include complexity for non-trivial functions
def process_requests(self, requests: List[str]) -> List[str]:
    # Use right data structure: dict for O(1) lookups
    results = {}
    for request in requests:
        results[request] = self.process(request)
    return list(results.values())
```

### Request Classification
```python
# Add keywords to main.py classification logic:
data_keywords = ['weather', 'stock', 'news', ...]
automation_keywords = ['open', 'launch', 'start', ...]
# Default: route to chat brain
```

## Performance Requirements
- **TTS**: 180 WPM speech rate, fresh engine instances for reliability
- **Automation**: Sub-0.1 second app launching via direct paths
- **STT**: Real-time with 30-second listening window
- **Memory**: Sessions → `data/sessions/`, facts → `data/facts.json`

## Configuration & Setup

### Required API Keys (`modules/brain/.env`)
```
GEMINI_API_KEY=your_key_here
```

### Data Structure
```
data/
├── applications.json     # App paths from scanner
├── facts.json           # Long-term memory facts
└── sessions/            # Timestamped conversation logs
```

### Testing Commands
```bash
# Test full system
python backend/main.py

# Test individual engines
python -c "from modules.tts_engine import TTSEngine; TTSEngine().speak('test')"
python -c "from modules.memory_manager import MemoryManager; mm = MemoryManager()"
```

## Security & Dependencies

### Security Rules
- Never hardcode secrets, use environment variables
- Validate and sanitize external inputs
- Parameterize database queries
- Mention encryption for sensitive data

### Dependency Management
- **Minimal dependencies**: Prefer stdlib or widely adopted libraries
- **Pin versions**: Use exact versions when possible
- **Justify large dependencies**: Explain why needed

## Testing & Reliability

### Testing Standards
```python
# Include unit tests for non-trivial logic
def test_tts_engine():
    engine = TTSEngine()
    result = engine.speak("test")
    assert result is True

# Cover edge cases: empty, null, boundary conditions
def test_empty_input():
    engine = TTSEngine()
    result = engine.speak("")
    assert result is False
```

### Error Recovery
- Use explicit error types with meaningful messages
- Provide graceful fallbacks when features unavailable
- Never swallow errors silently

## Key Debugging Points

### TTS Issues
- Check fresh engine creation in `_speak()`
- Verify fallback mechanisms activate
- Audio plays BEFORE text display

### Engine Routing
- Add debug prints in `_classify_request()`
- Verify keyword matching logic
- Check `_process_request()` error handling

### Memory System
- Sessions auto-save on conversation end
- Facts merge/update without overwriting
- All file operations have error handling

## Final Checklist (Before Committing)

- [ ] Header included (Explanation, Assumptions, Files, Commands)
- [ ] No secrets in code samples
- [ ] Complexity comments for non-trivial logic
- [ ] Minimal logs, short error handling
- [ ] No extra/unnecessary files
- [ ] No changes to `main.py` unless requested
- [ ] All engines remain independent and text-only
- [ ] Centralized TTS pattern maintained

## Frontend Integration (React + Electron)
- Backend runs independently via `python main.py`
- Frontend components in `frontend/src/components/`
- Electron main process in `frontend/electron/`

**Remember**: A.R.I.S.E. is production-ready with 100% TTS reliability, optimized performance, and modular engine design. Focus on maintaining the centralized TTS pattern and engine independence when making changes.