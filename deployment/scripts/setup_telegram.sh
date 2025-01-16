#!/bin/bash
# deployment/scripts/setup_telegram.sh
set -e

# Create directory structure
mkdir -p /opt/couldyou/telegram
mkdir -p /opt/couldyou/telegram/logs

# Copy telegram bot files
cp -r ${SCRIPT_DIR}/../telegram_bot/* /opt/couldyou/telegram/

# Set permissions
chown -R www-data:www-data /opt/couldyou/telegram

# Install systemd service
cp ${SCRIPT_DIR}/configs/telegram.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable couldyou-telegram
systemctl start couldyou-telegram
