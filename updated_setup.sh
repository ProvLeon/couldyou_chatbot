#!/bin/bash

# Add deadsnakes PPA for Python 3.11
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update

# Install Python 3.11 and required packages
sudo apt install -y python3.11 python3.11-venv python3.11-dev

# Install other dependencies
sudo apt install -y     nginx     git     build-essential     libssl-dev     libffi-dev     supervisor

# Create project directories
sudo mkdir -p /opt/couldyou_chatbot/{backend,telegram_bot,logs}

# Set correct permissions
sudo chown -R ubuntu:ubuntu /opt/couldyou_chatbot
