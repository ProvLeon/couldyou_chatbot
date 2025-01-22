#!/bin/bash

# deployment.sh
echo "Starting deployment of CouldYou? Chatbot Backend..."

# Update system packages
echo "Updating system packages..."
sudo apt-get update
sudo apt-get upgrade -y

# Install required system dependencies
echo "Installing system dependencies..."
sudo apt-get install -y python3.11 python3.11-venv python3.11-dev nginx supervisor

# Create project directory if it doesn't exist
echo "Setting up project directory..."
sudo mkdir -p /var/www/couldyou_chatbot
sudo chown -R $USER:$USER /var/www/couldyou_chatbot

# Clone or copy project files (adjust based on your source)
echo "Copying project files..."
cp -rf $HOME/couldyou_chatbot/backend/* /var/www/couldyou_chatbot/backend

# Setup Python virtual environment
echo "Setting up Python virtual environment..."
cd /var/www/couldyou_chatbot/backend
python3.11 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file
echo "Creating .env file..."
cat > .env << EOF
FLASK_ENV=production
TRANSFORMERS_CACHE="./model_cache"
HF_HOME="./model_cache"
GOOGLE_API_KEY="AIzaSyDlMO40t1n7kOVutn1CkSa-9CmWwodhOXI"
EOF

# Setup Nginx configuration
echo "Configuring Nginx..."
sudo bash -c 'cat > /etc/nginx/sites-available/couldyou_chatbot << EOF
server {
    listen 80;
    server_name 54.242.250.139;

    location / {
        proxy_pass http://unix:/var/www/couldyou_chatbot/backend/couldyou_chatbot.sock;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host \$host;
        proxy_cache_bypass \$http_upgrade;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    }
}
EOF'

# Enable the Nginx site
sudo ln -sf /etc/nginx/sites-available/couldyou_chatbot /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Setup Supervisor configuration
echo "Configuring Supervisor..."
sudo bash -c 'cat > /etc/supervisor/conf.d/couldyou_chatbot.conf << EOF
[program:couldyou_chatbot]
directory=/var/www/couldyou_chatbot/backend
command=/var/www/couldyou_chatbot/backend/venv/bin/gunicorn --workers 4 --bind unix:/var/www/couldyou_chatbot/backend/couldyou_chatbot.sock run:app
autostart=true
autorestart=true
stderr_logfile=/var/log/couldyou_chatbot/gunicorn.err.log
stdout_logfile=/var/log/couldyou_chatbot/gunicorn.out.log
user=$USER
environment=PATH="/var/www/couldyou_chatbot/backend/venv/bin"
EOF'

# Create log directory
sudo mkdir -p /var/log/couldyou_chatbot
sudo chown -R $USER:$USER /var/log/couldyou_chatbot

# Test Nginx configuration
echo "Testing Nginx configuration..."
sudo nginx -t

# Restart services
echo "Restarting services..."
sudo systemctl restart nginx
sudo systemctl restart supervisor

# Setup firewall rules if needed
echo "Setting up firewall rules..."
sudo ufw allow 'Nginx Full'
sudo ufw allow ssh

echo "Deployment completed!"
echo "Please ensure you update the .env file with your actual credentials"
echo "Your application should now be accessible at http://54.242.250.139"
