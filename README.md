Home Assistant configuration
============================

### Download script and install 1st stage
~~~
$ sudo apt-get install git -y
$ mkdir ~/GitHub
$ cd ~/GitHub
$ git clone git@github.com:hanmy75/home_assistant.git
$ ./install_1st.sh
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

(homeassistant) homeassistant@raspberrypi:/srv/homeassistant $ pip3 install --upgrade homeassistant=2024.3.3
~~~

### Install 2nd stage
~~~
$ cd ~/GitHub
$ ./install_2nd.sh
~~~

### Get SSL Certificate
```
$ sudo certbot certonly --standalone -d example.com

$ sudo chmod 755 /etc/letsencrypt/live/
$ sudo chmod 755 /etc/letsencrypt/archive/
$ sudo chmod -R 777 /etc/letsencrypt/
```

### rclone Configuration
```
https://rclone.org/googlephotos/
https://m.blog.naver.com/destinyrev/222515975596
```

