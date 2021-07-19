#!/bin/bash

USER=hmy75

# Patch of Home Assistant
sudo sed -i "/MAX_LENGTH_STATE_STATE/ c\MAX_LENGTH_STATE_STATE: Final = 1024" /srv/homeassistant/lib/python3.8/site-packages/homeassistant/const.py

# Install ESPHome
cd /home/pi
git clone https://github.com/hanmy75/esphome.git
cd /home/pi/esphome; export CRYPTOGRAPHY_DONT_BUILD_RUST=1; ./script/setup

# Stop nginx & transmission service
sudo systemctl stop nginx
sudo systemctl stop transmission-daemon

# Get configuration
sudo cp ~/home_assistant/configs/* / -rf

# Change permission
sudo chown pi.users /home/pi/*.sh
sudo chown homeassistant.homeassistant /home/homeassistant/.homeassistant -R
sudo chown -R $USER:$USER /etc/transmission-daemon
sudo mkdir -p /home/$USER/.config/transmission-daemon/
sudo ln -s /etc/transmission-daemon/settings.json /home/$USER/.config/transmission-daemon/
sudo chown -R $USER:$USER /home/$USER/.config/transmission-daemon/

# Create folder
sudo mkdir -p /mnt/HDD /mnt/USB /var/www/html/dash

# Update fstab
cat /etc/fstab /etc/fstab_append > /tmp/fstab
sudo cp /tmp/fstab /etc/fstab

# Auto log-in
sudo systemctl daemon-reload
sudo systemctl start transmission-daemon
sudo systemctl enable home-assistant@homeassistant
sudo systemctl start home-assistant@homeassistant
sudo systemctl enable autologin@.service
