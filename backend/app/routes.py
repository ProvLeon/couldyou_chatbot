# backend/app/routes.py
from flask import Blueprint, request, jsonify
from app.services.chat_service import ChatService
from app.middleware import error_handler
import asyncio

bp = Blueprint('main', __name__)
chat_service = ChatService()

@bp.route('/')
def health_check():
    return jsonify({
        'status': 'healthy',
        'message': 'CouldYou? Chat API is running'
    })

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


@bp.errorhandler(404)
def not_found_error(error):
    return jsonify({
        'error': 'Not Found',
        'message': 'The requested URL was not found on the server.'
    }), 404

@bp.errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': 'Internal Server Error',
        'message': 'An unexpected error occurred.'
    }), 500
