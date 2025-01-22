#!/bin/bash
# deployment/scripts/setup_backend.sh
sset -e

# Create logs directory
mkdir -p /opt/couldyou_chatbot/backend/logs

# Set permissions
chown -R www-data:www-data /opt/couldyou_chatbot/backend

# Install systemd service
cp /opt/couldyou_chatbot/deployment/configs/couldyou-backend.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable couldyou-backend
systemctl start couldyou-backend
