#!/bin/bash
# deployment/scripts/setup_nginx.sh
set -e

# Script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Log functions
log() {
    echo -e "\033[0;32m[$(date +'%Y-%m-%d %H:%M:%S')] $1\033[0m"
}

error() {
    echo -e "\033[0;31m[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $1\033[0m"
    exit 1
}

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    error "Please run as root"
fi

# Install Nginx if not already installed
if ! command -v nginx &> /dev/null; then
    log "Installing Nginx..."
    apt-get update
    apt-get install -y nginx
fi

# Create necessary directories
log "Creating necessary directories..."
mkdir -p /var/log/nginx
mkdir -p /etc/nginx/sites-available
mkdir -p /etc/nginx/sites-enabled

# Remove default configuration if it exists
if [ -f /etc/nginx/sites-enabled/default ]; then
    log "Removing default Nginx configuration..."
    rm /etc/nginx/sites-enabled/default
fi

# Copy Nginx configuration
log "Configuring Nginx..."
cp ${SCRIPT_DIR}/../configs/nginx.conf /etc/nginx/sites-available/couldyou

# Create symbolic link
log "Creating symbolic link..."
ln -sf /etc/nginx/sites-available/couldyou /etc/nginx/sites-enabled/

# Set proper permissions
log "Setting permissions..."
chown -R www-data:www-data /var/log/nginx
chmod 755 /etc/nginx/sites-available/couldyou

# Verify Nginx configuration
log "Testing Nginx configuration..."
nginx -t || error "Invalid Nginx configuration"

# Start/Enable Nginx service
log "Enabling and starting Nginx service..."
systemctl enable nginx
systemctl start nginx || systemctl restart nginx

# Configure firewall if UFW is installed
if command -v ufw &> /dev/null; then
    log "Configuring firewall..."
    ufw allow 'Nginx Full'
    ufw allow 80/tcp
    ufw allow 443/tcp
fi

# Create SSL directory (for future use)
log "Creating SSL directory..."
mkdir -p /etc/nginx/ssl

# Backup existing configuration
log "Creating backup of current configuration..."
mkdir -p /etc/nginx/backup
cp -r /etc/nginx/sites-available /etc/nginx/backup/
cp -r /etc/nginx/sites-enabled /etc/nginx/backup/

log "Nginx setup completed successfully!"

# Optional: Display status
log "Nginx status:"
systemctl status nginx --no-pager

# Display configured sites
log "Configured sites:"
ls -l /etc/nginx/sites-enabled/
