#!/bin/sh
# Run database migrations
python manage.py migrate --noinput
# Start the Gunicorn server
gunicorn ecom_site.wsgi:application --bind 0.0.0.0:10000