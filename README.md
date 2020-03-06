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
$ sudo apt-get install python3 python3-venv python3-pip python-pip git certbot nginx libssl-dev libffi-dev
$ sudo apt-get install samba samba-common-bin transmission-daemon
$ sudo pip2 install esphomeyaml
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
$ pip3 install --upgrade homeassistant
```

Reference : https://www.home-assistant.io/docs/installation/raspberry-pi


### Add user and update samba config
```
$ sudo adduser hmy75
$ sudo adduser hmy75 users
$ sudo adduser hmy75 debian-transmission
$ sudo adduser debian-transmission users
$ sudo smbpasswd -a hmy75
```

### Install configuration and script
```
$ cd ~
$ git clone https://github.com/hanmy75/home_assistant.git
$ sudo cp ~/home_assistant/configs/* / -rf
$ sudo chown pi.users *.sh
$ sudo chown homeassistant.homeassistant /home/homeassistant/.homeassistant -R
```


### Auto login
```
$ sudo systemctl enable home-assistant@homeassistant
$ sudo systemctl start home-assistant@homeassistant
$ sudo systemctl enable autologin@.service
```

### Get SSL Certificate
```
$ sudo certbot certonly --standalone -d example.com
```

### Renew SSL Certificate
```
$ crontab -e
------------------------------------------------------
0 */12 * * * root /home/pi/cert_renew.sh
------------------------------------------------------
```

### PIN Out
```
+5V : RED
GND : BROWN
RF SW  : GPIO18 BLUE
MOTION : GPIO22 GREEN
LIGHT  : GPIO27 YELLOW
THERMAL: GPIO17 ORANGE
```
