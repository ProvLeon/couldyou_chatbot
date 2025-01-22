#!/bin/bash
# deployment/scripts/setup_telegram.sh
set -e

# Create logs directory
mkdir -p /opt/couldyou_chatbot/telegram_bot/logs

# Set permissions
chown -R www-data:www-data /opt/couldyou_chatbot/telegram_bot

# Install systemd service
cp /opt/couldyou_chatbot/deployment/configs/couldyou-telegram.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable couldyou-telegram
systemctl start couldyou-telegram
