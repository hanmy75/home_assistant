#! /bin/bash

# Config for MBC
config_mbc()
{
	MBC_URL=$1
	ffmpeg -re  -i ${MBC_URL} -c:a copy -bsf:a aac_adtstoasc -f flv rtmp://localhost/live/mbc &>/dev/null &
}

# Config for KBS
config_kbs()
{
	KBS_URL=$1
	ffmpeg -re  -i ${KBS_URL} -c:a copy -bsf:a aac_adtstoasc -f flv rtmp://localhost/live/kbs &>/dev/null &
}


# Main
case "$1" in
	start)
		killall ffmpeg
		config_mbc "$(/home/pi/get_radio_url.py 'MBC FM4U')"
		config_kbs "$(/home/pi/get_radio_url.py 'KBS 1FM')"
	;;
	stop)
		killall ffmpeg
		config_mbc ""
		config_kbs ""
	;;
esac
