#!/bin/bash
# deployment/scripts/setup_nginx.sh
set -e

# Copy Nginx configuration
log "Configuring Nginx..."
cp ${SCRIPT_DIR}/configs/nginx.conf /etc/nginx/sites-available/couldyou

# Create symbolic link
ln -sf /etc/nginx/sites-available/couldyou /etc/nginx/sites-enabled/

# Test Nginx configuration
nginx -t || error "Invalid Nginx configuration"

# Restart Nginx
systemctl restart nginx
