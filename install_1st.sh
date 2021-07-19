#!/bin/bash

USER=hmy75
SOURCE_DIR=/home/pi/home_assistant

# apt-get update
sudo apt-get update
sudo apt-get upgrade -y

# Install python-3.8.0
tar -zxf $SOURCE_DIR/Python-3.8.0_prebuilt.tgz
cd /home/pi/Python-3.8.0; sudo make install
cd /home/pi; sudo rm /home/pi/Python-3.8.0 -rf

# Install package
sudo apt-get install -y python3 python3-dev python3-venv python3-pip libffi-dev libssl-dev libjpeg-dev zlib1g-dev autoconf build-essential libopenjp2-7 libtiff5 tzdata
sudo apt-get install -y git certbot nginx libnginx-mod-rtmp samba samba-common-bin transmission-daemon ffmpeg exfat-fuse

# Update pip
sudo pip3 install --upgrade pip
sudo pip3 install pre-commit

# Change password
echo "Change your password"
passwd

# Add user and update samba config
echo "Add user"
sudo adduser $USER
sudo adduser $USER users
sudo smbpasswd -a $USER

# Add an account for Home Assistant and create a directory
sudo useradd -rm homeassistant -G dialout,gpio,video
cd /srv
sudo mkdir homeassistant
sudo chown homeassistant:homeassistant homeassistant
