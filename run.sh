#!/bin/bash

# migrate database
python manage.py migrate

# start webserver
gunicorn -c gunicorn.conf.py config.wsgi
