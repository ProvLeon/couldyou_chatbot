#!/bin/bash
# setup.sh

# Create base directory
mkdir -p /opt/couldyou_chatbot
cd /opt/couldyou_chatbot || exit

# Clone repository
git clone https://github.com/ProvLeon/couldyou_chatbot.git .

# Set permissions
chown -R www-data:www-data /opt/couldyou_chatbot
