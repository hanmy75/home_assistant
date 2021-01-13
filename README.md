Home Assistant configuration
============================

### apt-get update
```
$ sudo apt-get update
$ sudo apt-get upgrade -y
```


### Install

- Install dependencies
```
$ sudo apt-get install python3-venv python3-pip
$ sudo apt-get install git certbot nginx libnginx-mod-rtmp samba samba-common-bin transmission-daemon ffmpeg exfat-fuse
```

- Install ESPHome
```
$ git clone https://github.com/hanmy75/esphome.git
$ cd esphome; ./script/setup
```

- Add an account for Home Assistant and create a directory
```
$ sudo useradd -rm homeassistant -G dialout,gpio,video
$ cd /srv
$ sudo mkdir homeassistant
$ sudo chown homeassistant:homeassistant homeassistant
```

- Virtual environment for Home Assistant
```
$ sudo -u homeassistant -H -s
$ cd /srv/homeassistant
$ python3 -m venv .
$ source bin/activate
```

- Install a required python package.
```
(homeassistant) homeassistant@raspberrypi:/srv/homeassistant $ python3 -m pip install wheel
```

- Install Home Assistant
```
(homeassistant) homeassistant@raspberrypi:/srv/homeassistant $ pip3 install homeassistant
```

- Run hass for first configuration
```
(homeassistant) homeassistant@raspberrypi:/srv/homeassistant $ hass
```

- UPDATING
```
$ sudo -u homeassistant -H -s
$ source /srv/homeassistant/bin/activate
(homeassistant) homeassistant@raspberrypi:/srv/homeassistant $ pip3 install --upgrade homeassistant
```

Reference : https://www.home-assistant.io/docs/installation/raspberry-pi


### Add user and update samba config
```
$ sudo adduser hmy75
$ sudo adduser hmy75 users
$ sudo smbpasswd -a hmy75
```

### Install configuration and script
```
$ cd ~
$ git clone https://github.com/hanmy75/home_assistant.git
$ ~/home_assistant/install.sh
```

### Get SSL Certificate
```
$ sudo certbot certonly --standalone -d example.com

$ sudo chmod 755 /etc/letsencrypt/live/
$ sudo chmod 755 /etc/letsencrypt/archive/
$ sudo chmod -R 777 /etc/letsencrypt/
```
