#! /bin/bash

# DASH folder
DASH_FOLDER=/var/www/html/dash

# Radio Channel Map
declare -A channelMap
channelMap["mbc"]="MBC FM4U"
channelMap["sbs"]="SBS Power FM"
channelMap["kbs"]="KBS 2FM"

# Check File Exist
isFileExist()
{
    result=0
    if [ -f "$DASH_FOLDER/$1" ]; then
        result=1
    fi
    echo $result
}

# Config ffmpge
config_ffmpeg()
{
	URL=$1
	INDEX=$2
	ffmpeg -re  -i ${URL} -c:a copy -bsf:a aac_adtstoasc -f flv rtmp://localhost/live/${INDEX} &>/dev/null &
}

# Check and Start transcoding
#runTranscoding()
#{
#    mpdFile=$1.mpd
#
#}

# Main
case "$1" in
	start)
        for _key in "${!channelMap[@]}"
        do
            # Check MPD file
            if [ "$(isFileExist "$_key.mpd")" -ne 1 ]; then
                echo "Start $_key transcoding"
                url="$(/home/pi/get_radio_url.py "${channelMap[$_key]}")"
                config_ffmpeg "$url" "$_key"
            fi
        done
	;;

	stop)
		killall ffmpeg
		rm -rf /var/www/html/dash/*
	;;
esac
