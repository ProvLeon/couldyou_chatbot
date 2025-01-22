# deploy_steps.sh
#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

warn() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING: $1${NC}"
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}"
    exit 1
}

prompt_continue() {
    echo -e "${YELLOW}"
    read -p "Continue to next step? (y/n) " -n 1 -r
    echo -e "${NC}"
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
}

# Step 1: System Updates and Dependencies
step1_system_setup() {
    log "Step 1: System Updates and Dependencies"

    sudo apt-get update
    sudo apt-get upgrade -y

    # Install system requirements
    sudo apt-get install -y $(cat deployment/requirements/system.txt)

    prompt_continue
}

# Step 2: Python Environment Setup
step2_python_setup() {
    log "Step 2: Setting up Python environments"

    # Backend virtual environment
    python3 -m venv backend/venv
    source backend/venv/bin/activate
    pip install -r deployment/requirements/backend.txt
    deactivate

    # Telegram bot virtual environment
    python3 -m venv telegram_bot/venv
    source telegram_bot/venv/bin/activate
    pip install -r deployment/requirements/telegram.txt
    deactivate

    prompt_continue
}

# Step 3: Environment Configuration
step3_env_setup() {
    log "Step 3: Setting up environment configuration"

    if [ ! -f .env ]; then
        cat > .env << EOF
FLASK_ENV=production
SECRET_KEY="$(openssl rand -hex 32)"
HF_HOME="./model_cache"
GOOGLE_API_KEY="AIzaSyDlMO40t1n7kOVutn1CkSa-9CmWwodhOXI"
BACKEND_URL="http://54.242.250.139"
TELEGRAM_BOT_TOKEN="7900644474:AAEVnfJSaaOFJjK-JZCOwtVh2Lmnz8YbGnc"
ALLOWED_USERS=  # Optional: comma-separated list of allowed user IDs

EOF
        warn "Please edit .env file with your actual credentials"
        nano .env
    else
        warn ".env file already exists. Please verify its contents"
        cat .env
    fi

    prompt_continue
}

# Step 4: Nginx Setup
step4_nginx_setup() {
    log "Step 4: Setting up Nginx"

    sudo bash deployment/scripts/setup_nginx.sh

    prompt_continue
}

# Step 5: Backend Service Setup
step5_backend_setup() {
    log "Step 5: Setting up Backend Service"

    sudo bash deployment/scripts/setup_backend.sh

    prompt_continue
}

# Step 6: Telegram Bot Service Setup
step6_telegram_setup() {
    log "Step 6: Setting up Telegram Bot Service"

    sudo bash deployment/scripts/setup_telegram.sh

    prompt_continue
}

# Step 7: Verify Services
step7_verify_services() {
    log "Step 7: Verifying Services"

    echo "Checking Nginx..."
    sudo systemctl status nginx

    echo "Checking Backend Service..."
    sudo systemctl status backend

    echo "Checking Telegram Bot Service..."
    sudo systemctl status telegram

    echo "Checking service logs..."
    sudo tail -n 20 /var/log/nginx/error.log
    sudo journalctl -u backend -n 20
    sudo journalctl -u telegram -n 20
}

# Main execution
main() {
    log "Starting deployment process..."

    step1_system_setup
    step2_python_setup
    step3_env_setup
    step4_nginx_setup
    step5_backend_setup
    step6_telegram_setup
    step7_verify_services

    log "Deployment completed successfully!"
}

# Run main function
main
