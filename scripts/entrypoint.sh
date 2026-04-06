#!/usr/bin/env bash
set -e

# Simple wait-and-run entrypoint for Docker deployments on Render
#  - waits/retries migrations until DB is ready
#  - runs collectstatic
#  - creates superuser if ADMIN_USERNAME and ADMIN_PASSWORD provided

# Try migrations with retries
n=0
until python manage.py migrate --noinput; do
  n=$((n+1))
  if [ $n -ge 30 ]; then
    echo "Migrations failed after 30 attempts"
    exit 1
  fi
  echo "Waiting for DB... (attempt $n)"
  sleep 2
done

# Collect static files
python manage.py collectstatic --noinput

# Create admin user if env vars provided
if [ -n "$ADMIN_USERNAME" ] && [ -n "$ADMIN_PASSWORD" ]; then
  python - <<'PY'
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE','ecom_site.settings')
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()
username = os.environ.get('ADMIN_USERNAME')
email = os.environ.get('ADMIN_EMAIL','admin@example.com')
password = os.environ.get('ADMIN_PASSWORD')
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print('Superuser created.')
else:
    print('Superuser already exists.')
PY
else
  echo "ADMIN_USERNAME or ADMIN_PASSWORD not set; skipping superuser creation."
fi

# Exec the CMD from Dockerfile (gunicorn)
exec "$@"
