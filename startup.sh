#!/bin/bash

touch /root/.Xauthority

Xvfb :0 -screen 0 1920x1080x24 &

export DISPLAY=:0
export XAUTHORITY=/dev/null

fluxbox &

sleep 3

exec uvicorn main:app --host 0.0.0.0 --port 5000
