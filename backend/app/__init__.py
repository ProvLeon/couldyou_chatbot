# backend/app/__init__.py
from flask import Flask
from flask_cors import CORS
from config import Config  # Changed from relative import

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    CORS(app)

    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)

    return app
