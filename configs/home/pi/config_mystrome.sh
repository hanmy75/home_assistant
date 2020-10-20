#! /bin/bash


BUTTON_IP=192.168.0.7
BUTTON_NAME="MYButton"
HA_SERVER=$(ifconfig | sed -En 's/127.0.0.1//;s/.*inet (addr:)?(([0-9]*\.){3}[0-9]*).*/\2/p')
HA_SERVER_PORT=8126

# Set single button
curl --location --request POST "http://${BUTTON_IP}/api/v1/action/single" --data-raw "get://${HA_SERVER}:${HA_SERVER_PORT}/api/mystrom?single=${BUTTON_NAME}"

# Set double button
curl --location --request POST "http://${BUTTON_IP}/api/v1/action/double" --data-raw "get://${HA_SERVER}:${HA_SERVER_PORT}/api/mystrom?double=${BUTTON_NAME}"

# Check API
curl --location --request GET "http://${BUTTON_IP}/api/v1/device"

# Set re-direct for http tocken
export host="\$host"
export remote_addr="\$remote_addr"
export HTTP_TOCKEN="$(cat /home/homeassistant/.homeassistant/secrets.yaml | grep 'http_tocken' | sed 's/ //g' | cut -d":" -f 2)"
envsubst  < /etc/nginx/conf.d/http_api.conf.template > /etc/nginx/conf.d/http_api.conf

systemctl restart nginx
