#!/bin/bash

# Get configuration
cd ~
git clone https://github.com/hanmy75/home_assistant.git
sudo systemctl stop transmission-daemon
sudo cp ~/home_assistant/configs/* / -rf

# Change permission
sudo chown pi.users *.sh
sudo chown homeassistant.homeassistant /home/homeassistant/.homeassistant -R
sudo chown -R hmy75:hmy75 /etc/transmission-daemon
sudo mkdir -p /home/hmy75/.config/transmission-daemon/
sudo ln -s /etc/transmission-daemon/settings.json /home/hmy75/.config/transmission-daemon/
sudo chown -R hmy75:hmy75 /home/hmy75/.config/transmission-daemon/

# Create folder
sudo mkdir -p /mnt/HDD /mnt/USB /var/www/html/dash

# Update fstab
sudo cat /etc/fstab /etc/fstab_append > /tmp/fstab
sudo cp /tmp/fstab /etc/fstab
sudo chmod 644 /etc/fstab

# Auto log-in
sudo systemctl daemon-reload
sudo systemctl start transmission-daemon
sudo systemctl enable home-assistant@homeassistant
sudo systemctl start home-assistant@homeassistant
sudo systemctl enable autologin@.service

