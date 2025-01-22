#!/bin/bash
# setup_venv.sh

create_venv() {
    directory=$1
    requirements="$directory/backend/$2"

    echo "Creating virtual environment in $directory"
    python3.11 -m venv "$directory/venv"

    echo "Installing requirements from $requirements"
    "$directory/venv/bin/pip" install --upgrade pip
    "$directory/venv/bin/pip" install -r "$requirements"
}

# Create backend environment
create_venv "backend" "requirements.txt"

# Create telegram bot environment
create_venv "telegram_bot" "telegram_bot/requirements.txt"
