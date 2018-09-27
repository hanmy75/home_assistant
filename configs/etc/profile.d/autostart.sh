# launch our autostart apps (if we are on the correct tty)
RUN_FOLDER=/home/pi

if [ "`tty`" = "/dev/tty1" ]; then
    # Turn off LED and HDMI
    $RUN_FOLDER/turn_off.sh

    # Launch flic daemon
    sudo $RUN_FOLDER/flicd -d -f $RUN_FOLDER/flic.sqlite3

fi
