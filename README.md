Home Assistant configuration
============================

### Download script and install 1st stage
~~~
$ sudo apt-get install git -y
$ git clone https://github.com/hanmy75/home_assistant.git
$ ~/home_assistant/install_1st.sh
~~~

### Install homeassistant
~~~
$ sudo -u homeassistant -H -s
$ cd /srv/homeassistant
$ python3 -m venv .
$ source /srv/homeassistant/bin/activate

(homeassistant) homeassistant@raspberrypi:/srv/homeassistant $ python3 -m pip install --upgrade pip
(homeassistant) homeassistant@raspberrypi:/srv/homeassistant $ pip3 install wheel
(homeassistant) homeassistant@raspberrypi:/srv/homeassistant $ pip3 install homeassistant
  or
(homeassistant) homeassistant@raspberrypi:/srv/homeassistant $ pip3 install homeassistant==0.116.1

(homeassistant) homeassistant@raspberrypi:/srv/homeassistant $ hass
~~~

### Update homeassistant
~~~
$ sudo -u homeassistant -H -s
$ source /srv/homeassistant/bin/activate

(homeassistant) homeassistant@raspberrypi:/srv/homeassistant $ pip3 install --upgrade homeassistant
~~~

### Install 2nd stage
~~~
$ ~/home_assistant/install_2nd.sh
~~~

### Get SSL Certificate
```
$ sudo certbot certonly --standalone -d example.com

$ sudo chmod 755 /etc/letsencrypt/live/
$ sudo chmod 755 /etc/letsencrypt/archive/
$ sudo chmod -R 777 /etc/letsencrypt/
```
