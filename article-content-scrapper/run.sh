#!/bin/bash

# Kill Xvfb if it's running
if pgrep Xvfb > /dev/null; then
    pkill Xvfb
fi

rm -f /tmp/.X99-lock
/usr/bin/Xvfb :99 -screen 0 1920x1080x24+32 &
export DISPLAY=:99
python main.py