#!/bin/bash

cd /var/manudux
python manage.py collectstatic --noinput
python manage.py migrate --noinput
exec gunicorn core.wsgi:application --bind 0.0.0.0:8866 --workers "${GUNICORN_WORKERS:-3}"
