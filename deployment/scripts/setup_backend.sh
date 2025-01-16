#!/bin/bash
# deployment/scripts/setup_backend.sh
set -e

# Create directory structure
mkdir -p /opt/couldyou/backend
mkdir -p /opt/couldyou/backend/logs

# Copy backend files
cp -r ${SCRIPT_DIR}/../backend/* /opt/couldyou/backend/

# Set permissions
chown -R www-data:www-data /opt/couldyou/backend

# Install systemd service
cp ${SCRIPT_DIR}/configs/backend.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable couldyou-backend
systemctl start couldyou-backend
