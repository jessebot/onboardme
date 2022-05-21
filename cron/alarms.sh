#!/usr/bin/env bash
# Simple script by JesseBot@linux to remind you to stop working
ALARM_TYPE=$1
SILENCE=$2

case $ALARM_TYPE in
    work_start_soon)
        banner_msg="Work Starts Soon"
        figlet -c -f banner $banner_msg > /tmp/wall_notice
        echo "It's almost time to start work. Save your place and make some" \
             "follow up notes." >> /tmp/wall_notice
        ;;

    work_start)
        banner_msg="Go To Work"
        figlet -c -f banner $banner_msg > /tmp/wall_notice
        echo "It's time to start working. Open your work laptop, and clock" \
             "in: Fill in timesheet, say good morning in chat, check emails," \
             "and open important tickets." >> /tmp/wall_notice
        ;;

    lunch)
        banner_msg="Take your Lunch!"
        figlet -c -f banner $banner_msg > /tmp/wall_notice
        echo "It's time to take lunch! Go have a protein shake and or a" \
             "salad, or order something healthy to snack on during your" \
             "break, and use the time to do something for yourself" \
             ":3" >> /tmp/wall_notice
        ;;

    lunch_end_soon)
        banner_msg="Lunch Hour Ends Soon."
        figlet -c -f banner $banner_msg > /tmp/wall_notice
        echo "Your lunch hour ends soon, so you should save what you're" \
             "doing, and make a note to follow up on any" \
             "loose ends." >> /tmp/wall_notice
        ;;

    lunch_end)
        banner_msg="Lunch is over."
        figlet -c -f banner $banner_msg > /tmp/wall_notice
        echo "Lunch has ended. Report back to work now." >> /tmp/wall_notice
        ;;

    break)
        banner_msg="Take a 5 minute break."
        figlet -c -f banner $banner_msg > /tmp/wall_notice
        echo "Take a 5 minute break. Get some water or green tea and perhaps" \
             "a small snack, a smackoroo, if you will." >> /tmp/wall_notice
        ;;

    work_end_soon)
        banner_msg="Working Hours End Soon"
        figlet -c -f banner $banner_msg > /tmp/wall_notice
        echo "It's almost time to stop working. Find a stopping place." \
             "Update your tickets. Save any important open tabs to your" \
             "bookmarks. Send that last email or message." >> /tmp/wall_notice
        ;;

    work_end)
        banner_msg="Working Hours Complete"
        figlet -c -f banner $banner_msg > /tmp/wall_notice
        echo "It's time to STOP WORK! Close all programs, except your time" \
             "sheet. Fill in your timesheet, and sign off. Close your work" \
             "laptop 🎉 " >> /tmp/wall_notice
        ;;

    work_end_serious)
        banner_msg="Stop Working!!"
        figlet -c -f banner $banner_msg > /tmp/wall_notice
        echo "Over time is not worth it. You have a life outside of work." \
             "Seriously, do something else. You're more than the" \
             "productivity you give your job. Take that back for" \
             "yourself. Make or order dinner. Hang out with your friends." \
             "Do some personal hobby. Be more than work." >> /tmp/wall_notice
        ;;
esac

# print the text in all logged in, terminals
wall /tmp/wall_notice

# If on Mac use the say program to speak the notice outloud.
if [ "$(uname)" = "Darwin" ]; then
    # if they set a second variable then silence the alarm
    if [ ! -z "$SILENCE" ]; then
        say -f /tmp/wall_notice
    # if they have this file in thier home directory, also silence the alarm
    elif [ ! -e "$HOME/.alarm_silence"  ]; then
        say -f /tmp/wall_notice
    fi
fi
