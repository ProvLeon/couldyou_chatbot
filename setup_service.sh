#!/bin/bash
# setup_service.sh
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

# Logging function
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

# Configuration
SERVICE_NAME="backend"
USER="ubuntu"
GROUP="ubuntu"
PROJECT_ROOT="/home/ubuntu/couldyou_chatbot"
BACKEND_DIR="${PROJECT_ROOT}/backend"
VENV_DIR="${BACKEND_DIR}/venv"
ENV_FILE="${PROJECT_ROOT}/.env"

# Check directory structure
log "Checking directory structure..."
[ -d "$PROJECT_ROOT" ] || error "Project root directory not found: $PROJECT_ROOT"
[ -d "$BACKEND_DIR" ] || error "Backend directory not found: $BACKEND_DIR"

# Check virtual environment
log "Checking virtual environment..."
if [ ! -d "$VENV_DIR" ]; then
    log "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
fi

# Check and create .env file if it doesn't exist
if [ ! -f "$ENV_FILE" ]; then
    log "Creating .env file..."
    cat > "$ENV_FILE" << EOF
FLASK_ENV=production
SECRET_KEY=$(openssl rand -hex 32)
GOOGLE_API_KEY=your-google-api-key
MONGODB_URI=mongodb://localhost:27017/couldyou
EOF
    chown $USER:$GROUP "$ENV_FILE"
    chmod 600 "$ENV_FILE"
    error "Please update the .env file with your credentials: $ENV_FILE"
fi

# Install dependencies
log "Installing dependencies..."
source "$VENV_DIR/bin/activate"
pip install -r "${BACKEND_DIR}/requirements.txt"
deactivate

# Set permissions
log "Setting permissions..."
chown -R $USER:$GROUP "$PROJECT_ROOT"
chmod -R 755 "$BACKEND_DIR"
chmod 600 "$ENV_FILE"

# Create service file
log "Creating systemd service..."
cat > "/etc/systemd/system/${SERVICE_NAME}.service" << EOF
[Unit]
Description=CouldYou Backend Service
After=network.target
StartLimitIntervalSec=0

[Service]
Type=simple
User=$USER
Group=$GROUP
RuntimeDirectory=couldyou_backend
LogsDirectory=couldyou_backend
WorkingDirectory=$BACKEND_DIR
Environment=PATH=$VENV_DIR/bin
EnvironmentFile=$ENV_FILE

ExecStartPre=/bin/bash -c 'test -d "$BACKEND_DIR"'
ExecStartPre=/bin/bash -c 'test -f "$ENV_FILE"'
ExecStartPre=/bin/bash -c 'test -d "$VENV_DIR"'

ExecStart=$VENV_DIR/bin/gunicorn --workers 4 --bind 127.0.0.1:5000 run:app

Restart=always
RestartSec=3
StartLimitBurst=5

NoNewPrivileges=true
PrivateTmp=true

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd
log "Reloading systemd..."
systemctl daemon-reload

# Enable and start service
log "Enabling and starting service..."
systemctl enable "${SERVICE_NAME}.service"
systemctl start "${SERVICE_NAME}.service"

# Check service status
log "Checking service status..."
if systemctl is-active --quiet "${SERVICE_NAME}.service"; then
    log "Service is running successfully"
else
    error "Service failed to start. Check logs with: journalctl -u ${SERVICE_NAME}.service"
fi

# Display service status
systemctl status "${SERVICE_NAME}.service"

log "Setup completed successfully!"
