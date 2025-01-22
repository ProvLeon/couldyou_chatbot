#!/bin/bash
# monitor_service.sh

SERVICE_NAME="backend"
NOTIFICATION_EMAIL="your-email@example.com"

check_service() {
    if ! systemctl is-active --quiet "${SERVICE_NAME}.service"; then
        echo "Service ${SERVICE_NAME} is down! Attempting restart..."
        systemctl restart "${SERVICE_NAME}.service"

        # Check if restart was successful
        if ! systemctl is-active --quiet "${SERVICE_NAME}.service"; then
            echo "Service ${SERVICE_NAME} failed to restart!" | mail -s "Service Alert" "$NOTIFICATION_EMAIL"
        fi
    fi
}

# Run health check
check_service
