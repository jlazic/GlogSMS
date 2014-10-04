#!/bin/bash
NAME="sms"
DJANGODIR=/home/python/sms
VIRTUALENVDIR=/home/python/virtualenvs/sms
BIND="127.0.0.1:8001" #Listen on localhost
USER=django
GROUP=django
NUM_WORKERS=3
DJANGO_SETTINGS_MODULE=project.settings
DJANGO_WSGI_MODULE=project.wsgi

echo "Starting $NAME as `whoami`"

# Activate the virtual environment
cd $VIRTUALENVDIR
source bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec $VIRTUALENVDIR/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER --group=$GROUP \
  --log-level=debug \
  --bind=$BIND