# couldyou_chatbot/telegram_bot/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:5000")

    # Add other configuration options as needed
    ALLOWED_USERS = os.getenv("ALLOWED_USERS", "").split(",")
    MAX_MESSAGE_LENGTH = 4096  # Telegram's max message length
