#!/bin/sh
python3 log/notify.py
python3 backend/app.py
front/manage.py runsslserver 0.0.0.0:8000
