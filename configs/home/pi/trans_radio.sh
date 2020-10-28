#! /bin/bash

# Config for MBC
export MBC_URL="$(./get_radio_url.py 'MBC FM')"
envsubst  < nginx.conf.template > /etc/nginx/nginx.conf
systemctl restart nginx

# Config for KBS
killall ffmpeg
KBS_URL="$(./get_radio_url.py 'KBS 1FM')"
ffmpeg -re  -i ${KBS_URL} -c:a copy -bsf:a aac_adtstoasc -f flv rtmp://localhost/live/kbs &>/dev/null &
