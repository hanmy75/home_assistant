#!/bin/bash

USER=hmy75

# apt-get update
sudo apt-get update
sudo apt-get upgrade -y

# Install package
sudo apt-get install python3-venv python3-pip -y
sudo apt-get install git certbot nginx libnginx-mod-rtmp php-fpm samba samba-common-bin transmission-daemon ffmpeg exfat-fuse -y

# Change password
echo "Change your password"
passwd

# Add user and update samba config
echo "Add user"
sudo adduser $USER
sudo adduser $USER users
sudo smbpasswd -a $USER

# Install ESPHome
git clone https://github.com/hanmy75/esphome.git
cd esphome; ./script/setup

# Add an account for Home Assistant and create a directory
sudo useradd -rm homeassistant -G dialout,gpio,video
cd /srv
sudo mkdir homeassistant
sudo chown homeassistant:homeassistant homeassistant
