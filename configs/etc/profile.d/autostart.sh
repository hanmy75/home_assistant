# launch our autostart apps (if we are on the correct tty)
RUN_FOLDER=/home/pi/home_assistant

if [ "`tty`" = "/dev/tty1" ]; then
    # Turn off LED and HDMI
    /home/pi/turn_off.sh

    # Launch flic daemon
    sudo $RUN_FOLDER/flicd -d -f /home/pi/flic.sqlite3
    sleep 4
    python3 $RUN_FOLDER/switch_flic_button.py &

fi
