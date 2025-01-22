#!/bin/bash
# deploy.sh

# Run pre-deployment checks
./pre_deploy_check.sh || exit 1

# Setup service
sudo ./setup_service.sh

# Setup monitoring
sudo cp monitor_service.sh /usr/local/bin/
sudo chmod +x /usr/local/bin/monitor_service.sh

# Add to crontab
(crontab -l 2>/dev/null; echo "*/5 * * * * /usr/local/bin/monitor_service.sh") | crontab -

echo "Deployment completed successfully!"
