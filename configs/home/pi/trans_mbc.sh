#! /bin/bash

BASE_URL="http://miniplay.imbc.com/AACLiveURL.ashx?protocol=RTMP&channel=mfm"
export MBC_URL="$(curl "${BASE_URL}" 2>/dev/null)"
envsubst  < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf

systemctl restart nginx
