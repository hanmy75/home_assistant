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
$ sudo apt-get install python3 python3-venv python3-pip git dnsmasq nginx certbot
$ sudo pip3 install requests
```

- Add an account for Home Assistant and create a directory
```
$ sudo useradd -rm homeassistant -G dialout,gpio
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


### Install configuration and script
```
$ cd ~
$ git clone https://github.com/hanmy75/home_assistant.git
$ sudo cp ~/home_assistant/configs/* / -rf
$ sudo chown pi.pi dynu.sh turn_off.sh
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


### DDNS (https://www.dynu.com)

- Config
```
$ cd ~
$ nano dynu.sh
------------------------------------------------------
echo url="https://api.dynu.com/nic/update?username=your_id&password=your_password" | curl -k -o ~/dynu.log -K -
------------------------------------------------------
$ chmod 755 dynu.sh
$ crontab -e
------------------------------------------------------
10 * * * * /home/pi/dynu.sh >/dev/null 2>&1
------------------------------------------------------
```


### PIN Out
```
RF Switch : GPIO17(GPIO_GEN_0)
IR  : in GPIO18 / out GPIO27
```
