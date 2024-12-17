# backend/app/services/chat_manager.py
from typing import List, Dict
import time

class ChatManager:
    def __init__(self):
        self.sessions: Dict[str, List[Dict]] = {}

    def create_session(self, session_id: str) -> None:
        if session_id not in self.sessions:
            self.sessions[session_id] = []

    def add_message(self, session_id: str, message: Dict) -> None:
        if session_id not in self.sessions:
            self.create_session(session_id)

        message['timestamp'] = time.time()
        self.sessions[session_id].append(message)

    def get_context(self, session_id: str, limit: int = 5) -> List[Dict]:
        if session_id not in self.sessions:
            return []

        return self.sessions[session_id][-limit:]

    def clear_session(self, session_id: str) -> None:
        if session_id in self.sessions:
            del self.sessions[session_id]
