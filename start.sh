#!/bin/sh
cd ..
python3 RAAD/log/notify.py &
python3 RAAD/backend/app.py &
python3 RAAD/front/manage.py runsslserver 0.0.0.0:8000 &
trap "pkill -f RAAD"
while true
do
    sleep 100
done
