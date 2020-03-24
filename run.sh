#!/bin/bash

# exit on error
set -e

# migrate database
python manage.py migrate

# load user groups
python manage.py load_groups

# start webserver
exec gunicorn -c gunicorn.conf.py config.wsgi
