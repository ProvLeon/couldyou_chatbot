#!/bin/bash
# deployment/install.sh

# Exit on any error
set -e

# Script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Load environment variables
if [ -f .env ]; then
    source .env
fi

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

# Log function
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}"
    exit 1
}

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    error "Please run as root"
fi

# Update system
log "Updating system packages..."
apt-get update && apt-get upgrade -y || error "Failed to update system packages"

# Install system dependencies
log "Installing system dependencies..."
xargs apt-get install -y < ${SCRIPT_DIR}/requirements/system.txt || error "Failed to install system dependencies"

# Run setup scripts
log "Setting up Python environment..."
bash ${SCRIPT_DIR}/scripts/setup_python.sh || error "Failed to setup Python environment"

log "Setting up Nginx..."
bash ${SCRIPT_DIR}/scripts/setup_nginx.sh || error "Failed to setup Nginx"

log "Setting up Backend service..."
bash ${SCRIPT_DIR}/scripts/setup_backend.sh || error "Failed to setup Backend service"

log "Setting up Telegram bot service..."
bash ${SCRIPT_DIR}/scripts/setup_telegram.sh || error "Failed to setup Telegram bot service"


# Step 5: Verify installation
step5_verify() {
    log "Step 5: Verifying installation"

    services=("nginx" "couldyou-backend" "couldyou-telegram")

    for service in "${services[@]}"; do
        if systemctl is-active --quiet "$service"; then
            log "$service is running"
        else
            error "$service failed to start"
        fi
    done
}


# Main function
main() {
    # step1_system_setup
    # step2_python_setup
    # step3_create_services
    # step4_setup_nginx
    step5_verify
}

# Run main function
main

log "Installation completed successfully!"
