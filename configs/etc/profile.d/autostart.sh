# launch our autostart apps (if we are on the correct tty)
RUN_FOLDER=/home/pi/home_assistant

if [ "`tty`" = "/dev/tty1" ]; then
    # Turn off LED and HDMI
    /home/pi/turn_off.sh

    # Launch flic daemon
    sudo $RUN_FOLDER/flicd -d -f /home/pi/flic.sqlite3

    # Run MJPEG Stream Server
    mjpg_streamer -o "output_http.so" -i "input_raspicam.so -x 640 -y 480 -fps 15" &
fi
