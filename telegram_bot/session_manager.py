# couldyou_chatbot/telegram_bot/session_manager.py
from typing import Dict, List, Optional
import time

class Session:
    def __init__(self):
        self.messages: List[Dict] = []
        self.last_activity: float = time.time()

    def add_message(self, text: str, is_user: bool):
        self.messages.append({
            "text": text,
            "is_user": is_user,
            "timestamp": time.time()
        })
        self.last_activity = time.time()

class SessionManager:
    def __init__(self):
        self.sessions: Dict[str, Session] = {}

    def get_session(self, user_id: str) -> Session:
        if user_id not in self.sessions:
            self.sessions[user_id] = Session()
        return self.sessions[user_id]

    def clear_session(self, user_id: str):
        if user_id in self.sessions:
            del self.sessions[user_id]

    def cleanup_old_sessions(self, max_age: int = 3600):
        """Remove sessions older than max_age seconds"""
        current_time = time.time()
        to_remove = []

        for user_id, session in self.sessions.items():
            if current_time - session.last_activity > max_age:
                to_remove.append(user_id)

        for user_id in to_remove:
            self.clear_session(user_id)
