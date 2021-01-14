#!/bin/bash

USER=hmy75

# Stop nginx & transmission service
sudo systemctl stop nginx
sudo systemctl stop transmission-daemon

# Get configuration
sudo cp ~/home_assistant/configs/* / -rf

# Change permission
sudo chown pi.users *.sh
sudo chown homeassistant.homeassistant /home/homeassistant/.homeassistant -R
sudo chown -R $USER:$USER /etc/transmission-daemon
sudo mkdir -p /home/$USER/.config/transmission-daemon/
sudo ln -s /etc/transmission-daemon/settings.json /home/$USER/.config/transmission-daemon/
sudo chown -R $USER:$USER /home/$USER/.config/transmission-daemon/

# Create folder
sudo mkdir -p /mnt/HDD /mnt/USB /var/www/html/dash

# Update fstab
sudo cat /etc/fstab_append >> /etc/fstab

# Auto log-in
sudo systemctl daemon-reload
sudo systemctl start transmission-daemon
sudo systemctl enable home-assistant@homeassistant
sudo systemctl start home-assistant@homeassistant
sudo systemctl enable autologin@.service
