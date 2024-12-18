from flask import Flask
from flask_cors import CORS
from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Configure CORS
    CORS(app,
            resources={r"/*": {
                "origins": ["http://localhost:3000", "https://couldyou-chatbot.onrender.com"],
                "methods": ["GET", "POST", "OPTIONS"],
                "allow_headers": ["Content-Type", "Authorization"],
                "expose_headers": ["Content-Range", "X-Content-Range"],
                "supports_credentials": True
            }}
    )

    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)

    return app
