#!/bin/bash

USER=hmy75
SOURCE_DIR=$PWD

# Patch of Home Assistant
sudo sed -i "/MAX_LENGTH_STATE_STATE/ c\MAX_LENGTH_STATE_STATE: Final = 1024" /srv/homeassistant/lib/python3.9/site-packages/homeassistant/const.py

# Install ESPHome
cd $SOURCE_DIR/../
git clone https://github.com/hanmy75/esphome.git
cd $SOURCE_DIR/../esphome; export CRYPTOGRAPHY_DONT_BUILD_RUST=1; ./script/setup

# Stop nginx & transmission service
sudo systemctl stop nginx
sudo systemctl stop transmission-daemon

# Get configuration
sudo cp $SOURCE_DIR/configs/* / -rf

# Change permission
sudo chown $USER.$USER /home/$USER/*.sh
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
sudo systemctl enable magicmirror.service
sudo systemctl start magicmirror.service
sudo systemctl enable home-assistant@homeassistant
sudo systemctl start home-assistant@homeassistant
sudo systemctl enable autologin@.service
