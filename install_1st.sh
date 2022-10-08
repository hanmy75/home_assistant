#!/bin/bash

USER=hmy75
SOURCE_DIR=$PWD

# apt-get update
sudo apt-get update
sudo apt-get upgrade -y

# Install package
sudo apt-get install -y python3 python3-dev python3-venv python3-pip libffi-dev libssl-dev libjpeg-dev zlib1g-dev autoconf build-essential libopenjp2-7 libtiff5 tzdata
sudo apt-get install -y git certbot nginx libnginx-mod-rtmp samba samba-common-bin transmission-daemon ffmpeg exfat-fuse

# Update pip
sudo pip3 install --upgrade pip
sudo pip3 install pre-commit
sudo pip3 install psutil

# Add user and update samba config
echo "Add samba user"
sudo smbpasswd -a $USER

# Add an account for Home Assistant and create a directory
sudo useradd -rm homeassistant -G dialout,gpio,video
cd /srv
sudo mkdir homeassistant
sudo chown homeassistant:homeassistant homeassistant
