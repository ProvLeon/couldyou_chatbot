#!/bin/bash
# deployment/scripts/setup_python.sh
set -e

# Create Python virtual environments
log "Creating virtual environments..."

# Backend venv
python3.9 -m venv /opt/couldyou/backend/venv
source /opt/couldyou/backend/venv/bin/activate
pip install --upgrade pip
pip install -r ${SCRIPT_DIR}/requirements/backend.txt
deactivate

# Telegram bot venv
python3.9 -m venv /opt/couldyou/telegram/venv
source /opt/couldyou/telegram/venv/bin/activate
pip install --upgrade pip
pip install -r ${SCRIPT_DIR}/requirements/telegram.txt
deactivate
