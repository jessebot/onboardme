#!/usr/bin/env bash
# Simple script by JesseBot@linux to remind you to stop working
ALARM_TYPE=$1

case $ALARM_TYPE in
    lunch)
        figlet -c -f banner Take your lunch > /tmp/lunch_art
        echo "It's time to take lunch :3" >> /tmp/lunch_art
        wall /tmp/lunch_art
        ;;

    stop_work)
        figlet -c -f banner Stop Working > /tmp/stop_working
        echo "It's time to stop working :)" >> /tmp/stop_working
        wall /tmp/stop_working
        ;;
esac
