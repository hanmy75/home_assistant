#! /bin/bash

# Config ffmpge
config_ffmpeg()
{
	URL=$1
	INDEX=$2
	ffmpeg -re  -i ${URL} -c:a copy -bsf:a aac_adtstoasc -f flv rtmp://localhost/live/${INDEX} &>/dev/null &
}

# Main
case "$1" in
	start)
		killall ffmpeg
		config_ffmpeg "$(/home/pi/get_radio_url.py 'MBC FM4U')" "mbc"
		config_ffmpeg "$(/home/pi/get_radio_url.py 'SBS Power FM')" "sbs"
		config_ffmpeg "$(/home/pi/get_radio_url.py 'KBS 2FM')" "kbs"
	;;
	stop)
		killall ffmpeg
		rm -rf /var/www/html/dash/*
	;;
esac
