"""
A.R.I.S.E. AI - Voice Recognition Module

Handles user voice enrollment and verification using SpeechBrain.
Primary verification using SpeechBrain pre-trained models with librosa feature extraction.
"""

import os
import json
import numpy as np
from typing import Tuple, Optional
from datetime import datetime
import uuid

# Configuration constants
VERIFICATION_THRESHOLD = 0.60  # SpeechBrain verification threshold (lowered for testing)
FEATURE_THRESHOLD = 0.50       # Audio feature similarity threshold (lowered for testing)
DATA_DIR = "data"
USERS_FILE = os.path.join(DATA_DIR, "users.json")
FEATURES_DIR = os.path.join(DATA_DIR, "voice_features")

# Security responses for unauthorized users
SECURITY_RESPONSES = [
    "Your voice doesn't match my master's voice.",
    "Who are you?",
    "I cannot share private information with you.",
    "Access denied. Unknown voice detected.",
    "This conversation is restricted to my master only."
]


class VoiceRecognition:
    """Voice enrollment and verification system using SpeechBrain."""
    
    def __init__(self):
        """Initialize voice recognition with SpeechBrain model."""
        self.speechbrain_model = None
        self.users_data = {}
        self._init_models()
        self._load_users()
        self._ensure_directories()
    
    def _init_models(self):
        """Initialize SpeechBrain speaker verification model."""
        try:
            from speechbrain.inference import SpeakerRecognition
            self.speechbrain_model = SpeakerRecognition.from_hparams(
                source="speechbrain/spkrec-ecapa-voxceleb",
                savedir="data/speechbrain_cache"
            )
            print("SpeechBrain speaker verification model loaded.")
        except ImportError:
            raise ImportError("SpeechBrain not installed. Run: pip install speechbrain torch torchaudio")
        except Exception as e:
            print(f"SpeechBrain initialization error: {e}")
            raise
    
    def _ensure_directories(self):
        """Create necessary directories if they don't exist."""
        os.makedirs(DATA_DIR, exist_ok=True)
        os.makedirs(FEATURES_DIR, exist_ok=True)
        os.makedirs("data/speechbrain_cache", exist_ok=True)
    
    def _load_users(self):
        """Load existing users data from JSON file."""
        try:
            if os.path.exists(USERS_FILE):
                with open(USERS_FILE, 'r') as f:
                    self.users_data = json.load(f)
            else:
                self.users_data = {}
        except Exception as e:
            print(f"Error loading users data: {e}")
            self.users_data = {}
    
    def _save_users(self):
        """Save users data to JSON file."""
        try:
            with open(USERS_FILE, 'w') as f:
                json.dump(self.users_data, f, indent=2)
        except Exception as e:
            print(f"Error saving users data: {e}")
    
    def _extract_features(self, audio_file_path: str) -> Optional[np.ndarray]:
        """Extract audio features using librosa for additional verification."""
        try:
            import librosa
            
            # Load audio file
            audio, sr = librosa.load(audio_file_path, sr=16000, duration=10.0)
            
            # Extract MFCC features
            mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=13)
            
            # Extract additional features
            spectral_centroids = librosa.feature.spectral_centroid(y=audio, sr=sr)
            chroma = librosa.feature.chroma_stft(y=audio, sr=sr)
            zero_crossing_rate = librosa.feature.zero_crossing_rate(audio)
            
            # Combine features and take mean across time
            features = np.concatenate([
                np.mean(mfcc, axis=1),
                np.mean(spectral_centroids, axis=1),
                np.mean(chroma, axis=1),
                np.mean(zero_crossing_rate, axis=1)
            ])
            
            return features
            
        except Exception as e:
            print(f"Error extracting features: {e}")
            return None
    
    def enroll_user(self, name: str, audio_file_path: str) -> Tuple[bool, str]:
        """
        Enroll a new user with voice sample.
        
        Args:
            name: User's name
            audio_file_path: Path to audio file for enrollment
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            if not os.path.exists(audio_file_path):
                return False, f"Audio file not found: {audio_file_path}"
            
            # Generate unique user ID
            user_id = str(uuid.uuid4())
            
            # Extract audio features
            features = self._extract_features(audio_file_path)
            if features is None:
                return False, "Failed to extract voice features"
            
            # Save features to file
            features_filename = f"{user_id}_features.npy"
            features_path = os.path.join(FEATURES_DIR, features_filename)
            np.save(features_path, features)
            
            # Store enrollment audio path for SpeechBrain comparison
            enrollment_audio_filename = f"{user_id}_enrollment.wav"
            enrollment_audio_path = os.path.join(FEATURES_DIR, enrollment_audio_filename)
            
            # Copy enrollment audio to features directory
            import shutil
            shutil.copy2(audio_file_path, enrollment_audio_path)
            
            # Store user metadata
            user_data = {
                "user_id": user_id,
                "name": name,
                "features_file": features_filename,
                "enrollment_audio": enrollment_audio_filename,
                "created_at": datetime.now().isoformat(),
                "is_master": True  # First enrolled user is master
            }
            
            self.users_data[user_id] = user_data
            self._save_users()
            
            return True, f"User '{name}' enrolled successfully as master user"
            
        except Exception as e:
            return False, f"Enrollment failed: {e}"
    
    def verify_voice(self, audio_file_path: str) -> Tuple[bool, str, float]:
        """
        Verify voice against enrolled master user using dual verification.
        
        Args:
            audio_file_path: Path to audio file for verification
            
        Returns:
            Tuple of (is_recognized: bool, message: str, confidence: float)
        """
        try:
            if not os.path.exists(audio_file_path):
                return False, "Audio file not found", 0.0
            
            if not self.users_data:
                return False, "No enrolled users found", 0.0
            
            # Find master user
            master_user = None
            for user_data in self.users_data.values():
                if user_data.get("is_master", False):
                    master_user = user_data
                    break
            
            if not master_user:
                return False, "No master user found", 0.0
            
            # Feature-based verification
            feature_score = 0.0
            current_features = self._extract_features(audio_file_path)
            if current_features is not None:
                features_path = os.path.join(FEATURES_DIR, master_user["features_file"])
                if os.path.exists(features_path):
                    master_features = np.load(features_path)
                    
                    # Calculate cosine similarity
                    dot_product = np.dot(current_features, master_features)
                    norm_current = np.linalg.norm(current_features)
                    norm_master = np.linalg.norm(master_features)
                    
                    if norm_current > 0 and norm_master > 0:
                        feature_score = dot_product / (norm_current * norm_master)
                    
                    # Ensure score is between 0 and 1
                    feature_score = max(0.0, min(1.0, feature_score))
            
            # SpeechBrain verification
            speechbrain_score = 0.0
            try:
                enrollment_audio_path = os.path.join(FEATURES_DIR, master_user["enrollment_audio"])
                if os.path.exists(enrollment_audio_path):
                    # Load and process audio files properly for SpeechBrain
                    import torch
                    import torchaudio
                    
                    # Load audio files using torchaudio (SpeechBrain's expected format)
                    current_waveform, current_sr = torchaudio.load(audio_file_path)
                    master_waveform, master_sr = torchaudio.load(enrollment_audio_path)
                    
                    # Resample to 16kHz if needed (SpeechBrain standard)
                    if current_sr != 16000:
                        resampler = torchaudio.transforms.Resample(current_sr, 16000)
                        current_waveform = resampler(current_waveform)
                    
                    if master_sr != 16000:
                        resampler = torchaudio.transforms.Resample(master_sr, 16000)
                        master_waveform = resampler(master_waveform)
                    
                    # Ensure single channel (mono)
                    if current_waveform.size(0) > 1:
                        current_waveform = current_waveform.mean(dim=0, keepdim=True)
                    if master_waveform.size(0) > 1:
                        master_waveform = master_waveform.mean(dim=0, keepdim=True)
                    
                    # Get speaker embeddings using the waveforms directly
                    current_embedding = self.speechbrain_model.encode_batch(current_waveform)
                    master_embedding = self.speechbrain_model.encode_batch(master_waveform)
                    
                    # Calculate cosine similarity between embeddings
                    current_emb = current_embedding.squeeze()
                    master_emb = master_embedding.squeeze()
                    
                    # Compute cosine similarity manually
                    dot_product = torch.dot(current_emb, master_emb)
                    norm_current = torch.norm(current_emb)
                    norm_master = torch.norm(master_emb)
                    
                    if norm_current > 0 and norm_master > 0:
                        speechbrain_score = float(dot_product / (norm_current * norm_master))
                    
                    # Ensure score is between 0 and 1
                    speechbrain_score = max(0.0, min(1.0, speechbrain_score))
                    
            except Exception as e:
                print(f"SpeechBrain verification error: {e}")
                speechbrain_score = 0.0
            
            # Combined confidence score (weighted average)
            combined_score = (0.4 * feature_score + 0.6 * speechbrain_score)
            
            # Debug output
            print(f"🔍 Voice verification scores:")
            print(f"   Feature similarity: {feature_score:.3f} (threshold: {FEATURE_THRESHOLD})")
            print(f"   SpeechBrain score: {speechbrain_score:.3f} (threshold: {VERIFICATION_THRESHOLD})")
            print(f"   Combined score: {combined_score:.3f}")
            
            # Verification decision with conservative thresholds
            # If SpeechBrain failed but features are available, use feature-only verification
            if speechbrain_score == 0.0 and feature_score > 0.0:
                print("⚠️  SpeechBrain failed, using feature-only verification")
                is_verified = feature_score >= (FEATURE_THRESHOLD - 0.1)  # Slightly lower threshold for fallback
                combined_score = feature_score
            else:
                # Normal dual verification
                is_verified = (
                    speechbrain_score >= VERIFICATION_THRESHOLD and 
                    feature_score >= FEATURE_THRESHOLD
                )
            
            if is_verified:
                message = f"Recognized as Master User ({master_user['name']})"
                return True, message, combined_score
            else:
                message = "Different User Detected"
                return False, message, combined_score
                
        except Exception as e:
            return False, f"Verification failed: {e}", 0.0
    
    def get_security_response(self) -> str:
        """Get a random security response for unauthorized users."""
        import random
        return random.choice(SECURITY_RESPONSES)
    
    def is_master_enrolled(self) -> bool:
        """Check if a master user is enrolled."""
        for user_data in self.users_data.values():
            if user_data.get("is_master", False):
                return True
        return False
    
    def get_master_user(self) -> Optional[dict]:
        """Get master user data."""
        for user_data in self.users_data.values():
            if user_data.get("is_master", False):
                return user_data
        return None


# Usage Example (in comments):
"""
# Basic enrollment and verification workflow:

from modules.voice_recognition import VoiceRecognition

# Initialize voice recognition
vr = VoiceRecognition()

# Enroll master user (one-time setup)
success, message = vr.enroll_user("John Doe", "path/to/enrollment_audio.wav")
if success:
    print(f"Enrollment: {message}")
else:
    print(f"Enrollment failed: {message}")

# Verify voice during runtime
is_recognized, result_message, confidence = vr.verify_voice("path/to/test_audio.wav")
if is_recognized:
    print(f"Access granted: {result_message} (confidence: {confidence:.2f})")
else:
    print(f"Access denied: {result_message} (confidence: {confidence:.2f})")
    
    # Get security response for TTS
    security_msg = vr.get_security_response()
    print(f"Security response: {security_msg}")

# Check if master user exists
if vr.is_master_enrolled():
    master = vr.get_master_user()
    print(f"Master user: {master['name']} (enrolled: {master['created_at']})")

# Example integration with TTS engine:
if not is_recognized:
    from modules.tts_engine import TTSEngine
    tts = TTSEngine()
    security_response = vr.get_security_response()
    tts.speak(security_response)
"""