# backend/app/middleware.py
from functools import wraps
from flask import jsonify
from typing import Callable
import traceback

def error_handler(f: Callable):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            # Log the error
            print(f"Error: {str(e)}")
            print(traceback.format_exc())

            return jsonify({
                "error": "An unexpected error occurred",
                "message": str(e)
            }), 500

    return decorated_function
