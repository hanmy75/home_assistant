#! /bin/bash
sudo sh -c "echo 0 > /sys/class/leds/led0/brightness"
sudo sh -c "echo 0 > /sys/class/leds/led1/brightness"

# Disable HDMI
/opt/vc/bin/tvservice -o
