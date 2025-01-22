#!/bin/bash
# pre_deploy_check.sh

# Check required files and directories
required_files=(
    "/home/ubuntu/couldyou_chatbot/backend/run.py"
    "/home/ubuntu/couldyou_chatbot/.env"
    "/home/ubuntu/couldyou_chatbot/backend/requirements.txt"
)

required_dirs=(
    "/home/ubuntu/couldyou_chatbot/backend"
    "/home/ubuntu/couldyou_chatbot/backend/venv"
    "/home/ubuntu/couldyou_chatbot/backend/app"
)

# Check files
for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "ERROR: Required file not found: $file"
        exit 1
    fi
done

# Check directories
for dir in "${required_dirs[@]}"; do
    if [ ! -d "$dir" ]; then
        echo "ERROR: Required directory not found: $dir"
        exit 1
    fi
done

# Check Python environment
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python3 is not installed"
    exit 1
fi

# Check virtual environment
if [ ! -f "/home/ubuntu/couldyou_chatbot/backend/venv/bin/python" ]; then
    echo "ERROR: Virtual environment not properly set up"
    exit 1
fi

# Check dependencies
source /home/ubuntu/couldyou_chatbot/backend/venv/bin/activate
if ! pip freeze > /dev/null; then
    echo "ERROR: Python dependencies not properly installed"
    exit 1
fi

echo "All pre-deployment checks passed!"
