# Explanation: JSON-based memory system with session buffer and long-term facts storage
# Assumptions: data/ directory will be created if missing, JSON serializable messages only
# Files to create: backend/modules/memory_manager.py
# Run commands: python -c "from modules.memory_manager import MemoryManager; mm = MemoryManager(); mm.add_message('user', 'test')"

import json
import os
import time
from pathlib import Path
from typing import Dict, List, Any, Optional

class MemoryManager:
    """
    Two-layer memory system: session buffer + long-term facts.
    Time: O(1) for add_message, O(n) for save/load operations
    Space: O(n) where n is buffer size + facts size
    """
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.sessions_dir = self.data_dir / "sessions"
        self.facts_file = self.data_dir / "facts.json"
        self.session_buffer: List[Dict[str, Any]] = []
        
        # Create directories if they don't exist
        self.sessions_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize facts.json if it doesn't exist
        if not self.facts_file.exists():
            self._write_json(self.facts_file, {})
    
    def add_message(self, role: str, content: str) -> None:
        """Add message to session buffer. O(1) operation."""
        self.session_buffer.append({
            "role": role,
            "content": content,
            "timestamp": time.time()
        })
    
    def save_session(self) -> str:
        """Save buffer to sessions file, clear buffer. Returns session_id."""
        if not self.session_buffer:
            return ""
        
        session_id = f"session_{int(time.time())}"
        session_file = self.sessions_dir / f"{session_id}.json"
        
        try:
            session_data = {
                "session_id": session_id,
                "created_at": time.time(),
                "messages": self.session_buffer.copy()
            }
            self._write_json(session_file, session_data)
            self.session_buffer.clear()
            print(f"Session saved: {session_id}")
            return session_id
        except Exception as e:
            print(f"Error saving session: {e}")
            return ""
    
    def load_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Load session from sessions folder. O(1) file operation."""
        session_file = self.sessions_dir / f"{session_id}.json"
        
        try:
            if session_file.exists():
                session_data = self._read_json(session_file)
                print(f"Session loaded: {session_id}")
                return session_data
            return None
        except Exception as e:
            print(f"Error loading session: {e}")
            return None
    
    def update_facts(self, new_facts: Dict[str, Any]) -> None:
        """Merge/update new facts into facts.json. O(n) where n is facts size."""
        try:
            current_facts = self.load_facts()
            current_facts.update(new_facts)
            self._write_json(self.facts_file, current_facts)
            print("Facts updated")
        except Exception as e:
            print(f"Error updating facts: {e}")
    
    def load_facts(self) -> Dict[str, Any]:
        """Return current facts as dict. O(1) file operation."""
        try:
            return self._read_json(self.facts_file)
        except Exception as e:
            print(f"Error loading facts: {e}")
            return {}
    
    def delete_all_sessions(self) -> bool:
        """Delete all session files and clear current session buffer. Returns True if successful."""
        try:
            # Clear current session buffer
            self.session_buffer.clear()
            
            # Delete all session files
            deleted_count = 0
            if self.sessions_dir.exists():
                for session_file in self.sessions_dir.glob("session_*.json"):
                    try:
                        session_file.unlink()  # Delete the file
                        deleted_count += 1
                    except Exception as e:
                        print(f"Error deleting session file {session_file}: {e}")
            
            print(f"Memory cleared: {deleted_count} session files deleted")
            return True
            
        except Exception as e:
            print(f"Error clearing memory: {e}")
            return False
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get statistics about current memory usage. Returns dict with session and fact counts."""
        try:
            stats = {
                "session_buffer_messages": len(self.session_buffer),
                "saved_sessions": 0,
                "stored_facts": 0
            }
            
            # Count saved session files
            if self.sessions_dir.exists():
                stats["saved_sessions"] = len(list(self.sessions_dir.glob("session_*.json")))
            
            # Count stored facts
            facts = self.load_facts()
            stats["stored_facts"] = len(facts)
            
            return stats
            
        except Exception as e:
            print(f"Error getting memory stats: {e}")
            return {"session_buffer_messages": 0, "saved_sessions": 0, "stored_facts": 0}
    
    def _read_json(self, file_path: Path) -> Dict[str, Any]:
        """Read JSON file safely."""
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _write_json(self, file_path: Path, data: Dict[str, Any]) -> None:
        """Write JSON file safely with proper formatting."""
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)