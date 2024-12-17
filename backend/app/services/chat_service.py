# backend/app/services/chat_service.py
from typing import Dict
from .nlp_service import NLPService
from .translation_service import TranslationService
from .chat_manager import ChatManager
import uuid

class ChatService:
    def __init__(self):
        self.nlp = NLPService()
        self.translator = TranslationService()
        self.chat_manager = ChatManager()

    async def process_message(self, message: str, session_id: str = None, language: str = "en") -> Dict:
        if not session_id:
            session_id = str(uuid.uuid4())

        context = self.chat_manager.get_context(session_id)
        response = await self.nlp.process_input(message, language)

        response_content = response.get("content", "I apologize, I couldn't process that request.")

        self.chat_manager.add_message(session_id, {
            "role": "user",
            "content": message
        })

        self.chat_manager.add_message(session_id, {
            "role": "assistant",
            "content": response_content
        })

        if language != "en":
            response_content = self.translator.translate(response_content, language)

        return {
            "session_id": session_id,
            "response": {
                "type": response.get("type", "simple"),
                "text": response_content
            }
        }
