FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends gcc libc-dev && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn
COPY . .
EXPOSE 8080
CMD ["gunicorn", "--bind", ":8080", "--workers", "2", "ecom_site.wsgi:application"]
COPY requirements.txt .
RUN pip install -r requirements.txt
# 1. First, create the database tables
RUN python manage.py migrate --noinput

# 2. Then, gather CSS files
RUN python manage.py collectstatic --noinput

# 3. Finally, run our admin script
RUN python manage.py shell < create_admin.py
