#!/bin/bash

USER=hmy75
SOURCE_DIR=$PWD

# apt-get update
sudo apt-get update
sudo apt-get upgrade -y

# Install package
sudo apt-get install -y python3 python3-venv libffi-dev libssl-dev libjpeg-dev zlib1g-dev autoconf build-essential libopenjp2-7 libtiff5 tzdata
sudo apt-get install -y python-dev-is-python3 python3-pip python3-psutil
sudo apt-get install -y certbot nginx libnginx-mod-rtmp samba samba-common-bin transmission-daemon ffmpeg exfat-fuse rclone

# Install node.js
sudo curl -sL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install Magic Mirror2 & MMM-BackgroundSlideShow
git clone https://github.com/MichMich/MagicMirror ~/MagicMirror/
git clone https://github.com/darickc/MMM-BackgroundSlideshow ~/MagicMirror/modules/MMM-BackgroundSlideshow
cd ~/MagicMirror/
npm install --only=prod --omit=dev
cd ~/MagicMirror/modules/MMM-BackgroundSlideshow
npm install

# Add user and update samba config
echo "Add samba user"
sudo smbpasswd -a $USER

# Add an account for Home Assistant and create a directory
sudo useradd -rm homeassistant -G dialout,gpio,video
cd /srv
sudo mkdir homeassistant
sudo chown homeassistant:homeassistant homeassistant
