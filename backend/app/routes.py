# backend/app/routes.py
from flask import Blueprint, request, jsonify
from app.services.chat_service import ChatService
from app.middleware import error_handler
import asyncio

bp = Blueprint('main', __name__)
chat_service = ChatService()

@bp.route('/api/chat', methods=['POST'])
@error_handler
def chat():
    data = request.json
    # Run the async function in a synchronous context
    response = asyncio.run(chat_service.process_message(
        message=data.get("message", ""),
        session_id=data.get("session_id"),
        language=data.get("language", "en")
    ))
    return jsonify(response)

@bp.route('/api/sessions/<session_id>', methods=['DELETE'])
@error_handler
def clear_session(session_id):
    chat_service.chat_manager.clear_session(session_id)
    return jsonify({'status': 'success'})
