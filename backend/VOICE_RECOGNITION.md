# Voice Recognition System - A.R.I.S.E. AI

## Overview
The voice recognition module provides secure user enrollment and verification using SpeechBrain's pre-trained speaker verification models with additional audio feature analysis for enhanced security.

## Features
- **Master User Enrollment**: One-time voice registration with unique embedding storage
- **Dual Verification**: Combines SpeechBrain speaker recognition with librosa audio features
- **Conservative Thresholds**: Prioritizes security over convenience (0.75 default threshold)
- **Security Responses**: Automatic denial messages for unauthorized access attempts
- **Persistent Storage**: Voice features and metadata stored in organized directories

## Installation
```bash
pip install speechbrain librosa torch torchaudio numpy
```

## Usage

### Basic Implementation
```python
from modules.voice_recognition import VoiceRecognition

# Initialize voice recognition
vr = VoiceRecognition()

# Enroll master user (one-time setup)
success, message = vr.enroll_user("Master User", "enrollment_audio.wav")
print(f"Enrollment: {message}")

# Verify voice during runtime
is_recognized, result_message, confidence = vr.verify_voice("test_audio.wav")

if is_recognized:
    print(f"Access granted: {result_message}")
else:
    print(f"Access denied: {result_message}")
    
    # Get security response for TTS
    security_msg = vr.get_security_response()
    print(f"Security response: {security_msg}")
```

### Integration with A.R.I.S.E. TTS
```python
from modules.voice_recognition import VoiceRecognition
from modules.tts_engine import TTSEngine

vr = VoiceRecognition()
tts = TTSEngine()

# Verify user and respond accordingly
is_recognized, _, confidence = vr.verify_voice("user_audio.wav")

if not is_recognized:
    security_response = vr.get_security_response()
    tts.speak(security_response)
    return  # Deny access
    
# Continue with normal operation
tts.speak("Welcome back, master.")
```

## Configuration

### Security Thresholds
Located in `voice_recognition.py`:
```python
VERIFICATION_THRESHOLD = 0.75  # SpeechBrain verification threshold
FEATURE_THRESHOLD = 0.65       # Audio feature similarity threshold
```

### Data Storage
- **Voice Features**: `data/voice_features/` (audio features + enrollment audio)
- **User Metadata**: `data/users.json` (user info, file references)
- **Model Cache**: `data/speechbrain_cache/` (SpeechBrain model files)

### Security Responses
Customizable responses in `voice_recognition.py`:
```python
SECURITY_RESPONSES = [
    "Your voice doesn't match my master's voice.",
    "Who are you?",
    "I cannot share private information with you.",
    "Access denied. Unknown voice detected.",
    "This conversation is restricted to my master only."
]
```

## Technical Details

### Verification Process
1. **Feature Extraction**: Librosa extracts MFCC, spectral centroids, chroma, and zero-crossing rate
2. **SpeechBrain Analysis**: Deep learning-based speaker embedding comparison
3. **Dual Scoring**: Combined weighted score (40% features + 60% SpeechBrain)
4. **Conservative Decision**: Both scores must exceed thresholds for access

### Performance Characteristics
- **Accuracy**: High precision with conservative thresholds
- **Speed**: ~2-3 seconds for verification (model loading time)
- **Storage**: ~100KB per enrolled user (features + audio copy)
- **Dependencies**: SpeechBrain, librosa, torch, torchaudio, numpy

### Error Handling
- Graceful degradation if audio processing fails
- Missing file detection and user-friendly error messages
- Model initialization error reporting
- Automatic directory creation for data storage

## API Reference

### VoiceRecognition Class

#### Methods
- `enroll_user(name: str, audio_file_path: str) -> Tuple[bool, str]`
- `verify_voice(audio_file_path: str) -> Tuple[bool, str, float]`
- `get_security_response() -> str`
- `is_master_enrolled() -> bool`
- `get_master_user() -> Optional[dict]`

#### Returns
- **Enrollment**: `(success: bool, message: str)`
- **Verification**: `(is_recognized: bool, message: str, confidence: float)`

## Integration Notes

### With A.R.I.S.E. Main System
- Keep module **completely separate** from `main.py`
- Use only for critical security checkpoints
- Always route TTS responses through main system's `_speak()` method
- Integrate with existing memory and session management

### Audio File Requirements
- **Format**: WAV, MP3, FLAC (supported by librosa)
- **Duration**: Minimum 2-3 seconds for reliable enrollment
- **Quality**: 16kHz sample rate recommended
- **Content**: Clear speech without background noise

## Security Considerations
- **Conservative Thresholds**: Prevents false positives
- **No Voice Storage**: Only features stored, not raw audio (except enrollment copy)
- **Unique User IDs**: UUID-based identification
- **Metadata Encryption**: Consider encrypting users.json for production
- **Access Logging**: Track verification attempts for security monitoring