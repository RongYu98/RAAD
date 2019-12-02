#!/bin/sh
cd ..
python3 RAAD/logs/notify.py &
python3 RAAD/backend/app.py &
python3 RAAD/front/manage.py runsslserver 0.0.0.0:8000 &
trap "pkill -f RAAD; sleep 2; kill $$" INT

while true
do
    sleep 100
done
