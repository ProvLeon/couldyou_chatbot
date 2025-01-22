#!/bin/bash
# deployment/scripts/setup_python.sh
set -e

# Create Python virtual environments
echo "Creating virtual environments..."

# Backend venv
python3.9 -m venv /opt/couldyou_chatbot/backend/venv
source /opt/couldyou_chatbot/backend/venv/bin/activate
pip install --upgrade pip
pip install -r /opt/couldyou_chatbot/backend/requirements.txt
deactivate

# Telegram bot venv
python3.9 -m venv /opt/couldyou_chatbot/telegram_bot/venv
source /opt/couldyou_chatbot/telegram_bot/venv/bin/activate
pip install --upgrade pip
pip install -r /opt/couldyou_chatbot/telegram_bot/requirements.txt
deactivate
