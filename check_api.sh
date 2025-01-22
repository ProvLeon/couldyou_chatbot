#!/bin/bash
# check_api.sh

echo "Checking Nginx configuration..."
sudo nginx -t

echo -e "\nChecking backend service status..."
sudo systemctl status couldyou-backend

echo -e "\nTesting API endpoints..."

# Test health endpoint
echo "Testing health endpoint..."
curl -v http://localhost:80/api/

# Test chat endpoint with proper headers
echo -e "\nTesting chat endpoint..."
curl -v -X POST \
    -H "Content-Type: application/json" \
    -H "Origin: http://localhost:3000" \
    -d '{"message":"test", "language":"en"}' \
    http://localhost:80/api/chat

# Check Nginx logs
echo -e "\nChecking Nginx error logs..."
sudo tail -n 20 /var/log/nginx/couldyou_error.log

echo -e "\nChecking Nginx access logs..."
sudo tail -n 20 /var/log/nginx/couldyou_access.log

# Check backend logs
echo -e "\nChecking backend logs..."
sudo journalctl -u couldyou-backend -n 20 --no-pager
