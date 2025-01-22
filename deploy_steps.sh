#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}"
    exit 1
}

warn() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING: $1${NC}"
}

# Step 1: Run updated setup script
step1_system_setup() {
    log "Step 1: Running system setup"
    sudo ./updated_setup.sh
}

# Step 2: Python Environment Setup
step2_python_setup() {
    log "Step 2: Setting up Python environments"

    # Backend virtual environment
    python3.11 -m venv backend/venv
    backend/venv/bin/pip install --upgrade pip
    backend/venv/bin/pip install -r requirements.txt

    # Telegram bot virtual environment
    python3.11 -m venv telegram_bot/venv
    telegram_bot/venv/bin/pip install --upgrade pip
    telegram_bot/venv/bin/pip install -r telegram_bot/requirements.txt
}

# Step 3: Create service files
step3_create_services() {
    log "Step 3: Creating service files"

    # Create backend service
    sudo bash -c 'cat > /etc/systemd/system/couldyou-backend.service << EOL
[Unit]
Description=CouldYou Backend Service
After=network.target

[Service]
User=ubuntu
Group=ubuntu
WorkingDirectory=/opt/couldyou_chatbot/backend
Environment="PATH=/opt/couldyou_chatbot/backend/venv/bin"
ExecStart=/opt/couldyou_chatbot/backend/venv/bin/gunicorn --workers 4 --bind 0.0.0.0:5000 run:app

[Install]
WantedBy=multi-user.target
EOL'

    # Create telegram service
    sudo bash -c 'cat > /etc/systemd/system/couldyou-telegram.service << EOL
[Unit]
Description=CouldYou Telegram Bot Service
After=network.target

[Service]
User=ubuntu
Group=ubuntu
WorkingDirectory=/opt/couldyou_chatbot/telegram_bot
Environment="PATH=/opt/couldyou_chatbot/telegram_bot/venv/bin"
ExecStart=/opt/couldyou_chatbot/telegram_bot/venv/bin/python bot.py

[Install]
WantedBy=multi-user.target
EOL'
}

# Step 4: Setup services
step4_setup_services() {
    log "Step 4: Setting up services"

    sudo systemctl daemon-reload
    sudo systemctl enable couldyou-backend couldyou-telegram
    sudo systemctl start couldyou-backend couldyou-telegram
}

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

# Main execution
main() {
    log "Starting deployment process..."

    step1_system_setup
    step2_python_setup
    step3_create_services
    step4_setup_services
    step5_verify

    log "Deployment completed successfully!"
}

# Run main function
main
