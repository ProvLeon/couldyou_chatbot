#!/bin/bash

# deployment_bot.sh
echo "Starting deployment of CouldYou? Telegram Bot..."

# Function to check and install Python 3.11
check_python() {
    if ! command -v python3.11 &> /dev/null; then
        echo "Python 3.11 not found. Installing..."
        sudo apt update
        sudo apt install -y software-properties-common
        sudo add-apt-repository -y ppa:deadsnakes/ppa
        sudo apt update
        sudo apt install -y python3.11 python3.11-venv python3.11-dev
    else
        echo "Python 3.11 is already installed"
    fi
}

# Function to setup project directory
setup_project_directory() {
    if [ ! -d "/var/www/couldyou_chatbot" ]; then
        echo "Creating project directory..."
        sudo mkdir -p /var/www/couldyou_chatbot
    fi

    echo "Setting directory permissions..."
    sudo chown -R $USER:$USER /var/www/couldyou_chatbot
}

# Function to setup the bot
setup_bot() {
    echo "Setting up Telegram bot..."

    # Copy bot files
    echo "Copying bot files..."
    sudo cp -rf  $HOME/couldyou_chatbot/telegram_bot/* /var/www/couldyou_chatbot/telegram_bot/

    # Setup virtual environment
    echo "Setting up Python virtual environment..."
    cd /var/www/couldyou_chatbot/telegram_bot
    python3.11 -m venv venv
    source venv/bin/activate

    # Install requirements
    echo "Installing Python dependencies..."
    pip install --upgrade pip
    pip install -r requirements.txt

    # Create .env file
    echo "Creating .env file..."
    cat > .env << EOF
    TELEGRAM_BOT_TOKEN="7900644474:AAEVnfJSaaOFJjK-JZCOwtVh2Lmnz8YbGnc"
    BACKEND_URL="http://54.242.250.139"
    ALLOWED_USERS=  # Optional: comma-separated list of allowed user IDs
EOF
}

# Function to setup Supervisor configuration
setup_supervisor() {
    echo "Setting up Supervisor configuration..."
    sudo bash -c 'cat > /etc/supervisor/conf.d/couldyou_telegram_bot.conf << EOF
[program:couldyou_telegram_bot]
directory=/var/www/couldyou_chatbot/telegram_bot
command=/var/www/couldyou_chatbot/telegram_bot/venv/bin/python bot.py
autostart=true
autorestart=true
stderr_logfile=/var/log/couldyou_telegram_bot/bot.err.log
stdout_logfile=/var/log/couldyou_telegram_bot/bot.out.log
user=$USER
environment=PATH="/var/www/couldyou_chatbot/telegram_bot/venv/bin"
EOF'

    # Create log directory
    sudo mkdir -p /var/log/couldyou_telegram_bot
    sudo chown -R $USER:$USER /var/log/couldyou_telegram_bot
}

# Function to start the bot
start_bot() {
    echo "Starting the bot..."
    sudo supervisorctl reread
    sudo supervisorctl update
    sudo supervisorctl restart couldyou_telegram_bot
}

# Main deployment process
main() {
    # Check if running as root
    if [ "$EUID" -ne 0 ]; then
        echo "Please run as root or with sudo"
        exit 1
    fi

    # Install required system packages
    apt-get update
    apt-get install -y supervisor

    # Run deployment steps
    check_python
    setup_project_directory
    setup_bot
    setup_supervisor
    start_bot

    echo "Deployment completed!"
    echo "Please update the .env file with your actual Telegram bot token"
    echo "Check logs at /var/log/couldyou_telegram_bot/"
}

# Execute main function
main

# Display status
echo "Checking bot status..."
sudo supervisorctl status couldyou_telegram_bot

echo "
Deployment completed! Important notes:
1. Update the .env file with your Telegram bot token:
   nano /var/www/couldyou_chatbot/telegram_bot/.env

2. Check logs:
   tail -f /var/log/couldyou_telegram_bot/bot.out.log
   tail -f /var/log/couldyou_telegram_bot/bot.err.log

3. Manage the bot:
   sudo supervisorctl restart couldyou_telegram_bot  # To restart
   sudo supervisorctl stop couldyou_telegram_bot     # To stop
   sudo supervisorctl start couldyou_telegram_bot    # To start
"
