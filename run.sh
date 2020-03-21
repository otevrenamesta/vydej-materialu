#!/bin/bash

# migrate database
python manage.py migrate

# load user groups
python manage.py load_groups

# start webserver
gunicorn -c gunicorn.conf.py config.wsgi
