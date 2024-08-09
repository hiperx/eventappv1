#!/bin/bash
source /var/www/html/venv/bin/activate
cd /var/www/html/eventapp/
#python3 manage.py runserver
nohup python3 manage.py runserver &