#! /bin/bash

# Config for MBC
config_mbc()
{
	export MBC_URL=$1
	envsubst  < nginx.conf.template > /etc/nginx/nginx.conf
	systemctl restart nginx
}

# Config for KBS
config_kbs()
{
	killall ffmpeg
	KBS_URL=$1
	ffmpeg -re  -i ${KBS_URL} -c:a copy -bsf:a aac_adtstoasc -f flv rtmp://localhost/live/kbs &>/dev/null &
}


# Main
case "$1" in
	start)
		config_mbc "$(./get_radio_url.py 'MBC FM')"
		config_kbs "$(./get_radio_url.py 'KBS 1FM')"
	;;
	stop)
		config_mbc "rtmp://localhost"
		config_kbs ""
	;;
esac
