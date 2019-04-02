# launch our autostart apps (if we are on the correct tty)

if [ "`tty`" = "/dev/tty1" ]; then
    # Turn off LED and HDMI
    /home/pi/turn_off.sh
fi
